import os, json, re, random, sys
from collections import Counter, defaultdict

IN = "github_repos.json"
OUT = "service_discovery_dataset.json"

TARGET = int(os.getenv("DATASET_SIZE", "250"))
MIN_OK = int(os.getenv("MIN_DATASET_SIZE", "210"))

random.seed(42)

SENT_MIN = 90     # أقل طول للجملة المقبولة
SENT_MAX = 320    # أقصى طول للجملة للـ query/relevance
GT_MIN   = 180    # أقل طول للـ ground_truth
GT_MAX   = 520    # أقصى طول للـ ground_truth

def normalize_ws(s: str) -> str:
    return re.sub(r"\s+", " ", (s or "").strip())

def split_sentences(text: str):
    if not text:
        return []
    # تقسيم بسيط على علامات انتهاء الجمل
    parts = re.split(r'(?<=[\.\?\!])\s+|\n+', text)
    sents = []
    seen = set()
    for p in parts:
        p = normalize_ws(p)
        if len(p) < SENT_MIN:
            continue
        if len(p) > 600:  # قص الجملة الطويلة جدًا
            p = p[:600].rstrip() + "."
        if p and p not in seen:
            seen.add(p)
            sents.append(p)
    return sents

def tokens(text: str):
    return set(re.findall(r"[a-zA-Z][a-zA-Z0-9\-]+", (text or "").lower()))

def jaccard(a, b):
    if not a or not b:
        return 0.0
    inter = len(a & b)
    if inter == 0:
        return 0.0
    union = len(a | b)
    return inter / union if union else 0.0

def build_long_sentence(sentences, target_min=GT_MIN, target_max=GT_MAX):
    # دمج 2-3 جُمل حقيقية في جملة واحدة طويلة بدون شرطات
    chosen = []
    total = 0
    for s in sentences[:5]:  # جرّب أول 5 جُمل طويلة
        if len(s) > SENT_MAX:
            continue
        chosen.append(s.rstrip("."))
        total = len(", ".join(chosen))
        if target_min <= total <= target_max:
            break
    if not chosen:
        # fallback: خُد أطول جملة مسموحة وكرر جملة تانية لو متاح
        candidates = [s.rstrip(".") for s in sentences if len(s) <= SENT_MAX]
        if not candidates:
            return ""
        chosen = [candidates[0]]
        if len(candidates) > 1:
            chosen.append(candidates[1])
    merged = ", ".join(chosen)
    # ضمهم كـ "جملة واحدة طويلة"
    return (merged + ".").strip()

def pick_sentence_from_repo(repo, used_set, avoid_texts):
    # اختر جملة “مميزة وطويلة” من وصف/README
    sents = split_sentences(repo.get("description","")) + split_sentences(repo.get("readme",""))
    random.shuffle(sents)
    for s in sents:
        if len(s) > SENT_MAX:  # خلي جمل relevance/queries معقولة الطول
            continue
        if s in used_set:
            continue
        if any(s == a or s in a or a in s for a in avoid_texts):
            continue
        used_set.add(s)
        return s
    return None

def main():
    if not os.path.exists(IN):
        print(f"❌ {IN} not found. Run fetch_github_data.py first.")
        sys.exit(1)

    with open(IN, "r", encoding="utf-8") as f:
        repos = json.load(f)

    # فلترة Repos اللي عندها نص كفاية
    filtered = []
    for r in repos:
        text = normalize_ws(r.get("text",""))
        desc = normalize_ws(r.get("description",""))
        rd   = normalize_ws(r.get("readme",""))
        if len(desc) + len(rd) < 200:   # لازم يبقى فيه مادة نصية كفاية
            continue
        r["text"] = text
        filtered.append(r)

    random.shuffle(filtered)
    print(f"📦 candidates after filtering: {len(filtered)}")

    # جهّز tokens لكل repo
    tok = [tokens(r["text"]) for r in filtered]
    by_org = defaultdict(list)
    for i, r in enumerate(filtered):
        by_org[r["org"]].append(i)

    # عنواين uniqueness
    used_queries = set()
    used_ground_truth = set()
    used_relevance = set()

    dataset = []
    for idx, r in enumerate(filtered):
        if len(dataset) >= TARGET:
            break

        org = r["org"]
        name = r["full_name"]

        # 1) query: جملة واحدة من الوصف/README “مميزة”
        cand_sents = split_sentences(r.get("description","")) + split_sentences(r.get("readme",""))
        if not cand_sents:
            continue
        # رتّب حسب الطول (الأطول أولاً) لضمان “سؤال طويل”
        cand_sents.sort(key=len, reverse=True)
        query = None
        for s in cand_sents:
            if SENT_MIN <= len(s) <= SENT_MAX and s not in used_queries:
                query = s
                break
        if not query:
            continue
        used_queries.add(query)

        # 2) description: وصف GitHub كما هو (ولو فاضي ناخد أول جملة من README)
        description = normalize_ws(r.get("description",""))
        if not description:
            # خد أول جملة مناسبة من الREADME
            for s in cand_sents[::-1]:
                if len(s) <= SENT_MAX:
                    description = s
                    break
        if not description:
            # ما فيش وصف مناسب
            used_queries.discard(query)
            continue

        # 3) ground_truth: جملة واحدة طويلة من دمج جُمل حقيقية
        long_sents = cand_sents[:]
        gt = build_long_sentence(long_sents, target_min=GT_MIN, target_max=GT_MAX)
        if not gt or gt in used_ground_truth or gt == query:
            # جرّب تكوين مختلف
            random.shuffle(long_sents)
            gt = build_long_sentence(long_sents, target_min=GT_MIN, target_max=GT_MAX)
        if not gt or gt in used_ground_truth or gt == query:
            used_queries.discard(query)
            continue
        used_ground_truth.add(gt)

        # 4) relevance selection via similarity (نصي فقط)
        t_self = tok[idx]

        # حضّر قوائم المرشحين
        # high: نفس org بأعلى تشابه
        high_candidates = []
        for j in by_org[org]:
            if j == idx:
                continue
            sim = jaccard(t_self, tok[j])
            high_candidates.append((sim, j))
        high_candidates.sort(reverse=True, key=lambda x: x[0])

        # medium: من منظمات أخرى بتشابه متوسط
        medium_candidates = []
        low_candidates = []
        for j, t in enumerate(tok):
            if j == idx:
                continue
            s = jaccard(t_self, t)
            if filtered[j]["org"] != org:
                if 0.06 <= s <= 0.30:
                    medium_candidates.append((s, j))
                elif s < 0.02:
                    low_candidates.append((s, j))
        random.shuffle(medium_candidates)
        random.shuffle(low_candidates)

        # اختار جُمل مميزة (بدون تكرار) للـ 4/4/4
        avoid = {query, gt, description}
        avoid_texts = list(avoid)

        def pick_many(cands, needed):
            chosen_texts = []
            seen_names = set()
            for _, j in cands:
                rr = filtered[j]
                if rr["full_name"] in seen_names:
                    continue
                sent = pick_sentence_from_repo(rr, used_relevance, avoid_texts)
                if not sent:
                    continue
                chosen_texts.append(sent)
                seen_names.add(rr["full_name"])
                if len(chosen_texts) == needed:
                    break
            return chosen_texts

        high = pick_many(high_candidates, 4)
        if len(high) < 4:
            # لو المنظمة صغيرة، وسّع الدائرة بأعلى تشابه عبر الكل
            others = [(jaccard(t_self, tok[j]), j) for j in range(len(tok)) if j != idx]
            others.sort(reverse=True, key=lambda x: x[0])
            extra = pick_many(others, 4 - len(high))
            high.extend(extra[:max(0, 4 - len(high))])

        medium = pick_many(medium_candidates, 4)
        if len(medium) < 4:
            # وسّع رينچ التشابه تدريجيًا
            fallback_med = []
            for j, t in enumerate(tok):
                if j == idx or filtered[j]["org"] == org:
                    continue
                s = jaccard(t_self, t)
                if 0.03 <= s < 0.06 or 0.30 < s <= 0.45:
                    fallback_med.append((s, j))
            random.shuffle(fallback_med)
            extra = pick_many(fallback_med, 4 - len(medium))
            medium.extend(extra[:max(0, 4 - len(medium))])

        low = pick_many(low_candidates, 4)
        if len(low) < 4:
            # خُد الأقل تشابهًا عالميًا
            all_sorted = sorted([(jaccard(t_self, tok[j]), j) for j in range(len(tok)) if j != idx], key=lambda x: x[0])
            extra = pick_many(all_sorted, 4 - len(low))
            low.extend(extra[:max(0, 4 - len(low))])

        # لو أي قائمة مش مكتمِلة 4 → تخطّي السجل بالكامل (علشان الفاليديتور)
        if not (len(high) == len(medium) == len(low) == 4):
            # ارجع الـ query/gt المستخدمة عشان ممكن نعيد استخدامها لاحقًا
            used_queries.discard(query)
            used_ground_truth.discard(gt)
            continue

        example = {
            "query": query,
            "description": description,
            "ground_truth": gt,
            "high_relevance": high,
            "medium_relevance": medium,
            "low_relevance": low
        }
        dataset.append(example)

    if len(dataset) < MIN_OK:
        raise ValueError(f"⚠️ Built only {len(dataset)} examples (<{MIN_OK}). Increase orgs or pages.")

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(dataset, f, ensure_ascii=False, indent=2)

    print(f"✅ Built {len(dataset)} examples → {OUT}")
    # quick assert
    bad = [i for i, x in enumerate(dataset, 1) if not (len(x["high_relevance"])==len(x["medium_relevance"])==len(x["low_relevance"])==4)]
    if bad:
        raise RuntimeError(f"Validator pre-check failed for entries: {bad[:10]}")

if __name__ == "__main__":
    main()
