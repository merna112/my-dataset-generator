import json
import os
import random

NUM_RECORDS = 210

# --- قاعدة المعرفة الموسعة بشكل كبير لضمان التفرد ---
KNOWLEDGE_BASE = {
    "RegistryTools": {
        "detailed_queries": [
            "A comprehensive explanation of tools for service registries.",
            "Comparing features of HashiCorp Consul vs. Netflix Eureka.",
            "How can a Key-Value store like etcd be used for service discovery?",
            "Best practices for leveraging DNS for service discovery in Kubernetes."
        ],
        "ground_truth_candidates": [
            "Using HashiCorp Consul for dynamic service registration and health checking.",
            "Implementing a registry with Netflix Eureka for Spring Boot applications.",
            "Leveraging DNS-based service discovery natively within Kubernetes (Kube-DNS).",
            "Using a distributed Key-Value store like etcd for discovery mechanisms."
        ],
        "high_relevance": ["Configuring a Consul agent in client or server mode.", "Setting up a multi-node Eureka server cluster.", "The gossip protocol used by Consul.", "Integrating a registry with an API Gateway."],
        "medium_relevance": ["Implementing /health endpoints in microservices.", "The CAP theorem in distributed systems.", "Dynamic configuration updates from the registry.", "Basics of gRPC communication."],
        "low_relevance": ["Manually updating a config file with IP addresses.", "Using a simple DNS A record.", "Hardcoding service endpoints in code.", "Fundamentals of TCP/IP networking."]
    },
    "DiscoveryPatterns": {
        "detailed_queries": [
            "An analysis of common microservice discovery patterns.",
            "Trade-offs between client-side and server-side discovery.",
            "An architectural overview of how services locate each other.",
            "A deep dive into the Service Registry pattern."
        ],
        "ground_truth_candidates": [
            "A detailed comparison of Client-Side vs. Server-Side Discovery patterns.",
            "Implementing the Client-Side Discovery pattern with a library like Netflix Ribbon.",
            "Implementing the Server-Side Discovery pattern using a reverse proxy.",
            "The role of the Service Registry in both discovery patterns."
        ],

        "high_relevance": ["Trade-offs between patterns regarding complexity and performance.", "How API Gateways facilitate the Server-Side Discovery pattern.", "The 'Service Discovery per Host' pattern.", "Challenges of discovery in multi-cloud environments."],
        "medium_relevance": ["The API Gateway pattern explained.", "The Circuit Breaker pattern for fault tolerance.", "Containerization of services using Docker.", "Orchestration with Kubernetes."],
        "low_relevance": ["Designing a monolithic architecture.", "Direct database-to-database communication.", "Using a shared file system for communication.", "Writing a basic REST API with Flask."]
    },
    "HealthChecking": {
        "detailed_queries": [
            "Best practices for microservice health checking.",
            "How do service registries use health checks?",
            "An overview of Kubernetes liveness and readiness probes."
        ],
        "ground_truth_candidates": [
            "Implementing robust health checking mechanisms for microservices.",
            "Configuring active health checks via an HTTP /health endpoint.",
            "Using passive health checks by monitoring failed connections.",
            "The role of Kubernetes Liveness, Readiness, and Startup probes."
        ],
        "high_relevance": ["How service registries use health status to update routing tables.", "Automatic removal of unhealthy service instances.", "Implementing custom health check logic.", "The importance of setting correct timeouts for health checks."],
        "medium_relevance": ["Centralized logging using the ELK stack.", "Distributed tracing with Jaeger or Zipkin.", "Metrics and monitoring with Prometheus and Grafana.", "Setting up alerting based on service health status."],
        "low_relevance": ["Manually checking a service with 'ping'.", "Relying on user complaints to detect outages.", "Using 'print' statements for debugging.", "Basic shell scripting for server management."]
    },
    "APIGateway": {
        "detailed_queries": [
            "The role of an API Gateway in a microservices architecture.",
            "Comparing API Gateway tools like Kong, Traefik, and Spring Cloud Gateway.",
            "How API Gateways relate to service discovery."
        ],
        "ground_truth_candidates": [
            "Using an API Gateway as a single entry point for all clients.",
            "Implementing routing and load balancing at the API Gateway level.",
            "Offloading cross-cutting concerns like authentication to the API Gateway.",
            "The API Gateway pattern vs. direct client-to-microservice communication."
        ],
        "high_relevance": ["Using an API Gateway for protocol translation (e.g., REST to gRPC).", "Implementing rate limiting and throttling on the API Gateway.", "Integrating the API Gateway with a service registry.", "Securing microservices with an API Gateway."],
        "medium_relevance": ["WebSockets vs. HTTP for real-time communication.", "Understanding RESTful API design principles.", "Securing APIs with OAuth 2.0 and JWT.", "Introduction to message brokers like RabbitMQ or Kafka."],
        "low_relevance": ["Building a simple web server with Node.js Express.", "Frontend development with React or Vue.", "SQL database design and normalization.", "Writing unit tests for a simple application."]
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
    
    all_possible_pairs = []
    for concept_key, concept_data in KNOWLEDGE_BASE.items():
        for query in concept_data["detailed_queries"]:
            for ground_truth in concept_data["ground_truth_candidates"]:
                all_possible_pairs.append((query, ground_truth, concept_key))
    
    if NUM_RECORDS > len(all_possible_pairs):
        raise ValueError(f"Cannot generate {NUM_RECORDS} unique records, only {len(all_possible_pairs)} are possible. Please expand the knowledge base or reduce NUM_RECORDS.")

    random.shuffle(all_possible_pairs)
    selected_pairs = all_possible_pairs[:NUM_RECORDS]
    
    dataset = [create_record_from_pair(q, gt, ck) for q, gt, ck in selected_pairs]
    
    output_dir = 'service_discovery_semantic_data'
    if not os.path.exists(output_dir): os.makedirs(output_dir)
            
    output_path = os.path.join(output_dir, 'service_discovery_semantic_queries.json')
    
    with open(output_path, 'w') as f:
        json.dump(dataset, f, indent=4)
    
    print(f"\nProfessional dataset saved to: {output_path}")

if __name__ == "__main__":
    main()
