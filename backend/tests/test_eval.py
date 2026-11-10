import json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from app.agent import ask, compare, validate_citations

Q = json.load(open(os.path.join(os.path.dirname(__file__), "eval_queries.json")))

def test_answer_accuracy_and_abstention():
    ok = 0; fails = []
    for q in Q:
        r = ask(q["query"])
        if q["expected"] is None:
            good = r["abstained"]
        else:
            good = (not r["abstained"]) and q["expected"] in [c["doc_id"] for c in r["citations"]]
        ok += good
        if not good: fails.append(q["query"])
    acc = ok / len(Q)
    print(f"accuracy={acc:.2%} fails={fails}")
    assert acc >= 0.9, fails

def test_citation_validation_rejects_fabricated():
    bad = [{"sentence": "Totally made up rule.", "doc_id": "DEMO-RBI-001", "para": 1}]
    assert validate_citations(bad)[0]["valid"] is False

def test_compare_detects_changes():
    r = compare("DEMO-RBI-004", "DEMO-RBI-004A")
    assert r["modified"] and r["added"]
