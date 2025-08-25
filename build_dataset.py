import json
import random

NUM_EXAMPLES = 250   # عدد الـ services المطلوبة (كل واحدة = 12 مثال)

QUERY_TEMPLATES = [
    "I need a service to handle {service} in my infrastructure",
    "Which tool should I use for {service}?",
    "Can you recommend something for {service} in production?",
    "What’s the best choice for managing {service}?",
    "Is there a reliable solution for {service} available?",
    "We’re planning to add {service}, what should we use?",
    "Looking for recommendations to implement {service} efficiently",
    "Any open-source project that solves {service}?",
    "Best practices around {service} in enterprise systems?",
]

RELEVANCE_LEVELS = ["high", "medium", "low"]

def load_github_repos(path="github_repos.json"):
    with open(path, "r") as f:
        repos = json.load(f)
    return [repo["name"] for repo in repos]

def build_dataset(num_examples=NUM_EXAMPLES):
    github_services = load_github_repos()
    available_services = len(github_services)

    if available_services < num_examples:
        raise ValueError(f"⚠️ محتاج على الأقل {num_examples} خدمات (حاليًا {available_services})")

    dataset = []
    used_queries = set()
    random.shuffle(github_services)

    id_counter = 1
    for service in github_services[:num_examples]:
        entry_examples = []

        for relevance in RELEVANCE_LEVELS:
            for _ in range(4):   # 4 أمثلة لكل مستوى relevance
                query_template = random.choice(QUERY_TEMPLATES)
                query = query_template.format(service=service)

                while query in used_queries:  # ضمان عدم التكرار
                    query_template = random.choice(QUERY_TEMPLATES)
                    query = query_template.format(service=service)

                example = {
                    "id": id_counter,
                    "query": query,
                    "ground_truth": service,
                    "relevance": relevance
                }

                entry_examples.append(example)
                dataset.append(example)
                used_queries.add(query)
                id_counter += 1

        # check إن كل entry عنده 12 مثال
        assert len(entry_examples) == 12, f"Entry for {service} not complete!"

    with open("service_discovery_dataset.json", "w") as f:
        json.dump(dataset, f, indent=2, ensure_ascii=False)

    print(f"✅ Dataset built: {len(dataset)} queries for {num_examples} services")
    print(f"📊 Each entry = 12 queries (4 high, 4 medium, 4 low)")

if __name__ == "__main__":
    build_dataset()
