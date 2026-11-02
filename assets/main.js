(function(){
  'use strict';
  const $=id=>document.getElementById(id),content=window.SITE_CONTENT;
  const escape=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  let language='en',filter='all',currentCitation=null,toastTimer;
  function toast(message){$('toast').textContent=message;$('toast').hidden=false;clearTimeout(toastTimer);toastTimer=setTimeout(()=>$('toast').hidden=true,4000);}
  function bibtex(p){
    const rows=['  title = {'+p.bibTitle+'}','  author = {'+p.bibAuthors+'}','  journal = {'+p.journal+'}','  year = {'+p.year+'}','  volume = {'+p.volume+'}','  pages = {'+p.pages+'}','  doi = {'+p.doi+'}'];
    if(p.arxiv)rows.push('  eprint = {'+p.arxiv+'}','  archivePrefix = {arXiv}');
    return '@article{'+p.id+',\n'+rows.join(',\n')+'\n}';
  }
  function download(name,text,type){const url=URL.createObjectURL(new Blob([text],{type})),a=document.createElement('a');a.href=url;a.download=name;a.hidden=true;document.body.appendChild(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(url),3000);}
  async function copy(text){try{if(!navigator.clipboard)throw Error('Clipboard unavailable');await navigator.clipboard.writeText(text);toast(content.translations[language].copied);}catch{toast(content.translations[language].copyFailed);}}
  function renderPublications(){
    const t=content.translations[language],pubs=content.publications.filter(p=>filter==='all'||p.category===filter);
    $('publicationCount').textContent=pubs.length+' '+(pubs.length===1?t.publication:t.publications);
    $('publicationList').innerHTML=pubs.map(p=>'<article class="publication"><div class="publication-year">'+p.year+'</div><div class="publication-content"><h3 class="publication-title"><a href="https://doi.org/'+escape(p.doi)+'" target="_blank" rel="noopener">'+escape(p.title)+'</a></h3><p class="publication-authors">'+escape(p.authors).replace('H. El Moumni','<strong>H. El Moumni</strong>')+'</p><p class="publication-journal">'+escape(p.journal)+' <strong>'+escape(p.volume)+'</strong>, '+escape(p.pages)+' ('+p.year+')</p><p class="publication-note">'+escape(language==='fr'?p.noteFr:p.noteEn)+'</p></div><div class="publication-links"><a href="https://doi.org/'+escape(p.doi)+'" target="_blank" rel="noopener">'+t.paper+' ↗</a>'+(p.arxiv?'<a href="https://arxiv.org/abs/'+escape(p.arxiv)+'" target="_blank" rel="noopener">arXiv ↗</a>':'')+'<button data-cite="'+escape(p.id)+'" aria-label="'+t.cite+' : '+escape(p.title)+'">'+t.cite+' +</button></div></article>').join('');
    document.querySelectorAll('[data-filter]').forEach(b=>{const active=b.dataset.filter===filter;b.classList.toggle('active',active);b.setAttribute('aria-pressed',String(active));});
  }
  function setFilter(value){filter=value;renderPublications();}
  document.querySelectorAll('[data-filter]').forEach(b=>b.addEventListener('click',()=>setFilter(b.dataset.filter)));
  document.querySelectorAll('[data-research-filter]').forEach(a=>a.addEventListener('click',()=>setFilter(a.dataset.researchFilter)));
  function setLanguage(value,persist=true){
    language=value==='fr'?'fr':'en';const t=content.translations[language];document.documentElement.lang=language;
    document.querySelectorAll('[data-i18n]').forEach(el=>{if(t[el.dataset.i18n]!=null)el.innerHTML=t[el.dataset.i18n];});
    $('enLabel').classList.toggle('chosen',language==='en');$('frLabel').classList.toggle('chosen',language==='fr');
    $('languageSwitch').setAttribute('aria-label',language==='en'?'Lire le site en français':'Read the website in English');
    $('closeCitation').setAttribute('aria-label',language==='en'?'Close citation':'Fermer la référence');
    $('menuButton').setAttribute('aria-label',language==='en'?'Open navigation':'Ouvrir la navigation');
    $('navigation').setAttribute('aria-label',language==='en'?'Main navigation':'Navigation principale');
    document.querySelector('.hero-visual img').alt=language==='en'?'Portrait of Hasan El Moumni':'Portrait de Hasan El Moumni';
    const researchLabels=language==='en'?['View publications on thermodynamics','View publications on black-hole shadows','View publications on quasi-periodic oscillations']:['Voir les publications en thermodynamique','Voir les publications sur les ombres des trous noirs','Voir les publications sur les oscillations quasi périodiques'];
    document.querySelectorAll('[data-research-filter]').forEach((a,i)=>a.setAttribute('aria-label',researchLabels[i]));
    document.querySelector('.filters').setAttribute('aria-label',language==='en'?'Filter publications':'Filtrer les publications');
    document.title=language==='en'?'Hasan El Moumni — Theoretical physicist':'Hasan El Moumni — Physicien théoricien';
    document.querySelector('meta[name="description"]').setAttribute('content',language==='en'?'Hasan El Moumni, Full Professor of theoretical physics at Ibn Zohr University, Agadir. Black-hole thermodynamics, generalized entropy and strong-gravity phenomenology.':'Hasan El Moumni, professeur de physique théorique à l’Université Ibn Zohr, Agadir. Thermodynamique des trous noirs, entropies généralisées et gravitation forte.');
    if(persist)try{localStorage.setItem('helmoumni-language',language);}catch{}
    renderPublications();
  }
  $('languageSwitch').addEventListener('click',()=>setLanguage(language==='en'?'fr':'en'));
  const dialog=$('citationDialog');
  $('publicationList').addEventListener('click',e=>{const button=e.target.closest('[data-cite]');if(!button)return;currentCitation=content.publications.find(p=>p.id===button.dataset.cite);if(!currentCitation)return;$('citationPaper').textContent=currentCitation.title;$('citationText').textContent=bibtex(currentCitation);dialog.showModal();});
  $('closeCitation').addEventListener('click',()=>dialog.close());
  dialog.addEventListener('click',e=>{if(e.target!==dialog)return;const r=dialog.getBoundingClientRect();if(e.clientX<r.left||e.clientX>r.right||e.clientY<r.top||e.clientY>r.bottom)dialog.close();});
  $('copyCitation').addEventListener('click',()=>{if(currentCitation)copy(bibtex(currentCitation));});
  $('downloadCitation').addEventListener('click',()=>{if(currentCitation)download(currentCitation.id+'.bib',bibtex(currentCitation)+'\n','application/x-bibtex;charset=utf-8');});
  $('copyEmail').addEventListener('click',()=>copy('h.elmoumni@uiz.ac.ma'));
  const menu=$('menuButton'),navigation=$('navigation');
  function closeMenu(){menu.setAttribute('aria-expanded','false');navigation.classList.remove('open');}
  menu.addEventListener('click',()=>{const open=menu.getAttribute('aria-expanded')!=='true';menu.setAttribute('aria-expanded',String(open));navigation.classList.toggle('open',open);});
  navigation.querySelectorAll('a').forEach(a=>a.addEventListener('click',closeMenu));
  document.addEventListener('keydown',e=>{if(e.key==='Escape')closeMenu();});
  if('IntersectionObserver' in window){const observer=new IntersectionObserver(entries=>{entries.forEach(entry=>{if(entry.isIntersecting)document.querySelectorAll('[data-nav]').forEach(a=>a.classList.toggle('active',a.dataset.nav===entry.target.id));});},{rootMargin:'-15% 0px -65% 0px'});document.querySelectorAll('main>section[id]').forEach(s=>observer.observe(s));}
  try{const saved=localStorage.getItem('helmoumni-language');if(saved==='fr')language='fr';}catch{}
  const requested=new URLSearchParams(location.search).get('lang');if(requested==='fr'||requested==='en')language=requested;
  setLanguage(language,false);
})();
