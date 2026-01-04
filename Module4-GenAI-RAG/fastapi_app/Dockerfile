# fastapi_app/Dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies (needed for some python packages)
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python libraries
# We include uvicorn (server), fastapi, and the AI tools
RUN pip3 install fastapi uvicorn python-multipart requests \
    llama-index llama-index-llms-ollama llama-index-embeddings-ollama llama-index-vector-stores-elasticsearch

# Copy our code
COPY . .

# Run the app
EXPOSE 8000
# Command to start the server (assumes your file is named main.py)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]