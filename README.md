# Sandeep Text-to-SQL AI Agent Playground

A full-stack web application powered by **FastAPI**, **LangChain**, and **Groq (Qwen)** that translates plain English questions into schema-valid SQLite queries, executes them against a MongoDB database, and explains the results.

---

## 🚀 Features

- **Natural Language to SQL:** Uses advanced LLMs to convert business queries into optimized SQL.
- **Privacy Protocol:** Automatically masks sensitive fields like `customer_email`, `phone`, and `aadhaar` to ensure compliance.
- **Streamed Agent Thoughts:** Watch the agent's chain-of-thought process stream in real-time.
- **Customizable API URL:** Configure your backend endpoint dynamically from the UI.
- **Modern UI:** Premium dark/light mode toggle with responsive glassmorphism styles.

---

## 📁 Repository Structure

```
├── HTML-Files/text-to-sql/   # Web frontend files
│   └── index.html            # Main UI Dashboard
├── CSS-Files/                # UI styling
│   └── style.css             # Custom stylesheets
├── app.py                    # FastAPI server & LangChain Agent logic
├── Dockerfile                # Containerization setup
├── requirements.txt          # Python dependencies
└── .gitignore                # Git ignore patterns (protects secrets)
```

---

## 💻 Local Setup & Execution

### 1. Configure Environment Variables
Create a `.env` file in the project root:
```env
mongodb_url=your_mongodb_connection_string
GROQ_API_KEY=your_groq_api_key
```

### 2. Install Dependencies
Ensure you have Python 3.10+ installed, then run:
```bash
pip install -r requirements.txt
```

### 3. Run the Backend
Start the FastAPI server on port 8000:
```bash
uvicorn app:app --port 8000 --reload
```

### 4. Run the Frontend
Simply open `HTML-Files/index.html` in any web browser.
