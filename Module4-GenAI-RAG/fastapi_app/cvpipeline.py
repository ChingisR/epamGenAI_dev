import os
import re
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext, Document
from llama_index.vector_stores.elasticsearch import ElasticsearchStore

# Configuration
ELASTIC_URL = os.getenv("ELASTIC_URL", "http://elasticsearch:9200")
INDEX_NAME = "student_cvs"

def extract_candidate_name(original_filename: str, text: str) -> str:
    """
    Extracts name using the original filename first, then falls back to text.
    """
    # 1. Try Filename (Best for "Chingis Rustemov_CV.pdf")
    if original_filename:
        # Remove extension and split
        base_name = os.path.splitext(original_filename)[0]
        name_parts = re.split(r'[_\s-]', base_name)
        
        # Filter junk words
        ignore_words = {"cv", "resume", "profile", "pdf", "data", "engineer", "scientist", "architect"}
        potential_names = [p for p in name_parts if p.lower() not in ignore_words and len(p) > 2]
        
        if potential_names:
            return " ".join(potential_names)

    # 2. Try First Line of Text (Fallback)
    lines = text.split('\n')
    for line in lines[:5]:
        clean_line = line.strip()
        if 3 < len(clean_line) < 50 and any(c.isalpha() for c in clean_line):
            return clean_line
            
    return "Unknown Candidate"

def process_pdf(file_path: str, original_filename: str = None):
    print(f"--- PROCESSING: {original_filename} ---")
    
    # 1. Load the PDF
    # We load raw documents first
    raw_documents = SimpleDirectoryReader(input_files=[file_path]).load_data()

    if not raw_documents:
        print("Warning: No text extracted from PDF.")
        return

    # 2. Prepare Data
    # Calculate name once using the first page
    first_page_text = raw_documents[0].text
    candidate_name = extract_candidate_name(original_filename, first_page_text)
    print(f"--- IDENTIFIED CANDIDATE: {candidate_name} ---")
    
    final_filename = original_filename or os.path.basename(file_path)

    # 3. Create NEW Documents (The Robust Fix)
    # Instead of modifying the 'raw_documents' which might be read-only,
    # we create fresh Document objects with exactly the data we want.
    documents_to_index = []

    for doc in raw_documents:
        # Prepare the baked-in header
        header = (
            f"Context from Candidate: {candidate_name}\n"
            f"Filename: {final_filename}\n"
            "----------------\n"
        )
        
        # Merge new metadata with existing (like page_label)
        new_metadata = doc.metadata.copy()
        new_metadata.update({
            "filename": final_filename,
            "candidate_name": candidate_name,
            "category": "CV"
        })

        # keys to ignore in LLM/Embeddings
        keys_to_exclude = [
            "file_path", "creation_date", "last_modified_date", 
            "filename", "candidate_name", "category", "page_label"
        ]

        # Create a FRESH Document object
        new_doc = Document(
            text=header + doc.text,  # Bake header directly into text
            metadata=new_metadata,
            excluded_llm_metadata_keys=keys_to_exclude,
            excluded_embed_metadata_keys=keys_to_exclude
        )
        documents_to_index.append(new_doc)

    # 4. Index to Elasticsearch
    try:
        vector_store = ElasticsearchStore(
            index_name=INDEX_NAME,
            es_url=ELASTIC_URL,
        )
        storage_context = StorageContext.from_defaults(vector_store=vector_store)
        
        VectorStoreIndex.from_documents(
            documents_to_index,
            storage_context=storage_context,
            show_progress=True
        )
        print("Successfully indexed.")
        
    except Exception as e:
        print(f"Failed to index {original_filename}: {e}")
        raise e