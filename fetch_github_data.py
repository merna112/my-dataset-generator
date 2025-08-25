import os
import json
import requests

OUTPUT_FILE = "github_repos.json"
ORGS = ["kubernetes", "hashicorp", "prometheus", "aws", "openstack", "microsoft"]

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
if not GITHUB_TOKEN:
    raise RuntimeError("❌ Missing GITHUB_TOKEN environment variable!")

HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json",
    "User-Agent": "dataset-builder"
}

def fetch_org_repos(org, max_pages=5):
    repos = []
    for page in range(1, max_pages + 1):
        url = f"https://api.github.com/orgs/{org}/repos?per_page=100&page={page}"
        print(f"📡 Fetching: {url}")
        try:
            resp = requests.get(url, headers=HEADERS, timeout=15)
            # --- Debug logging ---
            print(f"   ↳ Status: {resp.status_code}")
            if resp.status_code != 200:
                print(f"   ⚠️ Response: {resp.text[:300]}...")  # أول 300 كاركتر بس
                break

            data = resp.json()
            if not data:
                break
            for repo in data:
                repos.append({
                    "full_name": repo["full_name"],
                    "description": repo.get("description") or "",
                    "topics": repo.get("topics", []),
                    "org": org,
                    "readme": ""  # نجيبها بعدين
                })
        except Exception as e:
            print(f"   ❌ Error fetching {org}, page {page}: {e}")
            break
    return repos

def main():
    all_repos = []
    for org in ORGS:
        repos = fetch_org_repos(org)
        print(f"✅ {org}: {len(repos)} repos")
        all_repos.extend(repos)

    print(f"📦 المجموع الكلي: {len(all_repos)} repos")
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(all_repos, f, indent=2, ensure_ascii=False)
    print(f"💾 تم حفظ الداتا في {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
