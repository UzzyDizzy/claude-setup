<!--
research-status.md — DURABLE PROJECT MEMORY. Lives in the PROJECT ROOT.
Updated by ml-research-queries AFTER EVERY PROMPT. Edit stored answers only when the user says so.
Copy this template to ./research-status.md on first run; do not edit it in the skill folder.
-->

# Research Status
_Last updated: <YYYY-MM-DD HH:MM> · Session: <n> · Mode: scratch | resume_

## 0. Orientation
- Mode: <scratch | resume>
- Codebase tool: <graphify | understand-anything | none>
- Codebase artifact path: <./path/to/wiki-or-understanding.md>
- Last refreshed: <YYYY-MM-DD HH:MM>

## 1. Research Type
- [ ] Architecture / framework pipeline
- [ ] Conclusion via experiments
- [ ] Benchmark / dataset creation
_(one or a combination)_

## 2. Topic / Research Gap
<one or two sentences — scratch only>

## 3. Budget
- GPUs: <type · count · hours>
- APIs: <which · credit limit>
- Total cost / credit ceiling: <>
- Target system available now: <yes | no> — specs: <>

## 4. Folder Depth Policy
- Max CODE depth: <0 | 1 | 2 | …>
- Exempt (may nest freely): data/, saved_models/, checkpoints/, logs/, outputs/, <add…>

## 5. Research Goals  (candidates → selected)
- [x] <Goal A> — selected
- [ ] <Goal B>
- [ ] <Goal C>
_(every conclusion must map back to a selected goal)_

## 6. Architecture Spec
- Target complexity: <params / FLOPs / latency band>
- Must have: <>
- Must NOT have: <>
- Tech-merge idea (new contribution): <>
- Success criterion (ends Phase 4): <>

## 7. Experiment Plan
- Conclusive experiments target: <N>
- Ablations per pipeline: <N>
- Specific settings (metric / split / seeds / baseline to beat): <>

## 8. Backbone / External Models
- Backbone required: <yes | no>
- Backbone (OPEN-SOURCE only): <name · HF/repo id>
- Pipeline-only model: <name> served via <api | local>
- Reusable public code / deployed endpoint: <link>

## 9. Verification Policy
- Mode: <deterministic-only | full-on-target>
- Reason: <budget / system availability>

## 10. Open Questions  (deferred — never forgotten)
- [ ] <question> — trigger: <phase / condition that makes it active>

## 11. Decisions Log  (append-only, immutable)
- <YYYY-MM-DD>: decided <X> because <Y>.
