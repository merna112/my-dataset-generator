import json, sys, os, re

IN = "service_discovery_dataset.json"

def main():
    if not os.path.exists(IN):
        print(f"❌ {IN} not found")
        sys.exit(1)
    with open(IN, "r", encoding="utf-8") as f:
        data = json.load(f)

    errs = []
    seen_q = set()
    seen_gt = set()
    seen_rel = set()

    for i, x in enumerate(data, 1):
        # counts
        if len(x.get("high_relevance",[])) != 4:
            errs.append(f"[Entry {i}] High relevance count != 4")
        if len(x.get("medium_relevance",[])) != 4:
            errs.append(f"[Entry {i}] Medium relevance count != 4")
        if len(x.get("low_relevance",[])) != 4:
            errs.append(f"[Entry {i}] Low relevance count != 4")

        # lengths
        q = x.get("query","").strip()
        d = x.get("description","").strip()
        gt = x.get("ground_truth","").strip()

        if len(q) < 60: errs.append(f"[Entry {i}] Query too short")
        if len(gt) < 160: errs.append(f"[Entry {i}] Ground truth too short")
        if "-" in gt: errs.append(f"[Entry {i}] Ground truth must not contain '-'")

        # uniqueness
        if q in seen_q: errs.append(f"[Entry {i}] Duplicate query")
        seen_q.add(q)

        if gt in seen_gt: errs.append(f"[Entry {i}] Duplicate ground_truth")
        seen_gt.add(gt)

        for sec in ("high_relevance","medium_relevance","low_relevance"):
            for s in x.get(sec,[]):
                s = s.strip()
                if s in seen_rel:
                    errs.append(f"[Entry {i}] Duplicate relevance sentence across dataset")
                seen_rel.add(s)

    if errs:
        print("❌ Validation failed with errors:")
        for e in errs[:200]:
            print(" -", e)
        sys.exit(1)
    else:
        print(f"✅ Validation passed for {len(data)} entries.")

if __name__ == "__main__":
    main()
