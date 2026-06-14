---
name: ml-experiment-designer
description: >-
  Use when an ML project needs to decide WHICH experiments and ablations to run to actually settle a
  claim, and how to fit them in the compute budget. Trigger on "what experiments should I run", "how
  many ablations", "design the experiment", "is one run enough", "which baselines", "what's the
  minimal set to prove X", or any point where runs are about to be launched and their design isn't
  pinned down. It turns selected research goals into the SMALLEST set of runs whose outcomes are
  decision-changing, assigns seeds/splits/metrics, and budgets GPU-hours so the project converges
  instead of sprawling. Reads budget + goals from research-status.md; pairs with
  ml-content-researcher (baselines) and ml-deterministic-checks (verify before full runs).
---

# ML Experiment Designer

Design the **fewest** experiments whose results would change what you conclude. Every run must be tied
to a selected goal and must be falsifiable — if no outcome would change your mind, don't run it.

## Inputs (pull from research-status.md, don't re-ask)
Selected goals (§5) · budget: GPU-hours, APIs, ceiling (§3) · conclusive-experiment and ablation
targets (§7) · baselines from `ml-content-researcher`.

## Method
1. **Claim → experiment.** For each selected goal, write the claim as a testable hypothesis and the
   single comparison that would confirm or refute it (method vs baseline on metric+dataset).
2. **Minimal conclusive set.** Keep only experiments whose result is decision-changing. Merge runs
   that share a control. Cut anything that just "looks thorough".
3. **Ablations = one knob at a time.** Each ablation isolates exactly one component to attribute the
   effect. Order by expected information gain; stop at the §7 target unless a result demands one more.
4. **Controls.** Fix seeds (report ≥3 for any headline number), splits, metric, and the baseline to
   beat. Identical preprocessing across arms — the only difference is the variable under test.
5. **Budget fit.** Estimate cost per run (steps × step-time × seeds) and sum. If it exceeds the
   ceiling, shrink the grid (fewer seeds on ablations, smaller proxy model, shorter schedule for the
   sweep then full only on the winner) before asking for more compute.

## Output (compact, and append to research-index.md Experiments table)
```
| Exp ID | Goal | Hypothesis | Arms (method vs baseline) | Metric/dataset | Seeds | Est. GPU-h | Decision rule |
```
- **Decision rule** = the threshold that makes the result conclusive (e.g. "≥1.0 pt over baseline
  across 3 seeds, non-overlapping CI"). No decision rule → not ready to run.
- Mark which runs are the conclusive set vs ablations vs the sweep.

## Guardrails
- Prefer a proxy/sanity scale to de-risk the design, then full scale once the design holds.
- Always route the chosen design through `ml-deterministic-checks` before any full job.
- Underpowered comparisons (1 seed, no CI) are not conclusive — say so rather than over-claiming.
