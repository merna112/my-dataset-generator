import json
import os
import random

NUM_RECORDS = 250

CONCEPTS = {
    "MachineLearning": {
        "sub_topics": ["ImageRecognition", "Chatbot", "RecommendationEngine", "SentimentAnalysis"],
        "tech_stack": ["Python", "TensorFlow", "PyTorch", "Scikit-learn"],
        "search_tags": ["machine learning", "ai", "artificial intelligence", "prediction", "computer vision", "nlp", "chatbot"]
    },
    "WebDevelopment": {
        "sub_topics": ["E-commerceSite", "SocialNetwork", "BookingPlatform", "BlogEngine"],
        "tech_stack": ["JavaScript", "React", "NodeJS", "Django", "SQL", "MongoDB"],
        "search_tags": ["web", "website", "frontend", "backend", "full-stack", "e-commerce", "social media"]
    },
    "MobileDevelopment": {
        "sub_topics": ["GameApp", "UtilityApp", "HealthTracker", "FoodDeliveryApp"],
        "tech_stack": ["Kotlin", "Swift", "ReactNative", "Flutter"],
        "search_tags": ["mobile", "android", "ios", "app", "game", "food delivery"]
    },
    "CyberSecurity": {
        "sub_topics": ["Firewall", "PasswordManager", "VulnerabilityScanner", "SecureChat"],
        "tech_stack": ["Python", "C++", "Cryptography"],
        "search_tags": ["security", "cybersecurity", "encryption", "malware", "secure chat"]
    },
    "OperatingSystems": {
        "sub_topics": ["CustomShell", "FileSystem", "ProcessScheduler"],
        "tech_stack": ["C", "Assembly", "Rust"],
        "search_tags": ["os", "operating system", "kernel", "scheduler", "file system"]
    }
}

RELATED_CONCEPTS = {
    "MachineLearning": ["WebDevelopment"],
    "WebDevelopment": ["CyberSecurity"],
    "MobileDevelopment": ["WebDevelopment"]
}

def generate_project_name(concept, sub_topic, tech):
    return f"{concept}-{sub_topic}-{tech}-{random.choice(['Alpha', 'Beta', 'Omega'])}"

def create_cse_record():
    concept_key = random.choice(list(CONCEPTS.keys()))
    concept_info = CONCEPTS[concept_key]
    
    sub_topic = random.choice(concept_info["sub_topics"])
    tech = random.choice(concept_info["tech_stack"])
    
    ground_truth = generate_project_name(concept_key, sub_topic, tech)
    
    query = f"ideas for {random.choice(concept_info['search_tags'])} graduation project"
    description = f"A university project on {sub_topic.replace('_', ' ')} using {tech}, falling under the {concept_key} domain."
    
    high_relevance = {generate_project_name(concept_key, sub_topic, t) for t in concept_info["tech_stack"] if t != tech}
    high_relevance.update({generate_project_name(concept_key, st, tech) for st in concept_info["sub_topics"] if st != sub_topic})
    
    medium_relevance = set()
    for related_key in RELATED_CONCEPTS.get(concept_key, []):
        related_info = CONCEPTS[related_key]
        medium_relevance.add(generate_project_name(related_key, random.choice(related_info["sub_topics"]), random.choice(related_info["tech_stack"])))
    
    low_relevance = set()
    unrelated_keys = [k for k in CONCEPTS if k != concept_key and k not in RELATED_CONCEPTS.get(concept_key, [])]
    if unrelated_keys:
        low_key = random.choice(unrelated_keys)
        low_info = CONCEPTS[low_key]
        low_relevance.add(generate_project_name(low_key, random.choice(low_info["sub_topics"]), random.choice(low_info["tech_stack"])))

    return {
        "query": query,
        "description": description,
        "ground_truth": ground_truth,
        "tags": concept_info['search_tags'],
        "high_relevance": list(high_relevance)[:4],
        "medium_relevance": list(medium_relevance)[:4],
        "low_relevance": list(low_relevance)[:4],
    }

def main():
    dataset = [create_cse_record() for _ in range(NUM_RECORDS)]
    
    output_dir = 'cse_evaluation_data'
    if not os.path.exists(output_dir): os.makedirs(output_dir)
            
    output_path = os.path.join(output_dir, 'cse_project_queries.json')
    
    with open(output_path, 'w') as f:
        json.dump(dataset, f, indent=4)
    
    print(f"\nDataset saved to: {output_path}")

if __name__ == "__main__":
    main()
