#!/usr/bin/env bash
# Start (or reuse) the Folio Studio server for this project and print its link.
# Usage: bash ~/.claude/skills/folio-studio/studio/start_studio.sh [studio_dir]
HERE="$(cd "$(dirname "$0")" && pwd)"
SD="${1:-${FOLIO_STUDIO:-$PWD/.folio}}"
python3 "$HERE/folio.py" --studio "$SD" start
