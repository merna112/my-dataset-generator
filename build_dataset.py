import os
import re
import json
import random
import sys
from collections import defaultdict

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

# --- دوال مساعدة لتنظيف النصوص ---
def normalize_text(s: str) -> str:
    if not s: return ""
    s = re.sub(r"http\S+", " ", s)
    s = re.sub(r"[#*`>_~|]", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s

def get_sentences(text: str):
    if not text: return []
    text = normalize_text(text)
    # تقسيم ذكي يحافظ على الجمل الطويلة
    sentences = re.split(r'(?<=[.!?])\s+', text)
    return [s.strip() for s in sentences if len(s.split()) > 5] # تجاهل الجمل القصيرة جدًا

def create_long_snippet(sentences, min_len, max_len):
    random.shuffle(sentences)
    # محاولة إيجاد جملة واحدة طويلة أولاً
    for s in sentences:
        if min_len <= len(s) <= max_len:
            return s
    
    # إذا فشل، قم بدمج جملتين أو ثلاث
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
            
    return "" # إرجاع فارغ إذا لم يتم العثور على شيء مناسب

# --- دالة رئيسية لبناء السجل ---
def build_entry(anchor_repo, repo_pool, indices, used_texts):
    # 1. إنشاء Query فريد وطويل
    query_candidates = get_sentences(anchor_repo.get("readme", "")) + get_sentences(anchor_repo.get("description", ""))
    query = create_long_snippet(query_candidates, QUERY_MIN_LEN, QUERY_MAX_LEN)
    if not query or query in used_texts:
        return None
    used_texts.add(query)

    # 2. إنشاء Ground Truth فريد وأطول
    gt_candidates = get_sentences(anchor_repo.get("description", "")) + get_sentences(anchor_repo.get("readme", ""))
    ground_truth = create_long_snippet(gt_candidates, GT_MIN_LEN, GT_MAX_LEN)
    if not ground_truth or ground_truth in used_texts:
        used_texts.discard(query) # التراجع عن حجز الـ query
        return None
    used_texts.add(ground_truth)

    # 3. بناء قوائم الصلة (Relevance)
    def find_relevance_candidates(logic_func):
        candidates = []
        for repo in repo_pool:
            if repo["full_name"] == anchor_repo["full_name"]:
                continue
            if logic_func(anchor_repo, repo):
                candidates.append(repo)
        random.shuffle(candidates)
        return candidates

    # High: نفس المنظمة أو مواضيع مشتركة قوية
    high_candidates = find_relevance_candidates(
        lambda a, r: a["org"] == r["org"] or len(set(a["topics"]) & set(r["topics"])) >= 2
    )

    # Medium: موضوع واحد مشترك، منظمة مختلفة
    medium_candidates = find_relevance_candidates(
        lambda a, r: a["org"] != r["org"] and len(set(a["topics"]) & set(r["topics"])) == 1
    )

    # Low: لا مواضيع مشتركة، منظمة مختلفة
    low_candidates = find_relevance_candidates(
        lambda a, r: a["org"] != r["org"] and not set(a["topics"]) & set(r["topics"])
    )

    # 4. اختيار 4 جمل فريدة لكل مستوى مع خطط بديلة
    def pick_sentences(candidates, count, fallback_pools):
        sentences = []
        source_pools = [candidates] + fallback_pools
        for pool in source_pools:
            for repo in pool:
                if len(sentences) >= count: break
                sent_candidates = get_sentences(repo.get("readme", "")) + get_sentences(repo.get("description", ""))
                sentence = create_long_snippet(sent_candidates, REL_MIN_LEN, REL_MAX_LEN)
                if sentence and sentence not in used_texts:
                    sentences.append(sentence)
                    used_texts.add(sentence)
            if len(sentences) >= count: break
        return sentences[:count]

    high_relevance = pick_sentences(high_candidates, 4, [medium_candidates, low_candidates])
    medium_relevance = pick_sentences(medium_candidates, 4, [high_candidates, low_candidates])
    low_relevance = pick_sentences(low_candidates, 4, [medium_candidates, repo_pool])

    # 5. التحقق النهائي من الشروط
    if not (len(high_relevance) == 4 and len(medium_relevance) == 4 and len(low_relevance) == 4):
        # التراجع عن كل الحجوزات إذا فشل السجل
        used_texts.discard(query)
        used_texts.discard(ground_truth)
        for s in high_relevance + medium_relevance + low_relevance: used_texts.discard(s)
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
        print(f"❌ Error: '{INPUT_FILE}' not found. Run the data fetching script first.", file=sys.stderr)
        sys.exit(1)

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        repos = json.load(f)

    # فلترة أولية للمستودعات التي تحتوي على نصوص كافية
    usable_repos = []
    for r in repos:
        if len(r.get("description", "") or "") + len(r.get("readme", "") or "") > 200:
             # إضافة Topics و Org إذا لم تكن موجودة
            r["topics"] = r.get("topics", [])
            if "org" not in r or not r["org"]:
                r["org"] = r["full_name"].split('/')[0]
            usable_repos.append(r)
            
    print(f"Found {len(usable_repos)} usable repositories with sufficient text.")

    if len(usable_repos) < MINIMUM_RECORDS:
        print(f"⚠️ Warning: Only {len(usable_repos)} usable repos found, which is less than the minimum required {MINIMUM_RECORDS}.", file=sys.stderr)

    dataset = []
    used_texts = set()
    random.shuffle(usable_repos)

    for anchor_repo in usable_repos:
        if len(dataset) >= TARGET_RECORDS:
            break
        entry = build_entry(anchor_repo, usable_repos, None, used_texts)
        if entry:
            dataset.append(entry)

    if len(dataset) < MINIMUM_RECORDS:
         print(f"❌ Error: Could only build {len(dataset)} valid records, which is less than the minimum required {MINIMUM_RECORDS}.", file=sys.stderr)
         # sys.exit(1) # يمكنك تفعيل هذا السطر لإيقاف الـ pipeline إذا فشل

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(dataset, f, indent=2, ensure_ascii=False)

    print(f"✅ Successfully built dataset with {len(dataset)} records.")
    print(f"   Total unique text snippets used: {len(used_texts)}")
    print(f"   Dataset saved to '{OUTPUT_FILE}'")

if __name__ == "__main__":
    main()
