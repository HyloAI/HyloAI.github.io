---
date: '2026-11-05'
type: Study
title: When memory helps—and when it does not
title_zh: 记忆何时有效，何时无效
summary: Paired simulations show a strong occlusion benefit, exploratory action recall
  and limits on transfer.
summary_zh: 配对仿真实验展示遮挡下的收益、动作检索的探索性结果，以及迁移的边界。
topics:
- Memory
- Skills
image: /research/assets/memory-results.png
image_alt: Recorded memory comparisons with confidence intervals
featured: true
---

## The question

Memory can preserve a missing observation, retrieve an action or carry a verified skill. These mechanisms answer different questions. We compare each against its corresponding control rather than combining them into a single memory score.

## Method

The full examples were recorded on November 1, 2026, on a 128-core CPU workstation without a GPU. They use MuJoCo table/planar reach, fixed seeds and paired task instances. No LLM is used. Reported p-values in the source are exact two-sided McNemar tests on discordant pairs.

## Results

| Mechanism and conditions | Control → memory | Interpretation |
|---|---|---|
| Spatial recall; targets visible for only five steps, 300 pairs | 0.00 → 0.75 | Large benefit from retaining target positions; 225 candidate-only wins, no losses |
| Spatial recall; targets always visible | 0.75 → 0.75 | No added benefit when the observation remains available |
| Action recall; revisited scenes | 0.75 → 0.81 | Exploratory; p = 0.29 |
| Action recall; new held-out scenes | 0.69 → 0.75 | Exploratory; p = 0.24 |
| Frozen skill library; 200 fresh paired scenes | 0.47 → 0.86 | One verified noise-scale skill; 85 wins and 6 losses, p = 6e-19 |

Spatial recall does not solve instruction interpretation. Direct and push tasks reach 0.99, while indirect colour instructions reach 0.27 because the rule chooser cannot resolve phrases such as “the colour of a ripe tomato”.

## What limits the conclusion

Action-memory settings were chosen from a sweep on the example's splits, so those p-values are exploratory. Both six-point changes are non-significant. With looser retrieval and a well-tuned policy, a development run lost 11 points on revisited scenes and 12 on new scenes.

The skill-library example relies on a small proposer that suggests a noise-scale change. Its result does not demonstrate autonomous discovery of general robot skills. The across-session example repeatedly visits the same scenes, so a naive pooled significance estimate is not independent evidence across tasks.

Earlier recorded LIBERO-10 action-memory experiments also depended on scene familiarity. Their results should not be pooled with these state-based MuJoCo experiments. The retrieval representations and evaluation conditions differ.

## Reproduce and inspect

Run from the harness repository:

```bash
uv run python examples/memory/01_spatial_memory_occlusion.py
uv run python examples/memory/03_action_memory_scene_recall.py
uv run python examples/memory/04_skill_library.py
```

The [full reproduction record](/hylo-docs/developer-guide/validation/memory/) retains every example, its conditions, negative findings and commands. [Memory guides](/hylo-docs/user-guide/memory/) explain the supported backends and how to configure them.

[Recorded source](https://github.com/HyloAI/hylo-harness/blob/9c3138b645ba7ee25f663d26807898f4b5374cb6/examples/memory/README.md).
