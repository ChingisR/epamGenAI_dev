from llama_index.core import VectorStoreIndex, StorageContext, Settings
from llama_index.vector_stores.elasticsearch import ElasticsearchStore
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding
import sys

# 1. Setup Brain (Phi-3 with Memory Limit)
Settings.llm = Ollama(
    model="phi3", 
    request_timeout=360.0, 
    additional_kwargs={"num_ctx": 4096}
)
Settings.embed_model = OllamaEmbedding(model_name="nomic-embed-text")

# 2. Connect to Database
vector_store = ElasticsearchStore(
    index_name="student_cvs",
    es_url="http://localhost:9200",
)

# 3. Load Index
index = VectorStoreIndex.from_vector_store(
    vector_store,
    storage_context=StorageContext.from_defaults(vector_store=vector_store),
)

# 4. Enable Streaming (The Fix!)
query_engine = index.as_query_engine(streaming=True)

print("Asking AI (Watch for text below)...")
print("------------------------------------------------")

# 5. Stream the Answer to the Console
response = query_engine.query("Who has experience with Python and what is their background?")
response.print_response_stream()

print("\n------------------------------------------------")