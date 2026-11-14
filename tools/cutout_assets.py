#!/usr/bin/env python3
"""cutout_assets.py — C14 asset-layer pilot: raw sticker PNG -> transparent layer.

Flood-fill from the image borders: any pixel reachable from an edge whose
color is within TOL of that edge's reference color becomes transparent
(model 'solid flat navy' backgrounds are near-uniform, so border-referenced
flood fill is robust). Feather = 1px alpha ramp via distance-to-edge blur.

Usage: python3 cutout_assets.py <in.png> <out.png> [--tol 34] [--ref R,G,B]
Prints alpha coverage stats; exits 1 if cutout looks degenerate.
"""
import sys
from collections import deque

import numpy as np
from PIL import Image

TOL = 34


def cutout(src: str, dst: str, tol: int = TOL, ref=None) -> None:
    im = Image.open(src).convert("RGB")
    a = np.asarray(im).astype(np.float32)
    h, w, _ = a.shape

    if ref is None:
        # reference = median of the border ring (8px)
        ring = np.concatenate([
            a[:8].reshape(-1, 3), a[-8:].reshape(-1, 3),
            a[:, :8].reshape(-1, 3), a[:, -8:].reshape(-1, 3)])
        ref = np.median(ring, axis=0)
    ref = np.asarray(ref, dtype=np.int16)

    dist = np.sqrt(((a - ref) ** 2).sum(axis=2))
    bgish = dist <= tol

    # BFS from every border pixel that is bgish
    reach = np.zeros((h, w), dtype=bool)
    dq = deque()
    for x in range(w):
        for y in (0, h - 1):
            if bgish[y, x] and not reach[y, x]:
                reach[y, x] = True
                dq.append((y, x))
    for y in range(h):
        for x in (0, w - 1):
            if bgish[y, x] and not reach[y, x]:
                reach[y, x] = True
                dq.append((y, x))
    while dq:
        y, x = dq.popleft()
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            ny, nx = y + dy, x + dx
            if 0 <= ny < h and 0 <= nx < w and bgish[ny, nx] and not reach[ny, nx]:
                reach[ny, nx] = True
                dq.append((ny, nx))

    # soft band: pixels just outside tol (dist in [tol, tol+22]) and reachable-
    # adjacent get partial alpha, so the cutout edge is not jaggied
    soft = (dist > tol) & (dist <= tol + 22)
    soft_neighbour = np.zeros_like(soft)
    soft_neighbour[1:, :] |= reach[:-1, :]
    soft_neighbour[:-1, :] |= reach[1:, :]
    soft_neighbour[:, 1:] |= reach[:, :-1]
    soft_neighbour[:, :-1] |= reach[:, 1:]
    partial = soft & soft_neighbour

    alpha = np.where(reach, 0, 255).astype(np.uint8)
    alpha[partial] = 110
    # erode-partial cleanup: any partial pixel with >=3 opaque neighbours -> opaque
    op = (alpha > 200)
    n_op = (
        op[1:, :] .astype(np.uint8) * 0  # placeholder to keep shapes aligned
    )
    from scipy import ndimage as _nd  # light use only
    op_n = sum(np.roll(np.roll(op, sh, axis=ax), 0, axis=ax)
               for sh, ax in ((1, 0), (-1, 0), (0, 1), (0, -1)))
    alpha[partial & (op_n >= 3)] = 255

    out = Image.fromarray(np.dstack([
        np.asarray(im), alpha]))
    # gentle 1px blur on alpha only (feather)
    al = out.getchannel("A").filter(__import__("PIL.ImageFilter", fromlist=["GaussianBlur"]).GaussianBlur(0.8))
    out.putalpha(al)
    out.save(dst)

    cov = float((alpha > 128).mean())
    print(f"{dst}: opaque coverage {cov:.1%}  size {out.size}")
    if cov < 0.12 or cov > 0.97:
        print("  DEGENERATE cutout — adjust --tol/--ref", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    args = sys.argv[1:]
    tol = TOL
    ref = None
    if "--tol" in args:
        i = args.index("--tol"); tol = int(args[i + 1]); del args[i:i + 2]
    if "--ref" in args:
        i = args.index("--ref")
        ref = [int(v) for v in args[i + 1].split(",")]; del args[i:i + 2]
    cutout(args[0], args[1], tol, ref)
