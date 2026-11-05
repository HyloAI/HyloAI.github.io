---
date: '2026-11-05'
type: Study
title: Learning and improvement under independent evaluation
title_zh: 通过独立评测衡量学习与改进
summary: Small reach experiments expose data scaling, selection optimism and the power
  limits of promotion gates.
summary_zh: 小规模到达任务揭示数据规模效应、选择偏差，以及晋升检验的统计功效限制。
topics:
- Physical RSI
image: /assets/campaign-mujoco-reach-gain.png
image_alt: Recorded improvement campaign on MuJoCo reach
---

## The question

How much does a policy improve, and how reliably can an evaluation confirm that improvement? Learning curves, held-out reports and gate-power experiments answer different parts of this question.

## Method and results

The learning and evolution examples were measured on November 1, 2026, on MuJoCo planar reach. The learning jobs separate demonstration data, search rollouts and held-out evaluation. The campaign example starts from a flow policy with deliberately excessive sampling noise.

| Experiment | Recorded outcome | Evaluation scope |
|---|---|---|
| Flow policy trained from demonstrations | 0.397 with 10 demonstrations; 0.847 with 160 | 300 held-out episodes |
| Online CEM over steering settings | Starting setting 0.458; selected best 0.836 | 500 held-out episodes |
| Three-cycle improvement campaign | 0.440 → 0.726 → 0.762; two promotions | 500 fresh held-out episodes |
| Gate sensitivity to a roughly ten-point gain | About 26% of cycles promote it | Default 40 episodes per split; finite-pool resampling |

The CEM best setting scores 0.887 on the search cases used to select it and 0.836 held out. This gap illustrates selection optimism. The campaign improves a deliberately noisy baseline by lowering its sampling noise; it does not establish open-ended capability growth.

## Where evaluation breaks down

The gate-power study resamples a finite pool of real simulated episodes. At default split sizes, larger effects are easier to confirm: a roughly 29-point gain is promoted in about 99% of cycles, while a four-point gain is promoted in about 6.5%. These are measured properties of this experiment and protocol.

A calibrated success judge also loses precision under distribution shift. A judge calibrated to 0.95 precision labels another cell's episodes at 0.821 precision. Calibration alone cannot establish reliability on a new distribution.

A simulated field-rate change reverses the ranking of parent and candidate, triggering rollback after 40 field episodes. Passing a simulation gate therefore does not establish deployment robustness.

## Reproduce and inspect

- [Learning records](/hylo-docs/developer-guide/validation/learning/) include learning curves, calibration and online CEM commands.
- [Evolution records](/hylo-docs/developer-guide/validation/evolution/) include the campaign, gate-power study and rollback experiment.
- [Run a campaign](/hylo-docs/user-guide/campaigns/) explains the operational lifecycle.

Sources: [learning](https://github.com/HyloAI/hylo-harness/blob/9c3138b645ba7ee25f663d26807898f4b5374cb6/examples/learn/README.md), [evolution](https://github.com/HyloAI/hylo-harness/blob/9c3138b645ba7ee25f663d26807898f4b5374cb6/examples/evolve/README.md).
