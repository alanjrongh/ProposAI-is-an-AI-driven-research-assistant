import arxiv
import json
import os

# List of search queries across major global research domains
QUERIES = [
    "machine learning", "robotics", "biomedical", "economics",
    "quantum computing", "education", "energy", "environmental science",
    "psychology", "social networks", "transportation", "blockchain"
]

results = []

# Use the new arXiv client
client = arxiv.Client()

# Loop over all queries and collect abstracts
for query in QUERIES:
    search = arxiv.Search(
        query=query,
        max_results=50,
        sort_by=arxiv.SortCriterion.SubmittedDate
    )

    for result in client.results(search):
        results.append({
            "title": result.title.strip(),
            "text": result.summary.strip(),
            "label": 1,  # Accepted
            "source": "arXiv",
            "field": query.lower(),
            "region": "global",
            "year": result.updated.year
        })

# === Ensure the data/ folder exists ===
data_folder = os.path.join(os.path.dirname(__file__), "..", "data")
os.makedirs(data_folder, exist_ok=True)

# Save the results as JSON
save_path = os.path.join(data_folder, "global_accepted_arxiv.json")
with open(save_path, "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2)

print(f"✅ Saved {len(results)} abstracts to {save_path}")
