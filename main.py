#!/usr/bin/env python3
"""news-image-20261126 entry point.

Renders the front page with render.py (Pillow) and writes entry.png into
the output directory. Standard library only in this file; deterministic:
running it twice produces a byte-identical entry.png.

Usage:  MAKEFUN_OUTPUT_DIR=out python3 main.py
        (falls back to ./out when the variable is unset)
"""

import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or os.path.join(
        os.getcwd(), "out")
    os.makedirs(out_dir, exist_ok=True)
    tmp_path = os.path.join(out_dir, ".entry.tmp.png")
    final_path = os.path.join(out_dir, "entry.png")
    subprocess.run(
        [sys.executable, os.path.join(HERE, "render.py"), tmp_path],
        check=True,
    )
    shutil.move(tmp_path, final_path)
    print("wrote", final_path)


if __name__ == "__main__":
    main()
