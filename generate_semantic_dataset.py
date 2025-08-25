import json
import os
import random

NUM_RECORDS = 210

# --- قاعدة المعرفة الموسعة بشكل كبير جدًا (النسخة الصحيحة) ---
KNOWLEDGE_BASE = {
    "RegistryTools": {
        "detailed_queries": [
            "A comprehensive explanation of tools for service registries.",
            "Comparing features of HashiCorp Consul versus Netflix Eureka.",
            "How can a Key-Value store like etcd be used for service discovery?",
            "Best practices for leveraging DNS for service discovery in Kubernetes.",
            "An overview of service mesh technologies like Istio and their role in discovery.",
            "What are the core functionalities of a service registry?",
            "Exploring Apache Zookeeper as a service discovery mechanism."
        ],
        "ground_truth_candidates": [
            "Using HashiCorp Consul for dynamic service registration and health checking.",
            "Implementing a registry with Netflix Eureka for Spring Boot applications.",
            "Leveraging DNS-based service discovery natively within Kubernetes (Kube-DNS).",
            "Using a distributed Key-Value store like etcd for discovery mechanisms.",
            "Integrating a service mesh like Istio to handle service discovery and traffic management.",
            "The role of Apache Zookeeper in coordinating distributed systems.",
            "Core components of a service registry: registration, lookup, and health checking."
        ],
        "high_relevance": ["Configuring a Consul agent in client or server mode.", "Setting up a multi-node Eureka server cluster.", "The gossip protocol used by Consul.", "Integrating a registry with an API Gateway like Kong."],
        "medium_relevance": ["Implementing /health endpoints in microservices.", "The CAP theorem in distributed systems.", "Dynamic configuration updates from the registry.", "Basics of gRPC for inter-service communication."],
        "low_relevance": ["Manually updating a config file with IP addresses.", "Using a simple DNS A record.", "Hardcoding service endpoints in code.", "Fundamentals of TCP/IP networking."]
    },
    "DiscoveryPatterns": {
        "detailed_queries": [
            "An analysis of common microservice discovery patterns.",
            "Trade-offs between client-side and server-side discovery.",
            "An architectural overview of how services locate each other.",
            "A deep dive into the Service Registry architectural pattern.",
            "How does the Sidecar pattern facilitate service discovery?",
            "What is the role of a load balancer in server-side discovery?",
            "Explaining the 'service discovery per host' pattern."
        ],
        "ground_truth_candidates": [
            "A detailed comparison of Client-Side vs. Server-Side Discovery patterns.",
            "Implementing the Client-Side Discovery pattern with a library like Netflix Ribbon.",
            "Implementing the Server-Side Discovery pattern using a reverse proxy.",
            "The role of the Service Registry in both discovery patterns.",
            "Using the Sidecar pattern (e.g., with Envoy proxy) to abstract discovery logic.",
            "How load balancers like NGINX or HAProxy enable server-side discovery.",
            "The 'Service Discovery per Host' pattern using a local agent."
        ],
        "high_relevance": ["Trade-offs between patterns regarding complexity and performance.", "How API Gateways facilitate the Server-Side Discovery pattern.", "Challenges of discovery in multi-cloud environments.", "Service discovery in serverless architectures."],
        "medium_relevance": ["The API Gateway pattern explained.", "The Circuit Breaker pattern for fault tolerance.", "Containerization of services using Docker.", "Orchestration with Kubernetes for managing services."],
        "low_relevance": ["Designing a monolithic architecture.", "Direct database-to-database communication.", "Using a shared file system for communication.", "Writing a basic REST API with Flask."]
    },
    "HealthChecking": {
        "detailed_queries": [
            "Best practices for microservice health checking.",
            "How do service registries use health check status information?",
            "An overview of Kubernetes liveness and readiness probes.",
            "Differentiating between active and passive health checks.",
            "Implementing a custom /health endpoint in a service."
        ],
        "ground_truth_candidates": [
            "Implementing robust health checking mechanisms for microservices.",
            "Configuring active health checks by polling a dedicated HTTP /health endpoint.",
            "Using passive health checks by monitoring for failed connections.",
            "The distinct roles of Kubernetes Liveness, Readiness, and Startup probes.",
            "How service registries use health status to dynamically update routing tables."
        ],
        "high_relevance": ["Automatic removal of unhealthy service instances.", "Implementing custom health check logic beyond a simple status check.", "The importance of setting correct timeouts for health checks.", "Graceful shutdown procedures for services."],
        "medium_relevance": ["Centralized logging using the ELK stack.", "Distributed tracing with Jaeger or Zipkin.", "Metrics and monitoring with Prometheus and Grafana.", "Setting up alerting based on service health status."],
        "low_relevance": ["Manually checking a service with 'ping'.", "Relying on user complaints to detect outages.", "Using 'print' statements for debugging.", "Basic shell scripting for server management."]
    },
    "APIGateway": {
        "detailed_queries": [
            "The role of an API Gateway in a microservices architecture.",
            "Comparing API Gateway tools like Kong, Traefik, and Spring Cloud Gateway.",
            "How API Gateways integrate with service discovery mechanisms?",
            "What are the benefits of using an API Gateway?",
            "Explaining API composition and aggregation."
        ],
        "ground_truth_candidates": [
            "Using an API Gateway as a single entry point for all clients.",
            "Implementing routing and load balancing at the API Gateway level.",
            "Offloading cross-cutting concerns like authentication to the API Gateway.",
            "The API Gateway pattern vs. direct client-to-microservice communication.",
            "Implementing the API Composition pattern for aggregating results from multiple services."
        ],
        "high_relevance": ["Using an API Gateway for protocol translation (e.g., REST to gRPC).", "Implementing rate limiting and throttling on the API Gateway.", "Integrating the API Gateway dynamically with a service registry.", "Securing microservices with an API Gateway using JWT validation."],
        "medium_relevance": ["WebSockets vs. HTTP for real-time communication.", "Understanding RESTful API design principles.", "Securing APIs with OAuth 2.0 and OIDC.", "Introduction to message brokers like RabbitMQ or Kafka."],
        "low_relevance": ["Building a simple web server with Node.js Express.", "Frontend development with React or Vue.", "SQL database design and normalization.", "Writing unit tests for a simple application."]
    },
    "Observability": {
        "detailed_queries": [
            "Understanding observability in distributed systems.",
            "What are the three pillars of observability?",
            "Comparing centralized logging, distributed tracing, and metrics.",
            "How to implement distributed tracing for microservices?",
            "What is structured logging and why is it important?"
        ],
        "ground_truth_candidates": [
            "The three pillars of observability: logs, metrics, and traces.",
            "Implementing distributed tracing with open-source tools like Jaeger or Zipkin.",
            "Aggregating logs from multiple services using the ELK stack or Fluentd.",
            "Monitoring microservices with Prometheus for metrics collection and Grafana for visualization.",
            "Using structured logging (e.g., JSON format) for easier machine parsing."
        ],
        "high_relevance": ["Instrumenting application code to generate traces.", "The role of service meshes in providing observability.", "Correlation of logs, metrics, and traces for effective debugging.", "Setting up meaningful alerts based on SLOs and SLIs."],
        "medium_relevance": ["The difference between monitoring and observability.", "Introduction to time-series databases like InfluxDB.", "Cloud provider monitoring solutions (e.g., AWS CloudWatch).", "Building effective dashboards in Grafana."],
        "low_relevance": ["Reading log files manually on a server using 'tail' and 'grep'.", "Debugging with print statements.", "Using top/htop for real-time performance monitoring.", "Assuming services will never fail."]
    },
    "ConfigurationManagement": {
        "detailed_queries": [
            "How to manage configuration for hundreds of microservices?",
            "Externalized configuration pattern explained.",
            "What is a distributed configuration store?",
            "Managing secrets in a microservices environment.",
            "The role of feature flags in modern applications."
        ],
        "ground_truth_candidates": [
            "Using a centralized, externalized configuration store like Spring Cloud Config Server or Consul KV.",
            "The Externalized Configuration pattern for decoupling services from their config.",
            "Managing secrets securely with a tool like HashiCorp Vault.",
            "Injecting configuration into containers using Kubernetes ConfigMaps and Secrets.",
            "Implementing feature flags or toggles to control feature rollouts."
        ],
        "high_relevance": ["Dynamic 'hot reloading' of configuration without service restarts.", "Versioning configuration alongside application code.", "Hierarchical configuration for different environments (dev, staging, prod).", "Client-side libraries for accessing centralized configuration."],
        "medium_relevance": ["Using environment variables for configuration.", "Storing configuration in a version control system like Git.", "The 12-Factor App methodology for building modern applications.", "Introduction to GitOps principles."],
        "low_relevance": ["Hardcoding configuration values directly in the source code.", "Storing configuration in a simple .properties or .ini file.", "Manually SSH-ing into servers to change configuration.", "Storing plain-text passwords in configuration files."]
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
    print("Generating Final, Greatly Expanded, and Professional Semantic Dataset...")
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
    print(f"\nProfessional dataset with {len(dataset)} records saved to: {output_path}")

if __name__ == "__main__":
    main()
