import os
import shutil
import uuid
from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from cvpipeline import process_pdf

# LlamaIndex Imports
from llama_index.core import VectorStoreIndex, StorageContext, Settings
from llama_index.vector_stores.elasticsearch import ElasticsearchStore
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding

app = FastAPI()

# =========================================================
# 1. SETUP THE BRAIN (GLOBAL MEMORY FIX)
# =========================================================
# We read the configs from Docker environment variables
ollama_url = os.getenv("OLLAMA_BASE_URL", "http://ollama:11434")
elastic_url = os.getenv("ELASTIC_URL", "http://elasticsearch:9200")
model_name = os.getenv("OLLAMA_MODEL", "phi3")

print(f"--- INIT: Using Model: {model_name} at {ollama_url} ---")

# Configure the LLM with the Memory Limit (num_ctx=4096)
Settings.llm = Ollama(
    model=model_name,
    base_url=ollama_url,
    request_timeout=360.0,
    additional_kwargs={"num_ctx": 4096}  # <--- CRITICAL FIX TO PREVENT CRASH
)

# Configure the Embedding Model
Settings.embed_model = OllamaEmbedding(
    model_name="nomic-embed-text",
    base_url=ollama_url
)

# =========================================================
# 2. UPLOAD ENDPOINT (Existing Logic)
# =========================================================
@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    # Save the uploaded PDF to a temporary location.
    temp_filename = f"temp_{uuid.uuid4().hex}.pdf"
    temp_file_path = os.path.join("/tmp", temp_filename)
    
    with open(temp_file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    try:
        # Process the PDF using the embedding pipeline.
        process_pdf(temp_file_path)
        return {"status": "success", "message": "PDF processed and embeddings created."}
    except Exception as e:
        return {"status": "error", "message": str(e)}
    finally:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

# =========================================================
# 3. QUERY ENDPOINT (New! Needed for Web UI)
# =========================================================
class QueryRequest(BaseModel):
    query: str

@app.post("/query")
async def query_index(request: QueryRequest):
    try:
        # 1. Connect to the Database
        vector_store = ElasticsearchStore(
            index_name="student_cvs",
            es_url=elastic_url
        )
        
        # 2. Load the Index
        storage_context = StorageContext.from_defaults(vector_store=vector_store)
        index = VectorStoreIndex.from_vector_store(
            vector_store,
            storage_context=storage_context,
        )
        
        # 3. Ask the Question
        # We disable streaming here to keep the API simple for now
        query_engine = index.as_query_engine(streaming=False)
        response = query_engine.query(request.query)
        
        return {"response": str(response)}
        
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))