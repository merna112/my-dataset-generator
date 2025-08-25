import json
import os
import random

NUM_RECORDS = 210

KNOWLEDGE_BASE = {
    "RegistryTools": {
        "detailed_queries": [
            "A comprehensive explanation of tools used for service registries in a microservices architecture.",
            "Comparing the features and use-cases of HashiCorp Consul versus Netflix Eureka.",
            "How can a Key-Value store like etcd be effectively used to implement service discovery?",
            "What are the best practices for leveraging DNS for service discovery within a Kubernetes cluster?"
        ],
        "ground_truth_candidates": [
            "Using HashiCorp Consul for dynamic service registration and robust health checking.",
            "Implementing a highly available service registry with Netflix Eureka for Spring Boot applications.",
            "Leveraging DNS-based service discovery natively within Kubernetes (Kube-DNS/CoreDNS).",
            "Using a distributed Key-Value store like etcd or Zookeeper for service discovery mechanisms."
        ],
        "high_relevance": [
            "Configuring a Consul agent in client or server mode for a production environment.",
            "Setting up a multi-node Eureka server cluster to ensure high availability.",
            "A deep dive into the gossip protocol used by Consul for cluster management.",
            "Integrating a service registry with an API Gateway like Kong or Traefik for dynamic routing."
        ],
        "medium_relevance": ["Implementing health check endpoints (/health) in microservices.", "Understanding the CAP theorem in the context of distributed systems.", "Pushing dynamic configuration updates from the service registry to clients.", "Basics of gRPC for efficient inter-service communication."],
        "low_relevance": ["Manually updating a static configuration file with IP addresses.", "Using a simple DNS A record that points to a single service instance.", "Hardcoding service endpoints directly in the application source code.", "Fundamentals of TCP/IP networking and the OSI model."]
    },
    "DiscoveryPatterns": {
        "detailed_queries": [
            "A detailed analysis of common microservice discovery patterns.",
            "What are the main differences and trade-offs between client-side and server-side discovery?",
            "An architectural overview of how services locate each other in a distributed system."
        ],
        "ground_truth_candidates": [
            "A detailed comparison of Client-Side Discovery vs. Server-Side Discovery patterns and their use-cases.",
            "Implementing the Client-Side Discovery pattern effectively using a library like Netflix Ribbon or Spring Cloud LoadBalancer.",
            "Implementing the Server-Side Discovery pattern using a reverse proxy or a modern load balancer.",
            "The critical role of the Service Registry in both client-side and server-side discovery patterns."
        ],
        "high_relevance": [
            "An analysis of the trade-offs between discovery patterns regarding complexity, network hops, and performance.",
            "How modern API Gateways facilitate and simplify the Server-Side Discovery pattern.",
            "The 'Service Discovery per Host' pattern using a local agent like Consul agent or Sidecar proxy.",
            "Addressing the challenges of service discovery in multi-cloud or hybrid-cloud environments."
        ],
        "medium_relevance": ["The API Gateway pattern explained with practical examples.", "The Circuit Breaker pattern for improving fault tolerance in distributed systems.", "Containerization of services using Docker for consistent environments.", "Orchestration with Kubernetes for managing the complete lifecycle of services."],
        "low_relevance": ["Designing a traditional monolithic application architecture.", "Direct database-to-database communication between different applications.", "Using a shared file system for inter-application communication and data exchange.", "Writing a basic REST API with a simple framework like Flask or Express."]
    }
}

def create_unique_record(used_ground_truths, used_queries):
    while True:
        concept_key = random.choice(list(KNOWLEDGE_BASE.keys()))
        concept_data = KNOWLEDGE_BASE[concept_key]
        
        potential_query = random.choice(concept_data["detailed_queries"])
        potential_ground_truth = random.choice(concept_data["ground_truth_candidates"])

        if potential_ground_truth not in used_ground_truths and potential_query not in used_queries:
            used_ground_truths.add(potential_ground_truth)
            used_queries.add(potential_query)
            break
    
    high_relevance_pool = [item for item in concept_data["high_relevance"] if item != potential_ground_truth]
    high_relevance_list = random.sample(high_relevance_pool, min(len(high_relevance_pool), 4))

    medium_relevance_list = random.sample(concept_data["medium_relevance"], 4)
    low_relevance_list = random.sample(concept_data["low_relevance"], 4)

    return {
        "query": potential_query,
        "description": f"A semantic evaluation record for the concept: {concept_key}.",
        "ground_truth": potential_ground_truth,
        "high_relevance": high_relevance_list,
        "medium_relevance": medium_relevance_list,
        "low_relevance": low_relevance_list,
    }

def main():
    dataset = []
    used_ground_truths = set()
    used_queries = set()
    
    total_possible_records = sum(len(v["detailed_queries"]) for v in KNOWLEDGE_BASE.values())
    if NUM_RECORDS > total_possible_records:
        print(f"Warning: Requesting {NUM_RECORDS} records, but only {total_possible_records} unique queries are available.")

    while len(dataset) < NUM_RECORDS:
        record = create_unique_record(used_ground_truths, used_queries)
        if record:
            dataset.append(record)

    output_dir = 'service_discovery_semantic_data'
    if not os.path.exists(output_dir): os.makedirs(output_dir)
            
    output_path = os.path.join(output_dir, 'service_discovery_semantic_queries.json')
    
    with open(output_path, 'w') as f:
        json.dump(dataset, f, indent=4)
    
    print(f"\nProfessional dataset saved to: {output_path}")

if __name__ == "__main__":
    main()
