/* ============================================================
   visuals v2 — diagram.js
   The science beat: dark blueprint ground with a drifting grid,
   draw-on paths, arc arrows, mono labels, counting numbers,
   glowing icons. Pattern after vendor/what-if-animation
   sets/schematic.tsx (MIT, © 2026 FreshStack) + Kurzgesagt glow.
   ============================================================ */
V2.SCH = { ground: "#0A1220", grid: "#16243C", line: "#F6EFE3", dim: "#7E8DA6", live: "#FF8A3D", glow: "#FFB15A" };

/* blueprint ground: deep navy, drifting fine grid, registration marks, center glow */
V2.schematic = (t, id, parent, opts) => {
  const o = opts || {};
  const defs = V2.el("defs", {}, parent);
  const p1 = V2.el("pattern", { id: id + "g1", width: 44, height: 44, patternUnits: "userSpaceOnUse" }, defs);
  V2.el("path", { d: "M 44 0 L 0 0 0 44", fill: "none", stroke: V2.SCH.grid, "stroke-width": 1.5 }, p1);
  const p2 = V2.el("pattern", { id: id + "g5", width: 220, height: 220, patternUnits: "userSpaceOnUse" }, defs);
  V2.el("path", { d: "M 220 0 L 0 0 0 220", fill: "none", stroke: V2.SCH.grid, "stroke-width": 3 }, p2);
  const gg = V2.el("radialGradient", { id: id + "glow" }, defs);
  V2.el("stop", { offset: "0%", "stop-color": "#22406B", "stop-opacity": 0.9 }, gg);
  V2.el("stop", { offset: "100%", "stop-color": "#22406B", "stop-opacity": 0 }, gg);
  V2.el("rect", { x: -40, y: -40, width: 1160, height: 2000, fill: V2.SCH.ground }, parent);
  V2.el("circle", { cx: 540, cy: o.cy || 800, r: 860, fill: `url(#${id}glow)` }, parent);
  const drift = V2.el("g", { transform: `translate(${(t * 0.4) % 44} ${(t * 0.22) % 44})` }, parent);
  V2.el("rect", { x: -88, y: -88, width: 1280, height: 2120, fill: `url(#${id}g1)` }, drift);
  V2.el("rect", { x: -88, y: -88, width: 1280, height: 2120, fill: `url(#${id}g5)` }, drift);
  [[86, 96, 1, 1], [994, 96, -1, 1], [86, 1824, 1, -1], [994, 1824, -1, -1]].forEach(([x, y, sx, sy]) =>
    V2.el("path", { d: `M ${x} ${y + sy * 44} L ${x} ${y} L ${x + sx * 44} ${y}`, stroke: V2.SCH.dim, "stroke-width": 3, fill: "none", opacity: 0.6 }, parent));
};

/* a path that draws on over dur frames */
V2.drawOn = (d, t0, dur, color, w, fill, parent, op) => {
  const p = V2.easeOut(V2.clamp01(t0 / (dur || 10)));
  if (p <= 0) return;
  V2.el("path", { d, pathLength: 1, "stroke-dasharray": "1 1", "stroke-dashoffset": 1 - p, stroke: color || V2.SCH.line,
    "stroke-width": w || 5, fill: p >= 1 ? (fill || "none") : "none", "stroke-linecap": "round", "stroke-linejoin": "round",
    opacity: op === undefined ? 1 : op }, parent);
};

/* arc arrow that draws on, head pops at the end */
V2.arrow = (x0, y0, x1, y1, t0, dur, color, bend, parent) => {
  const mx = (x0 + x1) / 2 - (y1 - y0) * (bend === undefined ? 0.12 : bend);
  const my = (y0 + y1) / 2 + (x1 - x0) * (bend === undefined ? 0.12 : bend);
  V2.drawOn(`M ${x0} ${y0} Q ${mx} ${my} ${x1} ${y1}`, t0, dur || 8, color || V2.SCH.line, 6, "none", parent);
  if (V2.easeOut(V2.clamp01(t0 / (dur || 8))) >= 1) {
    const a = Math.atan2(y1 - my, x1 - mx);
    V2.el("path", { d: `M ${x1 - 24 * Math.cos(a - 0.45)} ${y1 - 24 * Math.sin(a - 0.45)} L ${x1} ${y1} L ${x1 - 24 * Math.cos(a + 0.45)} ${y1 - 24 * Math.sin(a + 0.45)}`,
      stroke: color || V2.SCH.line, "stroke-width": 6, fill: "none", "stroke-linecap": "round", "stroke-linejoin": "round" }, parent);
  }
};

/* mono label that pops on with backOut */
V2.schLabel = (x, y, t0, text, size, color, anchor, parent) => {
  if (t0 < 0) return;
  const s = V2.backOut(V2.clamp01(t0 / 6));
  V2.txt(x, y, text, { "text-anchor": anchor || "middle", "font-family": "Fragment Mono, monospace",
    "font-size": size || 36, fill: color || V2.SCH.line, "letter-spacing": 2,
    transform: `translate(${x} ${y}) scale(${s}) translate(${-x} ${-y})` }, parent);
};

/* number counting up with a glow (format fn for decimals) */
V2.countUp = (x, y, t0, to, dur, size, color, suffix, format, parent) => {
  if (t0 < 0) return;
  const v = to * V2.easeOut(V2.clamp01(t0 / (dur || 30)));
  const txt = format ? format(v) : Math.round(v).toLocaleString("en-US");
  V2.txt(x, y, txt + (suffix || ""), { "text-anchor": "middle", "font-family": "Fragment Mono, monospace",
    "font-size": size || 64, fill: color || V2.SCH.live, style: `filter: drop-shadow(0 0 16px ${V2.SCH.glow}66)` }, parent);
};

/* the atom, Kurzgesagt-grade: chunky broken rings, glowing nucleus, electron trails */
V2.atomIcon = (cx, cy, r, t, on, parent) => {
  const g = V2.el("g", { transform: `translate(${cx} ${cy}) scale(${1 + 0.05 * Math.sin(t / 9)})` }, parent);
  if (on > 0) V2.glow(0, 0, r * 0.9, "Teal", 0.5, g);
  const cols = [V2.P.teal, V2.P.blue, V2.P.nebPurple];
  /* three tilted chunky broken rings */
  [0, 60, 120].forEach((tilt, k) => {
    const rg = V2.el("g", { transform: `rotate(${tilt})` }, g);
    const rx = r, ry = r * 0.36;
    const col = cols[k];
    const w = r * 0.055;
    [[10, 130], [165, 110], [300, 30]].forEach(([a0, sw2], s) => {
      const p0 = { x: Math.cos(rad0(a0)) * rx, y: Math.sin(rad0(a0)) * ry };
      const p1 = { x: Math.cos(rad0(a0 + sw2)) * rx, y: Math.sin(rad0(a0 + sw2)) * ry };
      V2.el("path", { d: `M ${p0.x} ${p0.y} A ${rx} ${ry} 0 ${sw2 > 180 ? 1 : 0} 1 ${p1.x} ${p1.y}`,
        fill: "none", stroke: col, "stroke-width": w, "stroke-linecap": "round", opacity: 0.95 - s * 0.12 }, rg);
    });
    /* electron with a fading trail */
    const ph = t * 0.09 * (1 + k * 0.18) + k * 2.1;
    for (let tr = 5; tr >= 0; tr--) {
      const a = ph - tr * 0.13;
      V2.el("circle", { cx: Math.cos(a) * rx, cy: Math.sin(a) * ry, r: (tr === 0 ? 11 : 7 - tr) * (r / 300),
        fill: tr === 0 ? "#FFFFFF" : col, opacity: tr === 0 ? 1 : 0.5 - tr * 0.08 }, rg);
    }
  });
  function rad0(d) { return (d * Math.PI) / 180; }
  /* nucleus: white-hot core + amber bloom */
  V2.glow(0, 0, r * 0.34, "Warm", 0.9, g);
  V2.el("circle", { cx: 0, cy: 0, r: r * 0.085, fill: "#FFFFFF" }, g);
  V2.el("circle", { cx: 0, cy: 0, r: r * 0.13, fill: V2.P.amber, opacity: 0.55 }, g);
  return g;
};

/* ============================================================ UI ============================================================ */
V2.UI_MONO = "Fragment Mono, monospace";
V2.UI_DISPLAY = "'Bricolage Grotesque', 'DejaVu Sans', sans-serif";

/* dark translucent pill naming the beat (mono, blinking dot) */
V2.chip = (x, y, f, label, icon, parent) => {
  const g = V2.el("g", {}, parent);
  const wpx = 24 + label.length * 19 + (icon ? 40 : 0);
  V2.el("rect", { x: x - wpx / 2, y: y - 34, width: wpx, height: 68, rx: 34, fill: "#0A0E1E", opacity: 0.82, stroke: "#2A3358", "stroke-width": 2 }, g);
  if (icon === "dot")
    V2.el("circle", { cx: x - wpx / 2 + 30, cy: y, r: 8, fill: V2.P.orange, opacity: 0.5 + 0.5 * Math.sin(f / 5) }, g);
  V2.txt(x + (icon ? 14 : 0), y + 11, label, { "text-anchor": "middle", "font-family": V2.UI_MONO, "font-size": 30,
    fill: V2.P.cream, "letter-spacing": 2 }, g);
  return g;
};

/* small value tag with an optional mark drawn on after markT */
V2.tag = (x, y, t0, text, mark, markT, parent, accent) => {
  const g = V2.el("g", { opacity: V2.clamp01(t0 / 5) }, parent);
  const wpx = 36 + text.length * 21;
  V2.el("rect", { x: x - wpx / 2, y: y - 30, width: wpx, height: 60, rx: 14, fill: "#0A0E1E", opacity: 0.85, stroke: accent || V2.P.amber, "stroke-width": 2.5 }, g);
  V2.txt(x, y + 10, text, { "text-anchor": "middle", "font-family": V2.UI_MONO, "font-size": 31, fill: V2.P.cream, "letter-spacing": 1.5 }, g);
  if (mark && t0 > (markT === undefined ? 8 : markT)) {
    if (mark === "check")
      V2.el("path", { d: `M ${x + wpx / 2 - 34} ${y} l 9 10 l 18 -20`, stroke: V2.P.teal, "stroke-width": 5, fill: "none", "stroke-linecap": "round", "stroke-linejoin": "round" }, g);
    else
      V2.el("path", { d: `M ${x + wpx / 2 - 36} ${y - 9} l 18 18 M ${x + wpx / 2 - 18} ${y - 9} l -18 18`, stroke: "#E85D5D", "stroke-width": 5, "stroke-linecap": "round" }, g);
  }
  return g;
};

/* round dial with a readout: p fills the ring (0..1) */
V2.dial = (x, y, p, readout, parent, r) => {
  r = r || 78;
  const g = V2.el("g", {}, parent);
  V2.el("circle", { cx: x, cy: y, r, fill: "#0A0E1E", opacity: 0.85, stroke: "#2A3358", "stroke-width": 2.5 }, g);
  const cir = 2 * Math.PI * (r - 12);
  V2.el("circle", { cx: x, cy: y, r: r - 12, fill: "none", stroke: "#232B4C", "stroke-width": 9 }, g);
  V2.el("circle", { cx: x, cy: y, r: r - 12, fill: "none", stroke: V2.P.orange, "stroke-width": 9, "stroke-linecap": "round",
    "stroke-dasharray": `${cir * V2.clamp01(p)} ${cir}`, transform: `rotate(-90 ${x} ${y})` }, g);
  V2.txt(x, y + 12, readout, { "text-anchor": "middle", "font-family": V2.UI_MONO, "font-size": r * 0.42, fill: V2.P.cream }, g);
  return g;
};

/* label that pops up and drifts off (+1, x10) */
V2.floatLabel = (x, y, t0, text, color, size, parent) => {
  if (t0 < 0 || t0 > 24) return;
  const u = t0 / 24;
  V2.txt(x, y - u * 60, text, { "text-anchor": "middle", "font-family": V2.UI_DISPLAY, "font-weight": 800,
    "font-size": size || 66, fill: color || "#FFE27A", opacity: 1 - u * u }, parent);
};

/* concentric focus rings opening out (a realisation) */
V2.focusRings = (x, y, t0, color, parent) => {
  for (let i = 0; i < 3; i++) {
    const u = V2.clamp01((t0 - i * 4) / 18);
    if (u <= 0 || u >= 1) continue;
    V2.el("circle", { cx: x, cy: y, r: 30 + u * 130, fill: "none", stroke: color || "#FFE7B3",
      "stroke-width": 5 * (1 - u), opacity: 0.7 * (1 - u) }, parent);
  }
};
