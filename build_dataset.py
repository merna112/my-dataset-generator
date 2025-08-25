import json
import random
from pathlib import Path

MIN_ACCEPT = 200   # أقل عدد مطلوب
MAX_ENTRIES = 250  # أقصى عدد

def load_repos(path="github_repos.json"):
    with open(path, "r") as f:
        return json.load(f)

def build_dataset(repos):
    dataset = []
    used_queries = set()
    used_truths = set()

    # Shuffle to get diversity
    random.shuffle(repos)

    for repo in repos:
        name = repo["name"]
        org = repo.get("org", "")
        desc = repo.get("description", "").strip()
        readme = repo.get("readme", "").strip()
        topics = set(repo.get("topics", []))

        if not desc:
            continue

        # query = first sentence from desc or readme
        query = (desc.split(".")[0] if desc else readme.split(".")[0]).strip()
        if not query or query in used_queries:
            continue

        # description = raw GitHub description
        description = desc

        # ground_truth = longer (description + optional details)
        ground_truth = f"{desc}. This repository, {name}, is maintained under the {org} organization and provides production-grade features with active community support."

        if ground_truth in used_truths:
            continue

        # High relevance = 4 repos from same org
        high = [
            f"{r['name']} integrates closely with {name} to provide complementary functionality within {org} ecosystem."
            for r in repos if r.get("org") == org and r["name"] != name
        ]
        high = high[:4]

        # Medium relevance = 4 repos sharing topics
        medium = [
            f"{r['name']} addresses similar areas to {name}, overlapping partly on topics like {', '.join(r.get('topics', []))}."
            for r in repos if r["name"] != name and topics.intersection(r.get("topics", []))
        ]
        medium = medium[:4]

        # Low relevance = 4 random repos with no overlap
        low_candidates = [r for r in repos if r["name"] != name and not topics.intersection(r.get("topics", [])) and r.get("org") != org]
        random.shuffle(low_candidates)
        low = [
            f"{r['name']} is primarily focused on unrelated functionality ({r.get('description','unrelated project')})."
            for r in low_candidates[:4]
        ]

        # Ensure structure 4/4/4
        if len(high) == 4 and len(medium) == 4 and len(low) == 4:
            dataset.append({
                "query": query,
                "description": description,
                "ground_truth": ground_truth,
                "high_relevance": high,
                "medium_relevance": medium,
                "low_relevance": low
            })
            used_queries.add(query)
            used_truths.add(ground_truth)

        if len(dataset) >= MAX_ENTRIES:
            break

    if len(dataset) < MIN_ACCEPT:
        raise RuntimeError(f"❌ Built only {len(dataset)} entries (<{MIN_ACCEPT}). Add more orgs or pages.")

    return dataset

if __name__ == "__main__":
    repos = load_repos()
    dataset = build_dataset(repos)

    with open("service_discovery_dataset.json", "w") as f:
        json.dump(dataset, f, indent=2, ensure_ascii=False)

    print(f"✅ Built {len(dataset)} entries and saved to service_discovery_dataset.json")
