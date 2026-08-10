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

---

## 🌐 Deploying the Frontend (GitHub Pages)

The frontend is already configured and hosted for free on GitHub Pages:
👉 **[Live App UI](https://sandeep-10.github.io/Gen-ai-fast-api/HTML-Files/index.html)**

Since GitHub Pages only hosts static files, you will need to input your deployed backend API URL in the sidebar setting card to connect the frontend to your remote server.

---

## 🐳 Deploying the Backend

Because the backend runs Python, it cannot be hosted on GitHub Pages. You can deploy the backend container using one of the following methods:

### Method A: Hugging Face Spaces (Docker SDK - 100% Free)

1. Create a new Space on [Hugging Face](https://huggingface.co/spaces) and select **Docker** as the SDK.
2. Under **Settings > Variables and secrets**, add your environment variables:
   - `GROQ_API_KEY`
   - `mongodb_url`
3. Add a Hugging Face remote to your local repository and push:
   ```bash
   git remote add hf https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE_NAME
   git push hf master --force
   ```
4. Update the port mapping: Hugging Face default port is `7860`. You can configure Hugging Face to route to your container's port `8000` by adding this metadata block at the top of a new `README.md` (or adding it to this file if pushing to Hugging Face):
   ```yaml
   ---
   title: Fast-API Agent
   sdk: docker
   app_port: 8000
   ---
   ```

---

### Method B: Google Cloud Run (Serverless)

#### 1. Setup GCP CLI
```bash
gcloud auth login
gcloud config set project YOUR_PROJECT_ID
gcloud services enable artifactregistry.googleapis.com cloudbuild.googleapis.com run.googleapis.com
```

#### 2. Create Artifact Registry
```bash
gcloud artifacts repositories create fast-api-repo \
    --repository-format=docker \
    --location=us-central1
```

#### 3. Build & Deploy
Build your container image using Cloud Build:
```bash
gcloud builds submit --tag us-central1-docker.pkg.dev/YOUR_PROJECT_ID/fast-api-repo/fastapi-app:latest .
```

Deploy the image to Cloud Run (specifying port 8000):
```bash
gcloud run deploy fastapi-app \
    --image=us-central1-docker.pkg.dev/YOUR_PROJECT_ID/fast-api-repo/fastapi-app:latest \
    --platform=managed \
    --region=us-central1 \
    --allow-unauthenticated \
    --port=8000 \
    --set-env-vars="GROQ_API_KEY=your_key,mongodb_url=your_mongo_url"
```
