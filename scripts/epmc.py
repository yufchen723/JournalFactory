#!/usr/bin/env python3
"""epmc — Europe PMC, iCite and bioRxiv helpers (stdlib; no key, no email).

  epmc.py search "<query>" [--max 25] [--preprints]     Europe PMC search (use METHODS:"tool", CITES:<pmid>_MED, SRC:PPR)
  epmc.py citing <pmid> [--terms "spatial"] [--max 50]  papers citing a PMID, optionally filtered
  epmc.py refs <pmid>                                   reference list of a PMID
  epmc.py icite <pmid> [<pmid> ...]                     relative citation ratio and percentile (NIH iCite)
  epmc.py published <preprint-doi>                      has this bioRxiv preprint been published?
Only public search terms and identifiers are sent.
"""
import json, sys, time, urllib.parse, urllib.request, argparse
E = "https://www.ebi.ac.uk/europepmc/webservices/rest"


def get(url):
    for i in range(3):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "field-scan/0.1"}), timeout=40) as r:
                return json.loads(r.read().decode())
        except Exception as e:
            err = e; time.sleep(1.5 * (i + 1))
    raise SystemExit(f"request failed (treat as unverified, not as absent): {err}")


def row(r):
    return {"pmid": r.get("pmid", ""), "doi": r.get("doi", ""), "year": r.get("pubYear", ""), "journal": (r.get("journalInfo", {}).get("journal", {}) or {}).get("isoabbreviation", "") or r.get("bookOrReportDetails", {}).get("publisher", "") or r.get("source", ""),
            "first_author": (r.get("authorString", "").split(",")[0]), "title": r.get("title", ""), "cited_by": r.get("citedByCount", 0), "source": r.get("source", ""), "types": (r.get("pubTypeList", {}) or {}).get("pubType", [])}


def search(q, n=25):
    d = get(f"{E}/search?query={urllib.parse.quote(q)}&format=json&resultType=core&pageSize={min(n, 100)}&sort=CITED%20desc")
    return d.get("hitCount", 0), [row(r) for r in d.get("resultList", {}).get("result", [])]


def show(rows):
    for r in rows:
        print("\t".join(str(r[k]) for k in ("pmid", "year", "journal", "first_author", "cited_by", "title")) + ("\t[preprint]" if r["source"] == "PPR" else ""))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter); sp = ap.add_subparsers(dest="cmd", required=True)
    p = sp.add_parser("search"); p.add_argument("q"); p.add_argument("--max", type=int, default=25); p.add_argument("--preprints", action="store_true")
    p = sp.add_parser("citing"); p.add_argument("pmid"); p.add_argument("--terms", default=""); p.add_argument("--max", type=int, default=50)
    p = sp.add_parser("refs"); p.add_argument("pmid")
    p = sp.add_parser("icite"); p.add_argument("pmids", nargs="+")
    p = sp.add_parser("published"); p.add_argument("doi")
    a = ap.parse_args()
    if a.cmd == "search":
        n, rows = search(a.q + (" AND SRC:PPR" if a.preprints else ""), a.max); print(f"# {n} hits (most cited first)"); show(rows)
    elif a.cmd == "citing":
        n, rows = search(f"CITES:{a.pmid}_MED" + (f" AND ({a.terms})" if a.terms else ""), a.max); print(f"# {n} citing papers"); show(rows)
    elif a.cmd == "refs":
        d = get(f"{E}/MED/{a.pmid}/references?format=json&pageSize=1000")
        for r in d.get("referenceList", {}).get("reference", []):
            print("\t".join(str(r.get(k, "")) for k in ("id", "pubYear", "journalAbbreviation", "authorString", "title")))
    elif a.cmd == "icite":
        d = get("https://icite.od.nih.gov/api/pubs?pmids=" + ",".join(a.pmids) + "&fl=pmid,year,title,relative_citation_ratio,nih_percentile,citation_count,is_research_article")
        for r in d.get("data", []):
            print("\t".join(str(r.get(k, "")) for k in ("pmid", "year", "citation_count", "relative_citation_ratio", "nih_percentile", "is_research_article", "title")))
    elif a.cmd == "published":
        d = get(f"https://api.biorxiv.org/pubs/biorxiv/{a.doi}")
        c = d.get("collection", [])
        print(json.dumps(c[0], indent=1) if c else "no published version recorded")


if __name__ == "__main__":
    main()
