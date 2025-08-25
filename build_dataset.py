import os
import re
import json
import random
import sys

# --- الإعدادات الرئيسية ---
INPUT_FILE = "github_repos.json"
OUTPUT_FILE = "service_discovery_dataset.json"
TARGET_RECORDS = int(os.getenv("DATASET_SIZE", "210"))
MINIMUM_RECORDS = int(os.getenv("MIN_DATASET_SIZE", "200"))

# --- إعدادات جودة النصوص ---
QUERY_MIN_LEN = 80
QUERY_MAX_LEN = 300
GT_MIN_LEN = 150
GT_MAX_LEN = 500
REL_MIN_LEN = 80
REL_MAX_LEN = 300

random.seed(42)

# --- دوال مساعدة ---
def normalize_text(s: str) -> str:
    if not s:
        return ""
    s = re.sub(r"http\S+", " ", s)
    s = re.sub(r"[#*`>_~|]", " ", s)
    s = s.replace("-", " ")   # إزالة أي dashes
    s = re.sub(r"\s+", " ", s).strip()
    return s

def get_sentences(text: str):
    if not text:
        return []
    text = normalize_text(text)
    sentences = re.split(r'(?<=[.!?])\s+', text)
    return [s.strip() for s in sentences if len(s.split()) > 5]

def create_long_snippet(sentences, min_len, max_len):
    random.shuffle(sentences)
    for s in sentences:
        if min_len <= len(s) <= max_len:
            return s
    
    buffer = ""
    for s in sentences:
        if not buffer:
            buffer = s
        else:
            new_buffer = buffer + ". " + s
            if len(new_buffer) > max_len:
                continue
            buffer = new_buffer
        if len(buffer) >= min_len:
            return buffer
    return ""

# --- بناء السجل ---
def build_entry(anchor_repo, repo_pool, used_texts):
    if "full_name" not in anchor_repo:
        return None

    # 1. query
    query_candidates = get_sentences(anchor_repo.get("readme", "")) + get_sentences(anchor_repo.get("description", ""))
    query = create_long_snippet(query_candidates, QUERY_MIN_LEN, QUERY_MAX_LEN)
    if not query or query in used_texts:
        return None
    used_texts.add(query)

    # 2. ground_truth (مقدمة + snippet لضمان الطول)
    gt_candidates = get_sentences(anchor_repo.get("description", "")) + get_sentences(anchor_repo.get("readme", ""))
    snippet = create_long_snippet(gt_candidates, 50, GT_MAX_LEN - 100)
    ground_truth = (
        f"The repository {anchor_repo['full_name']} is a project that "
        f"{normalize_text(anchor_repo.get('description', ''))}. {snippet}"
    )
    ground_truth = normalize_text(ground_truth)

    if len(ground_truth) < GT_MIN_LEN or ground_truth in used_texts:
        used_texts.discard(query)
        return None
    used_texts.add(ground_truth)

    # 3. بناء قوائم الصلة
    def find_relevance_candidates(logic_func):
        candidates = []
        for repo in repo_pool:
            if "full_name" not in repo or repo["full_name"] == anchor_repo["full_name"]:
                continue
            if logic_func(anchor_repo, repo):
                candidates.append(repo)
        random.shuffle(candidates)
        return candidates

    high_candidates = find_relevance_candidates(
        lambda a, r: a.get("org") == r.get("org") or len(set(a.get("topics", [])) & set(r.get("topics", []))) >= 2
    )
    medium_candidates = find_relevance_candidates(
        lambda a, r: a.get("org") != r.get("org") and len(set(a.get("topics", [])) & set(r.get("topics", []))) == 1
    )
    low_candidates = find_relevance_candidates(
        lambda a, r: a.get("org") != r.get("org") and not set(a.get("topics", [])) & set(r.get("topics", []))
    )

    # 4. اختيار 4 جمل فريدة لكل مستوى
    def pick_sentences(candidates, count, fallback_pools):
        sentences = set()
        source_pools = [candidates] + fallback_pools
        for pool in source_pools:
            for repo in pool:
                if len(sentences) >= count:
                    break
                sent_candidates = get_sentences(repo.get("readme", "")) + get_sentences(repo.get("description", ""))
                sentence = create_long_snippet(sent_candidates, REL_MIN_LEN, REL_MAX_LEN)
                if sentence and sentence not in used_texts:
                    sentences.add(sentence)
                    used_texts.add(sentence)
            if len(sentences) >= count:
                break
        return list(sentences)[:count]

    high_relevance = pick_sentences(high_candidates, 4, [medium_candidates, low_candidates, repo_pool])
    medium_relevance = pick_sentences(medium_candidates, 4, [high_candidates, low_candidates, repo_pool])
    low_relevance = pick_sentences(low_candidates, 4, [medium_candidates, high_candidates, repo_pool])

    if not (len(high_relevance) == 4 and len(medium_relevance) == 4 and len(low_relevance) == 4):
        used_texts.discard(query)
        used_texts.discard(ground_truth)
        for s in high_relevance + medium_relevance + low_relevance:
            used_texts.discard(s)
        return None

    return {
        "query": query,
        "description": normalize_text(anchor_repo.get("description", "")) or f"A repository named {anchor_repo['full_name']}.",
        "ground_truth": ground_truth,
        "high_relevance": high_relevance,
        "medium_relevance": medium_relevance,
        "low_relevance": low_relevance
    }

# --- التشغيل الرئيسي ---
def main():
    if not os.path.exists(INPUT_FILE):
        print(f"❌ Error: '{INPUT_FILE}' not found.", file=sys.stderr)
        sys.exit(1)

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        repos = json.load(f)

    # فلترة repos
    usable_repos = []
    for r in repos:
        r["full_name"] = r.get("full_name", "unknown/repo")
        r["description"] = r.get("description", "")
        r["readme"] = r.get("readme", "")
        if len(r["description"]) + len(r["readme"]) > 50:  # أوسع شوية
            r["topics"] = r.get("topics", [])
            if "org" not in r or not r["org"]:
                r["org"] = r["full_name"].split('/')[0]
            usable_repos.append(r)

    print(f"Found {len(usable_repos)} usable repositories.")

    if len(usable_repos) < 50:
        print(f"❌ Error: Not enough usable repos.", file=sys.stderr)
        sys.exit(1)

    dataset = []
    used_texts = set()
    random.shuffle(usable_repos)

    for anchor_repo in usable_repos:
        if len(dataset) >= TARGET_RECORDS:
            break
        entry = build_entry(anchor_repo, usable_repos, used_texts)
        if entry:
            dataset.append(entry)

    if len(dataset) < MINIMUM_RECORDS:
        print(f"⚠️ Warning: Only built {len(dataset)} records (<{MINIMUM_RECORDS}).", file=sys.stderr)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(dataset, f, indent=2, ensure_ascii=False)

    print(f"✅ Successfully built dataset with {len(dataset)} records.")
    print(f"   Total unique snippets used: {len(used_texts)}")
    print(f"   Dataset saved to '{OUTPUT_FILE}'")

if __name__ == "__main__":
    main()
