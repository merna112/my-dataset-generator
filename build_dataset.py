import json
import random

# عدد الأمثلة المطلوب
NUM_EXAMPLES = 250

# قوالب Queries
QUERY_TEMPLATES = [
    "I need a service to handle {service} in my infrastructure",
    "Which tool should I use for {service}?",
    "Can you recommend something for {service} in production?",
    "What’s the best choice for managing {service}?",
    "Is there a reliable solution for {service} available?",
    "We’re planning to add {service}, what should we use?",
]

# فئات الـ relevance
RELEVANCE_LEVELS = ["high", "medium", "low"]

def load_github_repos(path="github_repos.json"):
    with open(path, "r") as f:
        repos = json.load(f)
    return [repo["name"] for repo in repos]

def build_dataset(num_examples=NUM_EXAMPLES):
    github_services = load_github_repos()
    available_services = len(github_services)

    print("======================================")
    print(f"📥 Loaded {available_services} services from GitHub")
    print("======================================")

    # لو أقل من المطلوب → نشتغل بالعدد الموجود بس
    if available_services < num_examples:
        print(f"⚠️ Requested {num_examples} examples but only {available_services} services available")
        num_examples = available_services

    dataset = []
    used_queries = set()
    used_ground_truth = set()

    random.shuffle(github_services)

    for i, service in enumerate(github_services[:num_examples]):
        query_template = random.choice(QUERY_TEMPLATES)
        query = query_template.format(service=service)

        while query in used_queries:  # ضمان عدم تكرار الـ queries
            query_template = random.choice(QUERY_TEMPLATES)
            query = query_template.format(service=service)

        relevance = random.choice(RELEVANCE_LEVELS)

        example = {
            "id": i + 1,
            "query": query,
            "ground_truth": service,
            "relevance": relevance
        }

        dataset.append(example)
        used_queries.add(query)
        used_ground_truth.add(service)

    # حفظ الملف
    with open("service_discovery_dataset.json", "w") as f:
        json.dump(dataset, f, indent=2, ensure_ascii=False)

    print("======================================")
    print(f"✅ Final dataset size: {len(dataset)} examples")
    print(f"📦 Unique ground_truth values: {len(used_ground_truth)}")
    print("======================================")
    print("👉 Saved to service_discovery_dataset.json")

if __name__ == "__main__":
    build_dataset()
