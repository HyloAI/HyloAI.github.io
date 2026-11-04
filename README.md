<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset=".github/assets/banner-dark.svg">
    <img src=".github/assets/banner-light.svg" width="100%" alt="hyloai.github.io: the Hylo website; plain HTML, no build step">
  </picture>
</p>

<p align="center">
  <a href="LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/license-Apache--2.0-c8442d?style=flat-square"></a>
  <a href="https://hyloai.github.io/"><img alt="Live at hyloai.github.io" src="https://img.shields.io/badge/live-hyloai.github.io-171c22?style=flat-square"></a>
  <img alt="English, 中文" src="https://img.shields.io/badge/languages-English%20%C2%B7%20%E4%B8%AD%E6%96%87-5b6168?style=flat-square">
</p>

# Hylo AI website

The site at https://hyloai.github.io/ (bilingual: English, 中文). Plain HTML, no build step: edit `index.html`, push to
`main`, GitHub Pages serves it. Images in `assets/` come from recorded runs (see hylo-docs).

The homepage and docs share five core concepts: Physical RSI, Worlds, Agents, Memory and Skills. Physical RSI
connects the other four. The homepage presents the five-step loop and four supporting capabilities in one section,
with stage links and highlights showing their relationships. Preserve the `#loop` and `#stack` anchors. Studio,
deployment and architecture are supporting entry points. Keep homepage copy concise and aligned with the docs'
concept definitions. Keep English text, Chinese
`data-i18n` entries and metadata aligned with the [docs wording guide](https://github.com/HyloAI/hylo-docs/blob/main/docs/developer-guide/docs.md#shared-website-wording). Case studies must state their robot, observation conditions
and measured scope; link detailed results to the documentation. Build and verify the linked docs before publishing.

After changing Chinese text, regenerate the MiSans subsets with `tools/subset_fonts.py` and check both languages.

Apache License 2.0. Copyright 2026 Hylo AI.
