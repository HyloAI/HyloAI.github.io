---
date: '2026-11-05'
type: Study
title: From a task program to a reusable skill
title_zh: 从任务程序到可复用技能
summary: A recorded sorting experiment separates program development, independent
  verification and later skill calls.
summary_zh: 一次分拣实验，分别记录程序开发、独立验证和后续技能调用。
topics:
- Skills
- Agents
image: /assets/skills-sorting.jpg
image_alt: Recorded Panda sorting task with coloured blocks and trays
featured: true
---

## The question

Can a model revise a supplied robot program, pass an independent evaluation and leave a skill that another agent actually calls? This recorded case follows one Panda sorting task family from a one-object-per-colour starter to multi-object sorting.

## Method

The model, `claude:sonnet`, develops `solve(robot)` on four development cases. The selected submission solves all four. Candidate execution uses `code.program`, with no model calls during the program's execution. The starter and its robot-tool helpers were supplied; this is program revision rather than a from-scratch system or model-weight training.

The selected program is frozen before the independent promotion gate. A separate held-out report does not select the candidate. The resulting skill, `sort_by_colour@1`, records its implementation digest and promotion evidence. Later agents retrieve it, verify its artifact integrity and call `skills.sort_by_colour(robot)`.

## Results

{{sorting_results}}

Two preceding local-model development attempts produced no qualifying candidate. The recorded walkthrough follows the selected Claude session. The three reuse episodes show actual retrieval and calls; they do not measure a paired improvement over an agent without skills.

## Scope and limitations

The task uses one Panda simulation, two 160 × 120 RGB-D cameras and simulator instance segmentation. This observation privilege matters: the experiment does not establish real-world visual recognition, hardware transfer or generalisation to other task families. Twelve pairs provide a small evaluation sample.

The video is a presentation of saved research records and a physics replay, with model waits shortened, motion timing edited and higher-resolution presentation cameras. It is not a live Studio authoring interface. Replayed joint/gripper states and final task verdicts were checked against their source traces.

## Reproduce and inspect

- [Watch the use case](/hylo-docs/user-guide/skills/development-and-reuse/) for the full recorded workflow.
- [Develop and reuse a program skill](/hylo-docs/user-guide/research-and-skills/) for commands and configuration. A new model run can produce different results.
- [Source and replay provenance](/assets/skills-sorting.provenance.json) includes the source revisions, program, evaluation, skill calls and trace/video hashes. The table above is generated from this record.
