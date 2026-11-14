#!/usr/bin/env python3
"""rembg_cutouts.py — proper alpha matting for the C14 asset pilot.

Runs rembg (U2Net) on the raw sticker assets, then post-processes:
- alpha erosion by 1px (kill edge fringe)
- discard tiny islands (<0.4% of opaque area)
Usage: python3 rembg_cutouts.py <in> <out>
"""
import sys

import numpy as np
from PIL import Image, ImageFilter
from rembg import new_session, remove

SESSION = None


def cut(src: str, dst: str) -> None:
    global SESSION
    if SESSION is None:
        SESSION = new_session("u2net")
    im = Image.open(src).convert("RGB")
    out = remove(im, session=SESSION)  # RGBA
    a = np.asarray(out)
    alpha = a[:, :, 3].copy()

    # hard threshold + 1px erode to remove halo fringe
    alpha = np.where(alpha > 140, 255, 0).astype(np.uint8)
    er = Image.fromarray(alpha).filter(ImageFilter.MinFilter(3))
    alpha = np.asarray(er)
    # feather 1px
    al_img = Image.fromarray(alpha).filter(ImageFilter.GaussianBlur(0.7))
    alpha = np.asarray(al_img)

    # drop tiny disconnected islands (keep the main subject mass)
    from scipy import ndimage
    solid = alpha > 128
    lab, n = ndimage.label(solid)
    if n > 1:
        sizes = ndimage.sum(solid, lab, range(1, n + 1))
        keep = {i + 1 for i, s in enumerate(sizes) if s >= 0.004 * solid.sum()}
        mask = np.isin(lab, list(keep))
        alpha = np.where(mask, alpha, 0).astype(np.uint8)

    rgba = np.dstack([a[:, :, :3], alpha])
    Image.fromarray(rgba, "RGBA").save(dst)
    cov = float((alpha > 128).mean())
    print(f"{dst}: opaque coverage {cov:.1%}")
    if cov < 0.08 or cov > 0.85:
        print("  suspicious coverage — inspect", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    cut(sys.argv[1], sys.argv[2])
