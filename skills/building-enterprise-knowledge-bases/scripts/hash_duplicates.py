#!/usr/bin/env python3
"""Find byte-identical duplicate files by SHA-256. Does not delete anything."""
from __future__ import annotations
import argparse
import hashlib
import json
from collections import defaultdict
from pathlib import Path

CHUNK = 1024 * 1024


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        while True:
            b = f.read(CHUNK)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("root")
    p.add_argument("--output", required=True)
    args = p.parse_args()
    root = Path(args.root).expanduser().resolve()
    if not root.is_dir():
        raise SystemExit(f"Root is not a directory: {root}")

    by_size = defaultdict(list)
    for path in root.rglob("*"):
        if path.is_file():
            try:
                by_size[path.stat().st_size].append(path)
            except OSError:
                pass

    groups = []
    for size, paths in by_size.items():
        if len(paths) < 2:
            continue
        by_hash = defaultdict(list)
        for path in paths:
            try:
                by_hash[sha256(path)].append(str(path))
            except OSError:
                pass
        for digest, members in by_hash.items():
            if len(members) > 1:
                groups.append({"sha256": digest, "size_bytes": size, "files": members})

    out = Path(args.output).expanduser()
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({"duplicate_groups": groups}, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Duplicate groups: {len(groups)}; report: {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
