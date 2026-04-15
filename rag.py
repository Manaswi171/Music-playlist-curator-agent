from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")

songs_db = [
    "Blinding Lights - upbeat happy song",
    "Let Her Go - emotional sad song",
    "Weightless - relaxing focus music",
    "Sunflower - chill vibe song"
]

vectors = model.encode(songs_db)
index = faiss.IndexFlatL2(vectors.shape[1])
index.add(np.array(vectors))

def search_similar(query):
    q_vec = model.encode([query])
    D, I = index.search(np.array(q_vec), k=3)
    return [songs_db[i] for i in I[0]]