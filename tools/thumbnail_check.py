#!/usr/bin/env python3
"""thumbnail_check.py — mechanical validation for a Shorts thumbnail.

What Studio/YouTube actually care about (2026):
- a single, readable subject at Shorts grid scale (checked visually by the gate/boss)
- aspect: YouTube accepts 9:16 (shorts feed) and 16:9 (desktop grid); 16:9 keeps more canvas
- resolution >= 720px short side; file size under YouTube's 2 MB image limit (we target <= 1.5 MB)

Checked here: dimensions/AR/size + simple luminance contrast (std-dev of luminance as a
proxy for readable silhouette). NOT a quality check — hook_B_u65.png passed by eyeball + boss.

Usage: tools/thumbnail_check.py <thumbnail.png>  [exits 0 pass, 2 fail]
Warnings print without failing; failures (missing/corrupt/too small/oversize) fail.
"""
import sys
from pathlib import Path


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    p = Path(sys.argv[1])
    fails, warns = [], []
    if not p.exists():
        print(f"FAIL: not found: {p}")
        return 2
    size_kb = p.stat().st_size / 1024
    if size_kb > 2048:
        fails.append(f"file size {size_kb:.0f} KB exceeds YouTube's 2 MB upload cap")
    elif size_kb > 1500:
        warns.append(f"file size {size_kb:.0f} KB > 1.5 MB; consider re-encode")
    from PIL import Image
    try:
        im = Image.open(p)
        im.verify()
        im = Image.open(p)
    except Exception as e:
        print(f"FAIL: not a decodable image ({e})")
        return 2
    w, h = im.size
    if min(w, h) < 720:
        fails.append(f"too small: {w}x{h} (short side must be >= 720px)")
    ar = w / h
    if ar >= 1.0:
        warns.append(f"16:9-ish AR {ar:.2f} — good for desktop grid; Shorts feed may letterbox")
    elif ar > 0.9:
        warns.append(f"near-square AR {ar:.2f} — Shorts grid effective tile")
    else:
        warns.append(f"vertical AR {ar:.2f} — fine for Shorts feed path (Studio desktop can set it)")
    g = im.convert("L")
    hist = g.histogram()
    n = w * h
    mean = sum(i * c for i, c in enumerate(hist)) / n
    var = sum((i - mean) ** 2 * c for i, c in enumerate(hist)) / n
    std = var ** 0.5
    if std < 40:
        warns.append(f"luminance std {std:.1f} — low contrast; subject may not pop at grid size")
    if fails:
        for f in fails:
            print(f"FAIL: {f}")
        for wrn in warns:
            print(f"warn: {wrn}")
        return 2
    print(f"PASS {w}x{h}  {size_kb:.0f}KB  AR={ar:.2f}  lumStd={std:.1f}")
    for wrn in warns:
        print(f"warn: {wrn}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
