import json
import os
import shutil
import subprocess

import pytest

import profiles as P
import taxonomy as T
from classify import KINDS, LABS, LEVELS, SECTORS, VISA, classify
from geo import REGIONS

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def sample_jobs():
    base = [
        ("Doctoral candidate in cellular senescence and extracellular-matrix ageing",
         "PhD project: senescent fibroblasts, SASP, SA-beta-gal staining and DNA damage after ionising radiation; "
         "wet-lab cell culture.", "Leibniz Institute on Aging (FLI)", "Jena, Germany", {}),
        ("Machine Learning Scientist, Protein Design", "Proficiency in Python and PyTorch; protein language models.",
         "Lila Sciences", "San Francisco, CA", {"sector": "ai-bio"}),
        ("Research Intern, Experimental Biology (Summer 2027)", "Mammalian cell culture and cell-based assays; for "
         "students enrolled in a Master's programme.", "Isomorphic Labs", "London, UK", {"sector": "ai-bio"}),
        ("Senior Scientist, Cell Biology", "PhD in cell biology and 8+ years of experience. We are unable to sponsor visas.",
         "Tabula Bio", "San Francisco", {"sector": "ai-bio"}),
        ("Postdoc in plant ecology", "Field ecology of crops and drought; Arabidopsis.", "Example University", "Uppsala, Sweden", {}),
        ("Project Assistant", "MSc in life sciences; cell culture.", "NCBS", "Bengaluru",
         {"keep_untagged": True, "topics": ["life.general"]}),
    ]
    jobs = [classify({"title": t, "description": d, "org": o, "location": loc, "hints": h}) for t, d, o, loc, h in base]
    jobs[0].update(cv=0.62, llm={"fit": 91, "why": "x"})
    jobs[1].update(cv=0.05, llm={"fit": 20, "why": "y"})
    jobs[5].update(pinned=True)
    return jobs


def test_profiles_yaml_is_valid():
    default, profs = P.load()
    assert default == "sulekha" and {"explore", "microbiology", "ai-labs", "internships", "ageing"} <= set(profs)


def test_sulekhas_ranking():
    _, profs = P.load()
    jobs = sample_jobs()
    s = {j["title"]: P.score(j, profs["sulekha"])[0] for j in jobs}
    phd = s["Doctoral candidate in cellular senescence and extracellular-matrix ageing"]
    intern = s["Research Intern, Experimental Biology (Summer 2027)"]
    assert phd >= 85 and phd > intern
    assert intern > s["Senior Scientist, Cell Biology"] and intern > s["Machine Learning Scientist, Protein Design"]
    assert s["Postdoc in plant ecology"] < 20 and s["Project Assistant"] >= P.PIN_FLOOR
    assert jobs[3]["needs_phd"] and not jobs[2]["needs_phd"]
    # the internships profile puts the internship first
    i = {j["title"]: P.score(j, profs["internships"])[0] for j in jobs}
    assert i["Research Intern, Experimental Biology (Summer 2027)"] >= i["Doctoral candidate in cellular senescence and extracellular-matrix ageing"]


def test_reasons_explain_the_score():
    _, profs = P.load()
    jobs = sample_jobs()
    labels = [r[0] for r in P.score(jobs[0], profs["sulekha"])[1]]
    assert labels[0] == "Ageing, senescence & longevity"
    for want in ("PhD position", "Wet lab", "Europe (incl. UK, CH, NO)", "Similar to the CV", "Claude fit check"):
        assert want in labels
    assert "Needs a PhD" in [r[0] for r in P.score(jobs[3], profs["sulekha"])[1]]
    assert "Near Bengaluru" in [r[0] for r in P.score(jobs[5], profs["sulekha"])[1]]


def test_off_topic_scores_zero():
    _, profs = P.load()
    assert P.score({"topics": ["org.plant"], "kind": "postdoc"}, profs["microbiology"])[0] == 0


def test_browser_and_python_scores_agree():
    node = shutil.which("node")
    if not node:
        pytest.skip("node is not installed")
    _, profs = P.load()
    profiles = list(profs.values()) + [P.normalise("t", {"label": "t", "interests": {"micro": 50, "org": "avoid"},
                                                          "cross_field": 0.3, "senior": -5, "coding": -9})]
    jobs = sample_jobs()
    ctx = {"taxonomy": {"fields": T.FIELDS, "subfields": {k: {"label": v[0], "field": T.field_of(k)}
                                                          for k, v in T.SUBFIELDS.items()}},
           "labels": {"kinds": KINDS, "sectors": SECTORS, "labs": LABS, "visa": VISA, "levels": LEVELS, "regions": REGIONS},
           "soft_cap": P.SOFT_CAP, "pin_floor": P.PIN_FLOOR}
    script = ("const S = require(%s); const d = JSON.parse(require('fs').readFileSync(0, 'utf8'));"
              "const c = S.makeContext(d.ctx);"
              "console.log(JSON.stringify(d.profiles.map(p => d.jobs.map(j => S.scoreJob(j, p, c)))));"
              % json.dumps(os.path.join(ROOT, "docs", "score.js")))
    out = subprocess.run([node, "-e", script], input=json.dumps({"jobs": jobs, "profiles": profiles, "ctx": ctx}),
                         capture_output=True, text=True, check=True)
    js = json.loads(out.stdout)
    for p, row in zip(profiles, js):
        for j, res in zip(jobs, row):
            score, reasons = P.score(j, p)
            assert res["score"] == score, (p["id"], j["title"])
            assert [[a, round(b, 9)] for a, b in res["reasons"]] == [[a, round(b, 9)] for a, b in reasons]
