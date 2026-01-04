import os
import shutil
import uuid
from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel

# LlamaIndex Imports
from llama_index.core import VectorStoreIndex, StorageContext, Settings, PromptTemplate
from llama_index.vector_stores.elasticsearch import ElasticsearchStore
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding

# Import pipeline
# We expect cvpipeline.py to be in the same directory
try:
    from cvpipeline import process_pdf
except ImportError:
    # Fallback to prevent immediate crash if file is missing
    print("WARNING: cvpipeline.py not found. Uploads will fail.")
    def process_pdf(path, original_filename=None): 
        raise NotImplementedError("cvpipeline.py is missing!")

app = FastAPI()

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
    request_timeout=3600.0,          # Wait up to 60 mins (large buffer)
    additional_kwargs={"num_ctx": 4096}
)

# 2. Configure the READER (Embedding Model)
Settings.embed_model = OllamaEmbedding(
    model_name="nomic-embed-text",
    base_url=ollama_url,
    request_timeout=3600.0           # Wait up to 60 mins for large uploads
)

# =========================================================
# 2. ENDPOINTS
# =========================================================
@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    # Create a temporary file to store the upload
    temp_filename = f"temp_{uuid.uuid4().hex}.pdf"
    temp_file_path = os.path.join("/tmp", temp_filename)
    os.makedirs("/tmp", exist_ok=True)
    
    try:
        # Write uploaded bytes to temp file
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # We pass 'original_filename=file.filename' so the pipeline knows 
        # the real name (e.g., "Chingis Rustemov_CV.pdf")
        process_pdf(temp_file_path, original_filename=file.filename)
        
        return {"status": "success", "message": "PDF processed and embeddings created."}
        
    except Exception as e:
        print(f"Upload Error: {e}")
        # Return structured error so app.py can display it nicely
        return {"status": "error", "message": str(e)}
        
    finally:
        # Cleanup temp file
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

class QueryRequest(BaseModel):
    query: str

@app.post("/query")
async def query_index(request: QueryRequest):
    try:
        # Connect to existing index
        vector_store = ElasticsearchStore(
            index_name="student_cvs", 
            es_url=elastic_url
        )
        storage_context = StorageContext.from_defaults(vector_store=vector_store)
        
        # Load the index (does not re-ingest data, just connects)
        index = VectorStoreIndex.from_vector_store(
            vector_store, 
            storage_context=storage_context
        )
        
        # --- IMPROVED PROMPT TEMPLATE ---
        # This fixes the issue where the model refuses to answer because it lacks "external access".
        # We explicitly tell it to use ONLY the provided context.
        text_qa_template_str = (
            "Context information is below.\n"
            "---------------------\n"
            "{context_str}\n"
            "---------------------\n"
            "Given the context information and NOT prior knowledge, "
            "answer the question: {query_str}\n"
            "If the answer is not in the context, explicitly say 'I cannot find this information in the CVs'.\n"
        )
        text_qa_template = PromptTemplate(text_qa_template_str)

        # Create Query Engine with the new template
        query_engine = index.as_query_engine(
            text_qa_template=text_qa_template,
            streaming=False
        )
        
        response = query_engine.query(request.query)
        
        return {"response": str(response)}
        
    except Exception as e:
        print(f"Query Error: {e}")
        # Return 500 error for system failures
        raise HTTPException(status_code=500, detail=str(e))