# simpleRAG.py

from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from transformers import pipeline

# -------------------------
# Step 1: Create documents
# -------------------------
documents = [
    "Python is a programming language used for AI and web development.",
    "Django is a backend framework written in Python.",
    "React is a frontend JavaScript library used for building UI.",
    "MongoDB is a NoSQL database commonly used in the MERN stack."
]

# -------------------------
# Step 2: Load embedding model
# -------------------------
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# Convert documents to embeddings
doc_embeddings = embedding_model.encode(documents)

# -------------------------
# Step 3: Create FAISS index
# -------------------------
dimension = doc_embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)

index.add(np.array(doc_embeddings))

# -------------------------
# Step 4: Load local LLM
# -------------------------
generator = pipeline("text-generation", model="distilgpt2")

# -------------------------
# Step 5: Ask question
# -------------------------
query = input("Ask a question: ")

# Convert query to embedding
query_embedding = embedding_model.encode([query])

# Search similar documents
k = 2
distances, indices = index.search(np.array(query_embedding), k)

# Retrieve context
context = ""
for i in indices[0]:
    context += documents[i] + "\n"

# -------------------------
# Step 6: Generate answer
# -------------------------
prompt = f"""
Use the following context to answer the question.

Context:
{context}

Question:
{query}

Answer:
"""

result = generator(prompt, max_length=200)

print("\nAnswer:")
print(result[0]["generated_text"])