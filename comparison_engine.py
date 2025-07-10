from sentence_transformers import SentenceTransformer
import numpy as np
import os
import json

model = SentenceTransformer("allenai-specter")

# Load global proposals
DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "global_proposals.json")
if os.path.exists(DATA_PATH):
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        global_proposals = json.load(f)
else:
    global_proposals = []

def compare_proposal(user_text):
    user_vec = model.encode([user_text])[0]

    similarities = []
    for item in global_proposals:
        comp_vec = model.encode([item["text"]])[0]
        sim = cosine_similarity(user_vec, comp_vec)
        similarities.append((item["title"], sim))

    similarities.sort(key=lambda x: x[1], reverse=True)
    return similarities[:3]

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
