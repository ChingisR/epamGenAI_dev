from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext, Settings
from llama_index.vector_stores.elasticsearch import ElasticsearchStore

def process_pdf(file_path):
    print(f"Processing: {file_path}")
    
    # 1. Connect to Elasticsearch
    # We use the hostname 'elasticsearch' because we are inside Docker
    vector_store = ElasticsearchStore(
        index_name="student_cvs",
        es_url="http://elasticsearch:9200",
    )
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    # 2. Read the single PDF file
    documents = SimpleDirectoryReader(
        input_files=[file_path]
    ).load_data()

    # 3. Create Index (Uploads to ES)
    VectorStoreIndex.from_documents(
        documents,
        storage_context=storage_context
    )
    print("Successfully indexed.")