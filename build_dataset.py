import json
import random

# عدد الأمثلة المطلوب
NUM_EXAMPLES = 210  # ممكن تزود لـ 250 لو عندك repos كفاية

# قوالب Queries (مش كلها أسئلة عشان التنويع)
QUERY_TEMPLATES = [
    "We are integrating {service} into our architecture and need the most resilient option.",
    "Adding {service} support is becoming critical for scaling our distributed system.",
    "Our infrastructure depends heavily on {service}, so we are looking for the most reliable solution.",
    "We want a discovery-ready tool to automate how {service} is managed in production.",
    "Ensuring smooth adoption of {service} without downtime is our top priority.",
    "To improve observability, we are searching for a scalable solution for {service}.",
    "Dynamic scaling requires a self-healing service for {service}.",
    "The team is planning to expand workloads and needs {service} integration with discovery.",
]

# قوالب ground_truth
GROUND_TRUTH_TEMPLATES = [
    "This service provides a highly scalable and production-ready implementation of {service}, ensuring seamless integration with microservices and discovery systems.",
    "A distributed platform designed specifically to handle {service} in dynamic, large-scale environments, guaranteeing automation and reliability.",
    "This tool offers fault tolerance and self-healing mechanisms for {service}, making it ideal for modern service discovery workloads.",
    "A solution that enables zero-downtime updates for {service}, powered by strong consensus and adaptive scaling features.",
    "This framework is widely adopted for managing {service} and integrates natively with Kubernetes, cloud, and on-premise infrastructures.",
]

# قوالب relevance (كل مستوى ليه 6 قوالب عشان التنويع)
HIGH_RELEVANCE_TEMPLATES = [
    "It directly supports {service} in distributed service discovery scenarios with high reliability.",
    "This option ensures automation and smooth scaling for {service} without manual intervention.",
    "It is designed for production-grade deployments where {service} is mission critical.",
    "Consensus-driven design makes it highly aligned with {service} in discovery workloads.",
    "Proven in production environments with large-scale use of {service}.",
    "Fault tolerance and high availability make it perfect for {service} integration.",
]

MEDIUM_RELEVANCE_TEMPLATES = [
    "It partially supports {service}, but requires external plugins for full discovery integration.",
    "Scaling {service} is possible but may need additional manual setup.",
    "It offers some discovery capabilities but lacks native hooks for {service}.",
    "Can handle workloads with {service}, though resilience is limited.",
    "Designed with observability in mind but only partially suitable for {service}.",
    "Reliable for staging but not always production-ready for {service}.",
]

LOW_RELEVANCE_TEMPLATES = [
    "This tool focuses mainly on CI/CD pipelines, not related to {service}.",
    "It is built for database management, unrelated to {service} in discovery systems.",
    "The solution emphasizes security scanning, not supporting {service}.",
    "Its main purpose is orchestration of storage, not {service}.",
    "Optimized for analytics pipelines but not suitable for {service} use cases.",
    "Has nothing to do with {service} or service discovery in distributed systems.",
]

def load_github_repos(path="github_repos.json"):
    with open(path, "r") as f:
        repos = json.load(f)
    return [repo["name"] for repo in repos]

def build_dataset(num_examples=NUM_EXAMPLES):
    github_services = load_github_repos()

    if len(github_services) < num_examples:
        raise ValueError(f"⚠️ محتاج على الأقل {num_examples} خدمات (حاليًا {len(github_services)})")

    dataset = []
    used_queries = set()
    used_ground_truth = set()

    random.shuffle(github_services)

    for service in github_services[:num_examples]:
        # query
        query_template = random.choice(QUERY_TEMPLATES)
        query = query_template.format(service=service)
        while query in used_queries:
            query = random.choice(QUERY_TEMPLATES).format(service=service)

        # description
        description = f"The user is seeking a discovery-friendly solution that integrates {service} with scalability, resilience, and automation."

        # ground_truth
        gt_template = random.choice(GROUND_TRUTH_TEMPLATES)
        ground_truth = gt_template.format(service=service)
        while ground_truth in used_ground_truth:
            ground_truth = random.choice(GROUND_TRUTH_TEMPLATES).format(service=service)

        # relevance
        high_relevance = random.sample(HIGH_RELEVANCE_TEMPLATES, 4)
        medium_relevance = random.sample(MEDIUM_RELEVANCE_TEMPLATES, 4)
        low_relevance = random.sample(LOW_RELEVANCE_TEMPLATES, 4)

        dataset.append({
            "query": query,
            "description": description,
            "ground_truth": ground_truth,
            "high_relevance": [r.format(service=service) for r in high_relevance],
            "medium_relevance": [r.format(service=service) for r in medium_relevance],
            "low_relevance": [r.format(service=service) for r in low_relevance],
        })

        used_queries.add(query)
        used_ground_truth.add(ground_truth)

    # حفظ الملف
    with open("service_discovery_dataset.json", "w") as f:
        json.dump(dataset, f, indent=2, ensure_ascii=False)

    print(f"✅ تم إنشاء {len(dataset)} entries فـ service_discovery_dataset.json بدون أي تكرار.")

if __name__ == "__main__":
    build_dataset()
