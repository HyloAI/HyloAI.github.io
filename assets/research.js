(() => {
  const dictionary = JSON.parse(document.getElementById('translations').textContent);
  const nodes = [...document.querySelectorAll('[data-i18n]')];
  const originals = new Map(nodes.map(n => [n, n.textContent]));
  const button = document.getElementById('lang');
  let lang = 'en';
  function apply(value) {
    lang = value === 'zh' ? 'zh' : 'en';
    document.documentElement.lang = lang === 'zh' ? 'zh-CN' : 'en';
    nodes.forEach(n => { n.textContent = lang === 'zh' ? (dictionary[n.dataset.i18n] || originals.get(n)) : originals.get(n); });
    button.textContent = lang === 'zh' ? 'EN' : '中文';
    button.setAttribute('aria-label', lang === 'zh' ? 'Switch to English' : '切换到中文');
    document.querySelectorAll('[data-zh-only]').forEach(n => { n.hidden = lang !== 'zh'; });
    updateCount();
  }
  let saved;
  try { saved = localStorage.getItem('hylo-lang'); } catch (_) {}
  apply(new URLSearchParams(location.search).get('lang') || saved || (navigator.language.startsWith('zh') ? 'zh' : 'en'));
  button.addEventListener('click', () => { apply(lang === 'zh' ? 'en' : 'zh'); try { localStorage.setItem('hylo-lang', lang); } catch (_) {} });
  const header = document.querySelector('.top'), menu = document.getElementById('menu');
  function close() { header.classList.remove('open'); menu.setAttribute('aria-expanded', 'false'); }
  menu.addEventListener('click', () => { const open = !header.classList.contains('open'); header.classList.toggle('open', open); menu.setAttribute('aria-expanded', String(open)); });
  document.addEventListener('keydown', event => { if (event.key === 'Escape' && header.classList.contains('open')) { close(); menu.focus(); } });
  document.addEventListener('click', event => { if (!header.contains(event.target)) close(); });
  header.addEventListener('focusout', event => { if (event.relatedTarget && !header.contains(event.relatedTarget)) close(); });
  document.querySelectorAll('.links a').forEach(a => a.addEventListener('click', close));
  const mobile = matchMedia('(max-width:800px)');
  mobile.addEventListener('change', () => { const active = document.activeElement; close(); if (mobile.matches && header.querySelector('.links').contains(active)) menu.focus(); });
  function updateCount() {
    const count = document.getElementById('results-count');
    if (!count) return;
    const n = [...document.querySelectorAll('.research-row')].filter(row => !row.hidden).length;
    count.textContent = lang === 'zh' ? `${n} 篇文章` : `${n} ${n === 1 ? "article" : "articles"}`;
  }
  document.querySelectorAll('.filter').forEach(button => button.addEventListener('click', () => {
    document.querySelectorAll('.filter').forEach(b => b.setAttribute('aria-pressed', String(b === button)));
    document.querySelectorAll('.research-row').forEach(row => { row.hidden = button.dataset.topic !== 'All' && !JSON.parse(row.dataset.topics).includes(button.dataset.topic); });
    updateCount();
  }));
})();
