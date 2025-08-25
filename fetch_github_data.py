import os, re, json, random

IN = "github_repos.json"
OUT = "service_discovery_dataset.json"
TARGET = int(os.getenv("NUM_EXAMPLES", "250"))  # your “>=200 (prefer 250)” rule
MIN_ACCEPT = 200

random.seed(42)

# ---------- helpers ----------
STOP = set("""a an the and or of to for in on with from across at as into by be is are was were can will should might may this that these those any it its his her their our your you we i they them he she us""".split())

def norm(s: str) -> str:
    if not s: return ""
    s = re.sub(r"https?://\S+", " ", s)          # drop URLs
    s = re.sub(r"[#*`>_~]", " ", s)              # drop md marks
    s = s.replace("\u00A0", " ").replace("\t", " ")
    s = s.replace("•", " ").replace("·", " ")
    s = s.replace("-", " ")                      # no hyphens in final strings
    s = re.sub(r"\s+", " ", s).strip()
    return s

def sent_split(txt: str):
    txt = norm(txt)
    parts = re.split(r"(?<=[\.\!\?])\s+|\n+", txt)
    return [p.strip() for p in parts if len(p.strip()) > 0]

def bag(tokens):
    return [t for t in re.findall(r"[A-Za-z0-9]+", tokens.lower()) if t not in STOP]

def overlap(a_tokens, b_tokens):
    return len(set(a_tokens) & set(b_tokens))

def long_snippet(desc, readme, min_chars=120, max_chars=300):
    # Build a natural snippet from sentences (prefer description, then README)
    candidates = sent_split(desc) + sent_split(readme)
    # try single long sentence first
    for s in candidates:
        if len(s) >= min_chars:
            return s[:max_chars].strip()
    # else stitch consecutive sentences until long enough
    buf = ""
    for s in candidates:
        if not buf:
            buf = s
        else:
            buf = (buf + " " + s).strip()
        if len(buf) >= min_chars:
            return buf[:max_chars].strip()
    return norm((desc + " " + readme)[:max_chars])

def ensure_unique_pick(text_pool, used_global, need=4, avoid=None, min_chars=140, max_chars=300):
    """Pick unique, long-ish items from text_pool (list of repos), each item: (desc, readme, name)."""
    picks = []
    avoid = avoid or set()
    random.shuffle(text_pool)
    for r in text_pool:
        cand = long_snippet(r.get("description",""), r.get("readme_text",""), min_chars=min_chars, max_chars=max_chars)
        if len(cand) < min_chars: 
            continue
        if cand in used_global or cand in avoid or cand in picks:
            continue
        picks.append(cand)
        if len(picks) == need:
            break
    return picks

# ---------- load ----------
with open(IN, "r") as f:
    REPOS = json.load(f)

# pre-filter usable repos (must have some text)
usable = []
for r in REPOS:
    desc = norm(r.get("description", ""))
    readme = norm(r.get("readme_text", ""))
    combined_len = len(desc) + len(readme)
    if combined_len < 60:  # too sparse to generate long fields
        continue
    r["description"] = desc
    r["readme_text"] = readme
    r["org"] = r.get("org") or (r.get("full_name","").split("/")[0] if r.get("full_name") else "")
    r["topics"] = r.get("topics", [])
    r["tokens"] = bag(desc + " " + " ".join(r["topics"]))
    usable.append(r)

if len(usable) < MIN_ACCEPT:
    raise ValueError(f"⚠️ Need at least {MIN_ACCEPT} repos with usable text (have {len(usable)}).")

anchor_count = min(TARGET, len(usable))
if anchor_count < MIN_ACCEPT:
    raise ValueError(f"⚠️ Not enough to reach {MIN_ACCEPT}. Got {anchor_count}.")

# build indices
by_org = {}
by_topic = {}
for r in usable:
    by_org.setdefault(r["org"], []).append(r)
    for t in r["topics"]:
        by_topic.setdefault(t.lower(), []).append(r)

# global uniqueness sets
USED_QUERIES = set()
USED_GT = set()
USED_REL = set()

def related_high(src):
    # same org first, then >=2 shared topics
    same_org = [x for x in by_org.get(src["org"], []) if x["full_name"] != src["full_name"]]
    shared_topics = []
    st = set([t.lower() for t in src["topics"]])
    if st:
        for t in st:
            shared_topics.extend([x for x in by_topic.get(t, []) if x["full_name"] != src["full_name"]])
    # unique list preserve order
    seen = set()
    out = []
    for x in same_org + shared_topics:
        if x["full_name"] in seen: 
            continue
        # prefer strong topic overlap
        if overlap(src["tokens"], x["tokens"]) >= 2 or x in same_org:
            out.append(x)
            seen.add(x["full_name"])
    return out

def related_medium(src):
    # one-topic overlap, different org
    st = set([t.lower() for t in src["topics"]])
    pool = []
    for t in st:
        pool.extend(by_topic.get(t, []))
    out = [x for x in pool if x["org"] != src["org"]]
    # plus moderate lexical overlap (without topics) as backup
    if len(out) < 20:
        for x in usable:
            if x["org"] == src["org"]: 
                continue
            if 1 <= overlap(src["tokens"], x["tokens"]) <= 2:
                out.append(x)
    # de-dup
    seen = set()
    uniq = []
    for x in out:
        if x["full_name"] in seen: 
            continue
        uniq.append(x); seen.add(x["full_name"])
    return uniq

def related_low(src):
    # different org, no topic overlap, near-zero token overlap
    st = set([t.lower() for t in src["topics"]])
    out = []
    for x in usable:
        if x["org"] == src["org"]:
            continue
        if st and st.intersection([t.lower() for t in x["topics"]]):
            continue
        if overlap(src["tokens"], x["tokens"]) == 0:
            out.append(x)
    if len(out) < 50:
        # fallback: low overlap <=1
        out.extend([x for x in usable if x["org"] != src["org"] and overlap(src["tokens"], x["tokens"]) <= 1])
    # de-dup
    seen = set(); uniq=[]
    for x in out:
        if x["full_name"] in seen: continue
        uniq.append(x); seen.add(x["full_name"])
    return uniq

def build_entry(src):
    # query: a natural long excerpt (desc/README) – unique globally
    q = long_snippet(src["description"], src["readme_text"], min_chars=120, max_chars=300)
    tries = 0
    while (q in USED_QUERIES or len(q) < 120) and tries < 5:
        # rotate by using more README or different stitching
        q = long_snippet(src["readme_text"], src["description"], min_chars=120, max_chars=320)
        tries += 1
    if q in USED_QUERIES:
        return None

    # description: repo description as-is (normalized)
    d = src["description"] if src["description"] else q[:200]

    # ground_truth: much longer combo from the same repo (desc + README excerpt)
    gt = norm((src["description"] + " " + long_snippet(src["readme_text"], "", min_chars=220, max_chars=600)).strip())
    if len(gt) < 220:
        gt = norm((src["description"] + " " + src["readme_text"])[:600])
    tries = 0
    while (gt in USED_GT or len(gt) < 220) and tries < 5:
        gt = norm((src["description"] + " " + long_snippet(src["readme_text"], "", min_chars=250, max_chars=650)))
        tries += 1
    if gt in USED_GT:
        return None

    # relevance pools
    high_pool   = related_high(src)
    med_pool    = related_medium(src)
    low_pool    = related_low(src)

    # select 4/4/4 unique, long items (global uniqueness)
    h = ensure_unique_pick(high_pool, USED_REL, need=4, avoid=set(), min_chars=140, max_chars=320)
    m = ensure_unique_pick(med_pool,  USED_REL, need=4, avoid=set(h), min_chars=140, max_chars=320)
    l = ensure_unique_pick(low_pool,  USED_REL, need=4, avoid=set(h)|set(m), min_chars=140, max_chars=320)

    # robust fallbacks to reach exactly 4
    def top_off(current, pools):
        for pool in pools:
            if len(current) >= 4: break
            more = ensure_unique_pick(pool, USED_REL, need=4-len(current),
                                      avoid=set(h)|set(m)|set(l), min_chars=140, max_chars=320)
            current.extend(more)
        return current[:4]

    h = top_off(h, [med_pool, low_pool, usable])
    m = top_off(m, [high_pool, low_pool, usable])
    l = top_off(l, [med_pool, high_pool, usable])

    if not (len(h)==len(m)==len(l)==4):
        return None

    # mark global uniqueness
    USED_QUERIES.add(q)
    USED_GT.add(gt)
    for s in h+m+l:
        USED_REL.add(s)

    return {
        "query": q,
        "description": d,
        "ground_truth": gt,
        "high_relevance": h,
        "medium_relevance": m,
        "low_relevance": l
    }

# ---------- build ----------
random.shuffle(usable)
dataset = []
for src in usable:
    if len(dataset) >= anchor_count:
        break
    e = build_entry(src)
    if e:
        dataset.append(e)

if len(dataset) < MIN_ACCEPT:
    raise RuntimeError(f"❌ Built only {len(dataset)} entries (<{MIN_ACCEPT}). Add more orgs or pages.")

with open(OUT, "w") as f:
    json.dump(dataset, f, indent=2, ensure_ascii=False)

print(f"✅ Built {len(dataset)} entries -> {OUT}")
print(f"   Uniqueness: queries={len(USED_QUERIES)}, ground_truth={len(USED_GT)}, relevance_strings={len(USED_REL)}")
