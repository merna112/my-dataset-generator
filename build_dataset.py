import json
import random
from faker import Faker

fake = Faker()

def generate_query():
    templates = [
        "I’m working on {context} and I need a reliable way to {task}. What would be the most efficient service to achieve this?",
        "How can I manage {context} in order to {task} without spending hours on manual intervention?",
        "For a team running {context}, what’s the recommended solution to {task} efficiently?",
        "I need a system that can {task} in {context}. Which service is best suited for this scenario?"
    ]
    context = random.choice([
        "a microservices environment running in Kubernetes",
        "a set of distributed APIs with high traffic",
        "a containerized workload that spikes during peak hours",
        "a hybrid cloud deployment spanning multiple clusters",
        "a service discovery system handling dynamic endpoints"
    ])
    task = random.choice([
        "automatically scale workloads based on resource usage",
        "dynamically discover services across changing environments",
        "maintain high availability during sudden traffic bursts",
        "balance requests intelligently across nodes",
        "integrate observability with scaling decisions"
    ])
    return random.choice(templates).format(context=context, task=task)

def generate_ground_truth():
    return (
        "The Kubernetes Horizontal Pod Autoscaler (HPA) is widely recognized as the optimal solution "
        "for automatically scaling containerized workloads. It continuously monitors live metrics, "
        "adjusts replicas dynamically, and integrates natively into the Kubernetes ecosystem. "
        "By eliminating manual scaling steps, it ensures smooth performance under fluctuating traffic, "
        "while maintaining resource efficiency and operational stability."
    )

def generate_high_relevance():
    options = [
        "KEDA extends scaling capabilities beyond CPU and memory by integrating event-driven triggers, "
        "making it highly effective for workloads tied to external event sources like message queues or streams.",
        "The Cluster Autoscaler complements HPA by dynamically adding or removing nodes to match scheduling demands, "
        "providing both pod-level and cluster-level elasticity.",
        "Service mesh platforms such as Istio enhance traffic routing and observability, which synergizes well with "
        "autoscaling policies for more resilient microservice deployments.",
        "Argo Rollouts introduces advanced deployment strategies like canary or blue-green releases, ensuring "
        "that autoscaling adjustments remain stable during software rollouts."
    ]
    return options

def generate_medium_relevance():
    options = [
        "Nomad provides job scheduling and scaling features but lacks the deep integration with Kubernetes’ native metrics.",
        "Helm charts simplify the configuration of scaling parameters but do not provide continuous dynamic autoscaling on their own.",
        "Docker Swarm supports basic scaling commands, though it does not include adaptive autoscaling logic.",
        "Serverless platforms like AWS Lambda scale functions seamlessly, but they are not designed for managing stateful Kubernetes services."
    ]
    return options

def generate_low_relevance():
    options = [
        "Jenkins pipelines are ideal for CI/CD automation but do not manage live workload scaling in production clusters.",
        "GitHub Actions can orchestrate testing and deployment workflows, yet they are not designed for runtime service autoscaling.",
        "Terraform provides infrastructure provisioning but cannot continuously monitor or adjust replica counts during runtime.",
        "Ansible automates configuration management and orchestration but is not suited for real-time workload scaling decisions."
    ]
    return options

def build_dataset(num_examples=210, output_file="dataset.json"):
    dataset = []
    for _ in range(num_examples):
        entry = {
            "query": generate_query(),
            "ground_truth": generate_ground_truth(),
            "high_relevance": generate_high_relevance(),
            "medium_relevance": generate_medium_relevance(),
            "low_relevance": generate_low_relevance()
        }
        dataset.append(entry)

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(dataset, f, indent=2, ensure_ascii=False)

    print(f"✅ Dataset built successfully with {num_examples} entries → {output_file}")

if __name__ == "__main__":
    build_dataset()
