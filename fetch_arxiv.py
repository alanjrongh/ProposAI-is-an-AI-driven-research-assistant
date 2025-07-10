import arxiv
import json
import os

def fetch_arxiv_papers(query="machine learning", max_results=50):
    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.SubmittedDate
    )

    results = []
    for result in search.results():
        results.append({
            "title": result.title.strip(),
            "text": result.summary.strip()
        })

    # Save to JSON
    save_path = os.path.join(os.path.dirname(__file__), "..", "data", "global_proposals.json")
    with open(save_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    print(f"✅ Saved {len(results)} papers to {save_path}")

# Uncomment below to test directly
# fetch_arxiv_papers("deep learning", max_results=100)
