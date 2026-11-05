---
date: '2026-11-05'
type: Study
title: 'Programs and tool-calling agents: reading the evidence'
title_zh: 程序与工具调用智能体：如何解读实验结果
summary: Separate supplied programs, model-written revisions and interactive tool
  use before comparing outcomes.
summary_zh: 区分预写程序、模型修改的程序和交互式工具调用，再理解各自的实验结果。
topics:
- Agents
- Skills
image: /assets/tools-llm-stack.jpg
image_alt: Panda robot stacking blocks in the recorded tool-calling demonstration
---

## The question

A successful robot episode can come from a supplied program, a program revised by a model or a model choosing tools during execution. Which part of the system did the experiment actually evaluate?

## Three distinct workflows

| Workflow | What changes | Evidence to inspect |
|---|---|---|
| Supplied task programs | A developer writes the policy logic | Observation access, supplied helpers, task coverage and failures |
| Model-developed programs | A model revises code before it is frozen for evaluation | Development cases, independent gate and held-out report |
| Interactive tool-calling agents | A model makes decisions during the episode | Tool trace, model calls and independent task verdict |

The [sorting skill study](/research/articles/program-skills/) belongs to the second category. The [recorded robot-control case](/hylo-docs/use-cases/robot-control/) belongs to the third. Their outcomes describe different experiments and should not be placed on a shared ranking.

## Conditions that matter

The existing program and tool records span scene construction, physics replay, motion, LIBERO and robot manipulation. Some paths use simulator segmentation or other privileged observations. Some worlds have motion demonstrations without success-rate evaluations. A working command or rendered video does not by itself measure task reliability.

The source records retain unsuccessful workflows, external replay limitations and paths that were not run. Consult the per-workflow conditions before quoting a headline rate.

## Reproduce and inspect

The [workflow records](/hylo-docs/developer-guide/validation/tool-agents/) separate each experiment and link its source scripts. For implementation, use the [program-development guide](/hylo-docs/user-guide/developing-strategies/) or the [tool-calling agent guide](/hylo-docs/user-guide/tool-agents/).

This overview is a guide to interpreting recorded evidence; it adds no new evaluation run.
