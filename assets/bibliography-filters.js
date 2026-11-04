(function () {
  'use strict';
  function normalize(s) { return s.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase(); }
  function matches(entry, filters) {
    return normalize(filters.query).split(/\s+/).filter(Boolean).every(term => normalize(entry.text).includes(term)) &&
      (filters.year === 'all' || entry.year === filters.year) &&
      (filters.status === 'all' || entry.status === filters.status) &&
      (filters.theme === 'all' || entry.themes.split(' ').includes(filters.theme));
  }
  if (typeof module !== 'undefined' && module.exports) { module.exports = { matches }; return; }
  const controls = document.getElementById('bibliographyControls');
  if (!controls) return;
  const get = id => document.getElementById(id);
  const entries = [...document.querySelectorAll('.bib-entry')];
  function update() {
    const filters = { query: get('bibSearch').value, year: get('bibYear').value, status: get('bibStatus').value, theme: get('bibTheme').value };
    let count = 0;
    entries.forEach(el => {
      const text = el.textContent + ' ' + [...el.querySelectorAll('a')].map(a => a.href).join(' ');
      const visible = matches({ text, ...el.dataset }, filters);
      el.hidden = !visible;
      if (visible) count++;
    });
    get('bibCount').textContent = count + ' / ' + entries.length + (document.documentElement.lang === 'fr' ? ' références' : ' references');
    get('bibEmpty').hidden = count !== 0;
  }
  controls.hidden = false;
  controls.addEventListener('input', update);
  controls.addEventListener('change', update);
  get('bibReset').addEventListener('click', () => {
    get('bibSearch').value = '';
    ['bibYear', 'bibStatus', 'bibTheme'].forEach(id => { get(id).value = 'all'; });
    update();
  });
  new MutationObserver(update).observe(document.documentElement, { attributes: true, attributeFilter: ['lang'] });
  update();
})();
