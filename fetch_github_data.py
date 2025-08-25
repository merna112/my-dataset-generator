import requests
import os
import json

# GitHub Token من Jenkins Environment
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
# المنظمة أو اليوزر اللي عايزة تجيبي منه الريبو
ORG = "kubernetes"   # ممكن تغيريها لأي org أو user كبير

# المسار اللي هيتحفظ فيه الداتا
OUTPUT_FILE = "github_repos.json"

def fetch_repos():
    all_repos = []
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}

    # نجيب لحد 1000 repo (10 صفحات × 100 repo)
    for page in range(1, 11):
        url = f"https://api.github.com/orgs/{ORG}/repos?per_page=100&page={page}"
        print(f"📡 Fetching: {url}")
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()

        if not data:  # لو الصفحة فاضية يبطل
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
    repos = fetch_repos()
    print(f"✅ تم جلب {len(repos)} repos من GitHub")

    with open(OUTPUT_FILE, "w") as f:
        json.dump(repos, f, indent=2, ensure_ascii=False)

    print(f"💾 تم حفظ الداتا في {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
