# Copilot Instructions for epamGenAI_dev

## Project Purpose
This is an **educational research project** on Generative AI applications, not production code. It consists of three interconnected markdown documents and a Python visualization script that demonstrates concept relationships.

## Project Architecture

### Core Components
1. **`research_report.md`** – Three enterprise GenAI use cases:
   - **RAG (Retrieval-Augmented Generation)**: Grounding LLMs with proprietary data via vector databases and chunking strategies
   - **AI-Assisted Code Generation**: Developer velocity vs. hallucination risk and code leakage concerns
   - **Synthetic Data Generation**: Privacy-safe training while maintaining data fidelity

2. **`vocabulary.md`** – 15 essential GenAI SME terms with engineering-focused definitions:
   - **Data Strategy terms** (Chunking Strategy, Chunk Overlap, Embeddings) are critical for RAG understanding
   - **Architecture terms** (Vector Database, Fine-tuning, Zero-shot) define implementation approaches
   - **Grounding terms** (Hallucination, Chain-of-Thought, Temperature) address reliability

3. **`generate_graph.py`** – Visualization script using networkx + matplotlib:
   - Maps vocabulary terms as nodes connected to the research report
   - Distinguishes **explicit mentions** (green nodes) from **implicit concepts** (blue nodes)
   - Uses weighted edges based on mention frequency

## Key Patterns & Conventions

### Content Relationships
- **Vocabulary terms are bidirectionally referenced**: Changes to definitions in `vocabulary.md` should be reflected in usage examples within `research_report.md`
- **Graph generation is deterministic**: The `generate_graph.py` uses a fixed seed (`seed=42`) to ensure consistent visualization layouts across runs
- **Chunking Strategy & Chunk Overlap** are particularly important – they connect multiple use cases (RAG, synthetic data, and data strategy discussions)

### Technical Approach
- Terms are identified through two mechanisms:
  - **Explicit**: Direct text matching (case-insensitive) in the report
  - **Implicit**: Domain logic (e.g., "splitting data" → Chunking Strategy)
- Color coding: Gold (root), Green (explicit), Blue (implicit-only)
- Edge weights represent mention frequency

## Critical Workflows

### Updating Research Content
When adding new GenAI use cases or concepts:
1. Add/update definitions in `vocabulary.md` (maintain engineering perspective)
2. Reference terms in `research_report.md` with natural language
3. If introducing new implicit relationships, update `generate_graph.py` logic (search for `implicit_counts` dictionary)
4. Regenerate graph: `python generate_graph.py` (produces `vocabulary_graph.png`)

### Extending the Graph
- Add new vocabulary items to `vocab_list` in `generate_graph.py`
- Implicit detection requires explicit logic – add conditions in the implicit_counts loop
- Node sizes and layout seed are configurable for visualization tuning

## Developer Context
- **Assignment context**: EPAM GenAI Course Assignment by Chingis R.
- **Dependencies**: matplotlib, networkx (required for visualization)
- **Output artifacts**: `vocabulary_graph.png` (generated, not version-controlled)

## Important Notes
- This is **educational content** – focus on clarity and conceptual accuracy over production robustness
- The research report uses **real enterprise tools** (Oracle Vector DB, Pinecone, LangChain, GitHub Copilot) as reference implementations
- The vocabulary is domain-specific – maintain consistent engineering perspective across updates
