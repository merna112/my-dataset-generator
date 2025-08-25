import json
import os
import random

NUM_RECORDS = 210

# --- قاعدة المعرفة الموسعة بشكل كبير لتوليد أكثر من 210 سجلًا فريدًا ---
KNOWLEDGE_BASE = {
    "RegistryTools": {
        "detailed_queries": [
            "A comprehensive explanation of tools for service registries like Consul and Eureka.",
            "Comparing the features and architectures of HashiCorp Consul versus Netflix Eureka.",
            "How can a Key-Value store such as etcd or Zookeeper be effectively used to implement service discovery?",
            "What are the best practices for leveraging native DNS for service discovery within a Kubernetes cluster?",
            "An overview of service mesh technologies like Istio and their role in service discovery."
        ],
        "ground_truth_candidates": [
            "Using HashiCorp Consul for dynamic service registration, health checking, and distributed Key-Value storage.",
            "Implementing a highly available service registry with Netflix Eureka for a fleet of Spring Boot applications.",
            "Leveraging the built-in DNS-based service discovery natively within Kubernetes (Kube-DNS/CoreDNS).",
            "Using a distributed Key-Value store like etcd as a foundational component for discovery mechanisms in large-scale systems.",
            "Integrating a service mesh like Istio or Linkerd to handle service discovery, routing, and traffic management."
        ],
        "high_relevance": ["Configuring a Consul agent in client or server mode for a production environment.", "Setting up a multi-node Eureka server cluster to ensure high availability.", "The gossip protocol used by Consul for cluster membership and failure detection.", "Integrating a service registry with an API Gateway like Kong or Traefik for dynamic routing."],
        "medium_relevance": ["Implementing health check endpoints (/health) in microservices.", "Understanding the CAP theorem in the context of distributed systems.", "Pushing dynamic configuration updates from the service registry to clients.", "Basics of gRPC for efficient inter-service communication."],
        "low_relevance": ["Manually updating a static configuration file with IP addresses.", "Using a simple DNS A record that points to a single service instance.", "Hardcoding service endpoints directly in the application source code.", "Fundamentals of TCP/IP networking and the OSI model."]
    },
    "DiscoveryPatterns": {
        "detailed_queries": [
            "A detailed analysis of common microservice discovery patterns and their trade-offs.",
            "What are the fundamental differences between client-side and server-side discovery?",
            "An architectural overview of how services locate and communicate with each other in a distributed system.",
            "A deep dive into the Service Registry architectural pattern.",
            "How does the Sidecar pattern facilitate service discovery?"
        ],
        "ground_truth_candidates": [
            "A detailed comparison of Client-Side Discovery vs. Server-Side Discovery patterns and their primary use-cases.",
            "Implementing the Client-Side Discovery pattern effectively using a smart client library like Netflix Ribbon or Spring Cloud LoadBalancer.",
            "Implementing the Server-Side Discovery pattern using a reverse proxy, load balancer, or an API Gateway.",
            "The critical role of the Service Registry as a central component in both client-side and server-side discovery patterns.",
            "Using the Sidecar pattern (e.g., with Envoy proxy) to abstract discovery logic away from the application."
        ],
        "high_relevance": ["An analysis of trade-offs between patterns regarding complexity, network hops, and performance.", "How modern API Gateways simplify the Server-Side Discovery pattern.", "The 'Service Discovery per Host' pattern using a local agent.", "Challenges of service discovery in multi-cloud or hybrid-cloud environments."],
        "medium_relevance": ["The API Gateway pattern explained with practical examples.", "The Circuit Breaker pattern for improving fault tolerance in distributed systems.", "Containerization of services using Docker for consistent environments.", "Orchestration with Kubernetes for managing the complete lifecycle of services."],
        "low_relevance": ["Designing a traditional monolithic application architecture.", "Direct database-to-database communication between different applications.", "Using a shared file system for inter-application communication and data exchange.", "Writing a basic REST API with a simple framework like Flask or Express."]
    },
    "HealthChecking": {
        "detailed_queries": [
            "What are the best practices for implementing microservice health checking?",
            "How do service registries like Consul use health check status information?",
            "An overview of Kubernetes liveness, readiness, and startup probes.",
            "Differentiating between active and passive health checks."
        ],
        "ground_truth_candidates": [
            "Implementing robust health checking mechanisms for microservices to ensure system reliability.",
            "Configuring active health checks by polling a dedicated HTTP /health or /ping endpoint.",
            "Using passive health checks by having the service registry monitor for failed connections or errors.",
            "The distinct roles of Kubernetes Liveness, Readiness, and Startup probes in managing pod lifecycle."
        ],
        "high_relevance": ["How service registries use health status to automatically update routing tables.", "Automatic removal and re-registration of unhealthy service instances.", "Implementing custom health check logic beyond a simple status check.", "The importance of setting correct timeouts and intervals for health checks."],
        "medium_relevance": ["Centralized logging for microservices using the ELK stack (Elasticsearch, Logstash, Kibana).", "Distributed tracing with tools like Jaeger or Zipkin to monitor request flows.", "Collecting and visualizing metrics with Prometheus and Grafana.", "Setting up an alerting system based on service health status and performance metrics."],
        "low_relevance": ["Manually checking if a service is running with the 'ping' command.", "Relying on user complaints and error reports to detect service outages.", "Using 'print' statements or console logs for debugging purposes.", "Basic shell scripting for starting and stopping server processes."]
    },
    "APIGateway": {
        "detailed_queries": [
            "What is the role of an API Gateway in a modern microservices architecture?",
            "Comparing popular API Gateway tools like Kong, Traefik, and Spring Cloud Gateway.",
            "How do API Gateways integrate with service discovery mechanisms?",
            "What are the benefits of using an API Gateway?"
        ],

        "ground_truth_candidates": [
            "Using an API Gateway as a single, unified entry point for all external clients.",
            "Implementing routing and load balancing for downstream services at the API Gateway level.",
            "Offloading cross-cutting concerns like authentication, rate limiting, and logging to the API Gateway.",
            "The API Gateway pattern versus direct client-to-microservice communication."
        ],
        "high_relevance": ["Using an API Gateway for protocol translation (e.g., external REST to internal gRPC).", "Implementing fine-grained rate limiting and throttling policies on the API Gateway.", "Integrating the API Gateway dynamically with a service registry like Consul.", "Securing microservice APIs with an API Gateway using patterns like JWT validation."],
        "medium_relevance": ["WebSockets vs. HTTP for real-time client-server communication.", "Understanding RESTful API design principles and best practices.", "Securing web APIs with OAuth 2.0 and OpenID Connect (OIDC).", "Introduction to asynchronous communication with message brokers like RabbitMQ or Kafka."],
        "low_relevance": ["Building a simple web server with Node.js and the Express framework.", "Frontend development using a JavaScript framework like React or Vue.", "SQL database design, normalization, and indexing.", "Writing and running unit tests for a simple application."]
    },
    "Containerization": {
        "detailed_queries": [
            "How does containerization with Docker impact service discovery?",
            "What are the benefits of running microservices in containers?",
            "An overview of container orchestration with Kubernetes.",
            "Explaining the concept of a Docker image and a container."
        ],
        "ground_truth_candidates": [
            "Using container orchestration platforms like Kubernetes to manage service discovery automatically.",
            "The role of Docker's ephemeral nature in making dynamic service discovery essential.",
            "How container networking and DNS work within a Kubernetes cluster.",
            "Using a sidecar proxy pattern in Kubernetes for service discovery."
        ],
        "high_relevance": ["Docker networking concepts: bridge, host, and overlay networks.", "Writing an effective Dockerfile for a microservice.", "Managing container lifecycles with Kubernetes Deployments and Services.", "The relationship between a Kubernetes Service and its underlying Pods."],
        "medium_relevance": ["Continuous Integration and Continuous Deployment (CI/CD) pipelines for containers.", "Storing container images in a registry like Docker Hub or Amazon ECR.", "Resource management (CPU/memory limits) for containers.", "Introduction to Infrastructure as Code (IaC) with tools like Terraform."],
        "low_relevance": ["Running applications on a bare-metal server.", "Virtualization with hypervisors like VMware or VirtualBox.", "Manual software installation and dependency management.", "File system permissions and user management in Linux."]
    },
    "FaultTolerance": {
        "detailed_queries": [
            "What is the Circuit Breaker pattern and how does it relate to service discovery?",
            "Strategies for building fault-tolerant microservices.",
            "How to handle failures when a discovered service is unavailable?",
            "Explaining concepts like retry mechanisms and timeouts."
        ],
        "ground_truth_candidates": [
            "Implementing the Circuit Breaker pattern to prevent cascading failures in a distributed system.",
            "Using a service registry's health check data to avoid routing requests to failing services.",
            "Configuring intelligent retry mechanisms with exponential backoff.",
            "The importance of setting appropriate timeouts for inter-service communication."
        ],
        "high_relevance": ["Bulkhead pattern for isolating service failures.", "The role of a service mesh in implementing fault tolerance patterns.", "Fallback mechanisms when a primary service is down.", "Distributed tracing for identifying bottlenecks and failure points."],
        "medium_relevance": ["Exception handling and error management in programming.", "Database replication and failover strategies.", "Load balancing for distributing traffic and avoiding single points of failure.", "Disaster recovery and business continuity planning."],
        "low_relevance": ["Assuming network communication is always reliable.", "Ignoring potential exceptions and errors in code.", "Running a single instance of every critical service.", "Restarting a server manually when it crashes."]
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
    print("Generating Final, Expanded, and Professional Semantic Dataset...")
    
    all_possible_pairs = []
    for concept_key, concept_data in KNOWLEDGE_BASE.items():
        for query in concept_data["detailed_queries"]:
            for ground_truth in concept_data["ground_truth_candidates"]:
                all_possible_pairs.append((query, ground_truth, concept_key))
    
    # الآن، هذا الرقم سيكون كبيرًا جدًا، أكبر من 210 بكثير
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
