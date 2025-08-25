import json
import os
import random

NUM_RECORDS = 210

# --- قاموس المعرفة المتخصص والموسع ---
SERVICE_DISCOVERY_KB = {
    "RegistryTools": {
        "ground_truth": ["Using tools like HashiCorp Consul or Netflix Eureka for dynamic service registration."],
        "high_relevance": ["Configuring a Consul agent in client/server mode.", "Setting up a Eureka server for Spring Boot clients.", "Using etcd or Zookeeper as a Key-Value store for service data.", "Leveraging DNS-based service discovery in Kubernetes."],
        "medium_relevance": ["Implementing health checks for registered services.", "Using an API Gateway to route traffic.", "Dynamic configuration updates from the service registry.", "Understanding the CAP theorem for distributed systems."],
        "low_relevance": ["Manually updating a config file with IP addresses.", "Using a simple DNS A record for service location.", "Hardcoding service endpoints in application code.", "Basics of TCP/IP networking."]
    },
    "DiscoveryPatterns": {
        "ground_truth": ["Comparing Client-Side Discovery vs. Server-Side Discovery patterns."],
        "high_relevance": ["Implementing Client-Side Discovery with a library like Netflix Ribbon.", "Implementing Server-Side Discovery using a load balancer.", "The role of the Service Registry in discovery patterns.", "Trade-offs between the two main discovery patterns."],
        "medium_relevance": ["The API Gateway pattern with tools like Kong or Traefik.", "The Circuit Breaker pattern for handling service failures.", "Containerization of services using Docker.", "Orchestration with Kubernetes."],
        "low_relevance": ["Designing a monolithic application architecture.", "Direct database-to-database communication.", "Using a shared file system for communication.", "Writing a basic REST API with Flask."]
    },
    "HealthChecking": {
        "ground_truth": ["Implementing robust health checking mechanisms for microservices."],
        "high_relevance": ["Configuring active health checks via an HTTP /health endpoint.", "Using passive health checks by monitoring failed connections.", "Kubernetes Liveness, Readiness, and Startup probes.", "How registries use health status to update routing tables."],
        "medium_relevance": ["Centralized logging using the ELK stack.", "Distributed tracing with Jaeger or Zipkin.", "Metrics and monitoring with Prometheus and Grafana.", "Setting up alerting based on service health status."],
        "low_relevance": ["Manually checking a service with the 'ping' command.", "Relying on user complaints to detect outages.", "Using 'print' statements for debugging.", "Basic shell scripting for server management."]
    }
}

# --- قوالب لزيادة التنوع ومنع التكرار ---
QUERY_TEMPLATES = ["looking for information on {}", "explain {}", "how to implement {}", "best practices for {}"]
DESC_TEMPLATES = ["A document explaining the concept of {}.", "This record provides an overview of {}.", "An entry detailing the implementation of {}."]
QUERY_TAGS = ["service registry", "discovery patterns", "health checks", "consul", "eureka", "microservices"]

def create_unique_semantic_record(used_pairs):
    while True:
        # نختار المكونات بشكل عشوائي
        query_template = random.choice(QUERY_TEMPLATES)
        desc_template = random.choice(DESC_TEMPLATES)
        random_tag = random.choice(QUERY_TAGS)
        concept_key = random.choice(list(SERVICE_DISCOVERY_KB.keys()))
        
        # نركب الـ Query والـ Description
        query = query_template.format(random_tag)
        description = desc_template.format(concept_key)
        
        # نتحقق من التفرد
        if (query, description) not in used_pairs:
            used_pairs.add((query, description))
            break
    
    concept_data = SERVICE_DISCOVERY_KB[concept_key]
    
    ground_truth_text = concept_data["ground_truth"][0]
    high_relevance_list = random.sample(concept_data["high_relevance"], 4)
    medium_relevance_list = random.sample(concept_data["medium_relevance"], 4)
    low_relevance_list = random.sample(concept_data["low_relevance"], 4)

    return {
        "query": query,
        "description": description,
        "ground_truth": ground_truth_text,
        "high_relevance": high_relevance_list,
        "medium_relevance": medium_relevance_list,
        "low_relevance": low_relevance_list,
    }

def main():
    print("Generating Final, Unique, Specialized Semantic Dataset...")
    dataset = []
    used_pairs = set()
    # نستخدم حلقة while لضمان الوصول إلى العدد المطلوب بالضبط
    while len(dataset) < NUM_RECORDS:
        dataset.append(create_unique_semantic_record(used_pairs))

    output_dir = 'service_discovery_semantic_data'
    if not os.path.exists(output_dir): os.makedirs(output_dir)
            
    output_path = os.path.join(output_dir, 'service_discovery_semantic_queries.json')
    
    with open(output_path, 'w') as f:
        json.dump(dataset, f, indent=4)
    
    print(f"\nFinal dataset saved to: {output_path}")

if __name__ == "__main__":
    main()
