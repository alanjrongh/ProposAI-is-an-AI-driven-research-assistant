import arxiv
import json
import os
import time

# arXiv categories — extend this as needed
CATEGORIES = [
    "cs.AI", "cs.LG", "cs.CV", "cs.CL", "math", "econ", "stat", "q-bio",
    "physics", "cs.RO", "cs.CR", "cs.SE", "cs.NI", "cs.HC", "cs.DC",
    "cs.SI", "cs.SD", "cs.IT", "cs.MA", "cs.DB", "eess", "astro-ph"
]

MAX_PER_CATEGORY = 1000
BATCH_SIZE = 100  # arXiv limits
SLEEP_BETWEEN_CALLS = 3  # seconds

all_papers = []
client = arxiv.Client()

print("📥 Starting full-scale arXiv data fetch...")

for category in CATEGORIES:
    count = 0
    print(f"\n🔎 Fetching category: {category}")
    
    search = arxiv.Search(
        query=f"cat:{category}",
        max_results=MAX_PER_CATEGORY,
        sort_by=arxiv.SortCriterion.SubmittedDate,
    )

    try:
        for result in client.results(search):
            all_papers.append({
                "title": result.title.strip(),
                "text": result.summary.strip(),
                "label": 1,
                "source": "arXiv",
                "field": category,
                "region": "global",
                "year": result.updated.year
            })

            count += 1
            if count % BATCH_SIZE == 0:
                print(f"  ✅ {count} papers fetched...")
                time.sleep(SLEEP_BETWEEN_CALLS)

            if count >= MAX_PER_CATEGORY:
                break

        print(f"✅ Done: {count} papers fetched from {category}")

    except Exception as e:
        print(f"❌ Error while fetching {category}: {e}")
        continue

print(f"\n📊 Total collected: {len(all_papers)} papers.")

# Save to data/arxiv_full.json
output_dir = os.path.join(os.path.dirname(__file__), "..", "data")
os.makedirs(output_dir, exist_ok=True)

save_path = os.path.join(output_dir, "arxiv_full.json")
with open(save_path, "w", encoding="utf-8") as f:
    json.dump(all_papers, f, indent=2)

print(f"\n✅ Saved {len(all_papers)} papers to {save_path}")
