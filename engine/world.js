/* ============================================================
   visuals v2 — world.js
   The world, not the animation: a night street set in one-point
   perspective with 25+ designed objects, light from a visible
   lamp, LightVeil pools, dust in the beam. Plus reusable room
   primitives (one-point perspective box) for future sets.
   ============================================================ */

/* one-point perspective room: point (u across, v down, w toward camera) */
V2.makeRoom = (vp, back, S) => {
  S = S || 3.4;
  const s = (w) => 1 / V2.lerp(1, 1 / S, w);
  const P = (u, v, w) => {
    const k = s(w);
    return { x: vp.x + (V2.lerp(back.x0, back.x1, u) - vp.x) * k, y: vp.y + (V2.lerp(back.y0, back.y1, v) - vp.y) * k };
  };
  const Q = (a) => a.map(([u, v, w]) => P(u, v, w)).map((p) => `${p.x.toFixed(1)},${p.y.toFixed(1)}`).join(" ");
  return { vp, back, s, P, Q };
};

/* a box in the room, drawn face by face, lighter on top, darker at sides */
V2.box = (r, u, v, w, front, top, side, rim, parent) => {
  const bx = (uu) => V2.lerp(r.back.x0, r.back.x1, uu);
  const by = (vv) => V2.lerp(r.back.y0, r.back.y1, vv);
  const g = V2.el("g", {}, parent);
  if (by(v[0]) > r.vp.y) V2.el("polygon", { points: r.Q([[u[0], v[0], w[0]], [u[1], v[0], w[0]], [u[1], v[0], w[1]], [u[0], v[0], w[1]]]), fill: top || front }, g);
  if (by(v[1]) < r.vp.y) V2.el("polygon", { points: r.Q([[u[0], v[1], w[0]], [u[1], v[1], w[0]], [u[1], v[1], w[1]], [u[0], v[1], w[1]]]), fill: side || front }, g);
  if (bx(u[0]) > r.vp.x) V2.el("polygon", { points: r.Q([[u[0], v[0], w[0]], [u[0], v[0], w[1]], [u[0], v[1], w[1]], [u[0], v[1], w[0]]]), fill: side || front }, g);
  if (bx(u[1]) < r.vp.x) V2.el("polygon", { points: r.Q([[u[1], v[0], w[0]], [u[1], v[0], w[1]], [u[1], v[1], w[1]], [u[1], v[1], w[0]]]), fill: side || front }, g);
  V2.el("polygon", { points: r.Q([[u[0], v[0], w[1]], [u[1], v[0], w[1]], [u[1], v[1], w[1]], [u[0], v[1], w[1]]]), fill: front }, g);
  if (rim) {
    const a = r.P(u[0], v[0], w[1]), b = r.P(u[1], v[0], w[1]);
    V2.el("path", { d: `M ${a.x} ${a.y} L ${b.x} ${b.y}`, stroke: V2.P.amber, "stroke-width": 2.5, opacity: 0.55 }, g);
  }
  return g;
};

/* ---------- the night street (hook + s0 + s7) ----------
   A full set: road converging up-frame, sidewalks, five buildings
   with lit windows, shopfronts, streetlamp with cone + glow,
   moon + stars, crosswalk, bin, hydrant, sign, mailbox. Returns
   the lamp light [x, y, r] for the veil. */
V2.streetNight = (t, seed, opts, parent) => {
  const o = opts || {};
  const g = V2.el("g", {}, parent);
  const HORIZON = o.horizon || 780;
  /* sky: deep navy gradient + stars + moon */
  const defs = V2.el("defs", {}, g);
  const sky = V2.el("linearGradient", { id: "streetSky", x1: 0, y1: 0, x2: 0, y2: 1 }, defs);
  V2.el("stop", { offset: "0%", "stop-color": "#05070F" }, sky);
  V2.el("stop", { offset: "70%", "stop-color": "#0B1026" }, sky);
  V2.el("stop", { offset: "100%", "stop-color": "#1A1F42" }, sky);
  V2.el("rect", { x: 0, y: 0, width: 1080, height: HORIZON, fill: "url(#streetSky)" }, g);
  V2.stars(t, seed, { x: 0, y: 0, w: 1080, h: HORIZON - 200 }, 46, 0.7, g);
  /* moon + bloom */
  const mx = o.moonX || 880, my = 200;
  V2.glow(mx, my, 190, "Cool", 0.5, g);
  V2.el("circle", { cx: mx, cy: my, r: 52, fill: "#F1F3FF" }, g);
  V2.el("path", { d: `M ${mx + 8} ${my - 52} A 52 52 0 0 1 ${mx + 8} ${my + 52} A 42 52 0 0 0 ${mx + 8} ${my - 52} Z`, fill: "#C6CEEC", opacity: 0.5 }, g);
  V2.el("circle", { cx: mx - 16, cy: my - 12, r: 9, fill: "#C6CEEC", opacity: 0.6 }, g);
  V2.el("circle", { cx: mx + 14, cy: my + 20, r: 6, fill: "#C6CEEC", opacity: 0.5 }, g);
  /* far skyline strip */
  for (let i = 0; i < 9; i++) {
    const bw = 60 + V2.rnd(seed + 9, i) * 90;
    const bh = 60 + V2.rnd(seed + 10, i) * 130;
    const bx = -30 + i * 128;
    V2.el("rect", { x: bx, y: HORIZON - bh - 60, width: bw, height: bh + 60, fill: "#12142E" }, g);
    for (let k = 0; k < 3; k++)
      if (V2.rnd(seed + 11, i * 5 + k) > 0.6)
        V2.el("rect", { x: bx + 8 + k * 14, y: HORIZON - bh - 44 + k * 22, width: 7, height: 9, fill: "#FFC27A", opacity: 0.8 }, g);
  }
  /* road (one-point perspective, converging up) */
  V2.el("rect", { x: 0, y: HORIZON, width: 1080, height: 1920 - HORIZON, fill: "#141726" }, g);
  V2.el("polygon", { points: `430,${HORIZON} 650,${HORIZON} 1080,1920 0,1920`, fill: "#1B2033" }, g);
  /* center dashes shrinking with depth */
  for (let i = 0; i < 9; i++) {
    const u = i / 9, y = HORIZON + 60 + Math.pow(u, 1.7) * (1920 - HORIZON - 80);
    const w = 4 + u * 26, h = 10 + u * 46;
    V2.el("rect", { x: 540 - w / 2, y, width: w, height: h, rx: w / 2, fill: "#C9CFE4", opacity: 0.28 + u * 0.3 }, g);
  }
  /* curbs */
  V2.el("polygon", { points: `0,${HORIZON + 8} 430,${HORIZON} 0,1920`, fill: "#232841" }, g);
  V2.el("polygon", { points: `650,${HORIZON} 1080,${HORIZON + 8} 1080,1920`, fill: "#232841" }, g);
  /* buildings, left and right, perspective-biased toward the middle */
  const building = (x, wdt, topY, baseY, wall, side, seedo, windows) => {
    V2.el("rect", { x, y: topY, width: wdt, height: baseY - topY, fill: wall }, g);
    V2.el("rect", { x: x + wdt - 14, y: topY, width: 14, height: baseY - topY, fill: side }, g);
    for (let r2 = 0; r2 < windows; r2++) {
      for (let c = 0; c < Math.max(2, Math.floor(wdt / 90)); c++) {
        const wx = x + 18 + c * (wdt - 40) / Math.max(2, Math.floor(wdt / 90));
        const wy = topY + 34 + r2 * ((baseY - topY - 60) / windows);
        const lit = V2.rnd(seedo, r2 * 7 + c) > 0.42;
        V2.el("rect", { x: wx, y: wy, width: 44, height: 54, rx: 4, fill: lit ? "#FFC27A" : "#1A2140", opacity: lit ? 0.85 : 0.9 }, g);
        if (lit) V2.el("rect", { x: wx + 8, y: wy + 12, width: 12, height: 30, fill: "#FFE2B0", opacity: 0.5 }, g);
      }
    }
  };
  building(0, 300, 330, HORIZON + 40, "#1E2140", "#151731", seed + 21, 4);
  building(310, 210, 480, HORIZON + 20, "#262A4C", "#1B1E3A", seed + 22, 3);
  building(740, 340, 380, HORIZON + 46, "#22264A", "#181B36", seed + 23, 4);
  /* shopfront with awning (right) */
  V2.el("rect", { x: 560, y: 640, width: 170, height: HORIZON - 620, fill: "#1B1E3A" }, g);
  V2.el("polygon", { points: "548,640 742,640 726,596 564,596", fill: "#C2447E" }, g);
  V2.el("polygon", { points: "548,640 742,640 738,628 552,628", fill: "#9E3370" }, g);
  V2.el("rect", { x: 584, y: 668, width: 120, height: 90, rx: 6, fill: "#FFE2B0", opacity: 0.92 }, g);
  const openTxt = V2.el("text", { x: 644, y: 722, "text-anchor": "middle", "font-family": "Fragment Mono, monospace", "font-size": 26, fill: "#3A2470" }, g);
  openTxt.textContent = "OPEN";
  /* mailbox + bin (left sidewalk) */
  V2.el("rect", { x: 60, y: 1005, width: 74, height: 96, rx: 10, fill: "#2E4A8A" }, g);
  V2.el("rect", { x: 60, y: 995, width: 74, height: 22, rx: 10, fill: "#24407A" }, g);
  V2.el("rect", { x: 88, y: 1030, width: 20, height: 8, rx: 4, fill: "#16224A" }, g);
  V2.el("ellipse", { cx: 97, cy: 1104, rx: 44, ry: 9, fill: "#000", opacity: 0.35 }, g);
  V2.el("rect", { x: 190, y: 1040, width: 62, height: 72, rx: 8, fill: "#2A5A46" }, g);
  V2.el("rect", { x: 190, y: 1030, width: 62, height: 16, rx: 8, fill: "#1F4636" }, g);
  V2.el("ellipse", { cx: 221, cy: 1116, rx: 38, ry: 8, fill: "#000", opacity: 0.35 }, g);
  /* hydrant (right sidewalk) */
  V2.el("rect", { x: 940, y: 1060, width: 40, height: 62, rx: 12, fill: "#C0392B" }, g);
  V2.el("circle", { cx: 960, cy: 1056, r: 16, fill: "#A93226" }, g);
  V2.el("rect", { x: 928, y: 1080, width: 64, height: 12, rx: 6, fill: "#A93226" }, g);
  V2.el("ellipse", { cx: 960, cy: 1126, rx: 34, ry: 8, fill: "#000", opacity: 0.35 }, g);
  /* street lamp: pole, head, cone, glow — THE light source */
  const LX = o.lampX === undefined ? 300 : o.lampX, LGY = o.lampY || 1180, LS = o.lampScale || 1;
  const lampTopY = LGY - 460 * LS;
  V2.glow(LX, lampTopY + 14, 240 * LS, "Warm", 0.62, g);
  V2.el("path", { d: `M ${LX - 8 * LS} ${LGY} L ${LX - 4 * LS} ${lampTopY + 40 * LS}`, stroke: "#10122A", "stroke-width": 15 * LS, "stroke-linecap": "round" }, g);
  V2.el("path", { d: `M ${LX - 4 * LS} ${lampTopY + 40 * LS} Q ${LX} ${lampTopY} ${LX + 62 * LS} ${lampTopY + 12 * LS}`, stroke: "#10122A", "stroke-width": 11 * LS, "stroke-linecap": "round", fill: "none" }, g);
  V2.el("path", { d: `M ${LX + 40 * LS} ${lampTopY + 10 * LS} L ${LX + 104 * LS} ${lampTopY + 10 * LS} L ${LX + 96 * LS} ${lampTopY + 30 * LS} L ${LX + 48 * LS} ${lampTopY + 30 * LS} Z`, fill: "#1A1D36" }, g);
  V2.el("ellipse", { cx: LX + 72 * LS, cy: lampTopY + 32 * LS, rx: 26 * LS, ry: 7 * LS, fill: "#FFE2B0" }, g);
  const headX = LX + 72 * LS, headY = lampTopY + 34 * LS;
  V2.el("path", { d: `M ${headX - 46 * LS} ${headY} L ${headX + 46 * LS} ${headY} L ${headX + 190 * LS} ${headY + 560 * LS} L ${headX - 190 * LS} ${headY + 560 * LS} Z`,
    fill: "url(#vCone)", opacity: 0.42, style: "mix-blend-mode:screen" }, g);
  /* the lamp's pool on the ground */
  V2.el("ellipse", { cx: headX, cy: LGY + 8, rx: 190 * LS, ry: 36 * LS, fill: "#FFD7A0", opacity: 0.14, style: "mix-blend-mode:screen" }, g);
  V2.el("ellipse", { cx: LX - 2, cy: LGY + 4, rx: 40 * LS, ry: 9 * LS, fill: "#000", opacity: 0.4 }, g);
  /* dust in the beam */
  V2.dust(t, seed + 31, { x: headX - 150, y: headY, w: 300, h: 480 }, 16, 0.5, g);
  return { lampLight: [headX, headY + 60, 380], headX, headY, LGY };
};

/* blurred dark foreground shape for depth (over-the-shoulder / frame edge) */
V2.foreground = (draw, blur, parent) => {
  const g = V2.el("g", { filter: `url(#vBlur${blur || 10})` }, parent);
  draw(g);
  return g;
};

/* a window onto the night sky (for interiors, future sets) */
V2.nightWindow = (x0, y0, w, h, t, seed, parent) => {
  const g = V2.el("g", {}, parent);
  V2.el("rect", { x: x0, y: y0, width: w, height: h, fill: "#0B1026" }, g);
  V2.stars(t, seed, { x: x0, y: y0, w, h: h * 0.8 }, Math.round((w * h) / 9000), 0.8, g);
  const mx = x0 + w * 0.72, my = y0 + h * 0.3;
  V2.glow(mx, my, w * 0.5, "Cool", 0.4, g);
  V2.el("circle", { cx: mx, cy: my, r: Math.min(w, h) * 0.16, fill: "#F1F3FF" }, g);
  for (let i = 0; i < 6; i++) {
    const bw = 14 + V2.rnd(seed, i) * 30, bh = 20 + V2.rnd(seed + 1, i) * (h * 0.25);
    V2.el("rect", { x: x0 + 6 + i * (w / 6), y: y0 + h - bh, width: bw, height: bh, fill: "#141634" }, g);
    if (V2.rnd(seed + 2, i) > 0.6)
      V2.el("rect", { x: x0 + 10 + i * (w / 6), y: y0 + h - bh + 8, width: 4, height: 5, fill: "#FFC27A", opacity: 0.85 }, g);
  }
  /* frame + mullions */
  V2.el("rect", { x: x0 - 10, y: y0 - 10, width: w + 20, height: 12, fill: "#1E1824" }, g);
  V2.el("rect", { x: x0 - 10, y: y0 + h - 2, width: w + 20, height: 10, fill: "#1E1824" }, g);
  V2.el("rect", { x: x0 - 10, y: y0 - 10, width: 12, height: h + 20, fill: "#1E1824" }, g);
  V2.el("rect", { x: x0 + w - 2, y: y0 - 10, width: 12, height: h + 20, fill: "#1E1824" }, g);
  V2.el("rect", { x: x0 + w / 2 - 4, y: y0, width: 8, height: h, fill: "#1E1824" }, g);
  return g;
};
