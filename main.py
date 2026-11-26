"""Entry point for the 'The World Today' front-page render.

Standard library only. It finds render.py next to this file, runs it
in a fresh interpreter, and makes sure the PNG lands where make.fun
expects it:

- MAKEFUN_OUTPUT_DIR set  -> entry.png goes there
- otherwise               -> entry.png goes next to this file

Usage:  python3 main.py
"""

import os
import subprocess
import sys


def script_dir():
    return os.path.dirname(os.path.abspath(__file__))


def output_dir():
    env = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if env:
        return env
    return script_dir()


def main():
    here = script_dir()
    renderer = os.path.join(here, "render.py")
    if not os.path.isfile(renderer):
        print("render.py not found next to main.py", file=sys.stderr)
        return 1
    target = output_dir()
    os.makedirs(target, exist_ok=True)
    env = dict(os.environ)
    env["MAKEFUN_OUTPUT_DIR"] = target
    done = subprocess.run(
        [sys.executable, renderer, target],
        env=env,
        check=False,
    )
    if done.returncode != 0:
        print("render.py failed", file=sys.stderr)
        return done.returncode
    made = os.path.join(target, "entry.png")
    if not os.path.isfile(made):
        print("entry.png was not produced", file=sys.stderr)
        return 1
    print(made)
    return 0


if __name__ == "__main__":
    sys.exit(main())
