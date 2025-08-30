import json
import os
import random

NUM_RECORDS = 210

# --- قاعدة المعرفة الموسعة بشكل جنوني لضمان النجاح ---
KNOWLEDGE_BASE = {
    "RegistryTools": {
        "detailed_queries": ["tools for service registries", "consul vs eureka", "etcd for service discovery", "dns in kubernetes for discovery", "service mesh and discovery", "core functions of a registry", "zookeeper for discovery", "comparing discovery tools"],
        "ground_truth_candidates": ["using hashicorp consul for registration and health checking", "implementing a registry with netflix eureka", "leveraging dns-based discovery in kubernetes", "using etcd as a key-value store for discovery", "integrating istio to handle discovery", "the role of apache zookeeper in coordination", "core components of a service registry api", "a survey of modern service discovery tools"],
        "high_relevance": ["configuring a consul agent", "setting up a multi-node eureka cluster", "the gossip protocol in consul", "integrating a registry with an api gateway"],
        "medium_relevance": ["implementing /health endpoints", "the cap theorem", "dynamic configuration updates", "basics of grpc"],
        "low_relevance": ["manual config file updates", "using a simple dns a record", "hardcoding service endpoints", "tcp/ip fundamentals"]
    },
    "DiscoveryPatterns": {
        "detailed_queries": ["microservice discovery patterns analysis", "client-side vs server-side discovery", "how services locate each other", "the service registry pattern deep-dive", "sidecar pattern for discovery", "load balancer role in discovery", "service discovery per host pattern", "shared registry pattern"],
        "ground_truth_candidates": ["a comparison of client-side vs. server-side discovery patterns", "implementing client-side discovery with netflix ribbon", "implementing server-side discovery with a reverse proxy", "the role of the service registry in discovery patterns", "using the sidecar pattern with envoy proxy", "how load balancers enable server-side discovery", "the 'service discovery per host' pattern with a local agent", "the shared registry pattern explained"],
        "high_relevance": ["trade-offs between patterns in complexity and performance", "how api gateways simplify server-side discovery", "challenges of discovery in multi-cloud environments", "service discovery in serverless architectures"],
        "medium_relevance": ["the api gateway pattern", "the circuit breaker pattern", "containerization with docker", "orchestration with kubernetes"],
        "low_relevance": ["designing a monolithic architecture", "direct database-to-database communication", "using a shared file system", "writing a basic rest api"]
    },
    "HealthChecking": {
        "detailed_queries": ["microservice health checking best practices", "how registries use health checks", "kubernetes liveness and readiness probes", "active vs passive health checks", "implementing a custom /health endpoint"],
        "ground_truth_candidates": ["implementing robust health checking mechanisms", "configuring active health checks via http polling", "using passive health checks by monitoring connections", "the roles of kubernetes liveness, readiness, and startup probes", "how registries use health status to update routing"],
        "high_relevance": ["automatic removal of unhealthy instances", "implementing custom health check logic", "setting correct timeouts for health checks", "graceful shutdown procedures"],
        "medium_relevance": ["centralized logging with the elk stack", "distributed tracing with jaeger", "metrics and monitoring with prometheus", "alerting based on service health"],
        "low_relevance": ["manual checking with 'ping'", "relying on user complaints", "debugging with 'print' statements", "basic shell scripting"]
    },
    "APIGateway": {
        "detailed_queries": ["role of an api gateway in microservices", "comparing api gateway tools", "api gateways and service discovery integration", "benefits of using an api gateway", "api composition and aggregation"],
        "ground_truth_candidates": ["using an api gateway as a single entry point", "implementing routing and load balancing at the gateway", "offloading cross-cutting concerns to the gateway", "api gateway pattern vs. direct client communication", "implementing the api composition pattern"],
        "high_relevance": ["using a gateway for protocol translation", "implementing rate limiting and throttling", "integrating the gateway with a service registry", "securing microservices with a gateway and jwt"],
        "medium_relevance": ["websockets vs. http", "restful api design principles", "securing apis with oauth 2.0", "introduction to message brokers"],
        "low_relevance": ["building a simple web server with express", "frontend development with react", "sql database design", "writing unit tests"]
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
    print("Generating Final, Guaranteed 210 Records Dataset...")
    all_possible_pairs = []
    for concept_key, concept_data in KNOWLEDGE_BASE.items():
        for query in concept_data["detailed_queries"]:
            for ground_truth in concept_data["ground_truth_candidates"]:
                all_possible_pairs.append((query, ground_truth, concept_key))
    
    random.shuffle(all_possible_pairs)
    
    dataset = []
    # --- هذا هو المنطق الجديد والمضمون ---
    # نأخذ كل الأزواج الفريدة المتاحة أولاً
    unique_pairs_to_use = all_possible_pairs
    
    # ننشئ السجلات من الأزواج الفريدة
    for q, gt, ck in unique_pairs_to_use:
        dataset.append(create_record_from_pair(q, gt, ck))
        
    # إذا لم نصل إلى 210، نكرر من البداية بشكل عشوائي حتى نصل
    while len(dataset) < NUM_RECORDS:
        q, gt, ck = random.choice(all_possible_pairs)
        dataset.append(create_record_from_pair(q, gt, ck))
        
    # نأخذ فقط أول 210 سجل لضمان العدد المطلوب بالضبط
    final_dataset = dataset[:NUM_RECORDS]
    random.shuffle(final_dataset) # نخلط الترتيب النهائي
    
    output_dir = 'service_discovery_semantic_data'
    if not os.path.exists(output_dir): os.makedirs(output_dir)
    output_path = os.path.join(output_dir, 'service_discovery_semantic_queries.json')
    with open(output_path, 'w') as f:
        json.dump(final_dataset, f, indent=4)
    print(f"\nProfessional dataset with exactly {len(final_dataset)} records saved to: {output_path}")

if __name__ == "__main__":
    main()
