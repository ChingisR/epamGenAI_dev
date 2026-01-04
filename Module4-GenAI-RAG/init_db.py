import time
from elasticsearch import Elasticsearch

# Retries connection for 30 seconds
def get_es_connection():
    es = Elasticsearch("http://localhost:9200")
    for _ in range(10):
        if es.ping():
            return es
        print("⏳ Waiting for Elasticsearch...")
        time.sleep(3)
    raise ConnectionError("Could not connect to localhost:9200")

def reset_index():
    es = get_es_connection()
    INDEX_NAME = "student_cvs"

    if es.indices.exists(index=INDEX_NAME):
        print(f"🗑️  Deleting old index '{INDEX_NAME}'...")
        es.indices.delete(index=INDEX_NAME)

    # HYBRID MAPPING: "content" (keyword) + "embedding" (vector)
    mapping = {
        "mappings": {
            "properties": {
                "content": {"type": "text", "analyzer": "standard"}, 
                "embedding": {
                    "type": "dense_vector",
                    "dims": 384,   # <--- Match this to your model (384 for MiniLM, 768 for Nomic)
                    "index": True,
                    "similarity": "cosine"
                },
                "metadata": {"type": "object"}
            }
        }
    }

    es.indices.create(index=INDEX_NAME, body=mapping)
    print(f"✅ Created HYBRID index '{INDEX_NAME}'")

if __name__ == "__main__":
    try:
        reset_index()
    except Exception as e:
        print(f"❌ Error: {e}")