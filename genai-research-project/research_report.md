# Research on Generative AI Applications

## 1. Retrieval-Augmented Generation (RAG) for Enterprise Knowledge
RAG enables getting properatry data of corporations and using them in locally deployed LLMs without exposing data outside. Also they can be used in feeding these data into cloud AI solutions. Thus LLMs get right context for generating grounded answers.

**Technical Challenges & Weak Points:**
One of the biggest challenges is finding a right balance in chunking data into embeddings for vector databases for getting grounded answers in LLM. There are weak points like context window limitation, latency due to search in vector databases and re-ranking results and so on.

**Existing Implementations:**
Oracle Vector Database creates vector embeddings which are searchable in PLSQL and integrated into Oracle 12 databases.
Pinecone is a popular vector database for custom RAG applications.
LangChain orchestrates the pipelines between RAG, LLM and UI.

## 2. AI-Assisted Code Generation and Refactoring
This pretained models are handful in programming like unit tests, documentation, generating code chunks etc.

**Technical Challenges & Weak Points:**
Hallucination is a weak point and this requires human review. Also there is risk of sharing code outside and traing the external AI on properatary code.  

**Existing Implementations:**
GitHub Copilot, Amazon Q Developer etc.

## 3. Synthetic Data Generation for Model Training
There are tools like Ragas, LangChain which can be used in generation of synthetic data for RAG.

**Technical Challenges & Weak Points:**
To ensure synthetic data close to real data is main challenge in these cases. Also there is a risk losing touch with reality due to extensive training on synthetic data. 

**Existing Implementations:**
Gretel.ai, Mostly AI and NVIDIA Omniverse Replicator are helpful for developers for generating synthetic data 