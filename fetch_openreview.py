import openreview
import json
import os

client = openreview.Client(baseurl='https://api.openreview.net')

# Fetch submissions from ICLR 2023
submissions = openreview.tools.iterget_notes(
    client,
    invitation='ICLR.cc/2023/Conference/-/Blind_Submission'
)

results = []

print("🔍 Fetching proposals from OpenReview (ICLR 2023)...")

for note in submissions:
    # Get decision (accepted or rejected)
    decision = client.get_notes(
        invitation='ICLR.cc/2023/Conference/Paper{}/-/Decision'.format(note.number)
    )
    if not decision:
        continue

    decision_text = decision[0].content['decision'].lower()
    if 'accept' in decision_text:
        label = 1
    elif 'reject' in decision_text:
        label = 0
    else:
        continue  # Skip uncertain cases

    results.append({
        "title": note.content.get("title", "").strip(),
        "text": note.content.get("abstract", "").strip(),
        "label": label,
        "source": "OpenReview",
        "field": "AI",
        "region": "global",
        "year": 2023
    })

    if len(results) >= 100:  # Limit to 100 proposals
        break

# Save results
output_path = os.path.join(os.path.dirname(__file__), "..", "data", "openreview_iclr2023.json")
os.makedirs(os.path.dirname(output_path), exist_ok=True)

with open(output_path, "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2)

print(f"✅ Saved {len(results)} OpenReview proposals to {output_path}")
