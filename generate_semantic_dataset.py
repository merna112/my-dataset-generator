import json
import os
import random

NUM_RECORDS = 210

KNOWLEDGE_BASE = {
    "RegistryTools": {
        "detailed_queries": [
            "A comprehensive explanation of tools used for service registries.",
            "Comparing the features of HashiCorp Consul versus Netflix Eureka.",
            "How can a Key-Value store like etcd be used for service discovery?",
            "Best practices for leveraging DNS for service discovery in Kubernetes."
        ],
        "ground_truth_candidates": [
            "Using HashiCorp Consul for dynamic service registration and health checking.",
            "Implementing a registry with Netflix Eureka for Spring Boot applications.",
            "Leveraging DNS-based service discovery natively within Kubernetes (Kube-DNS).",
            "Using a distributed Key-Value store like etcd for discovery mechanisms."
        ],
        "high_relevance": ["Configuring a Consul agent in client or server mode.", "Setting up a multi-node Eureka server cluster.", "Understanding the gossip protocol used by Consul.", "Integrating a service registry with an API Gateway like Kong."],
        "medium_relevance": ["Implementing health check endpoints in microservices.", "Understanding the CAP theorem for distributed systems.", "Dynamic configuration updates from the registry.", "Basics of gRPC for inter-service communication."],
        "low_relevance": ["Manually updating a static configuration file with IP addresses.", "Using a simple DNS A record for a single service.", "Hardcoding service endpoints in application code.", "Fundamentals of TCP/IP networking."]
    },
    "DiscoveryPatterns": {
        "detailed_queries": [
            "An analysis of common microservice discovery patterns.",
            "What are the trade-offs between client-side and server-side discovery?",
            "An architectural overview of how services locate each other."
        ],
        "ground_truth_candidates": [
            "A detailed comparison of Client-Side vs. Server-Side Discovery patterns.",
            "Implementing the Client-Side Discovery pattern with a library like Netflix Ribbon.",
            "Implementing the Server-Side Discovery pattern using a reverse proxy.",
            "The role of the Service Registry in both discovery patterns."
        ],
        "high_relevance": ["Trade-offs between patterns regarding complexity and performance.", "How API Gateways facilitate the Server-Side Discovery pattern.", "The 'Service Discovery per Host' pattern using a local agent.", "Challenges of service discovery in multi-cloud environments."],
        "medium_relevance": ["The API Gateway pattern explained.", "The Circuit Breaker pattern for fault tolerance.", "Containerization of services using Docker.", "Orchestration with Kubernetes for managing services."],
        "low_relevance": ["Designing a monolithic application architecture.", "Direct database-to-database communication.", "Using a shared file system for communication.", "Writing a basic REST API with Flask."]
    }
}

def create_record_from_pair(query, ground_truth, concept_key):
    concept_data = KNOWLEDGE_BASE[concept_key]
    
    high_relevance_pool = [item for item in concept_data["high_relevance"] if item != ground_truth]
    high_relevance_list = random.sample(high_relevance_pool, min(len(high_relevance_pool), 4))

    medium_relevance_list = random.sample(concept_data["medium_relevance"], 4)
    low_relevance_list = random.sample(concept_data["low_relevance"], 4)

    return {
        "query": query,
        "description": f"A semantic evaluation record for the concept: {concept_key}.",
        "ground_truth": ground_truth,
        "high_relevance": high_relevance_list,
        "medium_relevance": medium_relevance_list,
        "low_relevance": low_relevance_list,
    }

def main():
    print("Generating Final, Deterministic, and Professional Semantic Dataset...")
    
    # --- الخطوة 1: بناء قائمة بكل الأزواج الفريدة الممكنة ---
    all_possible_pairs = []
    for concept_key, concept_data in KNOWLEDGE_BASE.items():
        for query in concept_data["detailed_queries"]:
            for ground_truth in concept_data["ground_truth_candidates"]:
                all_possible_pairs.append((query, ground_truth, concept_key))
    
    # --- التحقق من أن لدينا ما يكفي من البيانات ---
    if NUM_RECORDS > len(all_possible_pairs):
        raise ValueError(f"Cannot generate {NUM_RECORDS} unique records, only {len(all_possible_pairs)} are possible with the current knowledge base.")

    # --- الخطوة 2: خلط القائمة واختيار العدد المطلوب ---
    random.shuffle(all_possible_pairs)
    selected_pairs = all_possible_pairs[:NUM_RECORDS]
    
    # --- الخطوة 3: بناء السجلات النهائية من الأزواج المختارة ---
    dataset = [create_record_from_pair(q, gt, ck) for q, gt, ck in selected_pairs]
    
    output_dir = 'service_discovery_semantic_data'
    if not os.path.exists(output_dir): os.makedirs(output_dir)
            
    output_path = os.path.join(output_dir, 'service_discovery_semantic_queries.json')
    
    with open(output_path, 'w') as f:
        json.dump(dataset, f, indent=4)
    
    print(f"\nProfessional dataset saved to: {output_path}")

if __name__ == "__main__":
    main()
