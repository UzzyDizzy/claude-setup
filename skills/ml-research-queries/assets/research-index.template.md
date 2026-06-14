<!--
research-index.md — REPO + EXPERIMENT MAP. Lives in the PROJECT ROOT.
Updated by ml-research-queries AFTER EVERY COMPLETED EXECUTION (any run that created/changed files
or produced results). Keep it consistent with disk and the codebase artifact; never invent paths.
Copy this template to ./research-index.md on first run.
-->

# Research Index
_Updated after each completed execution · Last: <YYYY-MM-DD HH:MM>_

## Folder Map  (respect the depth policy in research-status.md §4)
```
.
├── config.py
├── models.py
├── train.py
├── data/            # exempt — may nest
└── saved_models/    # exempt — may nest
```

## Files
| Path | Purpose | Key functions / classes | Status |
|------|---------|-------------------------|--------|
| config.py | hyperparams + paths | `Config` | done |
| models.py | model defs | `build_model()` | wip |

## Function / entry-point index
| Symbol | File:line | Signature | Called by |
|--------|-----------|-----------|-----------|
| `train()` | train.py:42 | `train(cfg) -> Metrics` | `__main__` |

## Experiments
| ID | Config | Status | Result artifact | Maps to goal | Conclusion |
|----|--------|--------|-----------------|--------------|------------|
| exp-001 | baseline | planned | — | Goal A | — |

## Datasets / checkpoints
| Name | Path | Size | Notes |
|------|------|------|-------|
| train split | data/train/ | <> | <> |
