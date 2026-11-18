#!/usr/bin/env python3
"""folio — command-line side of Folio Studio, used by the Claude Code session (and by hand).

  folio init <dir> --title "Figure 3" --mode canvas --size 180x120 [--from panel1.png panel2.png ...] [--md text.md]
  folio start [--studio DIR]                 start (or reuse) the studio server, print its link
  folio register <folio_dir>                 add a folio to the running studio
  folio ls                                   folios in this studio
  folio show <folio> [block]                 print the document (or one block)
  folio set <folio> <block> key=value ...    change geometry/style directly (x=10 y=4.5 w=60 pt=9 text="..." )
  folio text <folio> <block> [--file F|-]    replace a block's text from a file / stdin
  folio add <folio> text|image [key=value]   add a block
  folio rm <folio> <block>
  folio suggest <folio> <block> [key=value ...] [--why "..."]   propose a change; the user accepts in the page
  folio suggest <folio> --add type=text text="..." x=.. y=.. w=.. h=.. [--why ...]
  folio suggest <folio> --delete <block> [--why ...]
  folio shot <folio> [--region x,y,w,h | --block id] [--scale 3]   render a screenshot → prints the PNG path (open it with Read)
  folio export <folio> [--pdf|--png]
  folio pending [show|hook|watch|seen <id>|working <id>]          the Ask/Edit inbox of this studio
  folio answer <folio> <request_id> [--file F|-] [--changed a,b]  post an answer (becomes a thread entry + note)
  folio stop
  folio journal ls | show <id> | set <folio> <id> [--width single|mid|double]   journal profiles; attach one to a folio
  folio check <folio> [--json]                                    check a folio against its journal (size, text, resolution, word limits)
  folio paper init <dir> --journal <id> --title "..." [--figures 7] [--supp 0]   manuscript workspace: main text, front matter, one folio per figure

Studio dir: --studio, $FOLIO_STUDIO, or ./.folio.
"""
import argparse, json, os, re, shutil, subprocess, sys, time, urllib.request, urllib.error
from datetime import datetime

HERE = os.path.dirname(os.path.abspath(__file__))


def studio_dir(a):
    d = getattr(a, "studio", None) or os.environ.get("FOLIO_STUDIO") or os.path.join(os.getcwd(), ".folio")
    return os.path.abspath(d)


def jload(p, d=None):
    try:
        with open(p) as f:
            return json.load(f)
    except Exception:
        return d


def server_url(sd):
    try:
        with open(os.path.join(sd, "server_url.txt")) as f:
            return f.read().strip()
    except FileNotFoundError:
        return None


def alive(url):
    try:
        with urllib.request.urlopen(url.replace("/?t=", "/api/health?t="), timeout=2) as r:
            return r.status == 200
    except Exception:
        return False


def call(sd, path, body=None, method=None):
    url = server_url(sd)
    if not url or not alive(url):
        raise SystemExit("studio server is not running — run: folio start")
    base, tok = url.split("/?t=")
    req = urllib.request.Request(f"{base}{path}{'&' if '?' in path else '?'}t={tok}", data=json.dumps(body).encode() if body is not None else None,
                                 headers={"Content-Type": "application/json"}, method=method or ("POST" if body is not None else "GET"))
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.loads(r.read() or b"{}")


def folio_path(sd, fid):
    for e in jload(os.path.join(sd, "folios.json"), []):
        if e["id"] == fid:
            return e["path"]
    if os.path.isdir(fid) and os.path.exists(os.path.join(fid, "folio.json")):
        return os.path.abspath(fid)
    raise SystemExit(f"unknown folio {fid}; folio ls")


def load_doc(sd, fid):
    url = server_url(sd)
    if url and alive(url):
        d = call(sd, f"/api/folio/{fid}")
        d.pop("_hash", None)
        return d
    p = folio_path(sd, fid)
    d = jload(os.path.join(p, "folio.json"))
    for b in d.get("blocks", []):
        if b.get("type") == "text" and b.get("file") and "text" not in b:
            fp = os.path.join(p, b["file"])
            b["text"] = open(fp).read() if os.path.exists(fp) else ""
    return d


def save_doc(sd, fid, doc, why):
    url = server_url(sd)
    if url and alive(url):
        return call(sd, f"/api/folio/{fid}", {"doc": doc, "why": why})["hash"]
    p = folio_path(sd, fid)
    vd = os.path.join(p, "folio_review", "versions"); os.makedirs(vd, exist_ok=True)
    stamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    if os.path.exists(os.path.join(p, "folio.json")):
        shutil.copy2(os.path.join(p, "folio.json"), os.path.join(vd, f"{stamp}__folio.json"))
    out = json.loads(json.dumps(doc))
    for b in out.get("blocks", []):
        if b.get("type") == "text" and b.get("file"):
            fp = os.path.join(p, b["file"]); os.makedirs(os.path.dirname(fp), exist_ok=True)
            open(fp, "w").write(b.get("text", "")); b.pop("text", None)
    out["updated"] = datetime.now().isoformat(timespec="seconds")
    with open(os.path.join(p, "folio.json"), "w") as f:
        json.dump(out, f, indent=1, ensure_ascii=False)
    return "offline"


def parse_kv(items):
    out = {}
    for it in items:
        if "=" not in it:
            raise SystemExit(f"expected key=value, got {it}")
        k, v = it.split("=", 1)
        if v[:1] in "{[" and v:
            out[k] = json.loads(v); continue
        if v.lower() in ("true", "false"):
            out[k] = v.lower() == "true"
        else:
            try:
                out[k] = float(v) if "." in v or re.fullmatch(r"-?\d+", v) else v
                if isinstance(out[k], float) and out[k].is_integer() and "." not in v:
                    out[k] = int(out[k])
            except ValueError:
                out[k] = v
    return out


def png_size(path):
    try:
        from PIL import Image
        with Image.open(path) as im:
            return im.size
    except Exception:
        import struct
        with open(path, "rb") as h:
            sig = h.read(24)
        if sig[:8] == b"\x89PNG\r\n\x1a\n":
            return struct.unpack(">II", sig[16:24])
        return (4, 3)


# ----------------------------------------------------------------------------- Playwright (PDF export, screenshots)
# Installed automatically the first time a studio starts (one-time ~150 MB Chromium download into the user's
# Playwright cache), in the background; status in ~/.cache/folio-studio/playwright_setup.json.
# FOLIO_NO_AUTO_INSTALL=1 turns this off; `folio setup` runs it in the foreground.
SETUP_STATE = os.path.join(os.path.expanduser("~"), ".cache", "folio-studio", "playwright_setup.json")


def playwright_browser_present():
    import glob
    roots = [os.environ["PLAYWRIGHT_BROWSERS_PATH"]] if os.environ.get("PLAYWRIGHT_BROWSERS_PATH") else [
        os.path.expanduser("~/.cache/ms-playwright"), os.path.expanduser("~/Library/Caches/ms-playwright"),
        os.path.join(os.environ.get("LOCALAPPDATA", ""), "ms-playwright")]
    return any(r and glob.glob(os.path.join(r, "chromium*")) for r in roots)


def playwright_ready():
    import importlib
    importlib.invalidate_caches()
    try:
        import playwright.sync_api  # noqa
    except Exception:
        return False
    return playwright_browser_present()


def setup_state():
    st = jload(SETUP_STATE, {})
    if st.get("state") == "installing" and st.get("pid"):
        try:
            os.kill(st["pid"], 0)
        except OSError:
            st["state"] = "failed"; st.setdefault("error", "installer stopped")
    return st


def ensure_playwright(quiet=False):
    """Start the one-time background install when Playwright or its Chromium is missing."""
    if playwright_ready() or os.environ.get("FOLIO_NO_AUTO_INSTALL"):
        return "ready" if playwright_ready() else "off"
    st = setup_state()
    if st.get("state") == "installing":
        return "installing"
    if st.get("state") == "failed" and time.time() - st.get("time", 0) < 86400:
        if not quiet:
            print(f"PDF export: Playwright install failed earlier ({st.get('error', '')[:120]}); retry with: folio setup")
        return "failed"
    os.makedirs(os.path.dirname(SETUP_STATE), exist_ok=True)
    log = open(os.path.join(os.path.dirname(SETUP_STATE), "playwright_setup.log"), "a")
    p = subprocess.Popen([sys.executable, os.path.join(HERE, "folio.py"), "setup"], stdout=log, stderr=log,
                         stdin=subprocess.DEVNULL, start_new_session=True, close_fds=True)
    json.dump({"state": "installing", "pid": p.pid, "time": time.time()}, open(SETUP_STATE, "w"))
    if not quiet:
        print("PDF export: installing Playwright + Chromium in the background (one time, ~150 MB); "
              "until it finishes, Export uses the browser print dialog. Log: " + log.name)
    return "installing"


def cmd_setup(a):
    os.makedirs(os.path.dirname(SETUP_STATE), exist_ok=True)
    json.dump({"state": "installing", "pid": os.getpid(), "time": time.time()}, open(SETUP_STATE, "w"))
    steps = []
    try:
        import importlib
        try:
            import playwright  # noqa
        except Exception:
            steps.append([sys.executable, "-m", "pip", "install", "--quiet", "playwright"])
        steps.append([sys.executable, "-m", "playwright", "install", "chromium"])
        for cmd in steps:
            print("$", " ".join(cmd), flush=True)
            r = subprocess.run(cmd, capture_output=True, text=True)
            print(r.stdout[-2000:], r.stderr[-2000:], flush=True)
            if r.returncode:
                raise RuntimeError((r.stderr or r.stdout).strip().splitlines()[-1] if (r.stderr or r.stdout).strip() else f"exit {r.returncode}")
        importlib.invalidate_caches()
        if not playwright_ready():
            raise RuntimeError("Playwright installed but Chromium not found")
        json.dump({"state": "ok", "time": time.time()}, open(SETUP_STATE, "w"))
        print("Playwright ready: PDF / PNG export and server screenshots enabled")
    except Exception as e:
        json.dump({"state": "failed", "time": time.time(), "error": str(e)[:300]}, open(SETUP_STATE, "w"))
        raise SystemExit(f"Playwright setup failed: {e}\n(on Linux, missing system libraries: python3 -m playwright install-deps chromium, needs sudo)")


# ----------------------------------------------------------------------------- commands

def cmd_init(a):
    d = os.path.abspath(a.dir)
    os.makedirs(os.path.join(d, "assets"), exist_ok=True)
    w, h = (float(x) for x in a.size.split("x"))
    fid = a.id or re.sub(r"[^a-z0-9]+", "-", (a.title or os.path.basename(d)).lower()).strip("-")
    doc = {"folio_version": 1, "id": fid, "title": a.title or fid, "mode": a.mode, "page": {"w_mm": w, "h_mm": h, "margin_mm": a.margin},
           "style": {"font": "Arial, Helvetica, sans-serif", "text_pt": 8, "label_pt": 10}, "blocks": [], "created": datetime.now().isoformat(timespec="seconds")}
    blocks = doc["blocks"]
    if a.md:
        txt = open(a.md).read()
        if a.mode == "flow":
            for i, chunk in enumerate([c for c in re.split(r"\n{2,}", txt) if c.strip()]):
                blocks.append({"id": f"t{i+1:03d}", "type": "text", "text": chunk.strip(), "pt": 11 if not chunk.startswith("#") else 14})
        else:
            blocks.append({"id": "text1", "type": "text", "text": txt, "x": 2, "y": 2, "w": w - 4, "h": h - 4, "pt": 8})
    if a.panels:
        labels = "abcdefghijklmnopqrstuvwxyz"
        n = len(a.panels); cols = min(n, a.cols or (2 if n <= 4 else 3)); rows = -(-n // cols)
        gap = 4; lab_h = 5
        legend_h = 22 if a.mode == "canvas" else 0
        cw = (w - gap * (cols - 1)) / cols
        ch = (h - legend_h - gap * rows - lab_h * rows) / rows if a.mode == "canvas" else 60
        for i, src in enumerate(a.panels):
            name = re.sub(r"[^A-Za-z0-9_.\-]", "_", os.path.basename(src))
            dst = os.path.join(d, "assets", name)
            if os.path.abspath(src) != dst:
                shutil.copy2(src, dst)
            pw, ph = png_size(dst)
            bw = cw; bh = bw * ph / pw
            if bh > ch:
                bh = ch; bw = bh * pw / ph
            r, c = divmod(i, cols)
            x = c * (cw + gap); y = r * (ch + gap + lab_h)
            lab = labels[i]
            if a.mode == "canvas":
                blocks.append({"id": f"label_{lab}", "type": "text", "role": "label", "text": f"**{lab}**", "x": round(x, 1), "y": round(y, 1), "w": 6, "h": 5, "pt": 10})
                blocks.append({"id": f"panel_{lab}", "type": "image", "src": f"assets/{name}", "x": round(x, 1), "y": round(y + lab_h, 1), "w": round(bw, 1), "h": round(bh, 1), "fit": "contain"})
            else:
                blocks.append({"id": f"panel_{lab}", "type": "image", "src": f"assets/{name}", "w": round(min(bw, w - 2 * a.margin), 1), "h": round(bh, 1)})
                blocks.append({"id": f"cap_{lab}", "type": "text", "text": f"**{lab}** Caption.", "pt": 9})
        if a.mode == "canvas":
            blocks.append({"id": "legend", "type": "text", "role": "legend", "text": f"**{a.title or 'Figure'} | Title.** Legend text: one sentence per panel (**a**) … (**b**) …", "x": 0, "y": round(h - legend_h + 2, 1), "w": w, "h": legend_h - 2, "pt": 7})
    with open(os.path.join(d, "folio.json"), "w") as f:
        json.dump(doc, f, indent=1, ensure_ascii=False)
    os.makedirs(os.path.join(d, "folio_review"), exist_ok=True)
    print(f"created {os.path.join(d, 'folio.json')}  id={fid}  blocks={len(blocks)}")
    sd = studio_dir(a)
    reg = jload(os.path.join(sd, "folios.json"), [])
    reg = [e for e in reg if e["id"] != fid] + [{"id": fid, "path": d, "title": doc["title"], "mode": a.mode}]
    os.makedirs(sd, exist_ok=True)
    json.dump(reg, open(os.path.join(sd, "folios.json"), "w"), indent=1)
    url = server_url(sd)
    if url and alive(url):
        print(f"open: {url}&folio={fid}")
    else:
        print("studio not running: folio start")


def cmd_start(a):
    sd = studio_dir(a); os.makedirs(sd, exist_ok=True)
    url = server_url(sd)
    if url and alive(url):
        print(url); return
    sj = os.path.join(sd, "studio.json")
    cfg = jload(sj, {})
    sid = os.environ.get("CLAUDE_SESSION_ID") or a.session
    if sid:
        cfg["session_id"] = sid
    cfg.setdefault("project", os.getcwd()); cfg["started"] = datetime.now().isoformat(timespec="seconds")
    json.dump(cfg, open(sj, "w"), indent=1)
    log = open(os.path.join(sd, "server.out"), "a")
    cmd = [sys.executable, os.path.join(HERE, "server.py"), "--studio", sd] + (["--port", str(a.port)] if a.port else [])
    subprocess.Popen(cmd, stdout=log, stderr=log, stdin=subprocess.DEVNULL, start_new_session=True, close_fds=True)
    ensure_playwright()
    for _ in range(40):
        time.sleep(0.25)
        url = server_url(sd)
        if url and alive(url):
            print(url); return
    raise SystemExit("server did not start; see " + os.path.join(sd, "server.out"))


def cmd_stop(a):
    sd = studio_dir(a)
    try:
        url = server_url(sd)
        call(sd, "/api/shutdown", {})
        for _ in range(40):              # wait until the port is released, so a restart keeps it
            if not (url and alive(url)):
                break
            time.sleep(0.25)
        print("stopped")
    except SystemExit:
        print("not running")


def cmd_register(a):
    sd = studio_dir(a)
    d = os.path.abspath(a.folio_dir)
    doc = jload(os.path.join(d, "folio.json"))
    reg = jload(os.path.join(sd, "folios.json"), [])
    reg = [e for e in reg if e["id"] != doc["id"]] + [{"id": doc["id"], "path": d, "title": doc.get("title"), "mode": doc.get("mode")}]
    json.dump(reg, open(os.path.join(sd, "folios.json"), "w"), indent=1)
    url = server_url(sd)
    print(f"registered {doc['id']}" + (f"  open: {url}&folio={doc['id']}" if url else ""))


def cmd_ls(a):
    sd = studio_dir(a)
    url = server_url(sd)
    for e in jload(os.path.join(sd, "folios.json"), []):
        print(f"{e['id']:20s} {e.get('mode','?'):7s} {e.get('title','')}   {e['path']}")
    if url:
        print("studio:", url, "(running)" if alive(url) else "(stopped)")


def cmd_show(a):
    doc = load_doc(studio_dir(a), a.folio)
    if a.block:
        b = next((b for b in doc["blocks"] if b["id"] == a.block), None)
        print(json.dumps(b, indent=1, ensure_ascii=False))
    else:
        print(f"{doc['id']}  {doc.get('title')}  mode={doc.get('mode')}  page={doc['page']}")
        for b in doc["blocks"]:
            geo = f"x={b.get('x')} y={b.get('y')} w={b.get('w')} h={b.get('h')}"
            desc = b.get("src") if b["type"] == "image" else repr((b.get("text") or "")[:60])
            print(f"  {b['id']:14s} {b['type']:5s} {geo:40s} {desc}")


def cmd_set(a):
    sd = studio_dir(a); doc = load_doc(sd, a.folio)
    b = next((b for b in doc["blocks"] if b["id"] == a.block), None)
    if not b:
        raise SystemExit("no block " + a.block)
    kv = parse_kv(a.kv); b.update(kv)
    if "text" in kv and "html" not in kv:
        b.pop("html", None)              # rich text from the page is replaced by the new Markdown
    print("hash", save_doc(sd, a.folio, doc, f"claude set {a.block} {' '.join(a.kv)[:60]}"))


def cmd_text(a):
    sd = studio_dir(a); doc = load_doc(sd, a.folio)
    b = next((b for b in doc["blocks"] if b["id"] == a.block), None)
    if not b:
        raise SystemExit("no block " + a.block)
    b["text"] = sys.stdin.read() if a.file in (None, "-") else open(a.file).read()
    b.pop("html", None)
    print("hash", save_doc(sd, a.folio, doc, f"claude text {a.block}"))


def cmd_add(a):
    sd = studio_dir(a); doc = load_doc(sd, a.folio)
    kv = parse_kv(a.kv)
    b = {"id": kv.pop("id", None) or f"{a.type[:1]}{int(time.time()) % 100000}", "type": a.type}
    if a.type == "image" and "src" in kv and os.path.exists(kv["src"]):
        p = folio_path(sd, a.folio); name = os.path.basename(kv["src"]); dst = os.path.join(p, "assets", name)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        if os.path.abspath(kv["src"]) != dst:
            shutil.copy2(kv["src"], dst)
        kv["src"] = "assets/" + name
        if "h" not in kv and "w" in kv:
            pw, ph = png_size(dst); kv["h"] = round(kv["w"] * ph / pw, 1)
    b.update(kv); doc["blocks"].append(b)
    print(b["id"], "hash", save_doc(sd, a.folio, doc, f"claude add {b['id']}"))


def cmd_rm(a):
    sd = studio_dir(a); doc = load_doc(sd, a.folio)
    doc["blocks"] = [b for b in doc["blocks"] if b["id"] != a.block]
    print("hash", save_doc(sd, a.folio, doc, f"claude rm {a.block}"))


def cmd_suggest(a):
    sd = studio_dir(a)
    if a.delete:
        s = {"op": "delete", "block": a.delete, "why": a.why}
    elif a.add:
        kv = parse_kv(a.kv); kv.setdefault("id", f"n{int(time.time()) % 100000}"); kv.setdefault("type", "text")
        s = {"op": "add", "block": kv["id"], "new": kv, "why": a.why}
    else:
        if not a.block:
            raise SystemExit("block required")
        s = {"op": "update", "block": a.block, "new": parse_kv(a.kv), "why": a.why}
        if a.file:
            s["new"]["text"] = sys.stdin.read() if a.file == "-" else open(a.file).read()
    r = call(sd, f"/api/folio/{a.folio}/suggest", s)
    print("suggested", r["id"], "— the user sees ✎ on the block and can Accept / Reject")


def cmd_shot(a):
    sd = studio_dir(a)
    region = None
    if a.region:
        x, y, w, h = (float(v) for v in a.region.split(","))
        region = {"x": x, "y": y, "w": w, "h": h}
    elif a.block:
        doc = load_doc(sd, a.folio)
        b = next((b for b in doc["blocks"] if b["id"] == a.block), None)
        if not b:
            raise SystemExit("no block " + a.block)
        m = a.pad
        region = {"x": max(0, b["x"] - m), "y": max(0, b["y"] - m), "w": b["w"] + 2 * m, "h": b["h"] + 2 * m}
    r = call(sd, f"/api/folio/{a.folio}/screenshot", {"region": region, "scale": a.scale})
    if not r.get("ok"):
        raise SystemExit("screenshot failed: " + str(r.get("error")) + (" — Playwright is " + (setup_state().get("state") or "missing") + "; run: folio setup" if r.get("error") == "playwright-missing" else ""))
    print(r["path"])
    print("blocks:", ", ".join(r["blocks"]))


def cmd_export(a):
    sd = studio_dir(a)
    r = call(sd, f"/api/folio/{a.folio}/export", {"format": "png" if a.png else "pdf"})
    print(r.get("path") or r)


def cmd_pending(a):
    sd = studio_dir(a)
    reg = jload(os.path.join(sd, "folios.json"), [])
    items = []
    for e in reg:
        td = os.path.join(e["path"], "folio_review", "threads")
        if not os.path.isdir(td):
            continue
        for fn in sorted(os.listdir(td)):
            t = jload(os.path.join(td, fn))
            if t and t.get("status") in ("queued", "seen", "working"):
                items.append((e, t))
    sub = a.sub or "show"
    if sub in ("seen", "working"):
        for e, t in items:
            if t["id"] == a.id:
                call(sd, f"/api/request/{t['id']}/status", {"folio": e["id"], "status": sub})
                print(sub, t["id"])
        return
    if sub == "watch":
        return
    if sub == "hook" and not items:
        return
    if not items:
        print("no pending requests"); return
    print(f"FOLIO STUDIO: {len(items)} pending request(s) — answer each with: folio answer <folio> <id> --file answer.md")
    for e, t in items:
        r = t["request"]; an = r.get("anchor") or {}
        print(f"\n[{t['id']}] folio={e['id']} type={r['type']} status={t['status']} block={an.get('block')} time={r['time']}")
        if an.get("quote"):
            print("  selected:", an["quote"][:300].replace("\n", " "))
        if an.get("type") == "group":
            print("  group of", len(an.get("blocks") or []), "blocks:", ", ".join(an.get("blocks") or []), " bbox(mm):", an.get("bbox"))
        if an.get("region"):
            print("  region(mm):", an["region"], "blocks:", an.get("blocks"))
        print("  text:", r.get("text", "").replace("\n", "\n        "))
        if r.get("attachments"):
            print("  images=" + " ".join(os.path.join(e["path"], "folio_review", p) for p in r["attachments"]) + "   (open each with the Read tool before answering)")
        if r.get("follows"):
            print("  follows:", ", ".join(r["follows"]), "(read those threads first)")
        if r["type"] == "edit":
            print("  confirm_before_rerun:", r.get("confirm", True))


def cmd_answer(a):
    sd = studio_dir(a)
    text = sys.stdin.read() if a.file in (None, "-") else open(a.file).read()
    call(sd, "/api/answer", {"folio": a.folio, "id": a.id, "text": text, "changed": [c for c in (a.changed or "").split(",") if c], "note": not a.no_note})
    print("answered", a.id)


# ----------------------------------------------------------------------------- journals and paper mode (0.6.0)
def _journal(sd, jid):
    sys.path.insert(0, HERE); import journal as J
    js = J.journals(sd)
    if jid not in js:
        raise SystemExit(f"unknown journal {jid}; folio journal ls  (known: {', '.join(js)})")
    return J, js[jid]


def cmd_journal(a):
    sd = studio_dir(a)
    sys.path.insert(0, HERE); import journal as J
    if a.sub == "ls":
        for k, j in J.journals(sd).items():
            s = J.summary(j)
            print(f"{k:24} figs {str(s['main_display_items'] or '-'):3} words {str(s['main_text_words'] or '-'):6} widths {', '.join(f'{n} {v}' for n, v in s['widths_mm'].items()):32} text {s['font_pt']['min']}-{s['font_pt']['max']} pt  verified: {s['verified']}")
    elif a.sub == "show":
        print(json.dumps(_journal(sd, a.a1)[1], indent=1, ensure_ascii=False))
    elif a.sub == "set":
        if not a.a2:
            raise SystemExit("folio journal set <folio> <journal-id>")
        _, j = _journal(sd, a.a2)
        doc = load_doc(sd, a.a1); doc["journal"] = j["id"]
        if a.width:
            if a.width not in j["figure"]["widths_mm"]:
                raise SystemExit(f"{j['name']} widths: {', '.join(j['figure']['widths_mm'])}")
            doc["page"]["w_mm"] = j["figure"]["widths_mm"][a.width]
        save_doc(sd, a.a1, doc, f"journal = {j['id']}")
        print(f"{a.a1}: journal = {j['name']}" + (f", page width {doc['page']['w_mm']} mm" if a.width else ""))


def cmd_check(a):
    sd = studio_dir(a)
    doc = load_doc(sd, a.folio)
    jid = a.journal or doc.get("journal")
    if not jid:
        raise SystemExit("this folio has no journal; folio journal set <folio> <id>")
    J, j = _journal(sd, jid)
    r = J.check(doc, j, folio_path(sd, a.folio))
    if a.json:
        print(json.dumps(r, indent=1, ensure_ascii=False)); return
    mark = {"error": "✗", "warn": "!", "ok": "✓", "info": "·"}
    print(f"{a.folio} vs {r['name']}: {r['errors']} problem(s), {r['warnings']} warning(s)")
    for i in r["items"]:
        print(f"  {mark[i['level']]} {i['msg']}" + (f"  [{i['block']}]" if i.get("block") else ""))
    for s in r["counts"].get("sections", []):
        print(f"      {s['words']:6d}  {s['section']}  ({s['kind']})")


def _write_folio(sd, d, doc):
    os.makedirs(os.path.join(d, "assets"), exist_ok=True); os.makedirs(os.path.join(d, "folio_review"), exist_ok=True)
    if os.path.exists(os.path.join(d, "folio.json")):
        print(f"  kept existing {os.path.join(d, 'folio.json')}"); return
    json.dump(doc, open(os.path.join(d, "folio.json"), "w"), indent=1, ensure_ascii=False)
    reg = jload(os.path.join(sd, "folios.json"), [])
    reg = [e for e in reg if e["id"] != doc["id"]] + [{"id": doc["id"], "path": d, "title": doc["title"], "mode": doc["mode"]}]
    os.makedirs(sd, exist_ok=True); json.dump(reg, open(os.path.join(sd, "folios.json"), "w"), indent=1)
    print(f"  {doc['id']:14} {doc['mode']:6} {doc['page']['w_mm']:g} x {doc['page']['h_mm']:g} mm  {d}")


def cmd_paper(a):
    sd = studio_dir(a)
    J, j = _journal(sd, a.journal)
    root = os.path.abspath(a.dir); F = j["figure"]; L = j["limits"]; now = datetime.now().isoformat(timespec="seconds")
    base = lambda fid, title, mode, w, h, role, n=None, margin=0: {"folio_version": 1, "id": fid, "title": title, "mode": mode, "journal": j["id"],
        "paper": {"role": role, "n": n, "title": a.title}, "page": {"w_mm": w, "h_mm": h, "margin_mm": margin},
        "style": {"font": "Arial, Helvetica, sans-serif", "text_pt": F["font_pt"]["max"], "label_pt": F["panel_label"]["pt"]}, "blocks": [], "created": now}
    chunks = lambda md: [{"id": f"t{i+1:03d}", "type": "text", "text": c.strip(), "pt": 16 if c.startswith("# ") else 13 if c.startswith("#") else 11}
                         for i, c in enumerate([c for c in re.split(r"\n{2,}", md) if c.strip()])]
    print(f"{j['name']} manuscript workspace in {root}")
    doc = base("main-text", "Main text", "flow", 210, 297, "main_text", margin=22); doc["blocks"] = chunks(J.manuscript_md(j, a.title)); _write_folio(sd, os.path.join(root, "text", "main"), doc)
    doc = base("front-matter", "Highlights, in brief, cover letter", "flow", 210, 297, "front_matter", margin=22); doc["blocks"] = chunks(J.front_md(j)); _write_folio(sd, os.path.join(root, "text", "front_matter"), doc)
    W = max(F["widths_mm"].values()); H = min(F["max_height_mm"], F.get("recommended_height_mm") or F["max_height_mm"])
    up = F["panel_label"]["case"] == "upper"
    def fig(fid, title, role, n):
        doc = base(fid, title, "canvas", W, H, role, n)
        doc["blocks"] = [{"id": "label_a", "type": "text", "role": "label", "text": f"**{'A' if up else 'a'}**", "x": 0, "y": 0, "w": 6, "h": 5, "pt": F["panel_label"]["pt"]},
                         {"id": "hint", "type": "text", "text": f"{title}. Drop panels here (vector PDF/SVG where possible). Width {W:g} mm, height up to {F['max_height_mm']} mm, text {F['font_pt']['min']}–{F['font_pt']['max']} pt.", "x": 8, "y": 1, "w": W - 10, "h": 8, "pt": F["font_pt"]["max"], "color": "#777777"}]
        _write_folio(sd, os.path.join(root, "figures", fid), doc)
    for n in range(1, a.figures + 1):
        fig(f"fig{n}", f"Figure {n}", "figure", n)
    sname = "Figure S" if j.get("family") == "cell-press" else "Extended Data Fig. "
    for n in range(1, a.supp + 1):
        fig(f"figS{n}", f"{sname}{n}", "supp_figure", n)
    if any("raphical abstract" in x for x in j.get("front_matter", [])):
        doc = base("graphical-abstract", "Graphical abstract", "canvas", 101.6, 101.6, "graphical_abstract")
        doc["blocks"] = [{"id": "hint", "type": "text", "text": "Graphical abstract: one message, no data panels. Exports at 1200 × 1200 px (300 dpi).", "x": 4, "y": 4, "w": 93, "h": 10, "pt": 9, "color": "#777777"}]
        _write_folio(sd, os.path.join(root, "figures", "graphical_abstract"), doc)
    json.dump({"title": a.title, "journal": j["id"], "created": now, "figures": a.figures, "supp": a.supp}, open(os.path.join(root, "paper.json"), "w"), indent=1)
    print(f"next: folio --studio {sd} start   (limits verified: {j['verified']['level']})")


def main():
    ap = argparse.ArgumentParser(prog="folio", description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--studio")
    sp = ap.add_subparsers(dest="cmd", required=True)
    p = sp.add_parser("init"); p.add_argument("dir"); p.add_argument("--title"); p.add_argument("--id"); p.add_argument("--mode", choices=["canvas", "flow"], default="canvas")
    p.add_argument("--size", default="180x120", help="WxH in mm (A4 210x297, A0 841x1189)"); p.add_argument("--margin", type=float, default=15)
    p.add_argument("--from", dest="panels", nargs="*", default=[]); p.add_argument("--cols", type=int); p.add_argument("--md"); p.set_defaults(f=cmd_init)
    p = sp.add_parser("start"); p.add_argument("--port", type=int); p.add_argument("--session"); p.set_defaults(f=cmd_start)
    p = sp.add_parser("stop"); p.set_defaults(f=cmd_stop)
    p = sp.add_parser("setup", help="install Playwright + Chromium (PDF export, screenshots)"); p.set_defaults(f=cmd_setup)
    p = sp.add_parser("register"); p.add_argument("folio_dir"); p.set_defaults(f=cmd_register)
    p = sp.add_parser("ls"); p.set_defaults(f=cmd_ls)
    p = sp.add_parser("show"); p.add_argument("folio"); p.add_argument("block", nargs="?"); p.set_defaults(f=cmd_show)
    p = sp.add_parser("set"); p.add_argument("folio"); p.add_argument("block"); p.add_argument("kv", nargs="+"); p.set_defaults(f=cmd_set)
    p = sp.add_parser("text"); p.add_argument("folio"); p.add_argument("block"); p.add_argument("--file"); p.set_defaults(f=cmd_text)
    p = sp.add_parser("add"); p.add_argument("folio"); p.add_argument("type", choices=["text", "image", "shape"]); p.add_argument("kv", nargs="*"); p.set_defaults(f=cmd_add)
    p = sp.add_parser("rm"); p.add_argument("folio"); p.add_argument("block"); p.set_defaults(f=cmd_rm)
    p = sp.add_parser("suggest"); p.add_argument("folio"); p.add_argument("block", nargs="?"); p.add_argument("kv", nargs="*"); p.add_argument("--file"); p.add_argument("--add", action="store_true"); p.add_argument("--delete"); p.add_argument("--why", default=""); p.set_defaults(f=cmd_suggest)
    p = sp.add_parser("shot"); p.add_argument("folio"); p.add_argument("--region"); p.add_argument("--block"); p.add_argument("--pad", type=float, default=2); p.add_argument("--scale", type=float, default=3); p.set_defaults(f=cmd_shot)
    p = sp.add_parser("export"); p.add_argument("folio"); p.add_argument("--pdf", action="store_true"); p.add_argument("--png", action="store_true"); p.set_defaults(f=cmd_export)
    p = sp.add_parser("pending"); p.add_argument("sub", nargs="?", choices=["show", "hook", "watch", "seen", "working"]); p.add_argument("id", nargs="?"); p.set_defaults(f=cmd_pending)
    p = sp.add_parser("answer"); p.add_argument("folio"); p.add_argument("id"); p.add_argument("--file"); p.add_argument("--changed"); p.add_argument("--no-note", action="store_true"); p.set_defaults(f=cmd_answer)
    p = sp.add_parser("journal"); p.add_argument("sub", choices=["ls", "show", "set"]); p.add_argument("a1", nargs="?"); p.add_argument("a2", nargs="?"); p.add_argument("--width"); p.set_defaults(f=cmd_journal)
    p = sp.add_parser("check"); p.add_argument("folio"); p.add_argument("--journal"); p.add_argument("--json", action="store_true"); p.set_defaults(f=cmd_check)
    p = sp.add_parser("paper"); p.add_argument("sub", choices=["init"]); p.add_argument("dir"); p.add_argument("--journal", required=True); p.add_argument("--title", required=True)
    p.add_argument("--figures", type=int, default=7); p.add_argument("--supp", type=int, default=0); p.set_defaults(f=cmd_paper)
    a = ap.parse_args()
    a.f(a)


if __name__ == "__main__":
    main()
