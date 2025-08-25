import json
import random
from faker import Faker

fake = Faker()

def generate_entry(i):
    query = f"Q{i}: {fake.sentence(nb_words=12)} about service discovery in distributed systems."
    description = f"A semantic evaluation record for the service discovery query {i}."
    ground_truth = f"A detailed technical explanation {i} comparing client-side vs server-side discovery patterns with scalability, resilience, and fault tolerance considerations."

    high_relevance = [
        f"Advanced scenario {i}-H1: {fake.sentence(nb_words=10)} related to host-based service discovery.",
        f"Advanced scenario {i}-H2: {fake.sentence(nb_words=12)} focusing on API Gateway discovery facilitation.",
        f"Advanced scenario {i}-H3: {fake.sentence(nb_words=14)} addressing multi-cloud service resolution.",
        f"Advanced scenario {i}-H4: {fake.sentence(nb_words=11)} covering serverless service discovery challenges."
    ]

    medium_relevance = [
        f"Related concept {i}-M1: {fake.sentence(nb_words=10)} discussing containerized microservices.",
        f"Related concept {i}-M2: {fake.sentence(nb_words=12)} describing orchestration with Kubernetes.",
        f"Related concept {i}-M3: {fake.sentence(nb_words=11)} about resilience with circuit breaker patterns.",
        f"Related concept {i}-M4: {fake.sentence(nb_words=13)} explaining API Gateway pattern generally."
    ]

    low_relevance = [
        f"Peripheral topic {i}-L1: {fake.sentence(nb_words=10)} about monolithic system design.",
        f"Peripheral topic {i}-L2: {fake.sentence(nb_words=12)} on basic REST API implementation.",
        f"Peripheral topic {i}-L3: {fake.sentence(nb_words=14)} regarding direct database communication.",
        f"Peripheral topic {i}-L4: {fake.sentence(nb_words=11)} about shared filesystem approaches."
    ]

    return {
        "query": query,
        "description": description,
        "ground_truth": ground_truth,
        "high_relevance": high_relevance,
        "medium_relevance": medium_relevance,
        "low_relevance": low_relevance
    }

# توليد اكتر من 200
dataset = [generate_entry(i) for i in range(1, 251)]  # 250 queries

with open("service_discovery_dataset.json", "w") as f:
    json.dump(dataset, f, indent=4)

print("✅ Dataset generated: service_discovery_dataset.json")
