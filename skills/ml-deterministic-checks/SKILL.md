---
name: ml-deterministic-checks
description: >-
  Use before trusting that ML code will run — especially before launching any heavy/expensive job.
  Trigger on "will this run", "verify the code", "dry run", "shape check", "smoke test", "did I break
  training", "check before I submit the job", or any point where code is about to consume real GPU/API
  budget. It runs the strongest checks possible WITHOUT the full job — import/build, tensor
  shape/dtype flow, a 1–2 step forward+backward on tiny fake data, seed reproducibility, config
  validation — and only escalates to a real heavy run when the target system is available now. Reads
  the verification policy + budget from research-status.md; pairs with ml-pipeline-architect (after a
  build) and ml-experiment-designer (before full runs).
---

# ML Deterministic Checks

Catch failures with the cheapest test that would catch them. The default is to **prove the code will
run** without paying for a full job; escalate to a real run only when budget §3 says the target system
is available now (verification mode §9 = `full-on-target`).

## Decision: which mode
- `deterministic-only` (low-end dev machine, or budget says so) → run the deterministic battery below;
  do **not** download target-only heavy deps or launch real training.
- `full-on-target` (target hardware available now) → run the deterministic battery first, then a real
  short run, then the full job. Never skip the cheap battery — it turns a 6-hour failure into 6 seconds.

## Deterministic battery (cheap → strong)
1. **Static / import.** Byte-compile (`python -m py_compile`), import every module, resolve configs.
   Optional: type/lint pass. Catches syntax, bad imports, undefined names.
2. **Shape & dtype flow.** Build the model on `meta`/CPU with tiny dims; push one fake batch through;
   assert output shape/dtype and that the loss is a finite scalar. Catches the most common ML bugs
   without a GPU.
3. **One-step train.** 1–2 optimizer steps on a handful of synthetic samples; assert loss is finite,
   that it changes, and that named params received non-zero grads (catches detached graphs / frozen
   layers). Tiny batch, tiny model, CPU.
4. **Determinism.** Fix all seeds; run step 3 twice; assert identical loss/first-batch outputs.
   Non-reproducible → an unseeded op exists; locate it before scaling.
5. **Config / budget guards.** Validate required keys, paths exist (or are creatable), and the
   declared run cost fits the §3 ceiling. Fail loudly with the offending key.

Prefer real CPU execution over mocks — running tiny is more convincing than asserting on stubs.
Keep these as reusable functions/CLI flags (e.g. `--check`) so every change re-verifies fast.

## When the target system is available now (full-on-target)
After the battery passes: short real run (a few hundred steps, real data subset, 1 GPU) to confirm
throughput and memory; check it fits VRAM and the GPU-hour budget; only then launch the full job. If
heavy target-only deps are needed, install them only in this mode.

## Output (one line per check)
```
[pass/fail] <check> — <evidence>     e.g.  [pass] shape-flow — logits (8,10) float32, loss 2.31 finite
```
End with a go / no-go: list any failing check and the exact fix before re-running. No green battery →
no full job.
