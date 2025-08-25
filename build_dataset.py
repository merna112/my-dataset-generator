import json
import random

# الحد الأقصى للأمثلة
NUM_EXAMPLES = 250

# قوالب Queries (مش كلها أسئلة)
QUERY_TEMPLATES = [
    "Looking into integrating {service} as part of our platform services",
    "We are exploring solutions around {service} in cloud-native workflows",
    "Trying to evaluate best practices for {service} management",
    "Planning to extend system capabilities with {service}",
    "Searching for reliable technologies to cover {service} at scale",
    "Our architecture requires a solid approach to {service}",
    "Considering migration paths that involve {service}",
    "We want to benchmark different tools for {service}"
]

# أوصاف للخدمات
DESCRIPTION_TEMPLATES = [
    "This service is designed to improve scalability and fault-tolerance in distributed systems.",
    "It provides advanced automation capabilities suitable for large-scale enterprise operations.",
    "Known for its strong community support and frequent updates, making it reliable in production.",
    "It integrates seamlessly with CI/CD pipelines and modern DevOps practices.",
    "The service emphasizes security, monitoring, and compliance features for regulated environments.",
    "It is optimized for high throughput and low latency workloads across different clusters.",
    "Flexibility and modularity make it adaptable to various deployment scenarios.",
    "Often recommended for teams adopting microservices and containerized applications."
]

# توليد relevance طويلة (٤ عناصر)
def generate_relevance(service, level):
    base_text = {
        "high": f"Highly suitable for production-grade usage of {service}, offering robust reliability, scalability, and security features.",
        "medium": f"Moderately useful for {service}, fits well in certain contexts but may lack some advanced capabilities.",
        "low": f"Not generally recommended for critical {service} tasks, as it might have limited stability or ecosystem support."
    }

    expansions = {
        "high": [
            "Strong ecosystem adoption and proven track record in enterprise deployments.",
            "Seamless integrations with monitoring, logging, and orchestration layers.",
            "Performance benchmarks consistently show excellent resource efficiency.",
            "Comprehensive documentation and active community ensuring continuous improvements."
        ],
        "medium": [
            "Good option for smaller teams experimenting with {service}.",
            "Covers most essential requirements but lacks advanced optimizations.",
            "Integration paths exist but require additional setup effort.",
            "Community support is available but not as strong as leading alternatives."
        ],
        "low": [
            "Minimal adoption outside niche scenarios makes it risky for production.",
            "Missing core features required for complex {service} workloads.",
            "Documentation and updates are sparse, leading to potential maintenance issues.",
            "Few integrations with mainstream DevOps or observability tools."
        ]
    }

    return [base_text[level]] + [exp.format(service=service) for exp in expansions[level]]

def load_github_repos(path="github_repos.json"):
    with open(path, "r") as f:
        repos = json.load(f)
    return [repo["name"] for repo in repos]

def build_dataset(num_examples=NUM_EXAMPLES):
    github_services = load_github_repos()
    available_services = len(github_services)

    if available_services < 200:
        raise ValueError(f"⚠️ محتاج على الأقل 200 خدمة من GitHub (حاليًا {available_services})")

    dataset_size = min(num_examples, available_services)
    random.shuffle(github_services)

    dataset = []
    used_queries = set()

    for service in github_services[:dataset_size]:
        # نضمن query مختلفة
        query_template = random.choice(QUERY_TEMPLATES)
        query = query_template.format(service=service)
        while query in used_queries:
            query_template = random.choice(QUERY_TEMPLATES)
            query = query_template.format(service=service)

        description = random.choice(DESCRIPTION_TEMPLATES)

        entry = {
            "query": query,
            "description": description,
            "ground_truth": service,
            "high_relevance": generate_relevance(service, "high"),
            "medium_relevance": generate_relevance(service, "medium"),
            "low_relevance": generate_relevance(service, "low")
        }

        dataset.append(entry)
        used_queries.add(query)

    with open("service_discovery_dataset.json", "w") as f:
        json.dump(dataset, f, indent=2, ensure_ascii=False)

    print(f"✅ تم إنشاء {len(dataset)} مثال وحفظهم في service_discovery_dataset.json")

if __name__ == "__main__":
    build_dataset()
