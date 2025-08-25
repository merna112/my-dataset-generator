import json
import random

# Load fetched GitHub repos
with open("github_repos.json", "r", encoding="utf-8") as f:
    repos = json.load(f)

dataset = []

for i, repo in enumerate(repos, start=1):
    query = f"An architectural analysis of service discovery in {repo['name']} and how services locate each other."
    description = f"A semantic evaluation record for the repository {repo['name']}."
    ground_truth = f"A detailed exploration of {repo['name']} that compares client-side vs. server-side discovery mechanisms, scalability challenges, and fault tolerance strategies. Source: {repo['url']}"

    high_relevance = [
        f"The '{repo['name']}' project demonstrates host-based service discovery patterns.",
        "Challenges of discovery in heterogeneous or multi-cloud deployments.",
        "How API Gateways facilitate the Server-Side Discovery approach.",
        "Service discovery mechanisms in serverless and dynamic architectures."
    ]

    medium_relevance = [
        "The Circuit Breaker pattern for maintaining resilience.",
        "Containerization strategies for service deployments.",
        "Orchestration using Kubernetes for service management.",
        "An overview of API Gateway design patterns."
    ]

    low_relevance = [
        "Monolithic architecture design considerations.",
        "How to write a simple REST API with Flask.",
        "Direct database-to-database communication challenges.",
        "Using shared file systems for inter-process communication."
    ]

    dataset.append({
        "query": query,
        "description": description,
        "ground_truth": ground_truth,
        "high_relevance": high_relevance,
        "medium_relevance": medium_relevance,
        "low_relevance": low_relevance
    })

# نتاكد ان مفيش تكرار
unique_dataset = {entry["query"]: entry for entry in dataset}
final_dataset = list(unique_dataset.values())

with open("service_discovery_dataset.json", "w", encoding="utf-8") as f:
    json.dump(final_dataset, f, indent=4, ensure_ascii=False)

print("✅ Dataset generated: service_discovery_dataset.json")
