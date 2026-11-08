/* ============================================================
   youtube-engine / visuals v2 — core
   Owned engine distilled from vendor/what-if-animation (MIT,
   © 2026 FreshStack) + Kurzgesagt frame study. Framework-free:
   pure functions of the shot clock t, so any t draws the same
   frame (seek-driven renderer + reversible segments).
   Modules: core.js · space.js · rig.js · world.js · diagram.js · caption.js
   ============================================================ */
const V2 = {};

/* ---------- palette (craft laws: docs/rules.md §Scenes; the original
   docs/visual-craft.md was lost in a recycle before its first commit) ---------- */
V2.P = {
  bgDeep: "#070A18", bgRaised: "#0E1430",
  nebPurple: "#5B3A9E", nebPurple2: "#3A2470", nebMagenta: "#C2447E",
  amber: "#FFB054", orange: "#FF8A3D", teal: "#2FD4C5", blue: "#4AA8FF",
  cream: "#F6EFE3", ink: "#141222", dim: "#8A93B8",
  earthSea: "#1E5F8A", earthSea2: "#174C71", earthLand: "#2E8B57", earthLand2: "#246B43",
  crust: "#5C4038", crust2: "#4A3430", rock: "#6B4B42", rock2: "#57392F",
};

/* ---------- utils ---------- */
V2.lerp = (a, b, t) => a + (b - a) * t;
V2.clamp01 = (v) => Math.max(0, Math.min(1, v));
V2.easeInOut = (t) => (t <= 0 ? 0 : t >= 1 ? 1 : t < 0.5 ? 4*t*t*t : 1 - Math.pow(-2*t + 2, 3) / 2);
V2.easeOut = (t) => 1 - Math.pow(1 - V2.clamp01(t), 3);
V2.easeIn = (t) => Math.pow(V2.clamp01(t), 3);
V2.backOut = (t) => { const c1 = 1.70158, c3 = c1 + 1; t = V2.clamp01(t);
  return 1 + c3 * Math.pow(t - 1, 3) + c1 * Math.pow(t - 1, 2); };
/* piecewise value from [frame, value] keys */
V2.kf = (f, keys, ease) => {
  ease = ease || V2.easeInOut;
  if (f <= keys[0][0]) return keys[0][1];
  for (let i = 0; i < keys.length - 1; i++) {
    const [f0, v0] = keys[i], [f1, v1] = keys[i + 1];
    if (f <= f1) return V2.lerp(v0, v1, ease((f - f0) / Math.max(1e-6, f1 - f0)));
  }
  return keys[keys.length - 1][1];
};
/* seeded pseudo-random in 0..1 — never Math.random inside a frame */
V2.rnd = (seed, i) => { const s = Math.sin(seed * 31.7 + i * 12.9898) * 43758.5453; return s - Math.floor(s); };
/* a wobble that dies away (landings, knocks) */
V2.settle = (t, amp, speed, decay) => (t > 0 ? Math.sin(t * (speed || 1.4)) * amp * Math.exp(-t / (decay || 8)) : 0);
/* camera: centre world point (cx,cy) at zoom s in the 1080x1920 frame */
V2.cam = (cx, cy, s) => `translate(${540} ${960}) scale(${s}) translate(${-cx} ${-cy})`;

/* ---------- DOM helper ---------- */
V2.SVGNS = "http://www.w3.org/2000/svg";
V2.el = (tag, attrs, parent) => {
  const el = document.createElementNS(V2.SVGNS, tag);
  for (const k in attrs) if (attrs[k] !== undefined && attrs[k] !== null) el.setAttribute(k, attrs[k]);
  (parent || V2.root).appendChild(el);
  return el;
};
V2.txt = (x, y, str, attrs, parent) => {
  const t = V2.el("text", Object.assign({ x, y }, attrs || {}), parent);
  t.textContent = str;
  return t;
};

/* ---------- shared defs (mount once per frame) ---------- */
let _uid = 0;
V2.uid = (p) => (p || "v") + (_uid++);
V2.defs = (parent) => {
  const d = V2.el("defs", {}, parent);
  const radial = (id, stops) => {
    const g = V2.el("radialGradient", { id }, d);
    stops.forEach(([off, col, op]) => V2.el("stop", { offset: off, "stop-color": col, "stop-opacity": op }, g));
  };
  const linear = (id, attrs, stops) => {
    const g = V2.el("linearGradient", Object.assign({ id }, attrs), d);
    stops.forEach(([off, col, op]) => V2.el("stop", { offset: off, "stop-color": col, "stop-opacity": op }, g));
  };
  /* glow halos (screen-blended by the caller) */
  radial("vGlowWarm", [["0%", "#FFD7A0", 1], ["30%", "#FFB054", 0.35], ["100%", "#FFB054", 0]]);
  radial("vGlowCool", [["0%", "#9FC0FF", 1], ["30%", "#4AA8FF", 0.32], ["100%", "#4AA8FF", 0]]);
  radial("vGlowRed", [["0%", "#FF5A4A", 1], ["30%", "#FF5A4A", 0.32], ["100%", "#FF5A4A", 0]]);
  radial("vGlowTeal", [["0%", "#7DF0E4", 1], ["30%", "#2FD4C5", 0.3], ["100%", "#2FD4C5", 0]]);
  /* light cone fading downward */
  linear("vCone", { x1: 0, y1: 0, x2: 0, y2: 1 }, [["0%", "#FFD7A0", 0.5], ["100%", "#FFD7A0", 0]]);
  /* polar jets fading out along the beam */
  linear("vBeam", { x1: 0, y1: 1, x2: 0, y2: 0 }, [["0%", "#7DF0E4", 0.55], ["60%", "#7DF0E4", 0.18], ["100%", "#7DF0E4", 0]]);
  /* ambient-occlusion gradients */
  linear("vAOu", { x1: 0, y1: 1, x2: 0, y2: 0 }, [["0%", "#000", 0.5], ["100%", "#000", 0]]);
  linear("vAOd", { x1: 0, y1: 0, x2: 0, y2: 1 }, [["0%", "#000", 0.45], ["100%", "#000", 0]]);
  /* rim lights: tight warm edge + wide soft bloom (what-if kit) */
  const rim = (id, dx, edge, wide) => {
    const f = V2.el("filter", { id, x: "-40%", y: "-40%", width: "180%", height: "180%" }, d);
    V2.el("feDropShadow", { dx, dy: -1.5, stdDeviation: 2.2, "flood-color": edge, "flood-opacity": 1 }, f);
    V2.el("feDropShadow", { dx: 0, dy: 0, stdDeviation: 16, "flood-color": wide, "flood-opacity": 0.35 }, f);
  };
  rim("vRimR", 4, "#FFB15A", "#FF9A4A");
  rim("vRimL", -4, "#FFB15A", "#FF9A4A");
  rim("vRimTealR", 4, "#7DF0E4", "#2FD4C5");
  rim("vRimTealL", -4, "#7DF0E4", "#2FD4C5");
  /* depth-of-field blurs */
  [3, 6, 10, 16].forEach((b) => {
    const f = V2.el("filter", { id: "vBlur" + b, x: "-25%", y: "-25%", width: "150%", height: "150%" }, d);
    V2.el("feGaussianBlur", { stdDeviation: b }, f);
  });
  /* faint wall/paint texture */
  const wt = V2.el("filter", { id: "vWall", x: "0%", y: "0%", width: "100%", height: "100%" }, d);
  V2.el("feTurbulence", { type: "fractalNoise", baseFrequency: "0.006 0.012", numOctaves: 3, seed: 7, result: "n" }, wt);
  V2.el("feColorMatrix", { in: "n", type: "matrix", values: "0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 0.28 -0.09", result: "a" }, wt);
  V2.el("feComposite", { in: "a", in2: "SourceGraphic", operator: "in" }, wt);
  /* fine grain (the finish; shifts on twos) */
  const gr = V2.el("filter", { id: "vGrain", x: "0%", y: "0%", width: "100%", height: "100%" }, d);
  V2.el("feTurbulence", { type: "fractalNoise", baseFrequency: "0.9", numOctaves: 2, seed: 11, result: "n" }, gr);
  V2.el("feColorMatrix", { in: "n", type: "matrix", values: "0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 0.05 0" }, gr);
  /* vignette */
  radial("vVig", [["58%", "#05050A", 0], ["100%", "#05050A", 0.82]]);
  return d;
};

/* ---------- the finish: vignette + grain on twos ---------- */
V2.grade = (t) => {
  V2.el("rect", { x: -20, y: -20, width: 1120, height: 1960, fill: "url(#vVig)" });
  V2.el("rect", { x: 0, y: 0, width: 1080, height: 1920, filter: "url(#vGrain)", opacity: 0.5,
    transform: `translate(${(Math.floor(t / 2) % 2) * 3} ${Math.floor(t / 2) % 3})` });
};

/* soft glow blob (screen blend) */
V2.glow = (x, y, r, kind, o, parent) =>
  V2.el("circle", { cx: x, cy: y, r, fill: `url(#vGlow${kind || "Warm"})`, opacity: o === undefined ? 0.6 : o,
    style: "mix-blend-mode:screen" }, parent);

/* dark veil with soft holes where light pools — drawn over the set,
   characters after it stay bright (the what-if LightVeil) */
V2.veil = (id, lights, o, parent) => {
  const defs = V2.el("defs", {}, parent);
  const rg = V2.el("radialGradient", { id: id + "hole" }, defs);
  [["0%", 1], ["45%", 0.78], ["100%", 0]].forEach(([off, op]) =>
    V2.el("stop", { offset: off, "stop-color": "#000", "stop-opacity": op }, rg));
  const m = V2.el("mask", { id: id + "m", maskUnits: "userSpaceOnUse", x: -500, y: -500, width: 2200, height: 3000 }, defs);
  V2.el("rect", { x: -500, y: -500, width: 2200, height: 3000, fill: "#fff" }, m);
  lights.forEach(([x, y, r]) => V2.el("circle", { cx: x, cy: y, r, fill: `url(#${id}hole)` }, m));
  V2.el("rect", { x: -500, y: -500, width: 2200, height: 3000, fill: "#04030A", opacity: o, mask: `url(#${id}m)` }, parent);
};

/* dust motes drifting in a beam */
V2.dust = (t, seed, box, n, o, parent) => {
  const g = V2.el("g", { style: "mix-blend-mode:screen" }, parent);
  for (let i = 0; i < (n || 26); i++) {
    const sp = 0.4 + V2.rnd(seed + 2, i);
    const x = box.x + ((V2.rnd(seed, i) * box.w + Math.sin((t / 30) * sp + i) * 22 + t * 0.35 * sp) % box.w + box.w) % box.w;
    const y = box.y + ((V2.rnd(seed + 1, i) * box.h + Math.cos((t / 40) * sp + i * 2) * 16 - t * 0.22 * sp) % box.h + box.h) % box.h;
    const tw = 0.5 + 0.5 * Math.sin(t / 9 + i * 1.7);
    V2.el("circle", { cx: x, cy: y, r: 1.2 + V2.rnd(seed + 3, i) * 2.2, fill: "#FFE2B0", opacity: (o || 0.5) * (0.25 + 0.75 * tw) }, g);
  }
};
