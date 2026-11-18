#!/usr/bin/env python3
"""UserPromptSubmit hook: prints this session's pending Folio Studio requests (nothing when empty).
Install in <project>/.claude/settings.json:
 {"hooks":{"UserPromptSubmit":[{"hooks":[{"type":"command","command":"python3 ~/.claude/skills/folio-studio/studio/folio_hook.py"}]}]}}
"""
import json, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
try:
    inp = json.load(sys.stdin)
except Exception:
    inp = {}
sid = inp.get("session_id")
cwd = inp.get("cwd") or os.getcwd()
sd = os.environ.get("FOLIO_STUDIO") or os.path.join(cwd, ".folio")
if not os.path.isdir(sd):
    sys.exit(0)
try:
    cfg = json.load(open(os.path.join(sd, "studio.json")))
except Exception:
    cfg = {}
if cfg.get("session_id") and sid and cfg["session_id"] != sid:
    sys.exit(0)          # another session owns this studio
out = subprocess.run([sys.executable, os.path.join(HERE, "folio.py"), "--studio", sd, "pending", "hook"], capture_output=True, text=True).stdout
if out.strip():
    print(out)
