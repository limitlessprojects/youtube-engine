/* ============================================================
   visuals v2 — space.js
   Kurzgesagt-grade space primitives: chunky broken rings,
   glowing cores, nebula depth layers, two-tone planets.
   Every function is a pure function of t (seeded scatter).
   ============================================================ */

/* twinkling starfield over a box */
V2.stars = (t, seed, box, n, o, parent) => {
  for (let i = 0; i < (n || 60); i++) {
    const x = box.x + V2.rnd(seed, i) * box.w;
    const y = box.y + V2.rnd(seed + 1, i) * box.h;
    const tw = 0.55 + 0.45 * Math.sin(t / (7 + V2.rnd(seed + 3, i) * 9) + i * 2.1);
    V2.el("circle", { cx: x, cy: y, r: 1 + V2.rnd(seed + 2, i) * 2.1, fill: "#EAF0FF", opacity: (o || 0.8) * tw }, parent);
  }
};

/* 4-point sparkle that blooms and fades over ~18 frames from t0 */
V2.sparkle = (x, y, t0, s, color, parent) => {
  const u = V2.clamp01(t0 / 18);
  if (u <= 0 || u >= 1) return;
  const sc = (0.4 + 0.9 * Math.sin(u * Math.PI)) * (s || 1);
  const c = color || "#FFE7B3";
  const g = V2.el("g", { transform: `translate(${x} ${y}) scale(${sc})`, opacity: 1 - u * 0.55 }, parent);
  V2.el("path", { d: "M 0 -26 Q 3 -3 26 0 Q 3 3 0 26 Q -3 3 -26 0 Q -3 -3 0 -26 Z", fill: c }, g);
  V2.el("circle", { cx: 0, cy: 0, r: 4.5, fill: "#FFFFFF" }, g);
};

/* one soft nebula blob (unique gradient per blob) */
V2.nebula = (x, y, rx, ry, color, op, rot, parent) => {
  const id = V2.uid("nb");
  const defs = V2.el("defs", {}, parent);
  const g = V2.el("radialGradient", { id }, defs);
  V2.el("stop", { offset: "0%", "stop-color": color, "stop-opacity": op }, g);
  V2.el("stop", { offset: "62%", "stop-color": color, "stop-opacity": op * 0.45 }, g);
  V2.el("stop", { offset: "100%", "stop-color": color, "stop-opacity": 0 }, g);
  V2.el("ellipse", { cx: x, cy: y, rx, ry, fill: `url(#${id})`, transform: rot ? `rotate(${rot} ${x} ${y})` : undefined }, parent);
};

/* layered nebula field + starfield: the depth backdrop */
V2.nebulaField = (t, seed, parent, strength) => {
  const S = strength === undefined ? 1 : strength;
  V2.nebula(140, 330, 420, 260, V2.P.nebPurple2, 0.5 * S, -14, parent);
  V2.nebula(950, 470, 380, 300, V2.P.nebMagenta, 0.20 * S, 12, parent);
  V2.nebula(560, 1500, 520, 300, V2.P.nebPurple, 0.28 * S, 0, parent);
  V2.nebula(1010, 1290, 330, 230, V2.P.nebPurple2, 0.42 * S, 20, parent);
  V2.stars(t, seed, { x: 0, y: 0, w: 1080, h: 1920 }, 70, 0.85, parent);
  V2.sparkle(170, 560, (t + 5) % 90, 1.1, "#BFD4FF", parent);
  V2.sparkle(920, 1180, (t + 42) % 110, 0.9, "#FFD9C4", parent);
  V2.sparkle(240, 1500, (t + 70) % 130, 0.8, "#BFD4FF", parent);
};

/* horizontal speed streaks (motion in space) */
V2.speedLines = (t, seed, y0, y1, n, color, parent) => {
  for (let i = 0; i < n; i++) {
    const y = y0 + V2.rnd(seed, i) * (y1 - y0);
    const len = 60 + V2.rnd(seed + 1, i) * 150;
    const x = ((V2.rnd(seed + 2, i) * 1300 - t * (2 + V2.rnd(seed + 3, i) * 3)) % 1300 + 1300) % 1300 - 110;
    V2.el("line", { x1: x, y1: y, x2: x + len, y2: y, stroke: color || "#4AA8FF",
      "stroke-width": 4 + V2.rnd(seed + 4, i) * 4, "stroke-linecap": "round",
      opacity: 0.16 + V2.rnd(seed + 5, i) * 0.22 }, parent);
  }
};

/* chunky broken orbit ring: concentric arcs, round caps, alternating accents */
V2.orbitRings = (cx, cy, rx, ry, rot, t, opts, parent) => {
  const o = opts || {};
  const cols = o.colors || [V2.P.teal, V2.P.blue, V2.P.nebPurple];
  const rings = o.n || 4;
  const g = V2.el("g", { transform: `rotate(${rot || 0} ${cx} ${cy})` }, parent);
  for (let k = 0; k < rings; k++) {
    const f = 1 - k * (0.21 + 0.03 * (k % 2));
    const w = (o.w || 15) * (1 - k * 0.14);
    const col = cols[k % cols.length];
    const segs = o.segs || 3;
    for (let s = 0; s < segs; s++) {
      const a0 = ((s * 360) / segs + V2.rnd(seed0(k, s), 3) * 30 + (o.spin ? t * (o.spin * (1 - k * 0.15)) : 0)) % 360;
      const a1 = a0 + 300 / segs * (0.75 + V2.rnd(seed0(k, s + 9), 5) * 0.3);
      const large = a1 - a0 > 180 ? 1 : 0;
      const p0 = pol(cx, cy, rx * f, ry * f, a0);
      const p1 = pol(cx, cy, rx * f, ry * f, a1);
      V2.el("path", { d: `M ${p0.x} ${p0.y} A ${rx * f} ${ry * f} 0 ${large} 1 ${p1.x} ${p1.y}`,
        fill: "none", stroke: col, "stroke-width": w, "stroke-linecap": "round",
        opacity: o.opacity === undefined ? 0.92 : o.opacity }, g);
    }
  }
  function seed0(a, b) { return (o.seed || 5) * 7 + a * 13 + b * 3; }
  function pol(cx, cy, rx, ry, deg) {
    const a = (deg * Math.PI) / 180;
    return { x: cx + Math.cos(a) * rx, y: cy + Math.sin(a) * ry };
  }
};

/* a point on a broken ring (for placing satellites) */
V2.onOrbit = (cx, cy, rx, ry, rot, f, deg) => {
  const a = (deg * Math.PI) / 180;
  const x = cx + Math.cos(a) * rx * f, y = cy + Math.sin(a) * ry * f;
  const c = Math.cos(((rot || 0) * Math.PI) / 180), s = Math.sin(((rot || 0) * Math.PI) / 180);
  return { x: cx + (x - cx) * c - (y - cy) * s, y: cy + (x - cx) * s + (y - cy) * c };
};

/* THE black hole: glowing accretion arcs + photon ring + true-black core + optional jets */
V2.blackHole = (cx, cy, r, t, opts, parent) => {
  const o = opts || {};
  const g = V2.el("g", {}, parent);
  const pulse = 1 + Math.sin(t / 6) * 0.06;
  /* outer halo */
  V2.glow(cx, cy, r * 4.4 * pulse, o.kind || "Warm", o.halo === undefined ? 0.5 : o.halo, g);
  /* accretion disc: chunky broken arcs, two tones, slowly revolving */
  const arc = (f, w, col, a0, a1, op) => {
    const p0 = { x: cx + Math.cos(a0) * r * f * 2.05, y: cy + Math.sin(a0) * r * f * 1.15 };
    const p1 = { x: cx + Math.cos(a1) * r * f * 2.05, y: cy + Math.sin(a1) * r * f * 1.15 };
    V2.el("path", { d: `M ${p0.x} ${p0.y} A ${r * f * 2.05} ${r * f * 1.15} 0 ${a1 - a0 > Math.PI ? 1 : 0} 1 ${p1.x} ${p1.y}`,
      fill: "none", stroke: col, "stroke-width": w, "stroke-linecap": "round", opacity: op }, g);
  };
  const spin = t * 0.9;
  const cols = o.disc || [V2.P.amber, V2.P.orange];
  for (let k = 0; k < 2; k++) {
    const f = 1.15 - k * 0.22;
    arc(f, r * 0.30, cols[k % cols.length], spin * (1 - k * 0.2), spin * (1 - k * 0.2) + 2.1, 0.95 - k * 0.15);
    arc(f, r * 0.30, cols[(k + 1) % cols.length], spin * (1 - k * 0.2) + 2.9, spin * (1 - k * 0.2) + 4.6, 0.8 - k * 0.15);
    arc(f, r * 0.22, cols[(k + 2) % cols.length], spin * (1 - k * 0.2) + 5.2, spin * (1 - k * 0.2) + 6.0, 0.6 - k * 0.12);
  }
  /* polar jets */
  if (o.jets) {
    [-1, 1].forEach((s) => V2.el("path", { d: `M ${cx - r * 0.16} ${cy} L ${cx + r * 0.16} ${cy} L ${cx + r * 0.42} ${cy + s * r * 6} L ${cx - r * 0.42} ${cy + s * r * 6} Z`,
      fill: "url(#vBeam)", opacity: 0.5, transform: `rotate(${s < 0 ? 180 : 0} ${cx} ${cy})` }, g));
  }
  /* photon ring + event horizon */
  V2.el("circle", { cx, cy, r: r * 1.28, fill: "none", stroke: "#FFE7B3", "stroke-width": Math.max(2.5, r * 0.09), opacity: 0.9 }, g);
  V2.el("circle", { cx, cy, r, fill: "#000000" }, g);
  return g;
};

/* THE Earth: two-tone continents, night-side city lights, atmosphere rim, highlight arc */
V2.earth = (cx, cy, r, t, opts, parent) => {
  const o = opts || {};
  const g = V2.el("g", {}, parent);
  /* atmosphere halo */
  const id = V2.uid("atm");
  const defs = V2.el("defs", {}, g);
  const ag = V2.el("radialGradient", { id }, defs);
  const atmos = o.atmos === undefined ? 1 : o.atmos;
  V2.el("stop", { offset: "78%", "stop-color": "#4AA8FF", "stop-opacity": 0 }, ag);
  V2.el("stop", { offset: "92%", "stop-color": "#4AA8FF", "stop-opacity": 0.5 * atmos }, ag);
  V2.el("stop", { offset: "100%", "stop-color": "#4AA8FF", "stop-opacity": 0 }, ag);
  V2.el("circle", { cx, cy, r: r * 1.35, fill: `url(#${id})` }, g);
  /* ocean */
  V2.el("circle", { cx, cy, r, fill: o.oceanDim ? V2.P.earthSea2 : V2.P.earthSea }, g);
  /* continents: chunky blobs, two greens */
  const blob = (dx, dy, s, col) => {
    const x = cx + dx * r, y = cy + dy * r, k = s * r;
    V2.el("path", { d: `M ${x - k} ${y} q ${k * 0.4} ${-k * 0.75} ${k * 1.1} ${-k * 0.4} q ${k * 0.7} ${k * 0.25} ${k * 0.5} ${k * 0.6} q ${-k * 0.5} ${k * 0.5} ${-k * 1.05} ${k * 0.3} q ${-k * 0.55} ${-k * 0.1} ${-k * 0.55} ${-k * 0.5} z`, fill: col }, g);
  };
  blob(-0.42, -0.3, 0.34, V2.P.earthLand);
  blob(0.18, -0.05, 0.44, V2.P.earthLand2);
  blob(-0.1, 0.48, 0.30, V2.P.earthLand);
  blob(0.55, 0.4, 0.22, V2.P.earthLand2);
  /* night-side crescent: dark pole centered bottom-right, city lights on it */
  const night = o.night === undefined ? 0.5 : o.night;
  if (night > 0) {
    const sid = V2.uid("night");
    const sd = V2.el("defs", {}, g);
    const sg = V2.el("radialGradient", { id: sid, cx: "74%", cy: "74%", r: "92%" }, sd);
    V2.el("stop", { offset: "0%", "stop-color": "#070B24", "stop-opacity": Math.min(1, night + 0.12) }, sg);
    V2.el("stop", { offset: "60%", "stop-color": "#0A1030", "stop-opacity": night * 0.55 }, sg);
    V2.el("stop", { offset: "100%", "stop-color": "#0A1030", "stop-opacity": 0 }, sg);
    V2.el("circle", { cx, cy, r, fill: `url(#${sid})` }, g);
    for (let i = 0; i < 14; i++) {
      const a = 0.3 + V2.rnd(31, i) * 1.1, rr = 0.3 + V2.rnd(32, i) * 0.5;
      V2.el("circle", { cx: cx + Math.cos(a) * r * rr, cy: cy + Math.sin(a) * r * rr, r: 2 + V2.rnd(33, i) * 2.4,
        fill: "#FFC27A", opacity: 0.95 }, g);
    }
  }
  /* highlight arc hugging the limb, top-left (the Kurzgesagt two-tone rule) */
  const a0 = Math.PI * 1.08, a1 = Math.PI * 1.58;
  V2.el("path", { d: `M ${cx + Math.cos(a0) * r * 0.93} ${cy + Math.sin(a0) * r * 0.93} A ${r * 0.93} ${r * 0.93} 0 0 1 ${cx + Math.cos(a1) * r * 0.93} ${cy + Math.sin(a1) * r * 0.93}`,
    fill: "none", stroke: "#BFE3FF", "stroke-width": r * 0.05, "stroke-linecap": "round", opacity: 0.5 }, g);
  /* cracks glowing from inside (every pass of the hole): jagged, from the limb inward */
  const cracks = o.cracks || 0;
  for (let i = 0; i < cracks; i++) {
    const a = i * 2.4 + 0.7 + V2.rnd(41, i) * 0.5;
    const jag = 0.35 + V2.rnd(44, i) * 0.3;
    const x1 = cx + Math.cos(a) * r * 0.99, y1 = cy + Math.sin(a) * r * 0.99;
    const x2 = cx + Math.cos(a + jag * 0.3) * r * 0.78, y2 = cy + Math.sin(a + jag * 0.3) * r * 0.78;
    const x3 = cx + Math.cos(a + jag) * r * 0.58, y3 = cy + Math.sin(a + jag) * r * 0.58;
    V2.el("path", { d: `M ${x1} ${y1} L ${x2} ${y2} L ${x3} ${y3}`, fill: "none", stroke: V2.P.orange,
      "stroke-width": Math.max(2.5, r * 0.032), "stroke-linecap": "round", "stroke-linejoin": "round",
      opacity: o.crackOp === undefined ? 0.8 : o.crackOp, style: `filter:drop-shadow(0 0 ${r * 0.05}px ${V2.P.amber})` }, g);
  }
  return g;
};

/* cross-section strata: chunky bands with texture. Each band:
   y0 (top) / y1 (bottom) + fill, optional fill2 specks, boards/tiles */
V2.strata = (x0, x1, bands, parent) => {
  const g = V2.el("g", {}, parent);
  bands.forEach((b, i) => {
    V2.el("rect", { x: x0, y: b.y0, width: x1 - x0, height: b.y1 - b.y0, fill: b.fill }, g);
    if (b.fill2) {
      /* aggregate specks so bands aren't vector-flat */
      for (let k = 0; k < (b.n || 26); k++) {
        const sy = b.y0 + 8 + V2.rnd(61 + i, k) * (b.y1 - b.y0 - 16);
        const sx = x0 + 10 + V2.rnd(62 + i, k) * (x1 - x0 - 20);
        V2.el("circle", { cx: sx, cy: sy, r: 2 + V2.rnd(63 + i, k) * 4.5, fill: b.fill2, opacity: 0.5 }, g);
      }
    }
    if (b.boards) {
      for (let k = 1; k < 6; k++)
        V2.el("line", { x1: x0 + 8, y1: b.y0 + ((b.y1 - b.y0) / 6) * k, x2: x1 - 8, y2: b.y0 + ((b.y1 - b.y0) / 6) * k,
          stroke: b.line || "#3A2826", "stroke-width": 3, opacity: 0.6 }, g);
    }
    if (b.tiles) {
      for (let k = 0; k < 8; k++)
        V2.el("line", { x1: x0 + ((x1 - x0) / 8) * k + 14, y1: b.y0 + 6, x2: x0 + ((x1 - x0) / 8) * k + 14, y2: b.y1 - 6,
          stroke: b.line || "#3A3A44", "stroke-width": 3.5, opacity: 0.55 }, g);
      V2.el("line", { x1: x0 + 8, y1: b.y0 + (b.y1 - b.y0) * 0.5, x2: x1 - 8, y2: b.y0 + (b.y1 - b.y0) * 0.5,
        stroke: b.line || "#3A3A44", "stroke-width": 3.5, opacity: 0.55 }, g);
    }
  });
  return g;
};
