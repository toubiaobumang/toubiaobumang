#!/usr/bin/env python3
"""Create a deterministic file inventory without modifying source files."""
from __future__ import annotations
import argparse
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

SKIP_DIRS = {".git", "node_modules", "__pycache__"}


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("workspace")
    p.add_argument("--output", required=True)
    args = p.parse_args()
    root = Path(args.workspace).expanduser().resolve()
    if not root.is_dir():
        raise SystemExit(f"Workspace is not a directory: {root}")

    files = []
    exts = Counter()
    for path in root.rglob("*"):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if not path.is_file():
            continue
        try:
            st = path.stat()
        except OSError as e:
            files.append({"path": str(path), "error": str(e)})
            continue
        ext = path.suffix.lower() or "[no-extension]"
        exts[ext] += 1
        files.append({
            "path": str(path),
            "relative_path": str(path.relative_to(root)),
            "name": path.name,
            "extension": ext,
            "size_bytes": st.st_size,
            "mtime": datetime.fromtimestamp(st.st_mtime, tz=timezone.utc).isoformat(),
        })

    data = {
        "workspace": str(root),
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "file_count": len(files),
        "extensions": dict(exts.most_common()),
        "files": files,
    }
    out = Path(args.output).expanduser()
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Inventory written: {out} ({len(files)} files)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
