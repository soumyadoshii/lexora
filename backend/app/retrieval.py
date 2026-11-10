"""Hybrid retrieval: BM25 keyword + hashed char-ngram vectors (local semantic proxy),
fused with Reciprocal Rank Fusion, then reranked by query-term coverage."""
import json, math, re, os
from collections import Counter

STOP = set("a an the of to in on for and or is are was were be by with as at from that this what which who how when does do did shall under any every it its their than then there if not no can may per about tell me please must should".split())
DATA = os.path.join(os.path.dirname(__file__), "..", "data", "circulars.json")

def stem(w):
    for suf in ("ings", "ing", "ed", "es", "s", "ly"):
        if w.endswith(suf) and len(w) - len(suf) >= 4:
            return w[: -len(suf)]
    return w

def tokens(text):
    return [stem(w) for w in re.findall(r"[a-z0-9]+", text.lower()) if w not in STOP]

def split_sentences(text):
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if s.strip()]

def _vec(toks, n=3):
    v = Counter()
    for t in toks:
        p = f"#{t}#"
        for i in range(max(1, len(p) - n + 1)):
            v[p[i:i + n]] += 1
    return v

def _cos(a, b):
    num = sum(a[k] * b.get(k, 0) for k in a)
    den = math.sqrt(sum(x * x for x in a.values())) * math.sqrt(sum(x * x for x in b.values()))
    return num / den if den else 0.0

class Index:
    def __init__(self, path=DATA):
        self.docs = json.load(open(path, encoding="utf-8"))
        self.by_id = {d["id"]: d for d in self.docs}
        self.chunks = []
        for d in self.docs:
            for i, p in enumerate(d["paragraphs"]):
                toks = tokens(d["title"] + " " + p)
                self.chunks.append({"doc_id": d["id"], "para": i + 1, "text": p, "title": d["title"],
                                    "regulator": d["regulator"], "toks": toks, "tf": Counter(toks), "vec": _vec(toks)})
        self.N = len(self.chunks)
        self.avgdl = sum(len(c["toks"]) for c in self.chunks) / self.N
        df = Counter()
        for c in self.chunks:
            df.update(set(c["toks"]))
        self.idf = {t: math.log(1 + (self.N - n + .5) / (n + .5)) for t, n in df.items()}

    def bm25(self, q, c, k1=1.5, b=0.75):
        s = 0.0
        for t in set(q):
            f = c["tf"].get(t, 0)
            if f:
                s += self.idf[t] * f * (k1 + 1) / (f + k1 * (1 - b + b * len(c["toks"]) / self.avgdl))
        return s

    def coverage(self, q, c):
        qs = set(q)
        return len(qs & set(c["toks"])) / len(qs) if qs else 0.0

    def search(self, query, k=5, regulator=None):
        q = tokens(query)
        pool = [c for c in self.chunks if not regulator or c["regulator"] == regulator]
        qv = _vec(q)
        kw = sorted(pool, key=lambda c: -self.bm25(q, c))
        sem = sorted(pool, key=lambda c: -_cos(qv, c["vec"]))
        rrf = Counter()
        for ranking in (kw, sem):
            for r, c in enumerate(ranking):
                rrf[id(c)] += 1 / (60 + r + 1)
        top = max(rrf.values()) if rrf else 1
        out = []
        for c in pool:
            cov = self.coverage(q, c)
            score = 0.4 * rrf[id(c)] / top + 0.6 * cov
            out.append({**{k_: c[k_] for k_ in ("doc_id", "para", "text", "title", "regulator")},
                        "score": round(score, 4), "coverage": round(cov, 3),
                        "bm25": round(self.bm25(q, c), 3), "semantic": round(_cos(qv, c["vec"]), 3)})
        out.sort(key=lambda x: -x["score"])
        return out[:k]
