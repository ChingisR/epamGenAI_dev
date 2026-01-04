import logging
import sys

# 1. Turn on detailed logging to see hidden errors
logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

from llama_index.core import VectorStoreIndex, StorageContext
from llama_index.vector_stores.elasticsearch import ElasticsearchStore
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.core import Settings

print("--- 1. Initializing Embedding Model ---")
Settings.embed_model = OllamaEmbedding(model_name="nomic-embed-text")

print("--- 2. Connecting to Elasticsearch ---")
vector_store = ElasticsearchStore(
    index_name="student_cvs",
    es_url="http://localhost:9200",
)

# Load the index
storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = VectorStoreIndex.from_vector_store(
    vector_store,
    storage_context=storage_context,
)

print("--- 3. Testing Retrieval (Searching for 'Python') ---")
# specific command to just 'fetch' data, not generate an answer
retriever = index.as_retriever(similarity_top_k=3)
nodes = retriever.retrieve("experience with Python")

if not nodes:
    print("\n[FAILURE] No documents found! The database search returned 0 results.")
else:
    print(f"\n[SUCCESS] Found {len(nodes)} chunks of text.")
    for i, node in enumerate(nodes):
        print(f"\n--- Chunk {i+1} ---")
        # Print the first 200 characters of the found text
        print(node.node.get_content()[:200] + "...")