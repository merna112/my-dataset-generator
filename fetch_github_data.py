import requests
import json
import time

# Org names (قليلة عشان تبقي أسرع)
ORGS = ["kubernetes", "hashicorp", "prometheus", "aws", "openstack", "microsoft"]

# أقصى عدد صفحات هنجيبها من كل org
MAX_PAGES = 5   # كل صفحة = 100 repo -> 500 repo لكل org

# عشان تقللي الوقت -> مش هنجيب README
INCLUDE_README = False  

# Authentication (لو عندك GitHub token)
TOKEN = None  # ضيفي التوكين هنا لو عايزة تزودي السرعة
HEADERS = {"Authorization": f"token {TOKEN}"} if TOKEN else {}

def fetch_repos(org, per_page=100):
    repos = []
    for page in range(1, MAX_PAGES + 1):
        url = f"https://api.github.com/orgs/{org}/repos?per_page={per_page}&page={page}"
        print(f"📡 Fetching: {url}")
        r = requests.get(url, headers=HEADERS)
        if r.status_code != 200:
            print(f"⚠️ Failed for {org}, page {page}")
            break
        data = r.json()
        if not data:
            break
        for repo in data:
            repos.append({
                "org": org,
                "name": repo.get("name"),
                "description": repo.get("description") or "No description available",
                "url": repo.get("html_url")
            })
        time.sleep(0.1)  # صغير جدًا، أسرع
    return repos

def main():
    all_repos = []
    for org in ORGS:
        repos = fetch_repos(org)
        print(f"✅ {org}: {len(repos)} repos")
        all_repos.extend(repos)

    print(f"📦 المجموع الكلي: {len(all_repos)} repos")

    with open("github_repos.json", "w") as f:
        json.dump(all_repos, f, indent=2)

    print("💾 تم حفظ الداتا في github_repos.json")

if __name__ == "__main__":
    main()
