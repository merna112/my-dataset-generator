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
        "protocol": ["REST"],
        "search_tags": ["payment", "billing", "stripe", "invoice", "subscription", "charge"]
    },
    "DataAnalytics": {
        "sub_services": ["TrackingCollector", "MetricsDashboard", "AB_Testing_Engine", "DataWarehouseIngestor"],
        "owner_team": "DataTeam",
        "protocol": ["Kafka", "HTTP"],
        "search_tags": ["analytics", "metrics", "tracking", "a/b test", "dashboard", "data"]
    },
    "NotificationService": {
        "sub_services": ["EmailSender", "PushNotificationDispatcher", "SMS_Gateway", "WebhookService"],
        "owner_team": "GrowthTeam",
        "protocol": ["gRPC", "HTTP"],
        "search_tags": ["notification", "email", "sms", "push", "alert"]
    }
}

def generate_service_name(domain, sub_service, protocol, team):
    return f"{domain}-{sub_service}-{protocol}-{team}"

def create_service_record(record_id): # <-- تم تغيير اسم الدالة
    domain_key = random.choice(list(SERVICE_CATALOG.keys()))
    domain_info = SERVICE_CATALOG[domain_key]
    
    sub_service = random.choice(domain_info["sub_services"])
    protocol = random.choice(domain_info["protocol"])
    team = domain_info["owner_team"]
    status = random.choice(["PRODUCTION", "BETA", "DEPRECATED"])
    
    # --- هذا هو التعديل الأهم لضمان عدم التكرار ---
    query = f"{random.choice(domain_info['search_tags'])} service instance-{record_id}"
    description = f"Official microservice for {sub_service.replace('_', ' ')}. Instance ID: {record_id}. Owner: {team}. Protocol: {protocol}. Status: {status}."
    
    ground_truth = generate_service_name(domain_key, sub_service, protocol, team)
    
    high_relevance = set()
    while len(high_relevance) < 4:
        alt_protocol = random.choice([p for p in domain_info["protocol"] if p != protocol] or [protocol])
        alt_sub_service = random.choice([s for s in domain_info["sub_services"] if s != sub_service] or [sub_service])
        high_relevance.add(generate_service_name(domain_key, sub_service, alt_protocol, team))
        high_relevance.add(generate_service_name(domain_key, alt_sub_service, protocol, team))
        high_relevance.discard(ground_truth)

    medium_relevance = set()
    while len(medium_relevance) < 4:
        alt_domain_key = random.choice([d for d in SERVICE_CATALOG.keys() if d != domain_key])
        alt_domain_info = SERVICE_CATALOG[alt_domain_key]
        medium_relevance.add(generate_service_name(alt_domain_key, random.choice(alt_domain_info["sub_services"]), random.choice(alt_domain_info["protocol"]), alt_domain_info["owner_team"]))
        
    low_relevance = set()
    unrelated_domains = [d for d in SERVICE_CATALOG.keys() if d != domain_key]
    while len(low_relevance) < 4 and unrelated_domains:
        low_domain = random.choice(unrelated_domains)
        low_info = SERVICE_CATALOG[low_domain]
        low_relevance.add(generate_service_name(low_domain, random.choice(low_info["sub_services"]), random.choice(low_info["protocol"]), low_info["owner_team"]))

    return {
        "query": query,
        "description": description,
        "ground_truth": ground_truth,
        "high_relevance": list(high_relevance)[:4],
        "medium_relevance": list(medium_relevance)[:4],
        "low_relevance": list(low_relevance)[:4],
    }

def main():
    print("Generating Final, Optimized Service Discovery Dataset...")
    # --- لم نعد بحاجة إلى حلقة while المعقدة ---
    dataset = [create_service_record(i) for i in range(NUM_RECORDS)]

    output_dir = 'service_discovery_data'
    if not os.path.exists(output_dir): os.makedirs(output_dir)
            
    output_path = os.path.join(output_dir, 'service_catalog_queries.json')
    
    with open(output_path, 'w') as f:
        json.dump(dataset, f, indent=4)
    
    print(f"\nFinal, Optimized dataset saved to: {output_path}")

if __name__ == "__main__":
    main()
