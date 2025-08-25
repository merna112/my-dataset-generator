import json
import sys

with open("service_discovery_dataset.json", "r", encoding="utf-8") as f:
    dataset = json.load(f)

queries = set()
truths = set()
errors = []

for i, entry in enumerate(dataset, 1):
    q = entry.get("query")
    gt = entry.get("ground_truth")
    high = entry.get("high_relevance", [])
    medium = entry.get("medium_relevance", [])
    low = entry.get("low_relevance", [])

    # تحقق من uniqueness
    if q in queries:
        errors.append(f"[Entry {i}] Duplicate query: {q}")
    if gt in truths:
        errors.append(f"[Entry {i}] Duplicate ground_truth: {gt}")

    queries.add(q)
    truths.add(gt)

    # تحقق من العدد
    if len(high) != 4:
        errors.append(f"[Entry {i}] High relevance count != 4")
    if len(medium) != 4:
        errors.append(f"[Entry {i}] Medium relevance count != 4")
    if len(low) != 4:
        errors.append(f"[Entry {i}] Low relevance count != 4")

if errors:
    print("❌ Validation failed with errors:")
    for e in errors:
        print(" -", e)
    sys.exit(1)
else:
    print(f"✅ Validation passed: {len(dataset)} entries, all unique and well-formed.")
