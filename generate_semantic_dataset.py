import random
import json

def generate_dataset(num_queries_per_category=70):
    # --- Data for Generation (English) ---
    jenkins_concepts = [
        "CI/CD pipeline automation", "Continuous Integration", "Continuous Delivery",
        "Automated testing", "Deployment automation", "Code quality analysis",
        "Security scanning", "Artifact management", "Notification systems",
        "Distributed builds", "Dynamic agent provisioning", "Version control integration",
        "Credential management", "Monitoring and reporting", "Orchestration of complex workflows",
        "Infrastructure as Code (IaC) for pipelines", "Multi-branch pipeline support",
        "Containerized build environments", "Cloud-native deployments", "DevOps practices enforcement"
    ]

    common_plugins_high = [
        {"name": "Git Plugin", "desc": "for managing Git repositories, pulling code, and tracking changes.", "use_case": "automating build and test processes with every code change."},
        {"name": "Pipeline Plugin", "desc": "for building complex pipelines as \'code\' (Jenkinsfile) for complete CI/CD cycles.", "use_case": "defining build, deploy, and test stages programmatically and sequentially."},
        {"name": "Blue Ocean Plugin", "desc": "for a modern, intuitive user interface to visualize and manage pipelines.", "use_case": "improving user experience and easily tracking pipeline status."},
        {"name": "Kubernetes Plugin", "desc": "for dynamically running Jenkins agents on Kubernetes clusters.", "use_case": "automatically scaling the build environment and efficiently using Kubernetes resources."},
        {"name": "SonarQube Scanner", "desc": "for static code quality analysis and identifying security issues and programming errors.", "use_case": "ensuring continuous code quality and preventing the introduction of bugs."},
        {"name": "Jira Plugin", "desc": "for linking Jenkins with Jira to track tasks and display build status in Jira.", "use_case": "improving coordination between development teams and project management."},
        {"name": "Slack Notification Plugin", "desc": "for sending build status notifications to Slack channels.", "use_case": "keeping the team informed about CI/CD operations status."},
        {"name": "Credentials Binding Plugin", "desc": "for securely managing sensitive credentials (like passwords and API keys) within Jenkins.", "use_case": "providing a secure way to use secrets in build jobs."},
        {"name": "JUnit Plugin", "desc": "for analyzing and displaying JUnit test results graphically and in detail.", "use_case": "monitoring test results and quickly identifying issues."},
        {"name": "Maven Integration Plugin", "desc": "for advanced integration of Maven projects with Jenkins, including incremental builds.", "use_case": "improving the performance of Maven project builds."},
        {"name": "Docker Plugin", "desc": "for running build jobs inside isolated Docker containers.", "use_case": "ensuring consistent and repeatable build environments."},
        {"name": "Ansible Plugin", "desc": "for running Ansible playbooks from Jenkins for configuration management and deployment automation.", "use_case": "automating deployment operations and infrastructure management."},
        {"name": "GitHub Integration Plugin", "desc": "for deep integration with GitHub, including triggering builds on GitHub events.", "use_case": "connecting Jenkins with GitHub workflow for CI/CD."},
        {"name": "Pipeline: Multibranch Plugin", "desc": "for automatically discovering branches and creating pipelines for each branch in the repository.", "use_case": "efficiently managing CI/CD for multiple branches."},
        {"name": "Docker Pipeline Plugin", "desc": "for building, running, and managing Docker containers as part of your Jenkins pipeline.", "use_case": "incorporating Docker operations into CI/CD pipelines."},
        {"name": "Amazon EC2 Plugin", "desc": "for dynamically provisioning Jenkins agents on Amazon EC2.", "use_case": "scaling build resources in the cloud."},
        {"name": "Email Extension Plugin", "desc": "for sending customized and detailed email notifications after a build completes.", "use_case": "customizing build reports sent via email."},
        {"name": "Role-based Authorization Strategy", "desc": "for managing permissions and access control based on roles.", "use_case": "implementing precise security policies in Jenkins."},
        {"name": "Timestamper Plugin", "desc": "for adding timestamps to build log output.", "use_case": "improving readability of build logs and tracking events."},
        {"name": "Parameterized Trigger Plugin", "desc": "for conditionally triggering other jobs with parameter passing.", "use_case": "building complex job chains that depend on each other."}
    ]

    common_plugins_medium = [
        {"name": "Copy Artifact Plugin", "desc": "for copying artifacts from one build job to another.", "use_case": "reusing build outputs in subsequent jobs."},
        {"name": "Disk Usage Plugin", "desc": "for monitoring disk space consumption by Jenkins.", "use_case": "managing storage space on the Jenkins server."},
        {"name": "Build Blocker Plugin", "desc": "for preventing certain jobs from starting if other jobs are running.", "use_case": "avoiding build conflicts."},
        {"name": "Workspace Cleanup Plugin", "desc": "for cleaning up workspaces after builds complete.", "use_case": "maintaining disk space and organizing the build environment."},
        {"name": "Rebuild Plugin", "desc": "for re-running a previous build job with the same parameters.", "use_case": "facilitating retesting of fixes or redeployments."},
        {"name": "HTML Publisher Plugin", "desc": "for publishing HTML reports (e.g., coverage or test reports) on the build results page.", "use_case": "displaying interactive test results and reports."},
        {"name": "OWASP Dependency-Check Plugin", "desc": "for analyzing project dependencies for known security vulnerabilities.", "use_case": "improving application security by scanning dependencies."},
        {"name": "Build Pipeline View", "desc": "for graphically displaying sequential pipelines.", "use_case": "visualizing the build flow across multiple jobs."},
        {"name": "Active Directory Plugin", "desc": "for integration with Active Directory for authentication and user management.", "use_case": "managing users in Jenkins using Active Directory."},
        {"name": "LDAP Plugin", "desc": "for integration with LDAP servers for authentication and user management.", "use_case": "managing users in Jenkins using LDAP."},
        {"name": "Configuration as Code Plugin", "desc": "for defining Jenkins settings as code, simplifying configuration management.", "use_case": "managing Jenkins configuration in a traceable and version-controlled manner."},
        {"name": "Job DSL Plugin", "desc": "for defining Jenkins jobs using a Domain Specific Language (DSL) in Groovy.", "use_case": "programmatically creating Jenkins jobs."},
        {"name": "Prometheus Plugin", "desc": "for exporting Jenkins metrics to Prometheus for monitoring.", "use_case": "monitoring Jenkins performance using Prometheus."},
        {"name": "Metrics Plugin", "desc": "for providing internal metrics for Jenkins performance.", "use_case": "analyzing Jenkins performance."},
        {"name": "Safe Restart Plugin", "desc": "for safely restarting Jenkins after all ongoing jobs have completed.", "use_case": "restarting Jenkins without interrupting jobs."}
    ]

    common_plugins_low = [
        {"name": "Simple Theme Plugin", "desc": "for customizing the Jenkins UI appearance using CSS and JavaScript.", "use_case": "changing colors, fonts, and logos in Jenkins."},
        {"name": "Locale Plugin", "desc": "for changing the Jenkins UI language.", "use_case": "changing Jenkins language to Arabic or any other language."},
        {"name": "Timestamper Plugin", "desc": "for adding timestamps to build log output.", "use_case": "improving readability of build logs."},
        {"name": "Dashboard View", "desc": "for creating custom dashboards to display job status.", "use_case": "creating a custom dashboard for CI/CD jobs."},
        {"name": "Build Monitor Plugin", "desc": "for displaying build status on a large screen.", "use_case": "real-time monitoring of build status on a display screen."},
        {"name": "Folder Plugin", "desc": "for organizing jobs and projects within folders.", "use_case": "organizing a large number of Jenkins jobs."},
        {"name": "Green Balls Plugin", "desc": "for changing the color of build status balls from blue to green for success.", "use_case": "changing visual icons for build results."},
        {"name": "Global Build Stats Plugin", "desc": "for displaying general statistics about build operations.", "use_case": "getting an overview of build performance."},
        {"name": "Build Failure Analyzer", "desc": "for analyzing build logs and identifying common causes of failure.", "use_case": "automatically diagnosing reasons for build failures."},
        {"name": "Sidebar Link Plugin", "desc": "for adding custom links to the Jenkins sidebar.", "use_case": "adding quick links to external tools."}
    ]

    actions = [
        "automate", "integrate", "monitor", "optimize", "manage", "secure", "deploy", "build", "test",
        "track", "customize", "organize", "scale", "send notifications", "analyze", "clean up",
        "link", "dynamically provision", "define", "execute"
    ]

    problems = [
        "slow and complex build process", "difficulty tracking deployment status", "code quality issues",
        "manual repetition of operations", "unstable build environments", "difficulty managing credentials",
        "lack of visibility into CI/CD performance", "excessive resource consumption", "difficulty in team collaboration",
        "delay in error detection", "outdated and unintuitive user interface", "inability to scale",
        "dependency security issues", "difficulty deploying applications to Kubernetes", "lack of instant notifications",
        "build job conflicts", "disorganized jobs", "difficulty analyzing build logs",
        "need for consistent build environments", "configuration management issues"
    ]

    goals = [
        "achieve full CI/CD", "ensure code quality", "accelerate development cycle",
        "improve application security", "streamline deployment processes", "provide reliable build environments",
        "enhance team collaboration", "reduce human errors", "improve scalability",
        "gain comprehensive visibility into DevOps operations", "customize user experience",
        "automate infrastructure management", "effectively track changes", "securely manage sensitive data",
        "provide detailed reports", "organize large projects", "improve Jenkins performance itself",
        "facilitate troubleshooting", "integrate Jenkins with external tools"
    ]

    contexts = [
        "in a large development environment relying on microservices",
        "when working on a Java project using Maven",
        "in a DevOps team applying Agile methodologies",
        "to improve the CI/CD workflow for a Node.js application",
        "when deploying applications to a Kubernetes cluster",
        "to ensure security compliance in the development lifecycle",
        "in a cloud environment using AWS EC2",
        "for managing multi-branch projects in a Git repository",
        "when instant notifications via Slack are needed",
        "to visually analyze test results",
        "in an environment requiring precise permission management",
        "to automate routine Jenkins maintenance tasks",
        "when isolated build environments using Docker are needed",
        "to simplify Jenkins configuration itself",
        "in a project requiring precise tracking of resource consumption"
    ]

    query_templates = [
        "How can I {action} {jenkins_concept} for {problem} {context}?",
        "I\'m looking for a way to {action} {jenkins_concept} with the goal of {goal}, especially {context}. What is the appropriate tool or plugin?",
        "I have a problem with {problem} and I want to {action} {jenkins_concept} to achieve {goal}. Is there an effective solution in Jenkins?",
        "How can I {action} {jenkins_concept} more effectively? I\'m currently facing {problem} and I want to {goal} {context}. What are the recommendations?",
        "I want to {action} {jenkins_concept} for {goal}. What are the best practices or plugins that can help me in {context}?",
        "What plugin helps me to {action} {jenkins_concept}? I\'m working on {context} and I need to {goal}.",
        "How can I solve the {problem} issue using Jenkins? I want to {action} {jenkins_concept} to achieve {goal}.",
        "I need to {action} {jenkins_concept} in a {context} environment, and how can I ensure {goal}?",
        "What are the essential plugins I should use to {action} {jenkins_concept} and achieve {goal} in the context of {context}?",
        "How can I improve {jenkins_concept} to avoid {problem} and achieve {goal} in the context of {context}?"
    ]

    # --- Generation Logic ---
    data = []
    generated_queries = set()
    generated_ground_truths = set()

    def generate_unique_entry(relevance_category, plugins_list):
        max_attempts = 1000
        for _ in range(max_attempts):
            concept = random.choice(jenkins_concepts)
            action = random.choice(actions)
            problem = random.choice(problems)
            goal = random.choice(goals)
            context = random.choice(contexts)
            plugin_info = random.choice(plugins_list)

            query = random.choice(query_templates).format(
                action=action, jenkins_concept=concept, problem=problem, goal=goal, context=context
            )

            # **FIX APPLIED HERE**
            # Extract dictionary values into variables first
            plugin_name = plugin_info["name"]
            plugin_desc = plugin_info["desc"]
            plugin_use_case = plugin_info["use_case"]

            # Use the simple variables in the f-string to avoid syntax errors
            ground_truth = f"Using {plugin_name} {plugin_desc} This will help you with {plugin_use_case} to {action} {concept} and achieve {goal}."

            if len(query) > 100 and query not in generated_queries and len(ground_truth) > 100 and ground_truth not in generated_ground_truths:
                generated_queries.add(query)
                generated_ground_truths.add(ground_truth)
                return {"query": query, "ground_truth": ground_truth, "relevance": relevance_category}
        return None

    # --- Main Execution ---
    all_entries = []
    categories = {
        "high": common_plugins_high,
        "medium": common_plugins_medium,
        "low": common_plugins_low
    }

    for relevance, plugins in categories.items():
        count = 0
        while count < num_queries_per_category:
            entry = generate_unique_entry(relevance, plugins)
            if entry:
                all_entries.append(entry)
                count += 1

    # Ensure at least 4 of each category are present
    for relevance, plugins in categories.items():
        while sum(1 for d in all_entries if d["relevance"] == relevance) < 4:
            entry = generate_unique_entry(relevance, plugins)
            if entry:
                all_entries.append(entry)

    random.shuffle(all_entries)

    output_filename = "jenkins_service_discovery_dataset.json"
    with open(output_filename, "w", encoding="utf-8") as f:
        json.dump(all_entries, f, ensure_ascii=False, indent=4)
    
    print(f"Dataset generated successfully with {len(all_entries)} entries. Saved to {output_filename}")

if __name__ == "__main__":
    generate_dataset(num_queries_per_category=70)
