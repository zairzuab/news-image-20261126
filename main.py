#!/usr/bin/env python3
"""news-image-20261126 entrypoint (stdlib only).

Copies the pre-built front page (entry.png, drawn by draw_frontpage.py
with PIL on the author's machine) to $MAKEFUN_OUTPUT_DIR/entry.png.
The grader image has no Pillow, so this file imports nothing beyond
the standard library and never draws anything itself.
"""
import os
import shutil
import sys


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    src = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    if not os.path.isfile(src):
        sys.exit(f"missing source image: {src}")
    dst = os.path.join(out_dir, "entry.png")
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(src, dst)
    print(f"wrote {dst} ({os.path.getsize(dst)} bytes)")


if __name__ == "__main__":
    main()
