/* ============================================================
   visuals v2 — caption.js
   Bottom-band captions: Bricolage Grotesque 800, cream, amber
   emphasis, word-pop on the voice, measured wrap (max 3 lines),
   soft shadow so it reads over busy backgrounds.
   ============================================================ */
V2._meas = null;
V2.caption = (text, u, emWords, opts) => {
  const o = opts || {};
  if (!V2._meas) V2._meas = document.createElement("canvas").getContext("2d");
  const words = text.split(/\s+/);
  const em = new Set((emWords || []).map((w) => w.toLowerCase()));
  const fontOf = (s) => `800 ${s}px 'Bricolage Grotesque', 'DejaVu Sans', sans-serif`;
  const wOf = (w, s) => { V2._meas.font = fontOf(s); return Math.max(12, V2._meas.measureText(w).width); };
  let size = 58, lines = null, widths = null, spaceW = 0;
  for (; size >= 38; size -= 4) {
    V2._meas.font = fontOf(size);
    spaceW = V2._meas.measureText(" ").width;
    widths = words.map((w) => wOf(w, size));
    lines = [[]]; let wpx = 0;
    for (let i = 0; i < words.length; i++) {
      const add = widths[i] + (lines[lines.length - 1].length ? spaceW : 0);
      if (wpx + add > 930 && lines[lines.length - 1].length) { lines.push([]); wpx = 0; }
      lines[lines.length - 1].push(i);
      wpx += widths[i] + (lines[lines.length - 1].length > 1 ? spaceW : 0);
    }
    if (lines.length <= 3) break;
  }
  const lineH = size + 20;
  const shown = Math.floor(V2.easeOut(V2.clamp01(u / 0.6)) * words.length + 0.5001);
  const g = V2.el("g", {});
  const baseY = (o.y || 1700) - (lines.length - 1) * lineH / 2;
  lines.forEach((ln, li) => {
    const total = ln.reduce((a, i) => a + widths[i], 0) + spaceW * (ln.length - 1);
    let x = 540 - total / 2;
    const y = baseY + li * lineH;
    ln.forEach((i) => {
      if (i < shown) {
        const clean = words[i].toLowerCase().replace(/[^a-z-]/g, "");
        const isEm = em.has(clean);
        const pop = Math.max(0.72, Math.min(1, (u * words.length - i) * 0.6 + 0.4));
        const el = V2.txt(x, y, words[i], {
          "font-family": V2.UI_DISPLAY, "font-weight": 800, "font-size": size,
          fill: isEm ? V2.P.amber : V2.P.cream, opacity: pop,
          style: `filter: drop-shadow(0 3px 10px rgba(0,0,0,0.9)) drop-shadow(0 0 26px rgba(0,0,0,0.55))`,
          transform: `translate(${x} ${y}) scale(${pop}) translate(${-x} ${-y})`,
        }, g);
        el.setAttribute("paint-order", "stroke");
      }
      x += widths[i] + spaceW;
    });
  });
  return g;
};
