# short-0007 — "What if you were the last doctor on Earth?"

Rebuild note: the original build (day-020 session) died in a sandbox failure with
the content uncommitted and was wiped; this file re-authors it from the surviving
brief (`research/video-notes/alignment-emotion-whatif.md`, 9/10 alignment — the
channel's highest-alignment pitch on the board) with every r1–r5 gate directive
from that session baked in from the start.

## Identity

- **Premise:** you wake up the only doctor left. One patient. No backup, no grid,
  no resupply. Compassion + dread + duty (the register our views.csv already
  proved: emotion-framed explainainers run +160–480% over concept-clean ones).
- **Imprint / stamp:** `SOMEONE ALWAYS HAS TO STITCH.` — the deliberate loop back
  into #0006's closer word ("stitch"). s10 is the "Because" line that triggers the
  linter's closer-entity heuristic (expected WARN, not a defect).
- **Register:** engineer-flat serious narration (brief), no scary-music runs.
- **Zero-politics scrub (brief, non-negotiable):** no war, no geography, no
  "last war on earth" framing, no digits in narration (L-090/L-073 scrub —
  facts stay qualitative), noun in beat 1 ("doctor").

## Beats (hook + 12 scenes; s5 is visual-only — the operation is the event)

| id | narration | words | event (C18, lands u≥0.8) |
|---|---|---|---|
| hook | You're the last doctor on Earth. Nobody is coming. | 9 | title ON frame-0 (thumbnail rule beats audio-led preference — r3 directive), one heartbeat pulse in the lamp glow |
| s0 | One patient is still breathing in your dark ward. | 9 | the sheet rises and falls twice; doctor's hand lands on the rail at u≈0.7 |
| s1 | The blood bank keeps for a few weeks. Then it's empty. | 11 | three blood bags grey out one by one (countable, colour cue visible — r4) |
| s2 | Insulin survives only in the cold. The power died last night. | 11 | ice-pack frost breath; the ward's back lights die at "power" |
| s3 | Triage is simple now. Save the ones you can reach. | 10 | corridor of empty beds; two grey out, one stays warm |
| s4 | Your hands remember what the machines used to know. | 9 | monitor + ventilator ghost-fade out; hands flex |
| s5 | — (visual-only, ~2.4 s) | 0 | THE OPERATION: five stitches close the wound, last one lands u≥0.8, each with a tick ring |
| s6 | Out there, whole towns are still waiting for help. | 9 | window pull-back: dark town skyline, a few lit windows |
| s7 | The last supply truck never made it. | 7 | the truck dominates the frame (r4), headlights dim to dark |
| s8 | You mark every town you couldn't reach. | 7 | pen X-marks land on labelled map dots while the camera slides (static-map risk mitigated — critic note) |
| s9 | At dawn, you still have one patient, one job. | 9 | the window turns gold; first warm light in the ward (G9 pivot) |
| s10 | Because someone always has to stitch. | 6 | quiet close-up: doctor steady at the bedside, ECG steady |
| s11 | So you wash your hands, check the lamp, and begin again. | 11 | loop scene: hook's wide ward frame; the lamp flickers back ON; STAMP pops: SOMEONE ALWAYS HAS TO STITCH |

108 narrated words + a 2.4 s visual beat; rhythm 9,9,11,11,10,9,(0),9,7,7,9,6,11
(S8 variety ✓, no scene over ~3.4 s ✓, 13 beats ✓, opener 9w ✓, no digits ✓).

## Facts (S7 — cited, narration stays qualitative)

- **Blood shelf (s1):** FDA/CBER + AABB standards — stored red blood cells are
  transfusable for weeks depending on anticoagulant (platelets far less). Kept as
  "a few weeks".
- **Insulin cold chain (s2):** WHO / MedlinePlus guidance — insulin must stay
  refrigerated (~2–8 °C); heat degrades it. Kept as "only in the cold".
- **Triage doctrine (s3):** ATLS / START (American College of Surgeons) — in
  mass-casualty conditions, treat the survivable; greatest good for the greatest
  number. Kept as "save the ones you can reach".

## Visual world (v3, one continuous take)

One dark hospital ward at night. ONE lit bed under a surgical lamp cone — the
single visible light source (vGlow warm, cream shaft); everything else falls to
the bible's deep-space darks with a readable floor (bottom-third content — r2
directive) and a horizon band. The hero doctor recurs in hook, s0, s3, s4, s5,
s8, s9, s10, s11 (hero threading — r1 directive). ECG teal line = the recurring
data accent; amber lamp = the warm accent (one per scene, bible §1).

r1–r5 learnings baked in from frame one (do not relearn):
- title on frame-0 of the hook, not mid-scene (r1→r3)
- exposure: the lit zone reads as DARK-AND-LIT, never dead void (r3/r4 lifts)
- tighter cameras on the small-count scenes s1/s2/s3/s9 (r1)
- s7 truck dominant in frame (r4)
- labels with margins; blood-colour cue clearly visible (r4)

## Audio

edge-tts en-US-AndrewNeural, rate +15% (engineer-flat, mid-band ~202 WPM),
VO_GAP_S=0.25. SFX table in script.json: heartbeat thump under the hook, five
stitch ticks in s5, whoosh on the s6 pull-back, a soft thump when the truck
dies, a low riser into the dawn, blip + stamp thump in s11. Bed: the L-124
redesign (high pad + room tone) — this is the first short that ships it.
bed_peak 0.05, duck −12 dB.
