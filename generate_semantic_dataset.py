import json
import os
import random

NUM_RECORDS = 210

# --- قاعدة المعرفة النهائية (مع جمل طويلة ومفصلة) ---
KNOWLEDGE_BASE = {
    "RegistryTools": {
        "detailed_queries": [
            "Provide a comprehensive explanation of the primary tools used for implementing service registries in a modern, cloud-native microservices architecture.",
            "Conduct a detailed feature and architectural comparison between HashiCorp Consul and Netflix Eureka as service discovery solutions.",
            "How can a distributed Key-Value store like etcd or Zookeeper be effectively utilized as the foundational backend for a custom service discovery mechanism?",
            "What are the established best practices for leveraging the native DNS capabilities within a Kubernetes cluster for reliable service discovery?",
            "Offer a detailed overview of how service mesh technologies, such as Istio or Linkerd, fundamentally alter the approach to service discovery and traffic management."
        ],
        "ground_truth_candidates": [
            "A thorough guide on using HashiCorp Consul for dynamic service registration, robust health checking of services, and leveraging its distributed Key-Value store for configuration management.",
            "Implementing a highly available and fault-tolerant service registry using Netflix Eureka, specifically tailored for a fleet of Spring Boot applications in a large-scale deployment.",
            "Leveraging the built-in, resilient DNS-based service discovery natively within a Kubernetes environment (Kube-DNS/CoreDNS) for stateless and stateful services.",
            "Using a distributed Key-Value store like etcd as the foundational, consistent data layer for building custom discovery mechanisms in large-scale, distributed systems.",
            "Integrating an advanced service mesh like Istio or Linkerd to transparently handle service discovery, secure mTLS communication, and manage complex traffic routing."
        ],
        "high_relevance": [
            "A step-by-step tutorial on configuring a Consul agent in either client or server mode for a production-ready, multi-datacenter environment.",
            "Architectural patterns for setting up a multi-node, peer-aware Eureka server cluster to ensure high availability and prevent single points of failure.",
            "A deep-dive into the gossip protocol (Serf) used by Consul for efficient cluster membership, failure detection, and event propagation.",
            "A practical guide to integrating a service registry with an API Gateway like Kong or Traefik to enable dynamic upstream routing and load balancing."
        ],
        "medium_relevance": [
            "Best practices for implementing comprehensive health check endpoints (e.g., /health, /live, /ready) within microservices to report their status.",
            "A detailed explanation of the CAP theorem (Consistency, Availability, Partition tolerance) and its implications on the design of distributed systems like service registries.",
            "Techniques for pushing dynamic configuration updates from a service registry or config store to a fleet of running services without requiring restarts.",
            "An introduction to the fundamentals of gRPC for building high-performance, low-latency inter-service communication."
        ],
        "low_relevance": [
            "The process of manually updating a static configuration file (e.g., XML, YAML) with a list of service IP addresses and ports.",
            "Using a simple DNS A record that points to a single, non-redundant service instance, creating a single point of failure.",
            "The practice of hardcoding service endpoints and credentials directly in the application source code, which complicates updates and security.",
            "A basic overview of the TCP/IP networking stack and the layers of the OSI model, without discussing application-level protocols."
        ]
    },
    "DiscoveryPatterns": {
        "detailed_queries": [
            "Provide a detailed analysis of the most common microservice discovery patterns, including an evaluation of their respective trade-offs in real-world scenarios.",
            "What are the fundamental architectural and operational differences between the client-side discovery and server-side discovery patterns?",
            "Give a comprehensive architectural overview of the mechanisms that allow services to locate and communicate with each other in a highly dynamic, distributed system.",
            "Offer a deep dive into the Service Registry as a core architectural pattern, explaining its components and responsibilities.",
            "How does the Sidecar pattern, particularly in the context of service meshes, facilitate and enhance service discovery?"
        ],
        "ground_truth_candidates": [
            "A detailed technical comparison of the Client-Side Discovery pattern versus the Server-Side Discovery pattern, analyzing their primary use-cases, performance characteristics, and fault tolerance implications.",
            "A guide to implementing the Client-Side Discovery pattern effectively by integrating a smart client library like Netflix Ribbon or Spring Cloud LoadBalancer directly into the application.",
            "A walkthrough of implementing the Server-Side Discovery pattern by utilizing a reverse proxy, a modern load balancer, or a dedicated API Gateway to handle routing logic.",
            "The critical role of the Service Registry as a central, highly available component that acts as the source of truth for service locations in both client-side and server-side discovery patterns.",
            "Using the Sidecar pattern, often implemented with a proxy like Envoy, to completely abstract and decouple all service discovery and networking logic from the application code."
        ],
        "high_relevance": [
            "A thorough analysis of the trade-offs between discovery patterns, focusing on aspects like architectural complexity, network hops, latency, and overall system performance.",
            "A discussion on how modern API Gateways like Kong or Traefik can simplify and enhance the Server-Side Discovery pattern by centralizing routing, security, and observability.",
            "An exploration of the 'Service Discovery per Host' pattern, which utilizes a local agent on each node to reduce network traffic to the central registry.",
            "Addressing the significant challenges of implementing reliable service discovery in complex multi-cloud or hybrid-cloud environments."
        ],
        "medium_relevance": [
            "The API Gateway pattern explained with practical examples, demonstrating its role as a single entry point for external requests.",
            "A detailed explanation of the Circuit Breaker pattern as a critical tool for improving fault tolerance and preventing cascading failures in distributed systems.",
            "An overview of the benefits of containerizing services using Docker to create consistent, portable, and isolated runtime environments.",
            "An introduction to container orchestration with Kubernetes for managing the complete lifecycle of services, including deployment, scaling, and updates."
        ],
        "low_relevance": [
            "A guide to designing a traditional, tightly-coupled monolithic application architecture where components communicate via in-process calls.",
            "The anti-pattern of direct database-to-database communication between different applications, leading to high coupling and brittleness.",
            "Using a shared file system as a crude and unreliable method for inter-application communication and data exchange.",
            "A tutorial on writing a basic REST API with a simple framework like Flask or Express without considering distributed system challenges."
        ]
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
    print("Generating Final, Long-Form, Professional Semantic Dataset...")
    
    all_possible_pairs = []
    for concept_key, concept_data in KNOWLEDGE_BASE.items():
        for query in concept_data["detailed_queries"]:
            for ground_truth in concept_data["ground_truth_candidates"]:
                all_possible_pairs.append((query, ground_truth, concept_key))
    
    if NUM_RECORDS > len(all_possible_pairs):
        raise ValueError(f"FATAL: Cannot generate {NUM_RECORDS} unique records, only {len(all_possible_pairs)} are possible. Please expand the KNOWLEDGE_BASE.")

    random.shuffle(all_possible_pairs)
    selected_pairs = all_possible_pairs[:NUM_RECORDS]
    
    dataset = [create_record_from_pair(q, gt, ck) for q, gt, ck in selected_pairs]
    
    output_dir = 'service_discovery_semantic_data'
    if not os.path.exists(output_dir): os.makedirs(output_dir)
            
    output_path = os.path.join(output_dir, 'service_discovery_semantic_queries.json')
    
    with open(output_path, 'w') as f:
        json.dump(dataset, f, indent=4)
    
    print(f"\nProfessional dataset with {len(dataset)} records saved to: {output_path}")

if __name__ == "__main__":
    main()
