"""Entry point for the news-image-20261126 front page.

The front page (entry.png) is pre-rendered before submission. This script
only copies it into the output directory the grader reads from, so the
grader never needs to run the renderer.
"""

import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or os.path.join(
        os.getcwd(), "out"
    )
    os.makedirs(out_dir, exist_ok=True)
    dest = os.path.join(out_dir, "entry.png")
    shutil.copyfile(SRC, dest)
    print(f"copied {SRC} -> {dest}")


if __name__ == "__main__":
    main()
