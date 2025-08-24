import pandas as pd
import random
import json
import os

NUM_QUERIES = 250

DOMAINS = {
    "Backend": {"tech": ["Go", "Python", "Java", "Rust"], "types": ["Microservice", "API", "DataProcessor", "QueueConsumer"]},
    "Frontend": {"tech": ["React", "Vue", "Svelte", "Angular"], "types": ["WebApp", "ComponentLibrary", "PWA"]},
    "DataScience": {"tech": ["Python", "R", "Scala"], "types": ["ML_Model", "DataPipeline", "AnalyticsDashboard", "FeatureStore"]},
    "DevOps": {"tech": ["Terraform", "Kubernetes", "Ansible", "Docker"], "types": ["IaC_Module", "CI_Pipeline", "MonitoringStack"]},
    "Mobile": {"tech": ["Kotlin", "Swift", "ReactNative"], "types": ["AndroidApp", "iOSApp", "MobileSDK"]}
}

PROJECT_CODENAMES = ["Aether", "Helios", "Orion", "Cygnus", "Phoenix", "Valkyrie", "Nexus", "Apex"]
STATUS = ["Active", "Deprecated", "Experimental"]
QUERY_ACTIONS = ["find", "get", "show me", "where is the", "I need the"]

def generate_project_id(domain, codename, p_type, tech):
    return f"{domain}-{codename}-{p_type}-{tech}"

def get_related_tech(tech):
    relations = {"Go": "Docker", "Python": "Flask", "React": "TypeScript", "Terraform": "AWS"}
    return relations.get(tech)

def create_dataset_row():
    domain_key = random.choice(list(DOMAINS.keys()))
    domain_info = DOMAINS[domain_key]
    
    project_type = random.choice(domain_info["types"])
    tech = random.choice(domain_info["tech"])
    codename = random.choice(PROJECT_CODENAMES)
    status = random.choice(STATUS + ["Active"] * 3) 
    
    ground_truth = generate_project_id(domain_key, codename, project_type, tech)

    query_term_1 = random.choice([domain_key.lower(), project_type.replace("_", " ").lower()])
    query_term_2 = random.choice([tech.lower(), codename.lower()])
    query = f"{random.choice(QUERY_ACTIONS)} {query_term_1} {query_term_2}"
    
    description = f"A {status} {project_type.replace('_', ' ')} service within the {codename} project, built with {tech}. This service is owned by the {domain_key} team and handles core business logic."

    high_relevance = set()
    while len(high_relevance) < 4:
        alt_codename = random.choice([c for c in PROJECT_CODENAMES if c != codename])
        alt_tech = random.choice([t for t in domain_info["tech"] if t != tech] or [tech])
        high_relevance.add(generate_project_id(domain_key, codename, project_type, alt_tech))
        high_relevance.add(generate_project_id(domain_key, alt_codename, project_type, tech))
        high_relevance.discard(ground_truth)

    medium_relevance = set()
    while len(medium_relevance) < 4:
        alt_domain_key = random.choice([d for d in DOMAINS if d != domain_key])
        alt_domain_info = DOMAINS[alt_domain_key]
        alt_project_type = random.choice(alt_domain_info["types"])
        medium_relevance.add(generate_project_id(domain_key, codename, random.choice(domain_info["types"]), tech)) # Same project, different type
        medium_relevance.add(generate_project_id(alt_domain_key, codename, alt_project_type, random.choice(alt_domain_info["tech"]))) # Same codename, different domain
        medium_relevance.discard(ground_truth)

    low_relevance = set()
    while len(low_relevance) < 4:
        low_domain_key = random.choice([d for d in DOMAINS if d != domain_key])
        low_domain_info = DOMAINS[low_domain_key]
        low_codename = random.choice([c for c in PROJECT_CODENAMES if c != codename])
        low_project_type = random.choice(low_domain_info["types"])
        low_tech = random.choice(low_domain_info["tech"])
        low_relevance.add(generate_project_id(low_domain_key, low_codename, low_project_type, low_tech))
        
    return {
        "query": query,
        "service_description": description,
        "ground_truth": ground_truth,
        "high_relevance": json.dumps(list(high_relevance)[:4]),
        "medium_relevance": json.dumps(list(medium_relevance)[:4]),
        "low_relevance": json.dumps(list(low_relevance)[:4]),
    }

def main():
    print("Generating the most advanced evaluation dataset for Project Repository Search...")
    
    dataset = [create_dataset_row() for _ in range(NUM_QUERIES)]
    df = pd.DataFrame(dataset)

    output_dir = 'advanced_evaluation_data'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    output_path = os.path.join(output_dir, 'project_repo_queries.csv')
    df.to_csv(output_path, index=False)
    
    print("\nDataset generation complete.")
    print(f"File saved at: {output_path}")
    print(f"Total unique queries generated: {len(df)}")
    print("\nSample of the first 5 rows:")
    print(df.head().to_string())

if __name__ == "__main__":
    main()
