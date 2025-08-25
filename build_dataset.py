import json
import random

# قاعدة المعرفة الموسعة (لازم نزود الخدمات عشان نوصل 250 مثال)
KNOWLEDGE_BASE = {
    "authentication": [
        "OAuth2 authentication service for large-scale applications",
        "JWT-based user authentication service for mobile and web APIs",
        "Single Sign-On (SSO) provider that integrates with enterprise identity systems",
        "Multi-factor authentication API for securing sensitive user data",
        "Token-based authentication service with refresh token support",
        "Passwordless authentication using email magic links",
        "Enterprise LDAP authentication integration",
        "Biometric authentication service with fingerprint and face ID",
        "Decentralized identity management with DID support",
        "Role-based access control service for distributed systems"
    ],
    "logging": [
        "Centralized logging service for collecting and analyzing application logs",
        "Real-time log aggregation platform that scales with microservices",
        "Error monitoring and alerting service to detect issues in production",
        "Log storage and search system built on the ELK stack",
        "Cloud-based logging API with advanced search and filtering",
        "Audit logging system for compliance and security",
        "Structured JSON logging for machine-readable pipelines",
        "Distributed log collection with Fluentd integration",
        "Log anomaly detection using machine learning",
        "Serverless logging service optimized for AWS Lambda"
    ],
    "messaging": [
        "Message queue service with RabbitMQ for decoupled communication",
        "Kafka streaming platform for high-throughput data pipelines",
        "Pub/Sub messaging system for real-time event broadcasting",
        "Real-time notifications service for mobile and web applications",
        "Event-driven architecture support with guaranteed delivery",
        "High-availability message broker with clustering support",
        "Transactional message queue with exactly-once delivery",
        "Lightweight MQTT messaging service for IoT devices",
        "Event streaming platform with schema registry support",
        "Cloud-based messaging system with SLA-backed reliability"
    ],
    "monitoring": [
        "Application performance monitoring (APM) service with real-time metrics",
        "Distributed tracing platform for debugging microservices",
        "Prometheus-based monitoring system with alerting",
        "Cloud-native monitoring service with Grafana dashboards",
        "Real-time system health monitoring API for large-scale deployments",
        "Synthetic monitoring service for user experience testing",
        "Container monitoring with deep Kubernetes integration",
        "Log-based metrics monitoring with flexible queries",
        "Custom metrics ingestion service for heterogeneous systems",
        "Blackbox monitoring tool for network and endpoint availability"
    ]
}

# قوالب الـ Query (كتيرة عشان ميبقاش فيه تكرار سهل)
QUERY_TEMPLATES = [
    "I am building a new mobile app and I need a service that provides {}",
    "Can you recommend a reliable platform that supports {} for my application?",
    "Looking for an API that helps with {} in a production environment",
    "I need a scalable solution for {} in my project",
    "Which service would you suggest if I want to implement {} in my system?",
    "My enterprise system requires {} — what service should I choose?",
    "In terms of microservices architecture, which tool can deliver {}?",
    "For cloud-native workloads, what’s the best option to achieve {}?",
    "Our project cannot go live unless we have {} — any suggestions?",
    "I want to integrate {} into my DevOps workflow, which service is recommended?"
]

def generate_example(category, ground_truth, used_queries):
    # query باستخدام قالب مع ground truth
    while True:
        query_template = random.choice(QUERY_TEMPLATES)
        query = query_template.format(ground_truth.lower())
        if query not in used_queries:
            used_queries.add(query)
            break
    
    # high relevance (من نفس الفئة)
    high_relevance = random.sample([s for s in KNOWLEDGE_BASE[category] if s != ground_truth], 4)
    
    # medium relevance (من فئة قريبة)
    other_categories = [c for c in KNOWLEDGE_BASE if c != category]
    medium_category = random.choice(other_categories)
    medium_relevance = random.sample(KNOWLEDGE_BASE[medium_category], 4)
    
    # low relevance (من فئة تانية أبعد)
    remaining_categories = [c for c in other_categories if c != medium_category]
    low_category = random.choice(remaining_categories)
    low_relevance = random.sample(KNOWLEDGE_BASE[low_category], 4)
    
    return {
        "query": query,
        "ground_truth": ground_truth,
        "high_relevance": high_relevance,
        "medium_relevance": medium_relevance,
        "low_relevance": low_relevance
    }

def build_dataset(num_examples=250, output_file="service_discovery_dataset.json"):
    dataset = []
    used_queries = set()
    used_ground_truths = set()

    # نحول كل الخدمات لقائمة
    all_services = []
    for category, services in KNOWLEDGE_BASE.items():
        for service in services:
            all_services.append((category, service))

    if num_examples > len(all_services):
        raise ValueError(f"⚠️ محتاج على الأقل {num_examples} خدمات مختلفة في KNOWLEDGE_BASE (حاليًا {len(all_services)})")

    # نختار خدمات عشوائية بدون تكرار
    selected_services = random.sample(all_services, num_examples)

    for category, ground_truth in selected_services:
        example = generate_example(category, ground_truth, used_queries)
        dataset.append(example)
        used_ground_truths.add(ground_truth)

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(dataset, f, indent=4, ensure_ascii=False)

    print(f"✅ Dataset generated with {num_examples} unique examples -> {output_file}")

if __name__ == "__main__":
    build_dataset(250)
