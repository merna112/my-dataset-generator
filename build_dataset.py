import json
import random

INPUT_FILE = "github_repos.json"
OUTPUT_FILE = "service_discovery_dataset.json"

NUM_ENTRIES = 210  # العدد المطلوب

def load_repos():
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def build_dataset():
    repos = load_repos()
    random.shuffle(repos)

    dataset = []
    used_queries = set()

    for repo in repos:
        desc = repo["description"]
        if not desc or len(desc.split()) < 6:
            continue

        # query = جزء من الوصف (أول جملة أو أول 12 كلمة)
        query = " ".join(desc.split()[:12])
        if query in used_queries:
            continue
        used_queries.add(query)

        # description = الوصف الأصلي من GitHub
        description = desc

        # ground_truth = الوصف كامل + جملة إضافية للتوسيع
        ground_truth = (
            f"{desc} This project provides extended service discovery, "
            f"configuration, and integration features that scale across "
            f"cloud-native and hybrid infrastructures."
        )

        # high/medium/low relevance (نولّد من repos تانية عشان التنوع)
        other_repos = [r for r in repos if r["name"] != repo["name"]]
        random.shuffle(other_repos)

        high = [f"{r['name']} works closely with {repo['name']} to enhance discovery and integration workflows."
                for r in other_repos[:4]]

        medium = [f"{r['name']} provides related capabilities but diverges in focus compared to {repo['name']}."
                  for r in other_repos[4:8]]

        low = [f"{r['name']} is mainly about {r['description']} and has no direct link to {repo['name']}."
               for r in other_repos[8:12]]

        if len(high) < 4 or len(medium) < 4 or len(low) < 4:
            continue

        dataset.append({
            "query": query,
            "description": description,
            "ground_truth": ground_truth,
            "high_relevance": high,
            "medium_relevance": medium,
            "low_relevance": low
        })

        if len(dataset) >= NUM_ENTRIES:
            break

    if len(dataset) < NUM_ENTRIES:
        raise RuntimeError(f"❌ Only built {len(dataset)} entries (<{NUM_ENTRIES})")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(dataset, f, indent=2, ensure_ascii=False)

    print(f"✅ Dataset built with {len(dataset)} entries → {OUTPUT_FILE}")

if __name__ == "__main__":
    build_dataset()
