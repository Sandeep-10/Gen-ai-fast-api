# Deploying to Hugging Face Spaces (Docker SDK)

Hugging Face Spaces allows you to host containerized applications for free using the Docker SDK.

---

## Step 1: Create a Hugging Face Space

1. Go to [Hugging Face Spaces](https://huggingface.co/spaces) and click **Create new Space**.
2. **Name your Space** (e.g., `fastapi-agent`).
3. Select **Docker** as the Space SDK.
4. Select the **Blank** template.
5. Choose **Public** or **Private** visibility.
6. Click **Create Space**.

---

## Step 2: Configure the Port Mapping

By default, Hugging Face Spaces routes external traffic to port `7860` inside the container. Since your [Dockerfile](file:///c:/Users/chang/Downloads/Fast-api-Projects/Gen-ai-fast-api/Dockerfile) runs on port `8000`, you have two options:

### Option A: Tell Hugging Face to use Port 8000 (Recommended)
Add a `README.md` file to the root of your project containing the Hugging Face YAML metadata:

```yaml
---
title: Fast-API Agent
emoji: 🤖
colorFrom: blue
colorTo: indigo
sdk: docker
app_port: 8000
pinned: false
---
```
Adding `app_port: 8000` tells Hugging Face to route incoming requests directly to port 8000.

### Option B: Modify your Dockerfile to use Port 7860
Update your [Dockerfile](file:///c:/Users/chang/Downloads/Fast-api-Projects/Gen-ai-fast-api/Dockerfile)'s startup command at the bottom to:
```dockerfile
EXPOSE 7860
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]
```

---

## Step 3: Add Your Secrets/Environment Variables

Your FastAPI app requires `GROQ_API_KEY` and `mongodb_url`. In Hugging Face Spaces, secrets are configured in the Space settings:

1. In your Hugging Face Space, click the **Settings** tab at the top.
2. Scroll down to the **Variables and secrets** section.
3. Click **New secret** and add your environment variables:
   * **Name**: `GROQ_API_KEY` | **Value**: `[your_groq_api_key]`
   * **Name**: `mongodb_url` | **Value**: `[your_mongodb_connection_string]`

*Note: Hugging Face encrypts these secrets, making them safe to use and inaccessible to unauthorized users.*

---

## Step 4: Push Code to Hugging Face Git

Hugging Face Spaces are backed by a Git repository. You can push your code directly to the Hugging Face repository to trigger an automatic build and deploy.

1. In your Hugging Face Space, click the **Use via Git** button or look at the instructions page to get your Git remote URL. It will look like:
   ```bash
   https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE_NAME
   ```
2. In your terminal, add the Hugging Face repository as a new Git remote named `hf`:
   ```bash
   git remote add hf https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE_NAME
   ```
3. Push your code to Hugging Face:
   ```bash
   git push hf master --force
   ```
   *(If your local branch is named `main` instead of `master`, run `git push hf main:master --force`)*

Hugging Face will automatically detect your `Dockerfile`, build the container, inject your secrets, and deploy the application.
