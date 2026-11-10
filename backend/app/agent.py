"""Agentic workflow: retrieve -> draft grounded answer -> validate citations -> answer or abstain.
Plus document comparison. Fully local, no API key needed."""
from .retrieval import Index, tokens, split_sentences

ABSTAIN_COVERAGE = 0.6   # min share of query terms found in best chunk

_index = None
def get_index():
    global _index
    if _index is None:
        _index = Index()
    return _index

def _overlap(a, b):
    a, b = set(a), set(b)
    return len(a & b) / len(a | b) if a | b else 0.0

def validate_citations(claims, index=None):
    """Each claim must appear verbatim in the cited paragraph."""
    index = index or get_index()
    report = []
    for c in claims:
        doc = index.by_id.get(c["doc_id"])
        ok = bool(doc) and 1 <= c["para"] <= len(doc["paragraphs"]) and c["sentence"] in doc["paragraphs"][c["para"] - 1]
        report.append({"doc_id": c["doc_id"], "para": c["para"], "valid": ok})
    return report

def ask(query, regulator=None, index=None):
    index = index or get_index()
    steps = []
    hits = index.search(query, k=5, regulator=regulator)
    steps.append(f"Hybrid retrieval (BM25 + semantic, RRF, rerank) returned {len(hits)} candidates.")
    cov = hits[0]["coverage"] if hits else 0
    if cov < ABSTAIN_COVERAGE:
        steps.append(f"Best passage covers {cov:.0%} of query terms (< {ABSTAIN_COVERAGE:.0%}). Abstaining.")
        return {"answer": None, "abstained": True,
                "message": "I could not find supporting evidence for this in the indexed circulars.",
                "citations": [], "validation": [], "steps": steps}
    q = tokens(query)
    claims, seen = [], set()
    for h in hits[:3]:
        if h["coverage"] < ABSTAIN_COVERAGE:
            continue
        sents = split_sentences(h["text"])
        best = max(sents, key=lambda s: _overlap(q, tokens(s)))
        if _overlap(q, tokens(best)) > 0 and best not in seen:
            seen.add(best)
            claims.append({"sentence": best, "doc_id": h["doc_id"], "para": h["para"], "title": h["title"]})
    steps.append(f"Drafted {len(claims)} extractive claim(s) from top passages.")
    validation = validate_citations(claims, index)
    good = [c for c, v in zip(claims, validation) if v["valid"]]
    steps.append(f"Citation validation: {len(good)}/{len(claims)} claims verified against source text.")
    if not good:
        return {"answer": None, "abstained": True, "message": "No claim survived citation validation.",
                "citations": [], "validation": validation, "steps": steps}
    cites, parts = [], []
    for c in good:
        key = (c["doc_id"], c["para"])
        if key not in [(x["doc_id"], x["para"]) for x in cites]:
            cites.append({"n": len(cites) + 1, "doc_id": c["doc_id"], "para": c["para"], "title": c["title"],
                          "text": index.by_id[c["doc_id"]]["paragraphs"][c["para"] - 1]})
        n = [x["n"] for x in cites if (x["doc_id"], x["para"]) == key][0]
        parts.append(c['sentence'] + f' [{n}]')
    return {"answer": " ".join(parts), "abstained": False, "citations": cites,
            "validation": validation, "steps": steps}

def compare(id_a, id_b, index=None):
    index = index or get_index()
    A, B = index.by_id.get(id_a), index.by_id.get(id_b)
    if not A or not B:
        raise KeyError("Unknown document id")
    sa = [s for p in A["paragraphs"] for s in split_sentences(p)]
    sb = [s for p in B["paragraphs"] for s in split_sentences(p)]
    unchanged, modified, removed, used = [], [], [], set()
    for s in sa:
        best, bj = None, 0.0
        for j, t in enumerate(sb):
            if j in used: continue
            sc = _overlap(tokens(s), tokens(t))
            if sc > bj: best, bj = j, sc
        if best is not None and bj >= 0.95:
            used.add(best); unchanged.append(s)
        elif best is not None and bj >= 0.4:
            used.add(best); modified.append({"from": s, "to": sb[best]})
        else:
            removed.append(s)
    added = [t for j, t in enumerate(sb) if j not in used]
    return {"a": {"id": id_a, "title": A["title"]}, "b": {"id": id_b, "title": B["title"]},
            "unchanged": unchanged, "modified": modified, "removed": removed, "added": added}
