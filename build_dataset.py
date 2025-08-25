import json
import os

MIN_ACCEPT = 200  # أقل عدد Entries مطلوب

def build_dataset(repos):
    dataset = []

    for repo in repos:
        name = repo.get("name", "unknown-repo")
        org = repo.get("org", "unknown-org")
        desc = repo.get("description", "").strip()
        readme = repo.get("readme", "").strip() if repo.get("readme") else ""

        if not desc and not readme:
            continue

        # Query: أول جملة من README أو description
        query_source = readme if readme else desc
        query = query_source.split(".")[0].strip()
        if not query:
            continue

        # Description
        description = desc if desc else "No description provided."

        # Ground Truth
        ground_truth = f"{description} {readme[:300]}".strip()

        # دايمًا 4/4/4
        high = [
            f"{name} integrates with Consul to enable dynamic service discovery.",
            f"{name} enhances secure connectivity in distributed microservice environments.",
            f"{name} supports multi-cloud federation and health checking for discovery.",
            f"{name} works seamlessly with orchestration tools like Kubernetes and Nomad."
        ]

        medium = [
            "Etcd provides service registry capabilities but lacks full mesh features.",
            "Zookeeper supports coordination and discovery but with limited scalability.",
            "CoreDNS resolves DNS-based lookups but does not handle segmentation.",
            "Eureka is used for service discovery mainly in Spring/Netflix OSS."
        ]

        low = [
            "TensorFlow is a machine learning framework unrelated to service discovery.",
            "React is a frontend JavaScript library, not a networking solution.",
            "PostgreSQL is a relational database, not a service discovery tool.",
            "Linux kernel provides OS-level abstractions, not service discovery."
        ]

        dataset.append({
            "query": query,
            "description": description,
            "ground_truth": ground_truth,
            "high_relevance": high,
            "medium_relevance": medium,
            "low_relevance": low
        })

    return dataset

if __name__ == "__main__":
    if not os.path.exists("github_repos.json"):
        raise FileNotFoundError("❌ File github_repos.json not found. Run fetch_github_data.py first.")

    with open("github_repos.json", "r") as f:
        repos = json.load(f)

    dataset = build_dataset(repos)

    if len(dataset) < MIN_ACCEPT:
        raise RuntimeError(f"❌ Built only {len(dataset)} entries (<{MIN_ACCEPT}). Add more orgs or pages.")

    with open("service_discovery_dataset.json", "w") as f:
        json.dump(dataset, f, indent=2, ensure_ascii=False)

    print(f"✅ Built dataset with {len(dataset)} entries → saved to service_discovery_dataset.json")
