# Cosmic Clock ✦ PhD positions & internships for Sulekha Gupta

**Live site:** https://astrophysicist-abhi26.github.io/cosmic-clock/ · **Android app:** the *Android app* button on the site

Every morning at 07:00 IST a GitHub Action reads ~50 public sources and keeps three kinds of opportunity
for Sulekha (MSc Life Sciences, IISc Bengaluru):

| Tab | What it shows |
|---|---|
| **PhD positions** | Funded PhD posts and doctoral fellowships, Europe first: EURAXESS first-stage (R1) offers, MSCA doctoral networks, Nature Careers, Academic Positions, jobs.ac.uk, Max Planck, SciLifeLab, jobRxiv … |
| **Internships** | Three columns: **Bengaluru & India**, **Abroad**, **AI & biotech companies** — live postings plus curated schemes (SRFP, Charpak Lab, Max Planck internships …), each flagged when only enrolled students can apply |
| **Jobs after MSc** | Paid research-assistant, project and junior lab roles; jobs that require a PhD carry a badge and can be hidden |
| **Programmes** | Structured PhD programmes in Europe (EMBL, IMPRS Biology of Ageing, FLI, ERIBA, Vienna BioCenter, ISTA, DKFZ, Crick, CRG) and funding |
| **My tracker** | Her applications (saved → applied → interview → offer), notes, document checklist, calendar export |
| **Search elsewhere** | Ready-made LinkedIn / Google / Indeed searches from her profile |
| **Sources** | Health of every source, refreshed daily |

Postdoc and faculty posts are dropped (see `scraper/site.yaml`). Each posting is tagged with topics —
including new ones for her: *ageing, senescence & longevity*, *DNA damage & radiation biology*,
*extracellular matrix & mechanobiology*, *space biology* — compared with her CV (`scraper/cv/sulekha.txt`)
and scored 0–100 per ranking profile (`scraper/profiles.yaml`). Every card says why it got its score.

## Make it yours

| To change … | edit |
|---|---|
| name, person, which position types are dropped | `scraper/site.yaml` |
| how positions are ranked (topics, regions, “near Bengaluru” bonus, PhD-required penalty) | `scraper/profiles.yaml` — or live in the site’s **Tune** panel |
| PhD programmes and internship schemes | `scraper/programmes.yaml` (only checked dates are shown) |
| job boards, institutes, companies | `scraper/sources.yaml`, `institutes.yaml`, `companies.yaml` (test with `python scraper/doctor.py`) |
| the avatar, icon and launcher icon | `tools/make_art.py`, then `python tools/make_art.py` |

## Run it locally

```bash
pip install -r requirements.txt
python scraper/scrape.py --offline --out docs/jobs.json   # fixtures, no network
python scraper/scrape.py --out docs/jobs.json             # live run
cd docs && python -m http.server 8000                     # open http://localhost:8000
python -m pytest -q                                       # 54 tests
```

Deploying from scratch: **[RUNBOOK.md](RUNBOOK.md)**. Everything is plain Python and plain JavaScript; there is no
database and no build step. Data comes only from public adverts and official job-board APIs, respecting robots.txt.

Built for Sulekha by her friend Abhishek. The name comes from her Longevity India newsletter piece,
*“The Cosmic Clock: Decoding Aging, Pregnancy, and Microgravity”*.
