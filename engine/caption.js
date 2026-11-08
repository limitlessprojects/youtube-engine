/* ============================================================
   visuals v2 — caption.js  (v2.1, L-073/L-076: keyword captions)

   The caption band shows ONLY the scene's 2–4 KEYWORDS (the
   EMPHASIS list), big, popping in sequence as the voice hits
   them. Full-sentence karaoke subtitles are BANNED (boss
   directive 2026-11-08: "too many words on screen" — the
   published #0003 carried up to 22 words/frame and scored
   text_discipline 2.8/10 on the ultracritic rubric).

   Contract:
   V2.caption(text, u, emWords, opts)
     · emWords — the keyword list (≤5). THESE are the caption.
     · text   — full narration line, used ONLY for word-timing
       of the pops (index of keyword inside the line).
     · opts.size — base font px (default 74)
     · opts.y    — band center (default 1700)
   Fallback: if emWords is empty, renders the first 4 words of
   the line — never the whole sentence.
   ============================================================ */
V2._meas = null;
V2.caption = (text, u, emWords, opts) => {
  const o = opts || {};
  if (!V2._meas) V2._meas = document.createElement("canvas").getContext("2d");

  const line = (text || "").split(/\s+/).filter(Boolean);
  const clean = (w) => w.toLowerCase().replace(/[^a-z0-9-]/g, "");
  const lineIdx = new Map();
  line.forEach((w, i) => { if (!lineIdx.has(clean(w))) lineIdx.set(clean(w), i); });

  // keywords: strip punctuation, keep ≤5, dedupe, keep line order
  let kws = (emWords || []).map((w) => String(w)).filter(Boolean);
  const seen = new Set();
  kws = kws
    .map((w) => clean(w))
    .filter((w) => w && !seen.has(w) && seen.size < 5 && seen.add(w))
    .sort((a, b) => (lineIdx.get(a) ?? 99) - (lineIdx.get(b) ?? 99));
  if (!kws.length) kws = line.slice(0, 4).map(clean).filter(Boolean).slice(0, 4);

  const size = o.size || 74;
  const fontOf = (s) => `800 ${s}px 'Bricolage Grotesque', 'DejaVu Sans', sans-serif`;
  const wOf = (w) => { V2._meas.font = fontOf(size); return Math.max(30, V2._meas.measureText(w).width); };

  const spaceW = 42;
  const total = kws.reduce((a, w) => a + wOf(w), 0) + spaceW * (kws.length - 1);

  const g = V2.el("g", {});
  // scrim: dark pill behind the keywords so they survive bright backgrounds
  // on daylight phones (day-010 ultracritic directive on #0003's captions)
  const anyShown = kws.some((_, i) => {
    const at = kws.length === 1 ? 0 : (i / kws.length) * 0.55;
    return u > at;
  });
  if (anyShown && !o.noScrim) {
    const pad = 46;
    V2.el("rect", { x: 540 - total / 2 - pad, y: (o.y || 1700) - size * 0.82,
      width: total + pad * 2, height: size * 1.64, rx: size * 0.82,
      fill: "#0A0E1E", opacity: 0.5 }, g);
  }

  let x = 540 - total / 2;
  const y = o.y || 1700;

  kws.forEach((w, i) => {
    // pop timing: keyword i appears as the voice reaches it —
    // spread across the first 60% of the scene, staggered
    const at = kws.length === 1 ? 0 : (i / kws.length) * 0.55;
    const k = V2.backOut(V2.clamp01((u - at) / 0.12));
    if (k > 0.01) {
      const el = V2.txt(x + wOf(w) / 2, y, w, {
        "text-anchor": "middle", "font-family": V2.UI_DISPLAY,
        "font-weight": 800, "font-size": size, fill: V2.P.cream,
        opacity: 0.96 * k,
        style: `filter: drop-shadow(0 4px 12px rgba(0,0,0,0.92)) drop-shadow(0 0 30px rgba(0,0,0,0.5))`,
        transform: `translate(${x + wOf(w) / 2} ${y}) scale(${0.6 + 0.4 * k}) translate(${-(x + wOf(w) / 2)} ${-y})`,
      }, g);
      el.setAttribute("paint-order", "stroke");
    }
    x += wOf(w) + spaceW;
  });
  return g;
};
