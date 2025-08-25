import json
import random

NUM_EXAMPLES = 250

QUERY_TEMPLATES = [
    "I need a service to handle {service} in my infrastructure",
    "Which tool should I use for {service}?",
    "Can you recommend something for {service} in production?",
    "What’s the best choice for managing {service}?",
    "Is there a reliable solution for {service} available?",
    "We’re planning to add {service}, what should we use?",
]

RELEVANCE_LEVELS = ["high", "medium", "low"]

def load_github_repos(path="github_repos.json"):
    with open(path, "r") as f:
        repos = json.load(f)
    return [repo["name"] for repo in repos]

def build_dataset(num_examples=NUM_EXAMPLES):
    github_services = load_github_repos()
    available_services = len(github_services)

    print(f"📥 Loaded {available_services} services from GitHub")

    if available_services < num_examples:
        print(f"⚠️ Requested {num_examples} but only {available_services} available")
        num_examples = available_services

    dataset = []
    used_queries = set()

    random.shuffle(github_services)

    relevance_cycle = []
    # وزّع التكرار: 4 High + 4 Medium + 4 Low
    relevance_cycle.extend(["high"] * 4)
    relevance_cycle.extend(["medium"] * 4)
    relevance_cycle.extend(["low"] * 4)

    idx = 0
    for i, service in enumerate(github_services[:num_examples]):
        query_template = random.choice(QUERY_TEMPLATES)
        query = query_template.format(service=service)

        while query in used_queries:  # ضمان عدم التكرار
            query_template = random.choice(QUERY_TEMPLATES)
            query = query_template.format(service=service)

        relevance = relevance_cycle[idx % len(relevance_cycle)]  # توزيع مضبوط
        idx += 1

        example = {
            "id": i + 1,
            "query": query,
            "ground_truth": service,
            "relevance": relevance
        }

        dataset.append(example)
        used_queries.add(query)

    with open("service_discovery_dataset.json", "w") as f:
        json.dump(dataset, f, indent=2, ensure_ascii=False)

    print(f"✅ Dataset built: {len(dataset)} examples")
    print("📊 Distribution check:")
    print("High:", sum(1 for e in dataset if e["relevance"] == "high"))
    print("Medium:", sum(1 for e in dataset if e["relevance"] == "medium"))
    print("Low:", sum(1 for e in dataset if e["relevance"] == "low"))

if __name__ == "__main__":
    build_dataset()
