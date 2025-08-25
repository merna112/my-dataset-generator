import requests
import os
import json

# GitHub Token من Jenkins Environment
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

# منظمات رئيسية (نبدأ بيها)
PRIMARY_ORGS = ["kubernetes", "hashicorp", "prometheus", "aws", "microsoft"]

# fallback منظمات لو العدد أقل من المطلوب
FALLBACK_ORGS = ["apache", "google", "facebook", "netflix"]

OUTPUT_FILE = "github_repos.json"
MIN_REQUIRED = 210  # عشان build_dataset.py يشتغل


def fetch_repos_from_org(org, max_pages=10):
    all_repos = []
    headers = {"Authorization": f"token {GITHUB_TOKEN}"} if GITHUB_TOKEN else {}

    for page in range(1, max_pages + 1):  # لحد 1000 repo من كل org
        url = f"https://api.github.com/orgs/{org}/repos?per_page=100&page={page}"
        print(f"📡 Fetching: {url}")
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()

        if not data:
            break

        for repo in data:
            all_repos.append({
                "name": repo["name"],
                "full_name": repo["full_name"],
                "description": repo.get("description") or "",
                "html_url": repo["html_url"]
            })

    return all_repos


def main():
    all_repos = []

    # نجمع من المنظمات الرئيسية
    for org in PRIMARY_ORGS:
        repos = fetch_repos_from_org(org)
        print(f"✅ {org}: {len(repos)} repos")
        all_repos.extend(repos)

    # fallback لو العدد أقل من المطلوب
    if len(all_repos) < MIN_REQUIRED:
        print(f"⚠️ عدد الريبو الحالي {len(all_repos)}، هنكمل من fallback orgs...")
        for org in FALLBACK_ORGS:
            repos = fetch_repos_from_org(org)
            print(f"✅ {org}: {len(repos)} repos")
            all_repos.extend(repos)
            if len(all_repos) >= MIN_REQUIRED:
                break

    # بعد التجميع، نتحقق
    if len(all_repos) < MIN_REQUIRED:
        raise ValueError(f"❌ حتى بعد fallback، عدد الريبو {len(all_repos)} أقل من {MIN_REQUIRED}")

    print(f"📦 المجموع الكلي: {len(all_repos)} repos")

    with open(OUTPUT_FILE, "w") as f:
        json.dump(all_repos, f, indent=2, ensure_ascii=False)

    print(f"💾 تم حفظ الداتا في {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
