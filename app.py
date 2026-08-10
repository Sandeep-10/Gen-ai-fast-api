import os
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import pandas as pd
from pymongo import MongoClient
from langchain.tools import tool
from fastapi import FastAPI,Request
from pydantic import BaseModel
from langchain.agents import create_agent
from pprint import pprint
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse,StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware





app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="HTML-Files")

app.mount("/CSS-Files", StaticFiles(directory="CSS-Files"), name="CSS-Files")

load_dotenv()

groq_api_key = os.getenv('GROQ_API_KEY')

class UserQuery(BaseModel):
    question: str


# ponytail: qwen/qwen3-32b does not exist on Groq list of models; using active qwen/qwen3.6-27b instead.
model = ChatGroq(
    model="qwen/qwen3.6-27b",
    api_key=groq_api_key,
    max_retries=2,
)

mongodb_connection_string = os.getenv("mongodb_url")
@tool
def search_database(query : str )->str:
    """Returns the structure (schema) and sample columns of the sandeep database table so the agent knows how to query it."""
    mongo_client = MongoClient(mongodb_connection_string)
    collection = mongo_client['Database']['sandeep']
    
    # 1. Grab just ONE sample document to see what the columns are
    sample_data = collection.find_one()
    if not sample_data:
        return "The database collection is empty."
        
    # Remove MongoDB's internal ID object for cleaner text
    sample_data.pop('_id', None)
    
    # 2. Tell the agent exactly what columns exist
    columns = list(sample_data.keys())
    
    schema_info = f"""
    Database Table Name: sandeep
    Available Columns: {', '.join(columns)}
    Sample Document Format: {str(sample_data)}
    """
    return schema_info

system_prompt = '''
You are an intelligent Text-to-SQL agent built to query
a business database and return accurate, optimized SQL.
get the database schema_info from the search_database tool.
analyse and understand the database and then answer the question
YOUR BEHAVIOR:
- Convert user questions into valid SQLite SQL queries
- Always select only relevant columns — never use SELECT *
- Use table aliases for readability
- Add ORDER BY when ranking or sorting is implied
- Add LIMIT 10 unless user specifies otherwise
- Use ROUND() for decimal values
- Use GROUP BY correctly with aggregate functions
PRIVACY RULES:
- Never expose columns: customer_email, phone, aadhaar
- If asked for private data, respond:
  "That data is restricted due to privacy policy."
OUTPUT FORMAT:
Thought: <brief reasoning about what the question needs>
SQL:
```sql
<your SQL query here>
```
Result Explanation: <plain English explanation of what
the query does and what the result means>
HANDLE ERRORS:
- If question is too vague → ask one clarifying question
- If question needs unavailable data → explain what is
  missing politely
- If SQL would return no results → suggest why and offer
  an alternative query'''





agent  = create_agent(
    tools = [search_database],
    model = model,
    system_prompt = system_prompt
)


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse(request, "index.html")


@app.post("/ask-agent")
async def query_agent(user_question : UserQuery):
    async def event_generator():
        streaming =agent.astream_events(
            {
                "messages": [
                    {"role": "user", "content": user_question.question}
                ]
            },
            version="v2"
        )
        async for event in streaming:
            if event["event"] == "on_chat_model_stream":
                chunk = event["data"]["chunk"]
                if chunk.content:
                    yield chunk.content

    return StreamingResponse(event_generator(), media_type="text/plain")
