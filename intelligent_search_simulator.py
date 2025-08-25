import json
import os
from pprint import pprint
import random

DATASET_PATH = os.path.join('cse_evaluation_data', 'cse_project_queries.json')

def load_all_projects_with_tags(filepath):
    try:
        with open(filepath, 'r') as f:
            dataset = json.load(f)
    except FileNotFoundError:
        return None, None
    
    project_database = {}
    for record in dataset:
        all_projects_in_record = [record['ground_truth']] + record['high_relevance'] + record['medium_relevance'] + record['low_relevance']
        for project in all_projects_in_record:
            if project and project not in project_database:
                concept_key = project.split('-')[0]
                if concept_key in CONCEPTS:
                    project_database[project] = CONCEPTS[concept_key]['search_tags']
    
    return dataset, project_database

def find_matching_projects(query, project_database):
    query_words = set(query.lower().split())
    stop_words = {'ideas', 'for', 'graduation', 'project', 'a', 'an', 'the'}
    search_terms = query_words - stop_words
    
    matches = []
    for project, tags in project_database.items():
        if any(term in tag for term in search_terms for tag in tags):
            matches.append(project)
    return matches

def ranked_search(query_record, all_matches):
    gt = query_record['ground_truth']
    high = query_record['high_relevance']
    medium = query_record['medium_relevance']
    low = query_record['low_relevance']
    
    if gt in all_matches:
        return "Perfect Match", [gt]
        
    high_matches = [p for p in high if p in all_matches]
    if high_matches:
        return "High Relevance Matches", high_matches
        
    medium_matches = [p for p in medium if p in all_matches]
    if medium_matches:
        return "Medium Relevance Matches", medium_matches
        
    low_matches = [p for p in low if p in all_matches]
    if low_matches:
        return "Low Relevance Matches (better than nothing!)", low_matches
        
    return "No relevant projects found", []

def main():
    # This CONCEPTS dictionary needs to be defined here for the loading function to work
    global CONCEPTS
    CONCEPTS = {
        "MachineLearning": {"search_tags": ["machine learning", "ai", "artificial intelligence", "prediction", "computer vision", "nlp", "chatbot"]},
        "WebDevelopment": {"search_tags": ["web", "website", "frontend", "backend", "full-stack", "e-commerce", "social media"]},
        "MobileDevelopment": {"search_tags": ["mobile", "android", "ios", "app", "game", "food delivery"]},
        "CyberSecurity": {"search_tags": ["security", "cybersecurity", "encryption", "malware", "secure chat"]},
        "OperatingSystems": {"search_tags": ["os", "operating system", "kernel", "scheduler", "file system"]}
    }

    dataset, project_db = load_all_projects_with_tags(DATASET_PATH)
    if not dataset:
        print(f"Dataset not found. Please run Jenkins to generate '{DATASET_PATH}' first.")
        return

    test_record = random.choice(dataset)
    
    print("--- Simulating a User Search ---")
    print(f"User Query: \"{test_record['query']}\"")
    print(f"(The perfect answer should be: {test_record['ground_truth']})")
    
    all_potential_matches = find_matching_projects(test_record['query'], project_db)
    
    relevance_level, final_results = ranked_search(test_record, all_potential_matches)
    
    print("\n--- Final Ranked Results ---")
    print(f"Relevance Level Found: {relevance_level}")
    pprint(final_results)

if __name__ == "__main__":
    main()
