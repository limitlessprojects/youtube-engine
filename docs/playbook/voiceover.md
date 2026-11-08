# Playbook — Voiceover (stage 2 of 7)

> Purpose: synth narration, measure real durations, ASR-verify, and write the
> synced timeline back into script.json.
> Inputs: `content/<slug>/vo_lines.json` (from stage 1).
> Outputs: `vo/NN.mp3` (00=hook, 01..=scenes), `vo/asr_report.json`, updated
> `script.json` timestamps + `audio_dur_s` + `timeline`.

## Commands

```bash
# Default path (keyless, proven) — rate is PER-SCRIPT (rule V3):
VO_RATE=+25% python3 tools/vo_pipeline.py <slug>          # synth + measure + ASR + timeline
VO_RATE=+25% python3 tools/vo_pipeline.py <slug> --verify-only   # re-ASR existing files

# Optional Fish path (preferred voice, daily free credits, via CI):
#   dispatch .github/workflows/vo-gen.yml with slug (+ optional speed)
#   files land in content/<slug>/vo/fish/NN.mp3 — see dead-ends.md D6 before
#   trusting the speed knob. Decide Fish vs edge by ASR WER first, pacing band
#   as tiebreaker (day-009 rule).
```

The pipeline prints per-line verdicts and writes `asr_report.json`; it also
prints the synced starts — copy them into `script.json` (`hook.timestamp_start=0`,
scenes ascending, `audio_dur_s` per line) and set `timeline.total_s`,
`gap_s` (0.25 brisk / 0.45 default), `voice`, `wpm_measured`.

## Rules that bite here (docs/rules.md §Voice)

V1 measure never estimate · V2 ASR WER ≤0.15 · V3 VO_RATE per script ·
V4 decode-based validation · V6 em-dash → comma (automatic).

## Known failure modes

| Symptom | Cause | Fix |
|---|---|---|
| WPM measured out of 185–215 after synth | text-dependent pacing (238 vs 207 on same voice+rate) | bump `VO_RATE` (±10–20%), re-run; re-check band (rule V3) |
| ASR empty on a line | service flakes when hammered | built-in 2s sleeps + 3 retries; re-run `--verify-only` after cooldown |
| "birds" heard as singular | documented ASR model bias, not a TTS bug | accept (pipeline auto-tags `asr-plural-bias`); control-test per rule G5 before re-cutting |
| Fish files rejected by a validator | raw MPEG frame sync vs ID3 prefix (L-069) | decode-based validation only (vo-gen already fixed) |
| `z-ai asr` 400 error | it accepts WAV only (`-f` not `-i`) | pipeline converts to 16k mono WAV automatically — don't bypass it |

## Acceptance check

- `asr_report.json`: `n_fail: 0`, every line PASS (or PASS with documented bias).
- `script.json` timestamps = the pipeline's printed synced starts (spot-check 2).
- `timeline.wpm_measured` inside 185–215 (rule S5).
