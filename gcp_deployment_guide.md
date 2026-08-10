# Deploying to Google Cloud (Cloud Run & Artifact Registry)

This guide walks you through deploying this FastAPI application to Google Cloud. 

Google Container Registry (`gcr.io`) is deprecated. GCP now uses **Google Artifact Registry** to store container images, and **Google Cloud Run** to run them serverlessly.

---

## 1. Prerequisites & GCP Setup

1. **Install the Google Cloud CLI (`gcloud`)** if you haven't already.
2. **Authenticate** your terminal with Google Cloud:
   ```bash
   gcloud auth login
   ```
3. **Configure your GCP project ID**:
   ```bash
   gcloud config set project YOUR_PROJECT_ID
   ```
4. **Enable the required GCP APIs** (Artifact Registry, Cloud Build, and Cloud Run):
   ```bash
   gcloud services enable artifactregistry.googleapis.com \
                          cloudbuild.googleapis.com \
                          run.googleapis.com
   ```

---

## 2. Create an Artifact Registry Repository

Create a Docker repository in your preferred region (e.g., `us-central1`):

```bash
gcloud artifacts repositories create fast-api-repo \
    --repository-format=docker \
    --location=us-central1 \
    --description="Docker repository for FastAPI app"
```

Configure Docker local client helper to authenticate with the registry:
```bash
gcloud auth configure-docker us-central1-docker.pkg.dev
```

---

## 3. Build & Push using Google Cloud Build (No local Docker required)

Instead of building locally and pushing, you can use **Google Cloud Build** to build the image directly on GCP infrastructure:

```bash
gcloud builds submit --tag us-central1-docker.pkg.dev/YOUR_PROJECT_ID/fast-api-repo/fastapi-app:latest .
```
*(Replace `YOUR_PROJECT_ID` with your actual GCP Project ID)*

> [!NOTE]
> If you explicitly want to use the legacy Google Container Registry (GCR), run:
> ```bash
> gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/fastapi-app:latest .
> ```

---

## 4. Deploy to Google Cloud Run

Deploy the image to Google Cloud Run:

```bash
gcloud run deploy fastapi-app \
    --image=us-central1-docker.pkg.dev/YOUR_PROJECT_ID/fast-api-repo/fastapi-app:latest \
    --platform=managed \
    --region=us-central1 \
    --allow-unauthenticated \
    --port=8000 \
    --set-env-vars="GROQ_API_KEY=your_groq_api_key,mongodb_url=your_mongodb_connection_string"
```

### Key Deployment Flags Explained:
- `--image`: The location of the container image we built.
- `--allow-unauthenticated`: Makes the FastAPI service public.
- `--port=8000`: Cloud Run defaults to forwarding traffic to port `8080`. Since your `Dockerfile` exposes and starts Uvicorn on port `8000`, we pass `--port=8000` to direct Cloud Run's traffic correctly.
- `--set-env-vars`: Passes the required environmental variables to the container.

> [!TIP]
> For production environments, do not pass secrets like api keys directly in plain text. Instead, store them in **Google Secret Manager** and reference them in Cloud Run using:
> `--set-secrets="GROQ_API_KEY=GROQ_API_KEY_SECRET:latest,mongodb_url=MONGODB_URL_SECRET:latest"`

---

## Alternative: Auto-binding to the Cloud Run Port (Best Practice)

If you don't want to force `--port=8000` during deployment, you can update the `Dockerfile` to bind to the dynamic `PORT` environment variable supplied by Cloud Run (which defaults to `8080`).

Modify the `CMD` in your [Dockerfile](file:///c:/Users/chang/Downloads/Fast-api-Projects/Gen-ai-fast-api/Dockerfile) to:
```dockerfile
CMD ["sh", "-c", "uvicorn app:app --host 0.0.0.0 --port ${PORT:-8000}"]
```
If you do this, you can omit the `--port` flag when deploying, and Cloud Run will automatically bind to its default port.

---

## 5. Deploying via the Google Cloud Console (Web Interface)

If you prefer to deploy using the GCP Console website instead of the CLI, you have two options depending on where your code is:

### Option A: Direct Deployment from GitHub/Git (Recommended for Web)

Google Cloud Run can connect to your GitHub repository and build your Docker container automatically whenever you push code.

1. **Go to the Cloud Run Console**:
   Navigate to the [Google Cloud Run Console](https://console.cloud.google.com/run).
2. **Create Service**:
   Click the **Create Service** button at the top of the page.
3. **Select Source**:
   - Select **"Continuously deploy from a repository"**.
   - Click the **Set up with Cloud Build** button.
4. **Connect Repository**:
   - Choose your provider (e.g., GitHub).
   - Authenticate and select your repository containing this FastAPI project.
   - Click **Next**.
5. **Build Configuration**:
   - Select your main branch.
   - For Build Type, select **Dockerfile**.
   - Leave the Dockerfile path as `/Dockerfile` or `Dockerfile`.
   - Click **Save**.
6. **Service Settings**:
   - Enter a service name (e.g., `fastapi-app`).
   - Select a Region close to you (e.g., `us-central1`).
   - For **Ingress**, keep "Route all traffic".
   - For **Authentication**, select **"Allow unauthenticated invocations"** (if you want the API to be publicly accessible).
7. **Configure Variables & Ports**:
   - Expand the **Container, Networking, Security** section at the bottom.
   - Under the **Container** tab:
     - Change the **Container port** from `8080` to `8000` (since your `Dockerfile` exposes port `8000`).
     - Under **Variables & Secrets**, add the following environment variables:
       * **Name**: `GROQ_API_KEY` | **Value**: `[Your Groq Key]`
       * **Name**: `mongodb_url` | **Value**: `[Your MongoDB URI]`
8. **Deploy**:
   - Click **Create** at the bottom. GCP will build your container and deploy it automatically.

---

### Option B: Deploying a Pre-built Image via Console

If you have already built and pushed your image using `gcloud builds submit` (or local docker push to Artifact Registry):

1. **Go to the Cloud Run Console**:
   Navigate to the [Google Cloud Run Console](https://console.cloud.google.com/run).
2. **Create Service**:
   Click the **Create Service** button at the top of the page.
3. **Select Image**:
   - Select **"Deploy one revision from an existing container image"**.
   - Click **Browse** and select your container image from Artifact Registry (`us-central1-docker.pkg.dev/...`) or Container Registry.
4. **Service Settings**:
   - Select your Region.
   - Select **"Allow unauthenticated invocations"** under Authentication.
5. **Configure Ports & Variables**:
   - Expand the **Container, Networking, Security** section.
   - Set the **Container port** to `8000`.
   - Under **Variables & Secrets**, add `GROQ_API_KEY` and `mongodb_url` environment variables.
6. **Deploy**:
   - Click **Create**.
