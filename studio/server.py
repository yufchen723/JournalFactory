#!/usr/bin/env python3
"""Folio Studio review/edit server.

One studio per Claude Code session. Serves the editor, the folios it registers,
and the Ask/Edit inbox that the owning session answers.

  python3 server.py --studio <studio_dir> [--port N]

Binds 127.0.0.1 only; every request needs the token (query ?t=, header
X-Folio-Token, or the cookie the first visit sets). Writes only inside the
studio dir and the registered folio folders.
"""
import argparse, base64, hashlib, io, json, mimetypes, os, re, secrets, shutil, socket, subprocess, sys, threading, time, uuid
from datetime import datetime
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs, unquote

HERE = os.path.dirname(os.path.abspath(__file__))
EDITOR_DIR = os.path.join(HERE, "editor")
import sys as _sys
_sys.path.insert(0, HERE)
MAX_BODY = 64 * 1024 * 1024
IMAGE_MAGIC = {b"\x89PNG": "png", b"\xff\xd8\xff": "jpg", b"GIF8": "gif", b"RIFF": "webp"}

# --------------------------------------------------------------------------- state

class Studio:
    def __init__(self, root):
        self.root = os.path.abspath(root)
        os.makedirs(self.root, exist_ok=True)
        self.lock = threading.RLock()
        self.subscribers = []          # SSE queues
        self.folio_mtimes = {}
        self.cfg = self._load_json("studio.json", {})
        self.token = self.cfg.get("token") or secrets.token_urlsafe(18)
        self.cfg["token"] = self.token
        self._save_json("studio.json", self.cfg)

    # ---- paths
    def p(self, *a):
        return os.path.join(self.root, *a)

    def _load_json(self, name, default):
        try:
            with open(self.p(name)) as f:
                return json.load(f)
        except Exception:
            return default

    def _save_json(self, name, data):
        tmp = self.p(name + ".tmp")
        with open(tmp, "w") as f:
            json.dump(data, f, indent=1, ensure_ascii=False)
        os.replace(tmp, self.p(name))

    # ---- registry
    def folios(self):
        return self._load_json("folios.json", [])

    def folio_entry(self, fid):
        for e in self.folios():
            if e["id"] == fid:
                return e
        return None

    def register(self, path, fid=None):
        path = os.path.abspath(path)
        fj = os.path.join(path, "folio.json")
        with open(fj) as f:
            doc = json.load(f)
        fid = fid or doc.get("id") or os.path.basename(path)
        entries = [e for e in self.folios() if e["id"] != fid]
        entries.append({"id": fid, "path": path, "title": doc.get("title", fid), "mode": doc.get("mode", "canvas")})
        self._save_json("folios.json", entries)
        return fid

    def folio_dir(self, fid):
        e = self.folio_entry(fid)
        if not e:
            raise KeyError(fid)
        return e["path"]

    def review_dir(self, fid):
        d = os.path.join(self.folio_dir(fid), "folio_review")
        os.makedirs(d, exist_ok=True)
        return d

    # ---- folio document
    def load_folio(self, fid):
        d = self.folio_dir(fid)
        with open(os.path.join(d, "folio.json")) as f:
            doc = json.load(f)
        # resolve text files
        for b in doc.get("blocks", []):
            if b.get("type") == "text" and b.get("file") and "text" not in b:
                try:
                    with open(os.path.join(d, b["file"])) as f:
                        b["text"] = f.read()
                except FileNotFoundError:
                    b["text"] = ""
        doc["_hash"] = self.folio_hash(fid)
        return doc

    def folio_hash(self, fid):
        d = self.folio_dir(fid)
        h = hashlib.sha1()
        with open(os.path.join(d, "folio.json"), "rb") as f:
            h.update(f.read())
        for root, _, files in os.walk(os.path.join(d, "text")):
            for fn in sorted(files):
                with open(os.path.join(root, fn), "rb") as f:
                    h.update(fn.encode()); h.update(f.read())
        return h.hexdigest()[:12]

    VERSION_EVERY = 5          # one version per 5 changes (page edits, Claude's edits, accepted suggestions)

    def save_folio(self, fid, doc, why="editor", ops=1, archive_first=False):
        d = self.folio_dir(fid)
        with self.lock:
            vd = os.path.join(self.review_dir(fid), "versions")
            first = not (os.path.isdir(vd) and any(x.endswith("__folio.json") for x in os.listdir(vd)))
            if first or archive_first:            # the starting state, and the state before a restore
                self.archive(fid, "before: " + why if archive_first else "initial state")
            doc = dict(doc)
            doc.pop("_hash", None)
            doc["updated"] = datetime.now().isoformat(timespec="seconds")
            for b in doc.get("blocks", []):
                if b.get("type") == "text" and b.get("file"):
                    fp = os.path.join(d, b["file"])
                    os.makedirs(os.path.dirname(fp), exist_ok=True)
                    with open(fp, "w") as f:
                        f.write(b.get("text", ""))
                    b = b  # text stays in file; strip inline copy below
            out = json.loads(json.dumps(doc))
            for b in out.get("blocks", []):
                if b.get("type") == "text" and b.get("file"):
                    b.pop("text", None)
            tmp = os.path.join(d, "folio.json.tmp")
            with open(tmp, "w") as f:
                json.dump(out, f, indent=1, ensure_ascii=False)
            os.replace(tmp, os.path.join(d, "folio.json"))
            self.folio_mtimes[fid] = self._mtime(fid)
            sp = os.path.join(self.review_dir(fid), "version_state.json")
            try:
                with open(sp) as f:
                    vs = json.load(f)
            except Exception:
                vs = {"ops": 0, "why": []}
            vs["ops"] = vs.get("ops", 0) + max(1, int(ops or 1)); vs["why"] = (vs.get("why", []) + [why])[-12:]
            if vs["ops"] >= self.VERSION_EVERY:
                self.archive(fid, f"{vs['ops']} changes: " + "; ".join(vs["why"])[:300])
                vs = {"ops": 0, "why": []}
            os.makedirs(os.path.dirname(sp), exist_ok=True)
            with open(sp, "w") as f:
                json.dump(vs, f)
            h = self.folio_hash(fid)
            self.broadcast({"type": "folio", "folio": fid, "hash": h, "why": why})
            return h

    def archive(self, fid, why):
        d = self.folio_dir(fid)
        src = os.path.join(d, "folio.json")
        if not os.path.exists(src):
            return
        vd = os.path.join(self.review_dir(fid), "versions")
        os.makedirs(vd, exist_ok=True)
        stamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
        dst = os.path.join(vd, f"{stamp}__folio.json")
        if not os.path.exists(dst):
            shutil.copy2(src, dst)
            with open(os.path.join(vd, "VERSIONS.md"), "a") as f:
                f.write(f"- {stamp}  folio.json  {why}\n")
        # keep the last 200
        files = sorted(x for x in os.listdir(vd) if x.endswith("__folio.json"))
        for old in files[:-200]:
            os.remove(os.path.join(vd, old))

    def _mtime(self, fid):
        d = self.folio_dir(fid)
        m = os.path.getmtime(os.path.join(d, "folio.json"))
        td = os.path.join(d, "text")
        if os.path.isdir(td):
            for fn in os.listdir(td):
                m = max(m, os.path.getmtime(os.path.join(td, fn)))
        sd = os.path.join(d, "folio_review", "suggestions.json")
        if os.path.exists(sd):
            m = max(m, os.path.getmtime(sd))
        return m

    def watch_loop(self):
        while True:
            try:
                for e in self.folios():
                    fid = e["id"]
                    try:
                        m = self._mtime(fid)
                    except FileNotFoundError:
                        continue
                    if fid not in self.folio_mtimes:
                        self.folio_mtimes[fid] = m
                    elif m > self.folio_mtimes[fid] + 1e-6:
                        self.folio_mtimes[fid] = m
                        self.broadcast({"type": "folio", "folio": fid, "hash": self.folio_hash(fid), "why": "external"})
            except Exception as ex:
                self.log(f"watch error {ex}")
            time.sleep(1.0)

    # ---- review state (requests, threads, notes, suggestions)
    def review_json(self, fid, name, default):
        fp = os.path.join(self.review_dir(fid), name)
        try:
            with open(fp) as f:
                return json.load(f)
        except Exception:
            return default

    def save_review_json(self, fid, name, data):
        fp = os.path.join(self.review_dir(fid), name)
        with open(fp + ".tmp", "w") as f:
            json.dump(data, f, indent=1, ensure_ascii=False)
        os.replace(fp + ".tmp", fp)

    def add_request(self, fid, req):
        rid = datetime.now().strftime("%Y%m%d-%H%M%S") + "-" + secrets.token_hex(2)
        req = dict(req)
        req.update({"id": rid, "folio": fid, "time": datetime.now().isoformat(timespec="seconds"), "status": "queued"})
        # attachments
        imgs = req.pop("images", None) or []
        paths = []
        if imgs:
            ad = os.path.join(self.review_dir(fid), "attachments", rid)
            os.makedirs(ad, exist_ok=True)
            for i, im in enumerate(imgs[:8]):
                data = im.get("data", "")
                if "," in data:
                    data = data.split(",", 1)[1]
                raw = base64.b64decode(data)
                ext = None
                for magic, e in IMAGE_MAGIC.items():
                    if raw[:4].startswith(magic[:4]) or raw[:3] == magic[:3]:
                        ext = e
                if not ext or len(raw) > 12 * 1024 * 1024:
                    continue
                fn = f"{i+1:02d}.{ext}"
                with open(os.path.join(ad, fn), "wb") as f:
                    f.write(raw)
                paths.append(os.path.join("attachments", rid, fn))
        if paths:
            req["attachments"] = paths
        # conversation: same anchor → follow earlier requests
        follows = []
        for old in self.inbox(fid):
            if same_anchor(old.get("anchor"), req.get("anchor")):
                follows.append(old["id"])
        if follows:
            req["follows"] = follows
        with self.lock:
            with open(os.path.join(self.review_dir(fid), "inbox.jsonl"), "a") as f:
                f.write(json.dumps(req, ensure_ascii=False) + "\n")
            td = os.path.join(self.review_dir(fid), "threads")
            os.makedirs(td, exist_ok=True)
            with open(os.path.join(td, rid + ".json"), "w") as f:
                json.dump({"id": rid, "request": req, "answers": [], "status": "queued"}, f, indent=1, ensure_ascii=False)
        self.log(f"FOLIO_REQUEST id={rid} folio={fid} type={req.get('type')} block={(req.get('anchor') or {}).get('block')} images={len(paths)} follows={','.join(follows)}")
        self.broadcast({"type": "request", "folio": fid, "id": rid})
        return rid

    def inbox(self, fid):
        fp = os.path.join(self.review_dir(fid), "inbox.jsonl")
        out = []
        if os.path.exists(fp):
            with open(fp) as f:
                for line in f:
                    line = line.strip()
                    if line:
                        try:
                            out.append(json.loads(line))
                        except Exception:
                            pass
        return out

    def threads(self, fid):
        td = os.path.join(self.review_dir(fid), "threads")
        out = []
        if os.path.isdir(td):
            for fn in sorted(os.listdir(td)):
                if fn.endswith(".json"):
                    try:
                        with open(os.path.join(td, fn)) as f:
                            out.append(json.load(f))
                    except Exception:
                        pass
        return out

    def thread_path(self, fid, rid):
        return os.path.join(self.review_dir(fid), "threads", rid + ".json")

    def set_status(self, fid, rid, status):
        fp = self.thread_path(fid, rid)
        with self.lock:
            with open(fp) as f:
                t = json.load(f)
            t["status"] = status
            t["request"]["status"] = status
            with open(fp, "w") as f:
                json.dump(t, f, indent=1, ensure_ascii=False)
        self.broadcast({"type": "thread", "folio": fid, "id": rid, "status": status})

    def answer(self, fid, rid, text, changed=None, note=True):
        fp = self.thread_path(fid, rid)
        with self.lock:
            with open(fp) as f:
                t = json.load(f)
            t["answers"].append({"time": datetime.now().isoformat(timespec="seconds"), "text": text, "changed": changed or []})
            t["status"] = "done"
            t["request"]["status"] = "done"
            with open(fp, "w") as f:
                json.dump(t, f, indent=1, ensure_ascii=False)
            if note:
                notes = self.review_json(fid, "notes.json", [])
                notes = [n for n in notes if n.get("id") != rid]
                notes.append({"id": rid, "block": (t["request"].get("anchor") or {}).get("block"),
                              "quote": (t["request"].get("anchor") or {}).get("quote", ""),
                              "kind": t["request"].get("type"), "request": t["request"].get("text", ""),
                              "answer": text, "time": t["answers"][-1]["time"], "images": t["request"].get("attachments", [])})
                self.save_review_json(fid, "notes.json", notes)
        self.log(f"FOLIO_ANSWER id={rid} folio={fid}")
        self.broadcast({"type": "thread", "folio": fid, "id": rid, "status": "done"})

    # ---- suggestions (Claude proposes; the user accepts in the page)
    def suggestions(self, fid):
        return self.review_json(fid, "suggestions.json", [])

    def add_suggestion(self, fid, s):
        s = dict(s)
        s["id"] = "s" + secrets.token_hex(3)
        s["time"] = datetime.now().isoformat(timespec="seconds")
        s["status"] = "pending"
        with self.lock:
            lst = self.suggestions(fid)
            lst.append(s)
            self.save_review_json(fid, "suggestions.json", lst)
        self.broadcast({"type": "suggestions", "folio": fid})
        return s["id"]

    def resolve_suggestion(self, fid, sid, accept):
        with self.lock:
            lst = self.suggestions(fid)
            s = next((x for x in lst if x["id"] == sid), None)
            if not s:
                return False
            if accept and s["status"] == "pending":
                doc = self.load_folio(fid)
                blocks = {b["id"]: b for b in doc["blocks"]}
                if s.get("op") == "delete":
                    doc["blocks"] = [b for b in doc["blocks"] if b["id"] != s["block"]]
                elif s.get("op") == "add":
                    doc["blocks"].append(s["new"])
                else:
                    b = blocks.get(s["block"])
                    if b is not None:
                        for k, v in (s.get("new") or {}).items():
                            b[k] = v
                        if "text" in (s.get("new") or {}) and "html" not in s["new"]:
                            b.pop("html", None)      # new Markdown text replaces the page's rich text
                self.save_folio(fid, doc, why=f"accepted suggestion {sid}")
            s["status"] = "accepted" if accept else "rejected"
            s["resolved"] = datetime.now().isoformat(timespec="seconds")
            self.save_review_json(fid, "suggestions.json", lst)
        self.log(f"FOLIO_SUGGESTION {s['status']} id={sid} folio={fid}")
        self.broadcast({"type": "suggestions", "folio": fid})
        return True

    # ---- events
    def broadcast(self, ev):
        ev = dict(ev)
        ev["ts"] = time.time()
        data = "data: " + json.dumps(ev) + "\n\n"
        for q in list(self.subscribers):
            try:
                q.append(data)
            except Exception:
                pass

    def log(self, line):
        with open(self.p("server.log"), "a") as f:
            f.write(f"{datetime.now().isoformat(timespec='seconds')} {line}\n")


def same_anchor(a, b):
    if not a or not b:
        return False
    if a.get("type") == "screenshot" or b.get("type") == "screenshot":
        return False
    if a.get("block") != b.get("block") or sorted(a.get("blocks") or []) != sorted(b.get("blocks") or []):
        return False
    qa = re.sub(r"\s+", " ", (a.get("quote") or "")).strip()
    qb = re.sub(r"\s+", " ", (b.get("quote") or "")).strip()
    return qa == qb


# --------------------------------------------------------------------------- rendering helpers (Playwright)

def playwright_available():
    import glob, importlib
    importlib.invalidate_caches()          # see a Playwright installed while the server runs
    try:
        import playwright.sync_api  # noqa
    except Exception:
        return False
    roots = [os.environ["PLAYWRIGHT_BROWSERS_PATH"]] if os.environ.get("PLAYWRIGHT_BROWSERS_PATH") else [
        os.path.expanduser("~/.cache/ms-playwright"), os.path.expanduser("~/Library/Caches/ms-playwright"),
        os.path.join(os.environ.get("LOCALAPPDATA", ""), "ms-playwright")]
    return any(r and glob.glob(os.path.join(r, "chromium*")) for r in roots)


def playwright_setup_state():
    try:
        with open(os.path.join(os.path.expanduser("~"), ".cache", "folio-studio", "playwright_setup.json")) as f:
            return json.load(f).get("state", "")
    except Exception:
        return ""


def render_png(url, clip_px=None, scale=3, size_px=None):
    """Screenshot url (print mode) with Chromium. clip_px in CSS px. Returns PNG bytes."""
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        browser = p.chromium.launch()
        ctx = browser.new_context(device_scale_factor=scale, viewport={"width": max(800, int((size_px or (1200, 900))[0]) + 40), "height": max(600, int((size_px or (1200, 900))[1]) + 40)})
        page = ctx.new_page()
        page.goto(url, wait_until="networkidle")
        page.wait_for_timeout(300)
        kw = {"type": "png"}
        if clip_px:
            kw["clip"] = clip_px
        else:
            kw["full_page"] = True
        data = page.screenshot(**kw)
        browser.close()
        return data


def render_pdf(url, w_mm, h_mm, out_path):
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(url, wait_until="networkidle")
        page.wait_for_timeout(300)
        page.pdf(path=out_path, width=f"{w_mm}mm", height=f"{h_mm}mm", print_background=True, prefer_css_page_size=False, margin={"top": "0", "bottom": "0", "left": "0", "right": "0"}, page_ranges="1")
        browser.close()


# --------------------------------------------------------------------------- HTTP

class Handler(BaseHTTPRequestHandler):
    studio: Studio = None
    server_version = "FolioStudio/0.1"

    def log_message(self, fmt, *args):
        pass

    # ---- helpers
    def _token_ok(self, q):
        t = (q.get("t") or [None])[0] or self.headers.get("X-Folio-Token")
        if not t:
            c = self.headers.get("Cookie", "")
            m = re.search(r"folio_t=([A-Za-z0-9_\-]+)", c)
            t = m.group(1) if m else None
        return secrets.compare_digest(t or "", self.studio.token)

    def _send(self, code, body=b"", ctype="application/json", extra=None):
        if isinstance(body, (dict, list)):
            body = json.dumps(body, ensure_ascii=False).encode()
        elif isinstance(body, str):
            body = body.encode()
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        for k, v in (extra or {}).items():
            self.send_header(k, v)
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(body)

    def _json(self):
        n = int(self.headers.get("Content-Length") or 0)
        if n > MAX_BODY:
            raise ValueError("body too large")
        raw = self.rfile.read(n) if n else b"{}"
        return json.loads(raw or b"{}")

    def _file(self, path, ctype=None):
        if not os.path.isfile(path):
            return self._send(404, {"error": "not found"})
        ctype = ctype or mimetypes.guess_type(path)[0] or "application/octet-stream"
        with open(path, "rb") as f:
            self._send(200, f.read(), ctype)

    def _base_url(self):
        host = self.headers.get("Host") or f"127.0.0.1:{self.server.server_address[1]}"
        return f"http://{host}"

    # ---- routing
    def do_GET(self):
        u = urlparse(self.path)
        q = parse_qs(u.query)
        path = unquote(u.path)
        if not self._token_ok(q):
            return self._send(401, "<h3>Folio Studio: token required. Open the link from the terminal.</h3>", "text/html")
        extra = {}
        if q.get("t"):
            extra["Set-Cookie"] = f"folio_t={self.studio.token}; Path=/; SameSite=Strict"
        st = self.studio
        try:
            if path in ("/", "/index.html"):
                with open(os.path.join(EDITOR_DIR, "index.html"), "rb") as f:
                    return self._send(200, f.read(), "text/html; charset=utf-8", extra)
            if path.startswith("/editor/"):
                return self._file(os.path.join(EDITOR_DIR, os.path.basename(path)))
            if path == "/api/health":
                return self._send(200, {"ok": True, "playwright": playwright_available(), "playwright_setup": playwright_setup_state(), "claude_cli": shutil.which("claude") is not None})
            if path == "/api/folios":
                return self._send(200, st.folios())
            if path == "/api/journals":
                import journal as JN
                return self._send(200, [JN.summary(j) for j in JN.journals(st.root).values()])
            m = re.match(r"^/api/journal/([^/]+)$", path)
            if m:
                import journal as JN
                j = JN.journals(st.root).get(m.group(1))
                return self._send(200, j) if j else self._send(404, {"error": "unknown journal"})
            m = re.match(r"^/api/folio/([^/]+)/check$", path)
            if m:
                import journal as JN
                doc = st.load_folio(m.group(1)); jid = (q.get("journal") or [doc.get("journal")])[0]
                j = JN.journals(st.root).get(jid or "")
                if not j:
                    return self._send(200, {"journal": None, "items": [], "counts": {}, "errors": 0, "warnings": 0})
                return self._send(200, JN.check(doc, j, st.folio_dir(m.group(1))))
            m = re.match(r"^/api/folio/([^/]+)$", path)
            if m:
                return self._send(200, st.load_folio(m.group(1)))
            m = re.match(r"^/api/folio/([^/]+)/review$", path)
            if m:
                fid = m.group(1)
                return self._send(200, {"threads": st.threads(fid), "notes": st.review_json(fid, "notes.json", []), "suggestions": st.suggestions(fid)})
            m = re.match(r"^/api/folio/([^/]+)/versions$", path)
            if m:
                vd = os.path.join(st.review_dir(m.group(1)), "versions")
                files = sorted(os.listdir(vd)) if os.path.isdir(vd) else []
                return self._send(200, [f for f in files if f.endswith(".json")])
            m = re.match(r"^/api/folio/([^/]+)/version/([^/]+)$", path)
            if m:
                return self._file(os.path.join(st.review_dir(m.group(1)), "versions", os.path.basename(m.group(2))), "application/json")
            m = re.match(r"^/assets/([^/]+)/(.+)$", path)
            if m:
                fid, rel = m.group(1), m.group(2)
                base = os.path.realpath(st.folio_dir(fid))
                fp = os.path.realpath(os.path.join(base, rel))
                if not fp.startswith(base + os.sep):
                    return self._send(403, {"error": "forbidden"})
                return self._file(fp)
            m = re.match(r"^/review/([^/]+)/(.+)$", path)
            if m:
                fid, rel = m.group(1), m.group(2)
                base = os.path.realpath(st.review_dir(fid))
                fp = os.path.realpath(os.path.join(base, rel))
                if not fp.startswith(base + os.sep):
                    return self._send(403, {"error": "forbidden"})
                return self._file(fp)
            if path == "/api/events":
                return self._sse(q)
            return self._send(404, {"error": "not found"})
        except KeyError as ex:
            return self._send(404, {"error": f"unknown folio {ex}"})
        except Exception as ex:
            st.log(f"Traceback GET {path}: {ex!r}")
            return self._send(500, {"error": str(ex)})

    def _sse(self, q):
        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream")
        self.send_header("Cache-Control", "no-cache")
        self.end_headers()
        queue = []
        self.studio.subscribers.append(queue)
        try:
            self.wfile.write(b"data: {\"type\":\"hello\"}\n\n"); self.wfile.flush()
            last = time.time()
            while True:
                while queue:
                    self.wfile.write(queue.pop(0).encode()); self.wfile.flush()
                if time.time() - last > 15:
                    self.wfile.write(b": ping\n\n"); self.wfile.flush(); last = time.time()
                time.sleep(0.25)
        except Exception:
            pass
        finally:
            try:
                self.studio.subscribers.remove(queue)
            except ValueError:
                pass

    def do_POST(self):
        u = urlparse(self.path)
        q = parse_qs(u.query)
        path = unquote(u.path)
        if not self._token_ok(q):
            return self._send(401, {"error": "token"})
        st = self.studio
        try:
            m = re.match(r"^/api/folio/([^/]+)$", path)
            if m:   # save whole document from the editor
                fid = m.group(1)
                body = self._json()
                h = st.save_folio(fid, body.get("doc"), why=body.get("why", "editor"), ops=body.get("ops", 1), archive_first=bool(body.get("archive_first")))
                return self._send(200, {"ok": True, "hash": h})
            m = re.match(r"^/api/folio/([^/]+)/upload$", path)
            if m:
                fid = m.group(1)
                body = self._json()
                data = body.get("data", "")
                if "," in data:
                    data = data.split(",", 1)[1]
                raw = base64.b64decode(data)
                ext = None
                for magic, e in IMAGE_MAGIC.items():
                    if raw[:3] == magic[:3] or raw[:4] == magic:
                        ext = e
                if ext is None and raw[:5] == b"%PDF-":
                    ext = "pdf"
                if ext is None and b"<svg" in raw[:2000]:
                    ext = "svg"
                if not ext:
                    return self._send(400, {"error": "unsupported image"})
                name = re.sub(r"[^A-Za-z0-9_.\-]", "_", body.get("name") or "image")
                name = os.path.splitext(name)[0] + "." + ext
                ad = os.path.join(st.folio_dir(fid), "assets")
                os.makedirs(ad, exist_ok=True)
                fp = os.path.join(ad, name)
                i = 1
                while os.path.exists(fp):
                    fp = os.path.join(ad, f"{os.path.splitext(name)[0]}_{i}.{ext}"); i += 1
                with open(fp, "wb") as f:
                    f.write(raw)
                return self._send(200, {"ok": True, "src": "assets/" + os.path.basename(fp)})
            if path == "/api/request":
                body = self._json()
                fid = body.pop("folio")
                rid = st.add_request(fid, body)
                return self._send(200, {"ok": True, "id": rid})
            m = re.match(r"^/api/request/([^/]+)/status$", path)
            if m:
                body = self._json()
                st.set_status(body["folio"], m.group(1), body["status"])
                return self._send(200, {"ok": True})
            if path == "/api/answer":   # used by the Claude CLI helper
                body = self._json()
                st.answer(body["folio"], body["id"], body["text"], body.get("changed"), body.get("note", True))
                return self._send(200, {"ok": True})
            m = re.match(r"^/api/folio/([^/]+)/suggest$", path)
            if m:
                sid = st.add_suggestion(m.group(1), self._json())
                return self._send(200, {"ok": True, "id": sid})
            m = re.match(r"^/api/folio/([^/]+)/suggestion/([^/]+)/(accept|reject)$", path)
            if m:
                ok = st.resolve_suggestion(m.group(1), m.group(2), m.group(3) == "accept")
                return self._send(200 if ok else 404, {"ok": ok})
            m = re.match(r"^/api/folio/([^/]+)/notes/(update|delete)$", path)
            if m:
                fid, action = m.group(1), m.group(2)
                body = self._json()
                notes = st.review_json(fid, "notes.json", [])
                for n in notes:
                    if n["id"] == body["id"]:
                        if action == "delete":
                            n["hidden"] = True
                        else:
                            n.setdefault("history", []).append({"request": n.get("request"), "answer": n.get("answer")})
                            n["request"] = body.get("request", n.get("request"))
                            n["answer"] = body.get("answer", n.get("answer"))
                            n["edited"] = datetime.now().isoformat(timespec="seconds")
                st.save_review_json(fid, "notes.json", notes)
                st.log(f"FOLIO_NOTE {action} {body['id']} {fid}")
                st.broadcast({"type": "notes", "folio": fid})
                return self._send(200, {"ok": True})
            m = re.match(r"^/api/folio/([^/]+)/screenshot$", path)
            if m:
                return self._screenshot(m.group(1), self._json())
            m = re.match(r"^/api/folio/([^/]+)/export$", path)
            if m:
                return self._export(m.group(1), self._json())
            if path == "/api/translate":
                return self._translate(self._json())
            if path == "/api/shutdown":
                st.log("FOLIO_SERVER_STOPPED")
                self._send(200, {"ok": True})
                threading.Thread(target=self.server.shutdown, daemon=True).start()
                return
            return self._send(404, {"error": "not found"})
        except KeyError as ex:
            return self._send(404, {"error": f"unknown {ex}"})
        except Exception as ex:
            import traceback
            st.log("Traceback POST " + path + ": " + traceback.format_exc().replace("\n", " | "))
            return self._send(500, {"error": str(ex)})

    # ---- screenshot: server-side render of a region (mm) in print mode
    def _screenshot(self, fid, body):
        st = self.studio
        region = body.get("region")          # {x,y,w,h} in mm, or None = whole page
        doc = st.load_folio(fid)
        page = doc.get("page", {})
        sd = os.path.join(st.review_dir(fid), "screenshots")
        os.makedirs(sd, exist_ok=True)
        stamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
        fn = f"{stamp}.png"
        out = os.path.join(sd, fn)
        blocks_in = []
        for b in doc.get("blocks", []):
            if not region:
                blocks_in.append(b["id"]); continue
            bx, by, bw, bh = b.get("x", 0), b.get("y", 0), b.get("w", 0), b.get("h", 0)
            if bx < region["x"] + region["w"] and bx + bw > region["x"] and by < region["y"] + region["h"] and by + bh > region["y"]:
                blocks_in.append(b["id"])
        if body.get("data"):                 # client-rendered fallback image
            data = body["data"].split(",", 1)[1] if "," in body["data"] else body["data"]
            with open(out, "wb") as f:
                f.write(base64.b64decode(data))
            src = "client"
        else:
            if not playwright_available():
                return self._send(200, {"ok": False, "error": "playwright-missing", "blocks": blocks_in})
            url = f"{self._base_url()}/?t={st.token}&folio={fid}&print=1"
            PX = 96 / 25.4
            clip = None
            w_mm, h_mm = page.get("w_mm", 180), page.get("h_mm", 120)
            if region:
                clip = {"x": region["x"] * PX, "y": region["y"] * PX, "width": max(1, region["w"] * PX), "height": max(1, region["h"] * PX)}
            data = render_png(url, clip, scale=body.get("scale", 3), size_px=(w_mm * PX, h_mm * PX))
            with open(out, "wb") as f:
                f.write(data)
            src = "server"
        with open(out, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
        rel = os.path.join("screenshots", fn)
        st.log(f"FOLIO_SCREENSHOT folio={fid} file={rel} blocks={','.join(blocks_in)}")
        return self._send(200, {"ok": True, "file": rel, "path": out, "url": f"/review/{fid}/{rel}", "blocks": blocks_in, "region": region, "data": "data:image/png;base64," + b64, "renderer": src})

    def _export(self, fid, body):
        st = self.studio
        doc = st.load_folio(fid)
        page = doc.get("page", {})
        fmt = body.get("format", "pdf")
        od = os.path.join(st.folio_dir(fid), "export")
        os.makedirs(od, exist_ok=True)
        stamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
        if not playwright_available():
            return self._send(200, {"ok": False, "error": "playwright-missing", "setup": playwright_setup_state()})
        url = f"{self._base_url()}/?t={st.token}&folio={fid}&print=1"
        if fmt == "pdf":
            out = os.path.join(od, f"{fid}_{stamp}.pdf")
            render_pdf(url, page.get("w_mm", 180), page.get("h_mm", 120), out)
        else:
            out = os.path.join(od, f"{fid}_{stamp}.png")
            PX = 96 / 25.4
            data = render_png(url, {"x": 0, "y": 0, "width": page.get("w_mm", 180) * PX, "height": page.get("h_mm", 120) * PX}, scale=body.get("scale", 300 / 96), size_px=(page.get("w_mm", 180) * PX, page.get("h_mm", 120) * PX))
            with open(out, "wb") as f:
                f.write(data)
        st.log(f"FOLIO_EXPORT folio={fid} file={out}")
        return self._send(200, {"ok": True, "path": out})

    def _translate(self, body):
        text = (body.get("text") or "")[:4000]
        target = body.get("target", "zh-Hans")
        if not shutil.which("claude"):
            return self._send(200, {"ok": False, "error": "unavailable"})
        prompt = (f"Translate the text between the markers into {target}. Keep gene, protein and TF names, motif IDs, numbers, units, "
                  f"symbols and figure references unchanged. Output only the translation.\n<<<\n{text}\n>>>")
        try:
            r = subprocess.run(["claude", "-p", "--model", "haiku", "--output-format", "text", prompt], capture_output=True, text=True, timeout=60)
            if r.returncode != 0:
                return self._send(200, {"ok": False, "error": (r.stderr or "cli error")[:300]})
            return self._send(200, {"ok": True, "translation": r.stdout.strip()})
        except subprocess.TimeoutExpired:
            return self._send(200, {"ok": False, "error": "timeout"})


# --------------------------------------------------------------------------- main

def free_port(preferred=None):
    if preferred:                       # keep the studio's port across restarts (wait up to 5 s for the old server)
        for _ in range(20):
            with socket.socket() as s:
                s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                try:
                    s.bind(("127.0.0.1", preferred)); return preferred
                except OSError:
                    time.sleep(0.25)
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0)); return s.getsockname()[1]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--studio", required=True)
    ap.add_argument("--port", type=int)
    ap.add_argument("--register", action="append", default=[], help="folio folder to register")
    a = ap.parse_args()
    st = Studio(a.studio)
    for r in a.register:
        st.register(r)
    port = a.port or st.cfg.get("port")
    port = free_port(port)
    st.cfg["port"] = port
    st._save_json("studio.json", st.cfg)
    url = f"http://127.0.0.1:{port}/?t={st.token}"
    with open(st.p("server_url.txt"), "w") as f:
        f.write(url + "\n")
    Handler.studio = st
    httpd = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    httpd.daemon_threads = True
    threading.Thread(target=st.watch_loop, daemon=True).start()
    st.log(f"FOLIO_SERVER_STARTED {url}")
    print(url, flush=True)
    try:
        httpd.serve_forever()
    finally:
        st.log("FOLIO_SERVER_STOPPED")


if __name__ == "__main__":
    main()
