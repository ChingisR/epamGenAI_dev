import matplotlib.pyplot as plt
import networkx as nx

# --- CONFIGURATION ---
# 1. Define the Vocabulary (Nodes)
vocab_list = [
    "Tokenization", "Hallucination", "Temperature", "Inference", 
    "Context Window", "Embeddings", "Fine-tuning", "Zero-shot", 
    "Chain-of-Thought", "Vector Database", "Chunking Strategy", "Chunk Overlap"
]

# 2. Define the Report Content (The "Source")
report_text = """
Retrieval-Augmented Generation (RAG) allows Large Language Models (LLMs) to fetch relevant data.
The main technical challenge is the "context window" limitation.
If the vector search retrieves irrelevant chunks, the LLM will output a poor answer.
A weak point is "hallucination" in code logic.
We must balance splitting data to ensure statistical fidelity.
"""

# --- LOGIC ---
# 3. Calculate Connections (Edges)
explicit_counts = {}
implicit_counts = {}

normalized_text = report_text.lower()

for term in vocab_list:
    # Count Explicit mentions
    count = normalized_text.count(term.lower())
    explicit_counts[term] = count
    
    # Logic for Implicit mentions (simulated for the assignment)
    if term == "Chunking Strategy" and "splitting data" in normalized_text:
        implicit_counts[term] = 1
    elif term == "Vector Database" and "vector search" in normalized_text:
         implicit_counts[term] = 1
    elif term == "Embeddings" and "vector" in normalized_text:
         implicit_counts[term] = 1
    else:
        implicit_counts[term] = 0

# 4. Build the Graph
G = nx.Graph()
root_node = "GenAI Report"
G.add_node(root_node, color='gold', size=3000)

for term in vocab_list:
    total_weight = explicit_counts[term] + implicit_counts[term]
    
    # Only add nodes that have at least one connection (explicit or implicit)
    if total_weight > 0:
        # Green for explicit, Blue for implicit only
        color = 'lightgreen' if explicit_counts[term] > 0 else 'lightblue'
        G.add_node(term, color=color, size=1500)
        G.add_edge(root_node, term, weight=total_weight)

# --- RENDERING ---
# 5. Draw the Graph
plt.figure(figsize=(10, 8))
pos = nx.spring_layout(G, seed=42) # seed ensures consistent layout

# Get attributes
node_colors = [nx.get_node_attributes(G, 'color')[node] for node in G.nodes()]
node_sizes = [nx.get_node_attributes(G, 'size')[node] for node in G.nodes()]
edge_weights = [G[u][v]['weight'] * 2 for u,v in G.edges()]

# Draw
nx.draw(G, pos, with_labels=True, node_color=node_colors, node_size=node_sizes, 
        width=edge_weights, edge_color="gray", font_size=9, font_weight="bold")

# Legend / Annotation
plt.title("Vocabulary Usage Graph (Explicit vs Implicit)", fontsize=14)
plt.text(-0.9, -0.9, "Green = Explicit Mention\nBlue = Implicit Concept", fontsize=10, bbox=dict(facecolor='white', alpha=0.8))

# Save
output_filename = "vocabulary_graph.png"
plt.savefig(output_filename)
print(f"Success: Graph saved as '{output_filename}'")