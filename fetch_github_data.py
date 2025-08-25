import requests
import json
import os

# 📦 منظمات ضخمة عشان نجيب Repos كتير
ORGS = [
    "kubernetes",
    "hashicorp",
    "prometheus",
    "aws",
    "microsoft",
    "google",
    "apache",
    "cncf",
    "redhat-developer",
    "helm",
    "istio",
    "spiffe",
    "openstack"
]

MAX_PAGES = 30  # عدد الصفحات لكل org
PER_PAGE = 100  # كل صفحة = 100 repo
MIN_ACCEPT = 200  # أقل عدد مسموح
OUTPUT_FILE = "github_repos.json"

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
HEADERS = {"Authorization": f"token {GITHUB_TOKEN}"} if GITHUB_TOKEN else {}

def fetch_repos(org):
    repos = []
    for page in range(1, MAX_PAGES + 1):
        url = f"https://api.github.com/orgs/{org}/repos?per_page={PER_PAGE}&page={page}"
        print(f"📡 Fetching: {url}")
        resp = requests.get(url, headers=HEADERS)

        if resp.status_code != 200:
            print(f"⚠️ Failed to fetch from {org}, page {page}: {resp.status_code}")
            break

        data = resp.json()
        if not data:
            break

        for repo in data:
            desc = repo.get("description") or ""
            if len(desc.strip()) > 15:  # نفلتر أي وصف قصير جدًا
                repos.append({
                    "org": org,
                    "name": repo["name"],
                    "full_name": repo["full_name"],
                    "html_url": repo["html_url"],
                    "description": desc.strip()
                })

    print(f"✅ {org}: {len(repos)} repos")
    return repos

def main():
    all_repos = []
    for org in ORGS:
        all_repos.extend(fetch_repos(org))

    print(f"📦 المجموع الكلي: {len(all_repos)} repos")

    if len(all_repos) < MIN_ACCEPT:
        raise RuntimeError(f"❌ Built only {len(all_repos)} entries (<{MIN_ACCEPT}). Add more orgs or pages.")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(all_repos, f, indent=2, ensure_ascii=False)

    print(f"💾 تم حفظ الداتا في {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
