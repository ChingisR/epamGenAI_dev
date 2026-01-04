import os
import shutil
import uuid
from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel

# LlamaIndex Imports
from llama_index.core import VectorStoreIndex, StorageContext, Settings
from llama_index.vector_stores.elasticsearch import ElasticsearchStore
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding

# Import pipeline (handle missing file gracefully)
try:
    from cvpipeline import process_pdf
except ImportError:
    def process_pdf(path): raise NotImplementedError("cvpipeline.py is missing!")

# --- MOVE THIS LINE UP ---
app = FastAPI() 
# -------------------------

# =========================================================
# 1. SETUP THE BRAIN (WITH 6-MINUTE TIMEOUTS)
# =========================================================
ollama_url = os.getenv("OLLAMA_BASE_URL", "http://ollama:11434")
elastic_url = os.getenv("ELASTIC_URL", "http://elasticsearch:9200")
model_name = os.getenv("OLLAMA_MODEL", "phi3")

print(f"--- INIT: Using Model: {model_name} at {ollama_url} ---")

# 1. Configure the THINKER (Answer Generator)
Settings.llm = Ollama(
    model=model_name,
    base_url=ollama_url,
    request_timeout=3600.0,          # <--- WAIT 6 MINUTES FOR ANSWER
    additional_kwargs={"num_ctx": 4096}
)

# 2. Configure the READER (Embedding Model)
Settings.embed_model = OllamaEmbedding(
    model_name="nomic-embed-text",
    base_url=ollama_url,
    request_timeout=3600.0           # <--- WAIT 6 MINUTES FOR UPLOADS
)

# =========================================================
# 2. ENDPOINTS
# =========================================================
@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    temp_filename = f"temp_{uuid.uuid4().hex}.pdf"
    temp_file_path = os.path.join("/tmp", temp_filename)
    os.makedirs("/tmp", exist_ok=True)
    
    with open(temp_file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    try:
        process_pdf(temp_file_path)
        return {"status": "success", "message": "PDF processed and embeddings created."}
    except Exception as e:
        print(f"Upload Error: {e}")
        return {"status": "error", "message": str(e)}
    finally:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

class QueryRequest(BaseModel):
    query: str

@app.post("/query")
async def query_index(request: QueryRequest):
    try:
        vector_store = ElasticsearchStore(index_name="student_cvs", es_url=elastic_url)
        storage_context = StorageContext.from_defaults(vector_store=vector_store)
        index = VectorStoreIndex.from_vector_store(vector_store, storage_context=storage_context)
        
        # Query Engine
        query_engine = index.as_query_engine(streaming=False)
        response = query_engine.query(request.query)
        
        return {"response": str(response)}
        
    except Exception as e:
        print(f"Query Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))