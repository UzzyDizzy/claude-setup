---
name: ml-results-synthesizer
description: >-
  Use when experiments have produced numbers and the project needs CONCLUSIONS — the part that turns
  raw logs into a defensible result. Trigger on "make the results table", "what do the numbers say",
  "compare the ablations", "is the improvement real", "write up the findings", "did we beat the
  baseline", or any point where runs are done and a claim must be stated. It builds the comparison and
  ablation tables, computes deltas with seeds/variance, ties each finding to a research goal, states
  what is and isn't supported, and names the next experiment if the result is inconclusive. Reads
  goals + experiment plan from research-status.md and rows from research-index.md; closes the loop
  opened by ml-experiment-designer.
---

# ML Results Synthesizer

Convert runs into **conclusive substance**: claims that are tied to a goal, supported by the numbers,
and honest about uncertainty. This is where the project pays off — keep it tight and decision-grade.

## Inputs (from the state files)
Selected goals §5 · experiment plan + decision rules §7 · the `research-index.md` Experiments table
(IDs, configs, result artifacts).

## Build the result
1. **Main comparison table.** Method vs baseline(s) on the headline metric/dataset, with mean ± std
   over seeds. Bold the best; mark which arm is the contribution.
   ```
   | Method | Dataset/Metric | Mean ± std (n seeds) | Δ vs baseline | Decision rule met? |
   ```
2. **Ablation table.** One row per ablated component showing the metric with it removed/changed and
   the attributable delta — so the reader sees what each piece contributes.
   ```
   | Variant | Change from full | Metric | Δ from full | Reading |
   ```
3. **Is it real?** Apply the §7 decision rule. Report variance, not just a point estimate; with ≥3
   seeds give std or a simple CI and state whether arms overlap. A single-seed win is "suggestive",
   not "conclusive" — label it so.
4. **Tie to goals.** For each selected goal: Supported / Partially / Not supported, with the table row
   as evidence. Findings that map to no goal are noise — drop or flag them.
5. **If inconclusive,** say exactly why (underpowered, confound, ceiling) and name the single next
   experiment that would settle it — hand that back to `ml-experiment-designer`.

## Output
The two tables + a short findings paragraph (goal → verdict → evidence) + an explicit
limitations/threats line. Then update `research-index.md` Experiments rows with status and the
one-line conclusion per experiment.

## Guardrails
- Never round a non-significant gap into a win; report negative/flat results plainly — they are
  results.
- Keep reported vs reproduced numbers distinct; note seeds and exact dataset/split next to every
  figure so the claim is checkable.
