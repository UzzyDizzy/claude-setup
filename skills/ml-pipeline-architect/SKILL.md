---
name: ml-pipeline-architect
description: >-
  Use when designing or laying out the CODE for an ML project: the model/pipeline architecture, the
  repo's folder structure, how to merge two techniques into one design, or how to wire in an
  open-source backbone or an API/local model. Trigger on "design the architecture", "how should I
  structure the repo", "where do these files go", "which backbone", "set up the pipeline", "combine X
  and Y", or any moment before code is written for a new component. It enforces the project's
  folder-depth policy, keeps the design minimal and surgical, integrates ONLY open-source backbones,
  and produces a buildable module/function plan. Reads depth policy + backbone choice from
  research-status.md; pairs with ml-experiment-designer and ml-deterministic-checks.
---

# ML Pipeline Architect

Turn an agreed idea into the **smallest buildable structure** that satisfies the goals — no
speculative abstraction. Match the existing repo's style; touch only what the change needs.

## Inputs (from research-status.md — don't re-ask)
Architecture spec §6 (complexity, must-have / must-NOT-have, tech-merge idea, success criterion) ·
folder-depth policy §4 · backbone/model decisions §8 · the codebase artifact (graphify /
understand-anything) for the current layout.

## Folder-depth enforcement (hard rule)
The depth integer in §4 caps **code** nesting; artifact dirs are exempt.

| Depth | Allowed code layout | Example |
|------|----------------------|---------|
| 0 | all code files in root | `config.py`, `models.py`, `data.py`, `train.py`, `eval.py` |
| 1 | one level of code subfolders | `models/`, `data_pipeline/`, `training/` each one deep |
| 2 | two levels | `models/backbones/`, `data_pipeline/loaders/` |

Always exempt (may nest freely): `data/`, `saved_models/`, `checkpoints/`, `logs/`, `outputs/`,
`configs/` artifacts. If a clean design seems to need more depth than allowed, propose flattening
(longer filenames, not deeper trees) or ask the user to raise §4 — don't silently exceed it.

## Designing the architecture
1. **Restate the contribution** in one line, including the tech-merge idea — that fusion is the novel
   part, so make its interface explicit (where the two techniques meet, what tensor/contract flows).
2. **Module plan.** List modules with a one-line responsibility each, their public function/class
   signatures, and the data contract (shapes/dtypes) between them. Honor must-have / must-NOT-have.
3. **Backbone / external model wiring (§8).** Backbones must be **open-source** — load by HF/repo id,
   pin the version, expose a thin adapter so the rest of the pipeline is backbone-agnostic. For an
   API/local pipeline model, isolate it behind one interface; never hardcode secrets (env vars only).
   Reuse public implementations where §8 names one rather than reimplementing.
4. **Determinism hooks.** Centralize seed, device, and dtype in `config.py`; make every stochastic
   op seedable so `ml-deterministic-checks` can verify reproducibly.
5. **Minimal surface.** Only files the goals require. No frameworks-for-one-call, no premature config
   systems. Simplicity first.

## Output (and update research-index.md)
- A file/module map within the depth policy + a per-module signature list + the inter-module data
  contracts. Then update `research-index.md` (Folder Map, Files, Function index).
- Hand the build to implementation, then to `ml-deterministic-checks` before any heavy run.

## Guardrails
- Closed-weight models are not valid backbones — flag and substitute an open-source equivalent.
- Keep the diff surgical on existing repos; new abstractions need a concrete second use before they
  earn their place.
