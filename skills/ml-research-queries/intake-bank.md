# Intake bank — exact wording for Q1–Q10

Read this when the orchestrator needs precise phrasing, options, or the backbone sub-questions.
Each entry lists: the phase that activates it, the question, and how to record the answer in
`research-status.md`. Ask in small batches (≤3), never all at once.

## Table of contents
- Q1 Codebase understanding (graphify / understand-anything)
- Q2 Research type
- Q3 Budget
- Q4 Folder-depth policy
- Q5 Architecture + experiment specifics
- Q6 Backbone / external models (conditional)
- Q7 Verification mode
- Q8 Research index (no question — a write rule)
- Q9 Topic / research gap (scratch only)
- Q10 Research goals

---

## Q1 — Codebase understanding · Phase 0 (first invocation, then refresh)
> "Are we starting from scratch, or should I first understand an existing repo? And should I run
> **graphify** or **understand-anything** to build/refresh the codebase map?"

- Run the chosen tool; store the artifact **path** and **timestamp** under *Orientation*.
- Refresh rule (mandatory): re-run after any prompt that changed code; update the timestamp.
- Resume default: re-run whatever was chosen before unless the user switches.

## Q2 — Research type · Phase 1
> "What kind of research is this — (a) architecture / framework pipeline, (b) a conclusion drawn
> from experiments, or (c) benchmark / dataset creation? Pick one or a combination."

Record the selected set under *Research Type* as checkboxes.

## Q3 — Budget · Phase 1
> "What's the compute budget? GPUs (type, count, hours), APIs (which, credit limit), and a total
> cost/credit ceiling. Is the target system available **right now**, or are we developing on a
> low-end machine for later?"

Record under *Budget*. The "available now?" answer sets the default for Q7.

## Q4 — Folder-depth policy · Phase 1
> "How deep can the **code** tree go? 0 = everything in root (`config.py`, `models.py`,
> `train.py`, …). 1 = one level of subfolders (e.g. `models/`, `data_pipeline/`). 2 = two levels.
> Artifact dirs (`data/`, `saved_models/`, `checkpoints/`, `logs/`, `outputs/`) are exempt and may
> nest freely."

Record the integer under *Folder Depth Policy*. `ml-pipeline-architect` enforces it.

## Q5 — Architecture + experiment specifics · Phases 3–4
Ask **only specific** questions — no open-ended "what do you want?". Split across experiment design
(Phase 3) and architecture (Phase 4).

Experiment side (Phase 3):
> "How many **conclusive** experiments should land the claim? How many **ablations** per pipeline?
> Any specific setting/protocol this project needs (metric, split, seed policy, baseline to beat)?"

Architecture side (Phase 4):
> "Target complexity (params / FLOPs / latency band)? What must it **have**? What must it **NOT**
> have? Any two technologies to **merge into a new idea** here? What is the explicit success
> criterion that ends this phase?"

Record under *Architecture Spec* and *Experiment Plan*. Hand specifics to `ml-experiment-designer`
and `ml-pipeline-architect`.

## Q6 — Backbone / external models · Phase 4 (ask ONLY if needed)
Branch:
- **Backbone needed for the architecture?**
  > "Which **open-source** model is the backbone? (open-source only — name + Hugging Face / repo id.)"
- **No backbone, model used only inside the pipeline?**
  > "Which model, and how is it served — **API** or **local weights**?"
- **Any sub-component with a public implementation or deployed model?**
  > "Point me to the public code / deployed endpoint so we reuse rather than reimplement."

Rules: backbones must be **open-source**. For API models, record provider + that no secrets go in
code. Record everything under *Backbone / External Models*. `ml-pipeline-architect` wires it in.

## Q7 — Verification mode · Phase 6
> "Should generated code be verified by actually running heavy dependencies on the target system
> (the ones that only run on the budgeted hardware), or do we keep to **deterministic checks** that
> prove it will run without a full job?"

Default from Q3: target-available-now → offer full-on-target; otherwise deterministic-only. Record
under *Verification Policy*. `ml-deterministic-checks` executes the chosen mode.

## Q8 — Research index · all phases (write rule, not a question)
After every completed execution, update `./research-index.md`: folder map, file purposes, key
function/entry-point paths, experiment rows. Never let it drift from disk + the codebase artifact.

## Q9 — Topic / research gap · Phase 1 (scratch only)
> "State the research gap in one or two sentences — the specific thing that's missing or unproven
> that this project will address."

Record verbatim under *Topic / Research Gap*. This seeds Q10.

## Q10 — Research goals · Phase 2
1. Derive **candidate goals** from: the topic (Q9) + the codebase artifact (Q1) + any literature
   from `ml-content-researcher`. List them tersely (one line each).
2. Ask:
   > "Here are the candidate goals I see. Which do you want to target? You can pick several, reword
   > them, or add ones I missed."
3. Record selected vs deferred under *Research Goals*; selected goals drive Phases 3–7 and every
   conclusion must map back to one.
