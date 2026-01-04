import os
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext, Settings
from llama_index.vector_stores.elasticsearch import ElasticsearchStore
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.llms.ollama import Ollama

# 1. Setup the Brain (Must match query.py!)
print("--- Setting up AI Models ---")
Settings.embed_model = OllamaEmbedding(model_name="nomic-embed-text")
Settings.llm = Ollama(model="mistral")

# 2. Connect to Database
print("--- Connecting to Elasticsearch ---")
es_store = ElasticsearchStore(
    index_name="student_cvs",
    es_url="http://localhost:9200",
)
storage_context = StorageContext.from_defaults(vector_store=es_store)

# 3. Read PDFs directly
print("--- Reading PDF Files ---")
# This assumes your PDFs are in the current folder
documents = SimpleDirectoryReader(
    input_dir=".", 
    required_exts=[".pdf"]
).load_data()

print(f"Found {len(documents)} pages of text.")

# 4. Create Index (The Heavy Lifting)
print("--- Creating Embeddings & Uploading (This may take a minute) ---")
index = VectorStoreIndex.from_documents(
    documents,
    storage_context=storage_context,
    show_progress=True
)

print("--- SUCCESS! Data is indexed correctly. ---")