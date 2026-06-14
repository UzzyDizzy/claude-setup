---
name: ml-content-researcher
description: >-
  Use whenever an ML research task needs grounding in the literature: surveying prior work, finding
  the current SOTA, locating the strongest baselines, checking whether an idea already exists, or
  sharpening a research gap into something defensible. Trigger on "related work", "is this novel",
  "what's SOTA on X", "find papers / baselines for Y", "literature review", or any moment a claim of
  novelty or a method choice needs evidence. Built for token economy — search in tight passes,
  extract only decision-relevant facts, and write findings back to research-status.md instead of
  pasting walls of text. Pairs with ml-research-queries (Phase 2 goal discovery) and
  ml-experiment-designer (choosing baselines).
---

# ML Content Researcher

Ground research decisions in evidence **cheaply**. The goal is not a long survey; it is the few facts
that change a decision: what's already done, what the strongest baseline is, and where the real gap
sits. Optimize for signal per token.

## Tools, in priority order
1. **Consensus** (`Consensus:search`) — peer-reviewed claims with citations; best first stop for
   "does method X beat Y on Z".
2. **web_search / web_fetch** — arXiv, papers-with-code, official repos, blogs. Fetch the source for
   numbers; snippets are too thin to cite a result.
3. Prefer original sources (paper, official repo, leaderboard) over aggregators and forums.

## Search discipline (token economy)
- One tight query per sub-question; 1–6 words; reformulate rather than repeat.
- Scale passes to the question: a single novelty check ≈ 2–4 searches; a gap/SOTA map ≈ 6–12. Stop
  when the next search wouldn't change a decision.
- Search each distinct method/dataset separately — combined queries return shallow results for all.
- Pull exact figures (metric, dataset, split) only from the fetched source; paraphrase everything,
  quote almost never (<15 words, one per source).

## What to extract (and nothing more)
For each relevant work, capture only: method one-liner · key result (number + dataset + metric) ·
the limitation that leaves room · link. Drop everything that doesn't move a decision.

## Output — write it where it's reused
Return a compact table to the user **and** append the distilled version to `research-status.md`
(§2 Topic and §5 Goals) so the orchestrator can derive goals without re-searching:

```
| Work (year) | Method (1 line) | Best result (dataset/metric) | Gap it leaves | Link |
```
Then one paragraph: **where the defensible gap is** and **which 1–2 baselines to beat**. Hand the
baseline choice to `ml-experiment-designer`; hand a sharpened gap back to `ml-research-queries`.

## Guardrails
- Don't overstate novelty from absence of search hits — say "no direct prior work found in N passes",
  not "this is novel". Let the evidence stay tentative.
- Distinguish reported vs reproduced numbers; note when a result is author-reported only.
