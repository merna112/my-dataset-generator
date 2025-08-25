import json
import random

# قاعدة المعرفة (KNOWLEDGE_BASE)
DISCOVERY_PATTERNS = [
    "client-side discovery", "server-side discovery",
    "service registry with Eureka", "service registry with Consul",
    "Kubernetes DNS-based discovery", "API Gateway based discovery",
    "service mesh (Istio, Linkerd)", "headless services in Kubernetes"
]

CONTEXTS = [
    "microservices architecture", "serverless systems",
    "multi-cloud environments", "hybrid cloud deployments",
    "edge computing scenarios", "IoT networks",
    "container orchestration with Kubernetes", "fault-tolerant systems"
]

CHALLENGES = [
    "scalability", "latency", "network partitions",
    "resilience", "observability", "fault tolerance",
    "high availability", "dynamic scaling"
]

ACTIONS = [
    "analyze", "evaluate", "compare", "critique",
    "discuss", "optimize", "explain", "investigate"
]

LOW_TOPICS = [
    "monolithic applications", "basic REST API design",
    "direct database connections", "file-based configuration sharing",
    "SQL joins optimization", "desktop application patterns"
]

def generate_query(i):
    action = random.choice(ACTIONS)
    pattern = random.choice(DISCOVERY_PATTERNS)
    context = random.choice(CONTEXTS)
    challenge = random.choice(CHALLENGES)

    query = f"Q{i}: {action.capitalize()} how {pattern} addresses {challenge} in {context}, and contrast it with alternative discovery strategies."
    ground_truth = (
        f"This query examines the role of {pattern} within {context}. "
        f"It specifically highlights {challenge} challenges and provides a comparison against at least one other discovery approach. "
        f"The analysis should address trade-offs in scalability, resilience, and operational complexity."
    )

    return query, ground_truth, pattern, context, challenge

def generate_relevance(pattern, context, challenge):
    # High relevance = قريب جدًا من query
    high = random.sample(DISCOVERY_PATTERNS, 4)
    if pattern not in high:
        high[0] = pattern

    # Medium relevance = broader domain topics
    medium = random.sample(CONTEXTS + CHALLENGES, 4)
    if context not in medium:
        medium[0] = context

    # Low relevance = irrelevant topics
    low = random.sample(LOW_TOPICS, 4)

    return high, medium, low

# ------------------------
# بناء الـ dataset
# ------------------------
dataset = []
used_queries = set()
used_truths = set()

for i in range(1, 251):  # 250 queries
    query, ground_truth, pattern, context, challenge = generate_query(i)

    # تأكد من عدم التكرار
    if query in used_queries or ground_truth in used_truths:
        continue

    high, medium, low = generate_relevance(pattern, context, challenge)

    entry = {
        "query": query,
        "description": f"A semantic evaluation record for query {i}.",
        "ground_truth": ground_truth,
        "high_relevance": high,
        "medium_relevance": medium,
        "low_relevance": low
    }

    dataset.append(entry)
    used_queries.add(query)
    used_truths.add(ground_truth)

# حفظ الملف
with open("service_discovery_dataset.json", "w", encoding="utf-8") as f:
    json.dump(dataset, f, indent=4, ensure_ascii=False)

print(f"✅ Dataset generated with {len(dataset)} unique queries")
