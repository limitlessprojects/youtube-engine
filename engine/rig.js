/* ============================================================
   visuals v2 — rig.js
   One rig, one costume (Look) per character — ported from
   vendor/what-if-animation/studio/src/engine/rig.tsx (MIT,
   © 2026 FreshStack), restyled for our cast. Two-segment limbs,
   mitten hands, shoes, shaded torso, 9 expressions swapped
   through blinks, rim light, contact shadow, squash & stretch.
   Everything is a pure function of the pose.
   ============================================================ */

/* body measurements (local space: hips at 0,0, y down) */
const RIG = {
  UPPER_ARM: 62, FORE_ARM: 58, THIGH: 72, SHIN: 68,
  SHOULDER: { x: 42, y: -108 }, HIP: { x: 17, y: 0 },
  HEAD: { x: 0, y: -176, r: 62 },
};
RIG.LEG_LEN = RIG.THIGH + RIG.SHIN;

/* our cast (original designs; the rig code is MIT). kip = the hero:
   navy hoodie (catches the rim), amber drawstrings, cream face —
   the head stays the brightest thing on dark sets. */
V2.LOOKS = {
  kip: {
    skin: "#F6EFE3", skinShade: "#E2D3BE", hand: "#F6EFE3",
    jacket: "#3D4A78", jacketShade: "#2C3860", accent: "#FFB054",
    limb: "#EFE2CC", line: "#121019", shoe: "#2FB7A6",
    face: "#1D2033", hair: "#1D2033", extra: "hood",
  },
  kipAmber: {
    skin: "#F6EFE3", skinShade: "#E2D3BE", hand: "#F6EFE3",
    jacket: "#F2B33D", jacketShade: "#D4922A", accent: "#D4922A",
    limb: "#EFE2CC", line: "#121019", shoe: "#2FB7A6",
    face: "#1D2033", hair: "#1D2033",
  },
};

V2.basePose = {
  x: 540, y: 1200, scale: 1, facing: 1, tilt: 0, spin: 0, headTilt: 0,
  armL: { a: 10, b: -8 }, armR: { a: 10, b: -8 },
  legL: { a: 5, b: 0 }, legR: { a: -5, b: 0 },
  expr: "neutral", blink: 0, look: 0, glasses: 0, yaw: 0, squash: 0,
  handL: "open", handR: "open", sway: 0, glint: 0, glintColor: "#8FF0FF",
};

const mixLimb = (a, b, t) => ({ a: V2.lerp(a.a, b.a, t), b: V2.lerp(a.b, b.b, t) });

/* eased interpolation between pose keys; faces hold until their key */
V2.poseAt = (f, keys, from) => {
  const cur = from || V2.basePose;
  const full = [];
  let c = cur;
  for (const k of keys) { c = Object.assign({}, c, k.p); full.push({ f: k.f, p: c, ease: k.ease }); }
  if (f <= full[0].f) return full[0].p;
  for (let i = 0; i < full.length - 1; i++) {
    const A = full[i], B = full[i + 1];
    if (f <= B.f) {
      const t = (B.ease || V2.easeInOut)((f - A.f) / Math.max(1e-6, B.f - A.f));
      return {
        x: V2.lerp(A.p.x, B.p.x, t), y: V2.lerp(A.p.y, B.p.y, t),
        scale: V2.lerp(A.p.scale, B.p.scale, t),
        facing: t < 0.5 ? A.p.facing : B.p.facing,
        tilt: V2.lerp(A.p.tilt, B.p.tilt, t), spin: V2.lerp(A.p.spin, B.p.spin, t),
        headTilt: V2.lerp(A.p.headTilt, B.p.headTilt, t),
        armL: mixLimb(A.p.armL, B.p.armL, t), armR: mixLimb(A.p.armR, B.p.armR, t),
        legL: mixLimb(A.p.legL, B.p.legL, t), legR: mixLimb(A.p.legR, B.p.legR, t),
        expr: A.p.expr, handL: A.p.handL, handR: A.p.handR,
        blink: V2.lerp(A.p.blink, B.p.blink, t), look: V2.lerp(A.p.look, B.p.look, t),
        glasses: V2.lerp(A.p.glasses, B.p.glasses, t), yaw: V2.lerp(A.p.yaw, B.p.yaw, t),
        squash: V2.lerp(A.p.squash, B.p.squash, t), sway: V2.lerp(A.p.sway, B.p.sway, t),
        glint: A.p.glint, glintColor: A.p.glintColor,
      };
    }
  }
  return full[full.length - 1].p;
};

/* faces swap through a blink: two frames shut either side of each change */
V2.faceAt = (f, keys) => {
  let expr = keys[0][1], blink = 0;
  for (let i = 0; i < keys.length; i++) {
    const [k, e] = keys[i];
    if (f >= k) expr = e;
    if (i > 0 && f >= k - 2 && f < k + 1) blink = 1;
  }
  return { expr, blink };
};

const rad = (d) => (d * Math.PI) / 180;
const rotP = (p, deg, c) => {
  c = c || { x: 0, y: 0 };
  const r = rad(deg), dx = p.x - c.x, dy = p.y - c.y;
  return { x: c.x + dx * Math.cos(r) - dy * Math.sin(r), y: c.y + dx * Math.sin(r) + dy * Math.cos(r) };
};
const limbSpread = (yaw) => 1 - 0.85 * Math.min(1, Math.abs(yaw));
const turnWidth = (yaw) => 1 - 0.4 * Math.min(1, Math.abs(yaw));

/* joint positions in local space (props attach to hands with toWorld) */
V2.joints = (pose) => {
  const side = (s, limb, root, l1, l2, isLeg) => {
    const dir = isLeg ? pose.facing : s;
    const d1 = { x: dir * Math.sin(rad(limb.a)), y: Math.cos(rad(limb.a)) };
    const mid = { x: root.x + d1.x * l1, y: root.y + d1.y * l1 };
    const a2 = limb.a + limb.b;
    const d2 = { x: dir * Math.sin(rad(a2)), y: Math.cos(rad(a2)) };
    return { root, mid, end: { x: mid.x + d2.x * l2, y: mid.y + d2.y * l2 } };
  };
  const tR = (p) => rotP(p, pose.tilt);
  const sp = limbSpread(pose.yaw);
  const shL = { x: -RIG.SHOULDER.x * sp + pose.yaw * 6, y: RIG.SHOULDER.y };
  const shR = { x: RIG.SHOULDER.x * sp + pose.yaw * 6, y: RIG.SHOULDER.y };
  const armL = side(-1, pose.armL, shL, RIG.UPPER_ARM, RIG.FORE_ARM, false);
  const armR = side(1, pose.armR, shR, RIG.UPPER_ARM, RIG.FORE_ARM, false);
  const legL = side(-1, pose.legL, { x: -RIG.HIP.x * sp, y: 0 }, RIG.THIGH, RIG.SHIN, true);
  const legR = side(1, pose.legR, { x: RIG.HIP.x * sp, y: 0 }, RIG.THIGH, RIG.SHIN, true);
  const r = (o) => ({ root: tR(o.root), mid: tR(o.mid), end: tR(o.end) });
  return { armL: r(armL), armR: r(armR), legL, legR, head: tR(RIG.HEAD) };
};

/* local point to world space (attach props to hands) */
V2.toWorld = (pose, p) => {
  const spun = rotP(p, pose.spin, { x: 0, y: -90 });
  return { x: pose.x + spun.x * pose.scale, y: pose.y + spun.y * pose.scale };
};

/* where the feet are for a pose standing at hip y */
V2.feetBelowHips = (scale) => RIG.LEG_LEN * scale;

/* procedural profile walk: lean, bob, elbow bend, sway */
V2.walkPose = (x, phase, ground, scale, extra, facing) => {
  const s = Math.sin(phase);
  const g = typeof ground === "number" ? ground : ground(x);
  return Object.assign({}, V2.basePose, {
    x, y: g - RIG.LEG_LEN * (scale || 0.9) - Math.abs(Math.cos(phase)) * 7,
    scale: scale || 0.9, facing: facing || 1, yaw: facing || 1,
    tilt: 5 * (facing || 1), headTilt: 2 * Math.sin(phase * 2),
    sway: 10 * Math.sin(phase + 0.8),
    legL: { a: 28 * s, b: -Math.max(0, 40 * Math.sin(phase + 1.2)) },
    legR: { a: -28 * s, b: -Math.max(0, 40 * Math.sin(phase + 1.2 + Math.PI)) },
    armL: { a: 24 * s, b: 12 + 14 * Math.abs(s) },
    armR: { a: 24 * s, b: 12 + 14 * Math.abs(s) },
  }, extra || {});
};

/* ---------- the face: 9 expressions, brows + mouths + extras ---------- */
const Face = (pose, L) => {
  const { expr, blink, look, yaw } = pose;
  const ink = L.face, HEAD = RIG.HEAD;
  const ex = look * 7;
  const ay = Math.min(1, Math.abs(yaw));
  const farHidden = ay > 0.72;
  const farSide = yaw > 0 ? -1 : 1;
  const eyeY = HEAD.y - 4;
  const lid = expr === "smug" || expr === "cool" ? 0.45 : expr === "tired" ? 0.58 : 0;
  const open = Math.max(0.08, 1 - Math.max(blink, lid));
  const gg = V2.el("g", { transform: `translate(${yaw * 30} 0) scale(${1 - 0.28 * ay} 1)` });
  const eye = (cx) => {
    if (farHidden && Math.sign(cx) === farSide) return null;
    if (expr === "happy")
      return V2.el("path", { d: `M ${cx - 10} ${eyeY + 3} Q ${cx} ${eyeY - 9} ${cx + 10} ${eyeY + 3}`, stroke: ink, "stroke-width": 6, fill: "none", "stroke-linecap": "round" }, gg);
    if (expr === "oops")
      return V2.el("path", { d: `M ${cx - 9} ${eyeY - 6} L ${cx + 4} ${eyeY} L ${cx - 9} ${eyeY + 6}`, transform: cx > 0 ? `translate(${2 * cx},0) scale(-1,1)` : undefined, stroke: ink, "stroke-width": 6, fill: "none", "stroke-linecap": "round", "stroke-linejoin": "round" }, gg);
    if (expr === "dizzy")
      return V2.el("path", { d: `M ${cx - 7} ${eyeY - 7} L ${cx + 7} ${eyeY + 7} M ${cx + 7} ${eyeY - 7} L ${cx - 7} ${eyeY + 7}`, stroke: ink, "stroke-width": 5, "stroke-linecap": "round", fill: "none" }, gg);
    if (blink >= 0.95) {
      V2.el("path", { d: `M ${cx - 12} ${eyeY + 1} Q ${cx} ${eyeY + 8} ${cx + 12} ${eyeY + 1}`, stroke: ink, "stroke-width": 5, fill: "none", "stroke-linecap": "round" }, gg);
      if (expr === "tired")
        V2.el("path", { d: `M ${cx - 12} ${eyeY + 15} Q ${cx} ${eyeY + 22} ${cx + 12} ${eyeY + 15}`, stroke: "#8C7AA6", "stroke-width": 4.5, fill: "none", "stroke-linecap": "round", opacity: 0.85 }, gg);
      return;
    }
    const big = expr === "shock";
    const rx = big ? 11 : 7, ry = (big ? 13 : 10) * open;
    V2.el("ellipse", { cx: cx + ex, cy: eyeY + (lid ? 3 : 0), rx, ry, fill: ink }, gg);
    if (big && open > 0.5) V2.el("circle", { cx: cx + ex + 3.5, cy: eyeY - 4, r: 3.4, fill: "#fff" }, gg);
    if (lid)
      V2.el("path", { d: expr === "tired" ? `M ${cx - 13} ${eyeY - 1} Q ${cx} ${eyeY - 5} ${cx + 13} ${eyeY - 1}` : `M ${cx - 12} ${eyeY - 4} L ${cx + 12} ${eyeY - 2}`, stroke: ink, "stroke-width": 4, "stroke-linecap": "round", fill: "none" }, gg);
    if (expr === "tired")
      V2.el("path", { d: `M ${cx - 12} ${eyeY + 14} Q ${cx} ${eyeY + 21} ${cx + 12} ${eyeY + 14}`, stroke: "#8C7AA6", "stroke-width": 4.5, fill: "none", "stroke-linecap": "round", opacity: 0.85 }, gg);
  };
  const brows = {
    neutral: "", happy: "",
    smug: `M -34 ${eyeY - 22} L -12 ${eyeY - 20} M 12 ${eyeY - 26} L 34 ${eyeY - 30}`,
    shock: `M -32 ${eyeY - 28} Q -21 ${eyeY - 36} -10 ${eyeY - 29} M 10 ${eyeY - 29} Q 21 ${eyeY - 36} 32 ${eyeY - 28}`,
    worried: `M -32 ${eyeY - 18} L -12 ${eyeY - 26} M 12 ${eyeY - 26} L 32 ${eyeY - 18}`,
    oops: `M -32 ${eyeY - 20} L -12 ${eyeY - 16} M 12 ${eyeY - 16} L 32 ${eyeY - 20}`,
    cool: "", dizzy: "",
    tired: `M -33 ${eyeY - 17} Q -22 ${eyeY - 21} -11 ${eyeY - 19} M 11 ${eyeY - 19} Q 22 ${eyeY - 21} 33 ${eyeY - 17}`,
  };
  const mY = HEAD.y + 28;
  const mouths = {
    neutral: `M -10 ${mY} Q 0 ${mY + 4} 10 ${mY}`,
    happy: null, /* filled shape below */
    smug: `M -12 ${mY + 2} Q 4 ${mY + 8} 16 ${mY - 6}`,
    shock: null, worried: `M -16 ${mY + 4} Q -8 ${mY - 4} 0 ${mY + 4} Q 8 ${mY + 12} 16 ${mY + 4}`,
    oops: null, cool: `M -12 ${mY + 2} Q 4 ${mY + 8} 16 ${mY - 6}`,
    dizzy: `M -14 ${mY + 4} Q -7 ${mY - 4} 0 ${mY + 4} Q 7 ${mY + 12} 14 ${mY + 4}`,
    tired: `M -11 ${mY + 4} Q 0 ${mY} 11 ${mY + 4}`,
  };
  eye(-21); eye(21);
  if (brows[expr]) V2.el("path", { d: brows[expr], stroke: ink, "stroke-width": 5, fill: "none", "stroke-linecap": "round" }, gg);
  if (expr === "happy") V2.el("path", { d: `M -18 ${mY - 4} Q 0 ${mY + 20} 18 ${mY - 4} Z`, fill: ink }, gg);
  else if (expr === "shock") V2.el("ellipse", { cx: 0, cy: mY + 4, rx: 10, ry: 14, fill: ink }, gg);
  else if (expr === "oops") {
    V2.el("rect", { x: -18, y: mY - 6, width: 36, height: 16, rx: 6, fill: ink }, gg);
    V2.el("path", { d: `M -14 ${mY + 2} L 14 ${mY + 2}`, stroke: "#fff", "stroke-width": 3 }, gg);
  } else V2.el("path", { d: mouths[expr], stroke: ink, "stroke-width": 5, fill: "none", "stroke-linecap": "round" }, gg);
  if (expr === "shock" || expr === "oops")
    V2.el("path", { d: `M 52 ${HEAD.y - 30} q 6 10 0 16 q -6 -6 0 -16 Z`, fill: "#8FD3FF" }, gg);
  /* the eyes light up (a power, a realisation) */
  if (pose.glint > 0.01 && blink < 0.95) {
    [-21, 21].forEach((cx) => {
      if (farHidden && Math.sign(cx) === farSide) return;
      const gl = V2.el("g", { opacity: Math.min(1, pose.glint) }, gg);
      V2.el("circle", { cx: cx + ex, cy: eyeY, r: 17, fill: pose.glintColor, opacity: 0.2 }, gl);
      V2.el("circle", { cx: cx + ex, cy: eyeY, r: 12, fill: pose.glintColor, opacity: 0.28 }, gl);
      V2.el("ellipse", { cx: cx + ex, cy: eyeY + (lid ? 3 : 0), rx: 8, ry: Math.max(2, 11 * open), fill: pose.glintColor }, gl);
      V2.el("circle", { cx: cx + ex + 2.5, cy: eyeY - 3, r: 2.6, fill: "#FFFFFF" }, gl);
    });
  }
};

/* ---------- the Hero: draw order = depth, rim light, contact shadow ---------- */
V2.Hero = (pose, look, rimId, shadow, parent) => {
  const L = look || V2.LOOKS.kip;
  const j = V2.joints(pose);
  const HEAD = RIG.HEAD;
  const g = V2.el("g", {}, parent);
  /* contact shadow */
  if ((shadow === undefined ? 1 : shadow) > 0)
    V2.el("ellipse", { cx: pose.x, cy: pose.y + RIG.LEG_LEN * pose.scale + 10, rx: 70 * pose.scale, ry: 12 * pose.scale, fill: "#000", opacity: 0.25 * (shadow === undefined ? 1 : shadow) }, g);
  const body = V2.el("g", { transform: `translate(${pose.x} ${pose.y}) scale(${pose.scale}) rotate(${pose.spin} 0 -90)`,
    filter: `url(#${rimId || "vRimR"})` }, g);
  const inner = V2.el("g", { transform: `translate(0 ${RIG.LEG_LEN}) scale(${1 + 0.6 * pose.squash} ${1 - pose.squash}) translate(0 ${-RIG.LEG_LEN})` }, body);
  /* limbs: light fill + dark outline, so they read on dark sets */
  const limb = (o, w) => {
    const d = `M ${o.root.x} ${o.root.y} L ${o.mid.x} ${o.mid.y} L ${o.end.x} ${o.end.y}`;
    V2.el("path", { d, stroke: L.line, "stroke-width": w + 7, fill: "none", "stroke-linecap": "round", "stroke-linejoin": "round" }, inner);
    V2.el("path", { d, stroke: L.limb, "stroke-width": w, fill: "none", "stroke-linecap": "round", "stroke-linejoin": "round" }, inner);
  };
  const shoe = (o) =>
    V2.el("ellipse", { cx: o.end.x + pose.facing * 9, cy: o.end.y + 4, rx: 24, ry: 12, fill: L.shoe, stroke: L.line, "stroke-width": 4 }, inner);
  /* mitten hands: open (palm + thumb + knuckles) or point (fist + index) */
  const hand = (o, side, kind) => {
    const ang = (Math.atan2(o.end.x - o.mid.x, o.end.y - o.mid.y) * 180) / Math.PI;
    const h = V2.el("g", { transform: `translate(${o.end.x} ${o.end.y}) rotate(${-ang})` }, inner);
    if (kind === "point") {
      V2.el("rect", { x: -4, y: 10, width: 8, height: 24, rx: 4, fill: L.hand, stroke: L.line, "stroke-width": 3.5 }, h);
      V2.el("path", { d: "M -11 -2 Q -14 14 -6 18 L 7 18 Q 14 14 11 -2 Z", fill: L.hand, stroke: L.line, "stroke-width": 4, "stroke-linejoin": "round" }, h);
      V2.el("ellipse", { cx: side * 10, cy: 6, rx: 4.5, ry: 7, fill: L.hand, stroke: L.line, "stroke-width": 3.5 }, h);
    } else {
      V2.el("ellipse", { cx: side * 10, cy: 3, rx: 5.5, ry: 9, transform: `rotate(${side * -28} ${side * 10} 3)`, fill: L.hand, stroke: L.line, "stroke-width": 4 }, h);
      V2.el("ellipse", { cx: 0, cy: 10, rx: 11, ry: 15, fill: L.hand, stroke: L.line, "stroke-width": 4 }, h);
      V2.el("path", { d: "M -4 17 L -4 23 M 3 18 L 3 24", stroke: L.line, "stroke-width": 2, opacity: 0.45, "stroke-linecap": "round" }, h);
    }
  };
  const kw = turnWidth(pose.yaw);
  /* torso: jacket + shade + seam + collar */
  const torso = V2.el("g", { transform: `rotate(${pose.tilt}) translate(${pose.yaw * 6} 0) scale(${kw} 1)` }, inner);
  V2.el("path", { d: "M -46 -112 Q 0 -124 46 -112 L 40 2 Q 0 12 -40 2 Z", fill: L.jacket, stroke: L.line, "stroke-width": 4, "stroke-linejoin": "round" }, torso);
  V2.el("path", { d: "M 10 -116 Q 30 -114 46 -112 L 40 2 Q 26 8 12 9 Z", fill: L.jacketShade, opacity: 0.55 }, torso);
  V2.el("path", { d: "M 0 -112 L 0 4", stroke: L.jacketShade, "stroke-width": 4 }, torso);
  V2.el("path", { d: "M -22 -118 Q 0 -100 22 -118", stroke: L.accent, "stroke-width": 6, fill: "none", "stroke-linecap": "round" }, torso);
  /* draw order: far side first, so a turned body overlaps itself correctly */
  if (pose.yaw < 0) { limb(j.legR, 14); shoe(j.legR); limb(j.legL, 14); shoe(j.legL); }
  else { limb(j.legL, 14); shoe(j.legL); limb(j.legR, 14); shoe(j.legR); }
  if (pose.yaw < 0) { limb(j.armR, 12); hand(j.armR, -1, pose.handR); }
  else { limb(j.armL, 12); hand(j.armL, 1, pose.handL); }
  /* the hood: dark shell drawn UNDER the head so the face stays visible;
     drawstrings sway a beat behind the body */
  if (L.extra === "hood") {
    const hg = V2.el("g", { transform: `rotate(${pose.tilt}) rotate(${pose.headTilt * 0.5} 0 ${HEAD.y + 40})` }, inner);
    V2.el("path", { d: `M -70 ${HEAD.y + 14} Q -80 ${HEAD.y - 74} 0 ${HEAD.y - 80} Q 80 ${HEAD.y - 74} 70 ${HEAD.y + 14} Q 52 -100 0 -106 Q -52 -100 -70 ${HEAD.y + 14} Z`, fill: L.jacket, stroke: L.line, "stroke-width": 4 }, hg);
    const sw = pose.sway * 0.7 - pose.tilt * 0.6;
    V2.el("path", { d: `M -12 -108 Q ${-14 + sw * 0.3} -88 ${-16 + sw} -66 M 12 -108 Q ${14 + sw * 0.3} -88 ${16 + sw} -66`, stroke: L.accent, "stroke-width": 5, "stroke-linecap": "round", fill: "none" }, hg);
    V2.el("circle", { cx: -16 + sw, cy: -64, r: 5, fill: L.accent }, hg);
    V2.el("circle", { cx: 16 + sw, cy: -64, r: 5, fill: L.accent }, hg);
  }
  /* head group */
  const head = V2.el("g", { transform: `rotate(${pose.tilt}) rotate(${pose.headTilt} 0 ${HEAD.y + 40})` }, inner);
  V2.el("circle", { cx: HEAD.x, cy: HEAD.y, r: HEAD.r, fill: L.skin, stroke: L.line, "stroke-width": 4 }, head);
  V2.el("path", { d: `M ${HEAD.x + 14} ${HEAD.y + 58} A ${HEAD.r} ${HEAD.r} 0 0 0 ${HEAD.x + 60} ${HEAD.y + 14} A 70 70 0 0 1 ${HEAD.x + 14} ${HEAD.y + 58} Z`, fill: L.skinShade }, head);
  if (L.extra !== "hood")
    V2.el("path", { transform: `translate(${-pose.yaw * 16} 0)`, d: `M -6 ${HEAD.y - 60} q 10 -26 30 -18 q -16 2 -14 16 q -8 -10 -16 2 Z`, fill: L.hair }, head);
  const faceG = V2.el("g", {}, head);
  const savedRoot = V2.root; V2.root = faceG;
  Face(pose, L);
  V2.root = savedRoot;
  if (pose.yaw < 0) { limb(j.armL, 12); hand(j.armL, 1, pose.handL); }
  else { limb(j.armR, 12); hand(j.armR, -1, pose.handR); }
  return g;
};
