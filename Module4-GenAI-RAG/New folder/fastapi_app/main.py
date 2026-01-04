import os
import shutil
import logging
from typing import List

from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel

# --- LangChain & AI Imports ---
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# --- Critical: Elasticsearch Hybrid Search Imports ---
from langchain_elasticsearch import ElasticsearchStore
# This specific strategy class is required to fix your Error 500
from langchain_elasticsearch.vectorstores import ApproxRetrievalStrategy

# --- Configuration ---
from dotenv import load_dotenv

# 1. Setup Logging & Env
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
load_dotenv()

# 2. Configuration Variables
ES_URL = os.getenv("ELASTIC_URL", "http://elasticsearch:9200")
OLLAMA_URL = os.getenv("OLLAMA_BASE_URL", "http://ollama:11434")
# Note: Ensure you have pulled this model in Ollama (ollama pull nomic-embed-text)
# If using 'all-minilm', change this default.
EMBEDDING_MODEL_NAME = os.getenv("OLLAMA_EMBED_MODEL", "nomic-embed-text") 
LLM_MODEL_NAME = os.getenv("OLLAMA_MODEL", "phi3")
INDEX_NAME = "student_cvs"

app = FastAPI(title="RAG Resume Matcher (Hybrid)")

# 3. Initialize AI Models
logger.info(f"Connecting to Ollama at {OLLAMA_URL} with model {LLM_MODEL_NAME}")

# Embeddings (Vector creator)
embeddings = OllamaEmbeddings(
    base_url=OLLAMA_URL,
    model=EMBEDDING_MODEL_NAME
)

# LLM (The brain that answers)
llm = ChatOllama(
    base_url=OLLAMA_URL,
    model=LLM_MODEL_NAME,
    temperature=0
)

# 4. Initialize Elasticsearch with Hybrid Strategy
# This requires the index to have been created with 'text' and 'dense_vector' fields
vector_store = ElasticsearchStore(
    es_url=ES_URL,
    index_name=INDEX_NAME,
    embedding=embeddings,
    # CRITICAL FIX: This enables the Hybrid capabilities in the code
    strategy=ApproxRetrievalStrategy(hybrid=True)
)

# --- Pydantic Models ---
class QueryRequest(BaseModel):
    query: str

# --- API Endpoints ---

@app.get("/")
def read_root():
    return {"status": "ok", "service": "FastAPI RAG Backend"}

@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    """
    Uploads a PDF, splits it into chunks, and indexes it into Elasticsearch.
    """
    temp_file_path = f"temp_{file.filename}"
    
    try:
        # 1. Save file temporarily
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # 2. Load PDF
        logger.info(f"Processing file: {file.filename}")
        loader = PyPDFLoader(temp_file_path)
        docs = loader.load()
        
        # 3. Split Text (Chunks)
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        splits = text_splitter.split_documents(docs)
        
        # 4. Add Metadata (Optional but helpful)
        for doc in splits:
            doc.metadata["source"] = file.filename

        # 5. Index into Elasticsearch
        # This will create vectors AND store text for keyword search
        vector_store.add_documents(documents=splits)
        
        return {
            "message": f"Successfully indexed {len(splits)} chunks from {file.filename}",
            "filename": file.filename
        }

    except Exception as e:
        logger.error(f"Error processing PDF: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # Cleanup
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

@app.post("/query")
async def query_index(request: QueryRequest):
    """
    Performs a Hybrid Search (Keyword + Vector) and generates an answer.
    """
    try:
        query_text = request.query
        logger.info(f"Received query: {query_text}")

        # 1. Create Retriever (Hybrid Mode)
        # 'k': 5 means retrieve top 5 most relevant chunks
        retriever = vector_store.as_retriever(
            search_type="hybrid",
            search_kwargs={"k": 5}
        )

        # 2. Define the Prompt
        template = """Answer the question based ONLY on the following context. 
        If you don't know the answer, say "I don't know based on the provided documents."
        
        Context:
        {context}
        
        Question: 
        {question}
        """
        prompt = ChatPromptTemplate.from_template(template)

        # 3. Define the Chain
        chain = (
            {"context": retriever, "question": RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser()
        )

        # 4. Run Chain
        response_text = chain.invoke(query_text)
        
        # 5. (Optional) Get source documents for debugging
        # You can call retriever.invoke(query_text) separately if you want to return sources
        
        return {"response": response_text}

    except Exception as e:
        logger.error(f"Error generating response: {e}")
        raise HTTPException(status_code=500, detail=str(e))