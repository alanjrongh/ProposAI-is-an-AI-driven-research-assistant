import json
import os

data_dir = os.path.join(os.path.dirname(__file__), "..", "data")

# === Load existing datasets ===
def load_json(filename):
    path = os.path.join(data_dir, filename)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

print("🔁 Merging base dataset + OpenReview rejections...")

base_data = load_json("final_dataset.json")
new_rejections = load_json("openreview_rejections.json")

print(f"✅ Base entries: {len(base_data)}")
print(f"➕ New rejected entries: {len(new_rejections)}")

# === Merge and deduplicate by (title + abstract) ===
seen = set()
merged = []

for entry in base_data + new_rejections:
    uid = (entry["title"].lower().strip(), entry["text"].lower().strip())
    if uid not in seen:
        seen.add(uid)
        merged.append(entry)

print(f"🧠 Final merged total: {len(merged)}")

# === Save back to dataset ===
merged_path = os.path.join(data_dir, "final_dataset.json")
with open(merged_path, "w", encoding="utf-8") as f:
    json.dump(merged, f, indent=2)

print(f"✅ Saved updated final_dataset.json with merged rejections.")

