FROM python:3.11-slim

WORKDIR /app

# Copy and install dependencies first to leverage Docker cache layers
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Expose port 8000 for local/network access
EXPOSE 8000

# Start FastAPI application via uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
