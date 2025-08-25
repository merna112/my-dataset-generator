import json
import os
import random

NUM_RECORDS = 250

SERVICE_CATALOG = {
    "Authentication": {
        "sub_services": ["UserLoginAPI", "TokenValidation", "PasswordReset", "OAuthProvider"],
        "owner_team": "PlatformTeam",
        "protocol": ["REST", "gRPC"],
        "search_tags": ["auth", "login", "user", "sso", "jwt", "password"]
    },
    "PaymentProcessing": {
        "sub_services": ["StripeGateway", "PaypalConnector", "SubscriptionManager", "InvoiceGenerator"],
        "owner_team": "FinTechTeam",
        "protocol": ["REST", "SOAP"],
        "search_tags": ["payment", "billing", "stripe", "invoice", "subscription", "charge"]
    },
    "DataAnalytics": {
        "sub_services": ["TrackingCollector", "MetricsDashboard", "AB_Testing_Engine", "DataWarehouseIngestor"],
        "owner_team": "DataTeam",
        "protocol": ["Kafka", "HTTP", "gRPC"],
        "search_tags": ["analytics", "metrics", "tracking", "a/b test", "dashboard", "data"]
    },
    "NotificationService": {
        "sub_services": ["EmailSender", "PushNotificationDispatcher", "SMS_Gateway", "WebhookService"],
        "owner_team": "GrowthTeam",
        "protocol": ["gRPC", "HTTP", "SMTP"],
        "search_tags": ["notification", "email", "sms", "push", "alert"]
    }
}

def generate_service_name(domain, sub_service, protocol, team):
    return f"{domain}-{sub_service}-{protocol}-{team}"

def get_robust_alternatives(source_list, current_item, count=4):
    alternatives = [item for item in source_list if item != current_item]
    random.shuffle(alternatives)
    return alternatives[:count]

def create_unique_service_record(used_pairs):
    while True:
        domain_key = random.choice(list(SERVICE_CATALOG.keys()))
        domain_info = SERVICE_CATALOG[domain_key]
        
        sub_service = random.choice(domain_info["sub_services"])
        protocol = random.choice(domain_info["protocol"])
        team = domain_info["owner_team"]
        
        # --- هذا هو التعديل الأهم ---
        query = f"{random.choice(domain_info['search_tags'])} service"
        description = f"An official microservice responsible for {sub_service.replace('_', ' ')} operations."
        
        if (query, description) not in used_pairs:
            used_pairs.add((query, description))
            break

    ground_truth = generate_service_name(domain_key, sub_service, protocol, team)
    
    alt_protocols = get_robust_alternatives(domain_info["protocol"], protocol)
    alt_sub_services = get_robust_alternatives(domain_info["sub_services"], sub_service)
    
    high_relevance_pool = set()
    for p in alt_protocols: high_relevance_pool.add(generate_service_name(domain_key, sub_service, p, team))
    for s in alt_sub_services: high_relevance_pool.add(generate_service_name(domain_key, s, protocol, team))
    high_relevance = random.sample(list(high_relevance_pool), min(len(high_relevance_pool), 4))

    other_domains = [d for d in SERVICE_CATALOG.keys() if d != domain_key]
    random.shuffle(other_domains)
    
    medium_relevance = []
    low_relevance = []

    for domain in other_domains:
        info = SERVICE_CATALOG[domain]
        service = generate_service_name(domain, random.choice(info["sub_services"]), random.choice(info["protocol"]), info["owner_team"])
        if len(medium_relevance) < 4:
            medium_relevance.append(service)
        elif len(low_relevance) < 4:
            low_relevance.append(service)
    
    return {
        "query": query,
        "description": description,
        "ground_truth": ground_truth,
        "high_relevance": high_relevance,
        "medium_relevance": medium_relevance,
        "low_relevance": low_relevance,
    }

def main():
    print("Generating Final, Polished Service Discovery Dataset...")
    dataset = []
    used_pairs = set()
    while len(dataset) < NUM_RECORDS:
        dataset.append(create_unique_service_record(used_pairs))

    output_dir = 'service_discovery_data'
    if not os.path.exists(output_dir): os.makedirs(output_dir)
            
    output_path = os.path.join(output_dir, 'service_catalog_queries.json')
    
    with open(output_path, 'w') as f:
        json.dump(dataset, f, indent=4)
    
    print(f"\nPolished dataset saved to: {output_path}")

if __name__ == "__main__":
    main()
