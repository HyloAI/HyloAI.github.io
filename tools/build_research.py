"""Build the Research section from Markdown articles and versioned evidence records.

Run from the workspace: .venv/bin/python site/tools/build_research.py
Generated HTML is committed so the existing GitHub Pages deployment stays buildless.
"""
from pathlib import Path
from html import escape as e
import argparse
import json
import re
import markdown
import yaml

ROOT = Path(__file__).resolve().parents[1]
BASE = 'https://hyloai.github.io'
ZH = {
 'home':'首页','research':'研究','benchmarks':'评测','docs':'文档 ↗','menu':'菜单','skip':'跳到正文',
 'kicker':'Hylo Research','hero':'在交互中学习。','intro':'研究智能体如何行动、从经验中学习，并复用已验证的技能。每项结果都保留实验条件、证据和局限。',
 'featured':'精选研究','all':'全部研究','read':'阅读研究 →','explore':'查看评测 →','benchmark.title':'统一协议，分别评测',
 'benchmark.desc':'查看 MuJoCo reach 的已记录结果。不同协议版本单独展示，附带来源和复现方法。',
 'benchmark.hero':'Benchmarks','benchmark.intro':'按任务和评测协议组织的实验结果。每份记录说明测量范围、版本和来源。',
 'All':'全部','Skills':'技能','Agents':'智能体','Memory':'记忆','Physical RSI':'Physical RSI',
 'Study':'研究','Experiment':'实验','overview':'研究概览','contents':'本文内容','published':'发布于',
 'footer':'开源的物理 AI 平台','evidence':'本文整理已有实验记录；发布这篇文章没有产生新的评测结果。',
 'data':'下载结果数据 →','mujoco.title':'MuJoCo reach：参考策略评测','mujoco.summary':'两个协议版本的结果分别列出，保留各自的测量条件与来源。'
}

def span(key, text, tag='span', attrs=''):
    return f'<{tag} data-i18n="{e(key)}"{attrs}>{e(text)}</{tag}>'

def shell(title, description, path, body, translations=None):
    dictionary = ZH | (translations or {})
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)} · Hylo Research</title><meta name="description" content="{e(description)}">
<link rel="canonical" href="{BASE}{path}"><meta property="og:title" content="{e(title)} · Hylo Research">
<meta property="og:description" content="{e(description)}"><meta property="og:url" content="{BASE}{path}">
<link rel="icon" href="/assets/logo.svg" type="image/svg+xml"><link rel="stylesheet" href="/assets/research.css">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap">
</head><body><a class="skip" href="#main" data-i18n="skip">Skip to content</a>
<header class="top"><div class="wrap"><a class="brand" href="/" aria-label="Hylo home"><img src="/assets/logo.svg" alt="" width="30" height="30">Hylo</a>
<nav class="links" id="site-nav" aria-label="Main navigation"><a href="/" data-i18n="home">Home</a><a href="/research/" data-i18n="research" {'aria-current="page"' if path=='/research/' else 'aria-current="true"' if '/articles/' in path else ''}>Research</a><a href="/research/benchmarks/" data-i18n="benchmarks" {'aria-current="page"' if path=='/research/benchmarks/' else 'aria-current="true"' if '/benchmarks/' in path else ''}>Benchmarks</a><a href="/hylo-docs/" data-i18n="docs">Docs ↗</a><a href="https://github.com/HyloAI">GitHub ↗</a></nav>
<button class="lang" id="lang" aria-label="切换到中文" type="button">中文</button><button class="menu" id="menu" type="button" aria-expanded="false" aria-controls="site-nav" data-i18n="menu">Menu</button></div></header>
<main id="main" class="wrap">{body}</main>
<footer><div class="wrap"><span>© 2026 Hylo AI · {span('footer','The open foundation for physical AI')}</span><nav aria-label="Footer"><a href="/research/" data-i18n="research">Research</a><a href="/research/benchmarks/" data-i18n="benchmarks">Benchmarks</a><a href="/hylo-docs/" data-i18n="docs">Docs ↗</a></nav></div></footer>
<script id="translations" type="application/json">{json.dumps(dictionary,ensure_ascii=False).replace('<',chr(92)+'u003c')}</script><script src="/assets/research.js" defer></script></body></html>
'''

def render_md(source):
    md = markdown.Markdown(extensions=['tables','fenced_code','toc'],extension_configs={'toc':{'permalink':False}})
    html = md.convert(source)
    html = html.replace('<table>','<div class="table-scroll" role="region" aria-label="Results table" tabindex="0"><table>').replace('</table>','</table></div>')
    return html, md.toc

def sorting_table():
    data=json.loads((ROOT/'assets/skills-sorting.provenance.json').read_text())
    lines=['| Evaluation | Starter | Candidate | Scope |','|---|---|---|---|']
    for key,label in [('gate','Independent promotion gate'),('heldout','Held-out report')]:
        row=data[key]; scope=f"{row['n']} paired scenes"
        scope+=f"; {row['wins']} wins, {row['losses']} losses; p = {row['p']:.6g}" if key=='gate' else '; not used for selection'
        lines.append(f"| {label} | {row['parent']:.0%} | {row['candidate']:.0%} | {scope} |")
    reuse=data['reuse']; lines.append(f"| Later skill calls | — | {sum(x['success'] for x in reuse)}/{len(reuse)} | Separate validation scenes; no paired control |")
    return '\n'.join(lines)

def article_page(meta, body, slug):
    cover=f'<img class="article-cover" src="{e(meta["image"])}" alt="{e(meta["image_alt"])}">' if meta.get('image') else ''
    rendered,toc=render_md(body.replace('{{sorting_results}}',sorting_table()))
    header=f'''<div class="article-head"><div class="breadcrumb"><a href="/research/" data-i18n="research">Research</a> / {span(meta['type'],meta['type'])}</div>
<div class="eyebrow">{' · '.join(e(t) for t in meta['topics'])}</div>{span('title',meta['title'],'h1')}<p class="summary" data-i18n="summary">{e(meta['summary'])}</p>
<div class="meta">{span('published','Published')} <time datetime="{meta['date']}">{meta['date']}</time></div><p class="language-note" data-zh-only hidden>以下研究正文为英文，实验日期见正文。</p></div>'''
    layout=f'<div class="article-layout"><aside class="toc" aria-label="On this page">{span("contents","On this page","p")}{toc}</aside><article class="article-body" lang="en">{cover}{rendered}<p class="evidence-note" data-i18n="evidence">This article presents existing experimental records. Its publication adds no new evaluation run.</p></article></div>'
    return shell(meta['title'],meta['summary'],f'/research/articles/{slug}/',header+layout,{'title':meta['title_zh'],'summary':meta['summary_zh']})

def board_table(board):
    rows=board['rows']; extended='ci95' in rows[0]
    out=['| Rank | Policy | Success |'+(' 95% CI | Mean steps |' if extended else ''),'|---|---|---|'+('---|---|' if extended else '')]
    previous=None;rank=0
    for i,row in enumerate(rows,1):
        score=row['success_percent']
        if score!=previous:rank=i
        previous=score
        tail=f" {row['ci95'][0]:g}–{row['ci95'][1]:g}% | {row['mean_steps']} |" if extended else ''
        out.append(f"| {rank} | `{row['name']}` | {score:g}% |"+tail)
    return '\n'.join(out)

def benchmark_pages():
    data=json.loads((ROOT/'research/data/mujoco-reach.json').read_text())
    body='''## What is measured

These are reference-policy results on the small simulated `mujoco-reach` task. They do not rank general robot capability or policy families. Each scorecard belongs to one protocol name, version and digest. Different digests are separate boards, even when their human-readable names match.

The tables are recorded snapshots, not a live submission service. They use 100 episodes per policy; equal scores share a rank. The measurement date of the historical board was not specified in its source.
'''
    for board in data['boards']:
        body+=f"\n## {board['label']}\n\nProtocol: `mujoco-reach v1` · Digest: `{board['digest']}`. "
        body+=f"Recorded {board['recorded']}.\n\n" if board['recorded'] else 'Historical snapshot.\n\n'
        body+=board_table(board)+'\n\n'+f"[Source record]({board['source']}).\n"
        if not board.get('recorded'):body+='\nConfidence intervals and mean steps are reproduced from that historical source.\n'
        else:body+='\nMeasured on a 128-core CPU without a GPU. The source summary does not report per-row confidence intervals or mean steps for this board.\n'
    body+='''
## Comparison boundaries

The examples also change `safety.max_delta` to 0.05. That produces digest `7311c7b72f04043f`; its BC score of 36% belongs to a different protocol and is excluded from both boards above.

The paired comparison in the November 1 examples finds flow+steering-4 versus BC at 84% versus 71%, with 18 candidate-only wins and 5 losses (one-sided exact McNemar p = 0.0053). Flow+steering-4 versus flow has 5 wins and 4 losses (p = 0.50), so this run provides no evidence that steering improves flow.

No rows are imported from LIBERO, from demonstrations or from adaptive development runs. Those have different tasks and conditions.

## Reproduce and download

Run from the bench repository:

```bash
uv run python examples/showcase/01_leaderboard.py
uv run python examples/showcase/02_pairwise.py
```

Your installed protocol digest determines which board a new run belongs to. See [Run and compare evaluations](/hylo-docs/benchmarking/leaderboard/) for scoring and comparison commands, and [protocol definitions](/hylo-docs/benchmarking/protocols/) for the digest contract.

[Download the recorded tables](/research/data/mujoco-reach.json). This JSON is a transcription of the cited result tables, with source hashes; it is not a bundle of original scorecards or episode traces.
'''
    rendered,toc=render_md(body)
    head=f'''<div class="article-head"><div class="breadcrumb"><a href="/research/">Research</a> / <a href="/research/benchmarks/">Benchmarks</a></div><div class="eyebrow">MuJoCo · Reach</div>{span('mujoco.title','MuJoCo reach: reference policies','h1')}<p class="summary" data-i18n="mujoco.summary">Two protocol snapshots, with separate rankings and reproducible sources.</p><div class="meta">Updated <time datetime="{data['updated']}">{data['updated']}</time></div><p class="language-note" data-zh-only hidden>以下评测说明为英文。</p></div>'''
    page=head+f'<div class="article-layout"><aside class="toc" aria-label="On this page">{toc}</aside><article class="article-body" lang="en">{rendered}</article></div>'
    result={'research/benchmarks/mujoco-reach/index.html':shell('MuJoCo reach: reference policies','Recorded reference-policy results, separated by protocol digest.','/research/benchmarks/mujoco-reach/',page)}
    index=f'''<section class="hero"><p class="eyebrow">Hylo Research</p>{span('benchmark.hero','Benchmarks','h1')}<p class="intro" data-i18n="benchmark.intro">Recorded evaluations, organised by task and protocol. Each result identifies its scope, version and source.</p></section><section class="section"><div class="benchmark-banner"><div><p class="eyebrow">MuJoCo · 2 protocol snapshots</p><h2>Reference policies on reach</h2><p data-i18n="benchmark.desc">Explore recorded MuJoCo reach results. Protocol versions remain separate, with sources and reproduction steps.</p></div><a class="text-link" href="/research/benchmarks/mujoco-reach/" data-i18n="explore">Explore benchmark →</a></div></section><section class="section"><h2 data-i18n="research">Research</h2><p>For experiments outside a shared evaluation protocol, read the <a href="/research/#all-research">research articles</a>. To evaluate your own agent, follow <a href="/hylo-docs/benchmarking/leaderboard/">Run and compare evaluations</a>.</p></section>'''
    result['research/benchmarks/index.html']=shell('Benchmarks','Recorded evaluations by task and protocol.','/research/benchmarks/',index)
    return result

def build():
    pages={};articles=[];translations={}
    for path in sorted((ROOT/'content/research').glob('*.md')):
        _,front,body=path.read_text().split('---',2);meta=yaml.safe_load(front);meta['slug']=path.stem
        pages[f'research/articles/{path.stem}/index.html']=article_page(meta,body,path.stem);articles.append(meta)
        translations[f'{path.stem}.title']=meta['title_zh'];translations[f'{path.stem}.summary']=meta['summary_zh']
    order=['program-skills','when-memory-helps','phase-guided-repair','measuring-improvement','programs-and-tools']
    articles.sort(key=lambda m:order.index(m['slug']))
    features=[];rows=[]
    for meta in articles:
        slug=meta['slug'];href=f'/research/articles/{slug}/'
        title=span(slug+'.title',meta['title']);summary=span(slug+'.summary',meta['summary'],'p')
        metadata=f'<div class="meta"><time datetime="{meta["date"]}">{meta["date"]}</time>{span(meta["type"],meta["type"])}</div>'
        if meta.get('featured'):
            picture=f'<img src="{e(meta["image"])}" alt="{e(meta["image_alt"])}" loading="lazy">' if meta.get('image') else ''
            features.append(f'<article class="feature {"feature-main" if not features else ""}"><a href="{href}">{picture}{metadata}<h3>{title}</h3></a>{summary}<a class="text-link" href="{href}" data-i18n="read">Read study →</a></article>')
        rows.append(f'<article class="research-row" data-topics="{e(json.dumps(meta["topics"]),quote=True)}"><time datetime="{meta["date"]}">{meta["date"]}</time><div><h3><a href="{href}">{title}</a></h3>{summary}</div><div class="topics">'+ ' · '.join(span(t,t) for t in meta['topics'])+'</div></article>')
    filters=''.join(f'<button class="filter" type="button" data-topic="{topic}" aria-pressed="{str(topic=="All").lower()}" data-i18n="{topic}">{topic}</button>' for topic in ['All','Agents','Memory','Skills','Physical RSI'])
    body=f'''<section class="hero"><p class="eyebrow" data-i18n="kicker">Hylo Research</p>{span('hero','Learning through interaction.','h1')}<p class="intro" data-i18n="intro">How agents act, learn from experience and reuse verified skills. Findings grounded in recorded experiments, with conditions and limits kept in view.</p><div class="hero-links"><a href="#all-research" data-i18n="all">All research</a><a href="/research/benchmarks/" data-i18n="benchmarks">Benchmarks</a></div></section>
<section class="section"><div class="section-head">{span('featured','Featured research','h2')}</div><div class="featured">{''.join(features)}</div></section>
<section class="section"><div class="benchmark-banner"><div><p class="eyebrow">Benchmarks</p>{span('benchmark.title','One protocol. A fair comparison.','h3')}{span('benchmark.desc','Explore recorded MuJoCo reach results. Protocol versions remain separate, with sources and reproduction steps.','p')}</div><a class="text-link" href="/research/benchmarks/" data-i18n="explore">Explore benchmarks →</a></div></section>
<section class="section" id="all-research"><div class="section-head">{span('all','All research','h2')}<span class="results-count" id="results-count" role="status">{len(articles)} articles</span></div><div class="filters" role="group" aria-label="Filter research by topic">{filters}</div>{''.join(rows)}</section>'''
    pages['research/index.html']=shell('Research','Studies of agents, memory, skills and physical self-improvement.','/research/',body,translations)
    pages.update(benchmark_pages())
    return pages

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--check',action='store_true');args=parser.parse_args()
    pages=build();stale=[]
    for name,text in pages.items():
        path=ROOT/name
        if args.check:
            if not path.exists() or path.read_text()!=text:stale.append(name)
        else:
            path.parent.mkdir(parents=True,exist_ok=True);path.write_text(text)
    if stale:raise SystemExit('Rebuild stale research pages: '+', '.join(stale))
    print(f'{"Checked" if args.check else "Built"} {len(pages)} research pages.')

if __name__=='__main__':main()
