# GenAI SME Vocabulary

## Core Concepts
Retrieval-Augmented Generation (RAG) is a process of retrieving data and using it as a context in augmeting a response. RAG enables getting properatry data which are on-cloud or on premise, and using them in locally deployed LLMs without exposing data outside. Also they can be used in feeding these data into cloud AI solutions. Thus LLMs get right context for generating grounded answers. One of the biggest challenges in this process is finding a right balance in chunking data into embeddings for vector databases for getting grounded answers in LLM. There are weak points like context window limitation, latency due to search in vector databases and re-ranking results and so on. Oracle Vector Database creates vector embeddings which are searchable in PLSQL and integrated into Oracle 23 databases. Pinecone is a popular vector database for custom RAG applications. LangChain orchestrates the pipelines between RAG, LLM and UI. There are tools like Ragas, LangChain which can be used in generation of synthetic data for RAG. Ensuring synthetic data close to real data is main challenge in these cases. Also there is a risk losing touch with reality due to extensive training on synthetic data. Gretel.ai, Mostly AI and NVIDIA Omniverse Replicator are helpful for developers for generating synthetic data.

Hallucination of AI-Assisted Code Generation and Refactoring is its weak point and requires human review. Also there is risk of sharing code outside and traing the external AI on properatary code.  

Tokenization is a process of converting text to chunks for embedding and putting into a vector database.



