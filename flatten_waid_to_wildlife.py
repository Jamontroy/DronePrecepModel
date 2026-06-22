"""
flatten_waid_to_wildlife.py
---------------------------
WAID ships labels with 6 class IDs (0-5: sheep, cattle, seal, camel, kiang,
zebra). This rewrites the first column of every YOLO label file to 0, so the
dataset becomes a single class (0 = wildlife) that matches wildlife.yaml.

Why this is needed: an Ultralytics data.yaml does not remap labels. If the YAML
says nc=1 but a label file still references class 5, training errors out. The
merge has to happen in the label files themselves — that's this script.

This edits label files IN PLACE. Keep the original WAID download/zip so you can
revert if needed. Running it more than once is harmless (0 stays 0).

Usage:
    python flatten_waid_to_wildlife.py /path/to/WAID/WAID
"""

import sys
from pathlib import Path


def flatten(root: str):
    root = Path(root)
    if not root.exists():
        sys.exit(f"Path does not exist: {root}")

    # Every .txt that lives inside a folder named 'labels' (covers train/val/test).
    label_files = [f for f in root.rglob("*.txt") if "labels" in f.parts]
    if not label_files:
        sys.exit(f"No label .txt files found under a 'labels' folder in {root}. "
                 "Check the path / dataset structure.")

    boxes = 0
    for f in label_files:
        out = []
        for line in f.read_text().splitlines():
            line = line.strip()
            if not line:
                continue
            parts = line.split()
            parts[0] = "0"            # force class id -> 0 (wildlife)
            out.append(" ".join(parts))
            boxes += 1
        f.write_text("\n".join(out) + ("\n" if out else ""))

    print(f"Flattened {len(label_files)} label files "
          f"({boxes} boxes) to single class 0 = wildlife.")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Usage: python flatten_waid_to_wildlife.py /path/to/WAID/WAID")
    flatten(sys.argv[1])
