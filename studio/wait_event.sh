#!/usr/bin/env bash
# Event-only waiter: exits only when the studio has something for the session to act on.
# Usage: bash wait_event.sh [studio_dir]   (run with Bash run_in_background, no timeout)
SD="${1:-${FOLIO_STUDIO:-$PWD/.folio}}"
LOG="$SD/server.log"
HERE="$(cd "$(dirname "$0")" && pwd)"
touch "$LOG"
START=$(wc -l < "$LOG")
while true; do
  P=$(python3 "$HERE/folio.py" --studio "$SD" pending hook 2>/dev/null)
  if [ -n "$P" ]; then echo "$P"; exit 0; fi
  NEW=$(tail -n +$((START+1)) "$LOG" | grep -E "FOLIO_REQUEST|FOLIO_SUGGESTION|FOLIO_NOTE|FOLIO_SERVER_STOPPED|Traceback" | head -20)
  if [ -n "$NEW" ]; then echo "FOLIO STUDIO EVENT:"; echo "$NEW"; python3 "$HERE/folio.py" --studio "$SD" pending show; exit 0; fi
  if ! python3 - "$SD" <<'PY' 2>/dev/null; then echo "FOLIO_SERVER_STOPPED"; exit 0; fi
import sys,urllib.request
u=open(sys.argv[1]+"/server_url.txt").read().strip().replace("/?t=","/api/health?t=")
urllib.request.urlopen(u,timeout=3)
PY
  sleep 20
done
