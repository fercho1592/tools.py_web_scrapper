"""Simple script to replace import package name occurrences.

Usage: run from repository root; it will modify `.py` files under `src/`.
"""

import pathlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"


def replace_in_file(path: Path, old: str, new: str) -> bool:
    text = path.read_text(encoding="utf-8")
    if old not in text:
        return False
    new_text = text.replace(old, new)
    path.write_text(new_text, encoding="utf-8")
    return True


def main():
    changed_files = []
    for p in SRC.rglob("*.py"):
        # Skip virtual environments or hidden folders if any
        if "/." in str(p):
            continue
        if replace_in_file(p, "feature_interfaces", "contracts"):
            changed_files.append(p.relative_to(ROOT))

    print(f"Rewrote imports in {len(changed_files)} files")
    for f in changed_files:
        print(f" - {f}")


if __name__ == "__main__":
    main()
