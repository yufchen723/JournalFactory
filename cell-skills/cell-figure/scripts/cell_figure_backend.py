#!/usr/bin/env python3
"""Remember the plotting backend (python or r) for Cell figures.

    cell_figure_backend.py get          -> prints python, r, or nothing
    cell_figure_backend.py set r
    cell_figure_backend.py clear
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

CONFIG = Path(os.environ.get("CELL_FIGURE_CONFIG", "~/.config/journal-factory/cell-figure.json")).expanduser()


def main(argv: list[str]) -> int:
    cmd = argv[1] if len(argv) > 1 else "get"
    data = {}
    if CONFIG.is_file():
        try:
            data = json.loads(CONFIG.read_text())
        except ValueError:
            data = {}
    if cmd == "get":
        print(data.get("backend", ""))
        return 0
    if cmd == "set" and len(argv) > 2 and argv[2].lower() in ("python", "r"):
        data["backend"] = argv[2].lower()
        CONFIG.parent.mkdir(parents=True, exist_ok=True)
        CONFIG.write_text(json.dumps(data))
        print(data["backend"])
        return 0
    if cmd == "clear":
        data.pop("backend", None)
        if CONFIG.is_file():
            CONFIG.write_text(json.dumps(data))
        return 0
    print(__doc__, file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
