from github import Github
import json
import os

# Connect to GitHub
token = os.getenv("GITHUB_TOKEN")
g = Github(token)

# Search for repos about service discovery
query = "service discovery architecture"
result = g.search_repositories(query, sort="stars", order="desc")

repos_data = []
for repo in result[:200]:  # هنجمع أول 200 Repo
    repos_data.append({
        "name": repo.full_name,
        "description": repo.description,
        "url": repo.html_url,
        "stars": repo.stargazers_count
    })

with open("github_repos.json", "w", encoding="utf-8") as f:
    json.dump(repos_data, f, indent=4, ensure_ascii=False)

print("✅ GitHub data fetched into github_repos.json")
