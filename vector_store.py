import faiss
import os
import json
from sentence_transformers import SentenceTransformer
from file_chat import extract_text

VECTOR_INDEX_FILE = "memory/friday_index.faiss"
DOC_STORE_FILE = "memory/friday_chunks.json"
model = SentenceTransformer("all-MiniLM-L6-v2")

def chunk_text(text, chunk_size=500):
    words = text.split()
    return [" ".join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]

def embed_chunks(chunks):
    return model.encode(chunks)

def add_document(filepath):
    if not os.path.exists(filepath):
        return "File not found."

    text = extract_text(filepath)
    chunks = chunk_text(text)
    embeddings = embed_chunks(chunks)

    index = faiss.IndexFlatL2(len(embeddings[0]))
    if os.path.exists(VECTOR_INDEX_FILE):
        index = faiss.read_index(VECTOR_INDEX_FILE)
    index.add(embeddings)
    faiss.write_index(index, VECTOR_INDEX_FILE)

    store = {}
    if os.path.exists(DOC_STORE_FILE):
        store = json.load(open(DOC_STORE_FILE))
    store.update({f"{filepath}_{i}": c for i, c in enumerate(chunks)})
    json.dump(store, open(DOC_STORE_FILE, "w"), indent=2)

    return f"✅ Document '{os.path.basename(filepath)}' added to memory."

def query_memory(question, top_k=5):
    if not os.path.exists(VECTOR_INDEX_FILE) or not os.path.exists(DOC_STORE_FILE):
        return "No documents stored yet."

    chunks = json.load(open(DOC_STORE_FILE))
    values = list(chunks.values())

    query_vector = model.encode([question])
    index = faiss.read_index(VECTOR_INDEX_FILE)
    _, I = index.search(query_vector, top_k)

    return "\n".join(values[i] for i in I[0])
