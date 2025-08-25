import requests
import os
import base64
import time
import json

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
HEADERS = {"Authorization": f"token {GITHUB_TOKEN}"} if GITHUB_TOKEN else {}

ORGS = ["kubernetes", "hashicorp", "aws", "microsoft", "openstack", "prometheus"]
PER_PAGE = 100
MAX_PAGES = 15

def fetch_repos(org):
    repos = []
    for page in range(1, MAX_PAGES + 1):
        url = f"https://api.github.com/orgs/{org}/repos?per_page={PER_PAGE}&page={page}"
        print(f"📡 Fetching: {url}")
        r = requests.get(url, headers=HEADERS)
        if r.status_code != 200:
            print(f"⚠️ Failed to fetch {url}: {r.status_code}")
            break
        data = r.json()
        if not data:
            break
        for repo in data:
            repos.append({
                "name": repo["name"],
                "org": org,
                "description": repo.get("description") or ""
            })
        time.sleep(0.2)  # عشان الـ rate limit
    print(f"✅ {org}: {len(repos)} repos")
    return repos

def fetch_readme(org, repo):
    url = f"https://api.github.com/repos/{org}/{repo}/readme"
    r = requests.get(url, headers=HEADERS)
    if r.status_code != 200:
        return ""
    try:
        content = r.json().get("content")
        if content:
            return base64.b64decode(content).decode("utf-8", errors="ignore")
    except Exception:
        return ""
    return ""

if __name__ == "__main__":
    all_repos = []
    for org in ORGS:
        repos = fetch_repos(org)
        for r in repos:
            r["readme"] = fetch_readme(r["org"], r["name"])
            all_repos.append(r)
            time.sleep(0.2)
    print(f"📦 المجموع الكلي: {len(all_repos)} repos")

    with open("github_repos.json", "w") as f:
        json.dump(all_repos, f, indent=2, ensure_ascii=False)

    print("💾 تم حفظ الداتا في github_repos.json")
