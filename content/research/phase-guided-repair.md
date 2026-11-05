---
date: '2026-11-05'
type: Experiment
title: 'Phase-guided program repair: an initial study'
title_zh: 分阶段程序修复：初步实验
summary: The repair lifecycle works in integration tests; five real-model probes produced
  no promoted candidate.
summary_zh: 修复流程通过了集成检查；五次真实模型尝试均未产生晋升候选。
topics:
- Agents
- Physical RSI
featured: true
---

## The question

Can an explicit phase plan and recall of earlier repairs help a model develop a successful robot program? The optional `harness.program` strategy combines phase planning, bounded program development and evidence-linked repair notes.

## Method

The strategy asks for observable phases, completion conditions, fallbacks and step budgets. It runs a development session on `search` cases. All selected development cases must succeed before a candidate reaches selection and an independent gate. Repair notes reference failed cases and successful replays and become available only from active, promoted lineages.

This is an independent design adaptation inspired by HarnessPAI. The pinned upstream project had no project licence; no upstream source, prompts or templates were copied. It is not a reproduction of the authors' benchmark result.

## Results

The November 4, 2026 record contains five real-model probes:

| Probe | Model | Outcome |
|---|---|---|
| v1 | gpt-oss:20b | No submitted program; tool-call mistakes and token-budget exhaustion |
| v2 | qwen3.5:35b-a3b | Planning timed out; no completed model reply |
| v3 | gpt-oss:20b | No submitted program; incomplete toolkit context |
| v4 | gpt-oss:20b | No submitted program; definitions changed without submission |
| v5 | gpt-oss:20b | Four submissions; each solved 0/2 development cases |

No candidate reached gate or held-out evaluation. No repair notes were admitted from these real-model attempts. A scripted-model integration test exercised repair, gate, approval, recall and rollback; that validates orchestration rather than autonomous task improvement.

## Scope and limitations

The probes used a CPU toy environment with red/blue block instructions and privileged test-double perception. They were not RoboMME, MIKASA-Robo or deployment-observation-only robot evaluations. Model-inference hardware was not established by the record.

The final four submissions are adaptive revisions on the same two cases, not eight independent benchmark samples. The observed program targeted the red block under both instructions. Correct workflow mechanics did not compensate for weak program synthesis.

## Reproduce and inspect

- [Strategy and reproduction record](/hylo-docs/developer-guide/validation/phase-guided/) includes the implementation, source paths and experimental conditions.
- [Program-development guide](/hylo-docs/user-guide/research-and-skills/) describes how the strategy fits the campaign lifecycle.
- [Dated experiment record](https://github.com/HyloAI/hylo-docs/blob/c2de438c9219ac27106067f10b83f3c9c3010dcb/docs/research/experiments/2026-11-04-harness-program-evolution.md) preserves the complete attempt history.
- [Machine-readable results](/research/data/phase-guided-repair.json) retain outcome counts and evidence hashes.
