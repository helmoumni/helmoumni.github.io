"""Reproducible update from the checked INSPIRE snapshot and explicit overrides."""
from pathlib import Path
import subprocess,json,re,unicodedata,html
root=Path(__file__).resolve().parents[1]
subprocess.run(['python3',str(root/'scripts/import-bibliography.py')],check=True,stdout=subprocess.DEVNULL)
old=json.loads((root/'assets/bibliography.json').read_text());snapshot=json.loads((root/'data/inspire-bibliography.json').read_text());hs=snapshot['records'];overrides=json.loads((root/'data/bibliography-overrides.json').read_text())
def key(s):return re.sub('[^a-z0-9]','',unicodedata.normalize('NFKD',s).encode('ascii','ignore').decode().lower())
def clean(s):
 s=re.sub(r'<[^>]+>','',s);return s.replace('$','').replace('\\','').strip()
used=set();records=[];changes=[]
def enrich(p,h):
 used.add(h['id']);q=dict(p);q['inspireId']=h['id'];q['inspireUrl']='https://inspirehep.net/literature/'+h['id'];q['checked']='2026-11-04';q['archivedDetails']=p.get('details','')
 title=next((t['title'] for t in h['titles'] if '<' not in t['title']),h['titles'][0]['title']);q['title']=clean(title)
 q['authors']='; '.join(h['authors']);q['bibAuthors']=' and '.join(h['authors'])
 dois=list(dict.fromkeys(d['value'] for d in h['dois'] if d.get('material')!='erratum'))
 q['doi']=dois[0] if dois else None;q['errata']=[d['value'] for d in h['dois'] if d.get('material')=='erratum']
 q['arxiv']=h['arxiv'][0] if h['arxiv'] else p.get('arxiv');pub=next((x for x in h['publication_info'] if x.get('material')!='erratum' and x.get('journal_title')),None)
 q['status']='published' if pub else 'preprint'
 if h['id']=='2625186':q['status']='unconfirmed'
 if pub:
  q['year']=pub['year'];q['journal']=pub['journal_title'];q['volume']=pub.get('journal_volume','');q['pages']=(pub['page_start']+('–'+pub['page_end'] if pub.get('page_end') and pub['page_end']!=pub['page_start'] else '')) if pub.get('page_start') else pub.get('artid','')
  if q['year']>2026:q['status']='forthcoming'
 else:
  q['year']=int(h['date'][:4]) if h.get('date') else p.get('year',2026);q['journal']='';q['volume']='';q['pages']=''
 if p['id'] in overrides:q['year']=overrides[p['id']]['year'];q['yearSource']=overrides[p['id']]['source']
 q['details']=q['authors']+' — '+(f"{q['journal']} {q['volume']}, {q['pages']} ({q['year']})" if pub else 'arXiv:'+str(q['arxiv']))
 q['url']='https://doi.org/'+q['doi'] if q['doi'] else ('https://arxiv.org/abs/'+q['arxiv'] if q.get('arxiv') else q['inspireUrl']);q['linkType']='doi' if q['doi'] else ('arxiv' if q.get('arxiv') else 'inspire')
 name=q['title'].lower();themes=[]
 if re.search('therm|entropy|phase|critical|heat|rényi|renyi|unruh|cosmic censorship|wick|joule',name):themes.append('thermodynamics')
 if re.search('shadow|deflection|light|optical|observational',name):themes.append('observations')
 if re.search('string|holograph|cft|m-theory|brane|qubit|complexity|entanglement',name):themes.append('holography')
 if re.search('quasinormal|qpo|particle|chaos|hawking|accretion|neutrino|dynamics',name):themes.append('dynamics')
 q['themes']=themes or ['thermodynamics']
 changes.append({'id':q['id'],'inspireId':h['id'],'oldYear':p.get('year'),'year':q['year'],'oldTitle':p.get('title'),'title':q['title'],'status':q['status']});records.append(q)
for p in old:
 matches=[h for h in hs if any(key(t['title'])==key(p['title']) for t in h['titles']) or (p.get('arxiv') and p['arxiv'] in h['arxiv']) or (p.get('doi') and any(d['value'].lower()==p['doi'].lower() for d in h['dois']))]
 assert len(matches)==1,(p['id'],len(matches));enrich(p,matches[0])
# A near-identical M-theory publisher record is held out pending an explicit version link.
held=['2765745']
for h in hs:
 if h['id'] in used or h['id'] in held:continue
 assert 'H.El.Moumni.1' in h['authorIds']
 enrich({'id':'inspire-'+h['id'],'source':'inspire-update','sourceOrdinals':[]},h)
records.sort(key=lambda p:(-p['year'],p['title']))
assert len({p['inspireId'] for p in records})==len(records)
for f in ['doi','arxiv']:
 vals=[p[f].lower() for p in records if p.get(f)];assert len(vals)==len(set(vals))
(root/'assets/bibliography.json').write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n')
report={'checked':'2026-11-04','count':len(records),'added':len(records)-len(old),'doiCount':sum(bool(p['doi']) for p in records),'statuses':{s:sum(p['status']==s for p in records) for s in ['published','preprint','unconfirmed','forthcoming']},'changes':changes,'unresolved':[{'record':'weebly-07','candidateInspireId':'2765745','reason':'Same six authors and near-identical topic/abstract, but no explicit arXiv-to-publication link. Candidate not added separately to avoid likely double counting.'}],'yearOverrides':overrides}
(root/'data/bibliography-update-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
# Export only identified fields; do not invent journal metadata for preprints.
def bibescape(s):return str(s).replace('&',r'\&').replace('%',r'\%').replace('_',r'\_').replace('{','').replace('}','')
bs=[]
for p in records:
 fields={'title':p['title'],'author':p['bibAuthors'],'year':p['year']}
 for name in ['journal','volume','pages','doi']:
  if p.get(name):fields[name]=p[name]
 if p.get('arxiv'):fields.update(eprint=p['arxiv'],archivePrefix='arXiv')
 fields['url']=p['inspireUrl']
 bs.append('@'+('article' if p['journal'] else 'misc')+'{'+p['id']+',\n'+',\n'.join('  '+k+' = {'+bibescape(v)+'}' for k,v in fields.items())+'\n}')
(root/'assets/bibliography.bib').write_text('\n\n'.join(bs)+'\n')
t={'en':{},'fr':{}}
def tr(k,en,fr,tag='span',attrs=''):
 t['en'][k]=en;t['fr'][k]=fr;return f'<{tag} data-i18n="{k}" {attrs}>{en}</{tag}>'
esc=html.escape
body='<section class="section" id="publications"><div class="container">'+tr('b5title','Publications & preprints','Publications et prépublications','h1')+tr('b5intro',f'{len(records)} references · metadata checked against INSPIRE on 4 November 2026.',f'{len(records)} références · métadonnées contrôlées dans INSPIRE le 4 novembre 2026.','p')+tr('b5note','Journal records, preprints and forthcoming issues are distinguished below. One M-theory version link remains to be confirmed. Topic tags are editorial; a paper may belong to several themes.','Les notices de revue, les prépublications et les numéros à paraître sont distingués ci-dessous. Un rapprochement de versions en théorie M reste à confirmer. Les thèmes sont un classement éditorial ; un article peut relever de plusieurs axes.','p','class="archive-note"')
body+='<div class="academic-profiles"><a class="text-link" href="assets/bibliography.bib" download>BibTeX ↓</a><a class="text-link" href="assets/bibliography.json" download>JSON ↓</a></div><div class="bibliography-controls" id="bibliographyControls" hidden>'
body+='<label>'+tr('bsearch','Search title, author or DOI','Rechercher un titre, auteur ou DOI')+'<input id="bibSearch" type="search"></label>'
options={'theme': [('all','All themes','Tous les thèmes'),('thermodynamics','Thermodynamics','Thermodynamique'),('observations','Observations','Observations'),('holography','Holography & strings','Holographie et cordes'),('dynamics','Dynamics','Dynamique')],'status':[('all','All statuses','Tous les statuts'),('published','Journal record','Notice de revue'),('preprint','Preprint','Prépublication'),('forthcoming','Forthcoming issue','Numéro à paraître'),('unconfirmed','Version to confirm','Version à confirmer')]}
for kind,opts in options.items():
 body+='<label>'+tr('blabel'+kind,kind.title(),'Thème' if kind=='theme' else 'Statut')+f'<select id="bib{kind.title()}">'
 for value,en,fr in opts:body+=tr('b'+kind+value,en,fr,'option',f'value="{value}"')
 body+='</select></label>'
body+='<label>'+tr('byear','Year','Année')+'<select id="bibYear">'+tr('byearall','All years','Toutes les années','option','value="all"')
for y in sorted({p['year'] for p in records},reverse=True):body+=f'<option value="{y}">{y}</option>'
body+='</select></label><button class="text-link" id="bibReset" type="button">'+tr('breset','Reset','Réinitialiser')+'</button></div><p id="bibCount" role="status" aria-live="polite"></p><p id="bibEmpty" hidden>'+tr('bempty','No matching reference.','Aucune référence correspondante.')+'</p>'
for p in records:
 body+=f'<article class="publication bib-entry" id="{p["id"]}" data-year="{p["year"]}" data-status="{p["status"]}" data-themes="{" ".join(p["themes"])}"><div class="publication-year">{p["year"]}</div><div class="publication-content"><h2 class="publication-title">{esc(p["title"])}</h2><p class="publication-authors">{esc(p["details"])}</p><p class="publication-note">'+tr('bstatus'+p['status'],*[ (en,fr) for v,en,fr in options['status'] if v==p['status']][0])+'</p>'
 if p['status']=='unconfirmed':body+=tr('bversion','The archive mentions a journal publication, but INSPIRE does not link this preprint to it. Identification remains pending.','L’archive mentionne une publication en revue, mais INSPIRE ne la relie pas à cette prépublication. L’identification reste en attente.','p')
 body+='</div><div class="publication-links">'
 if p['doi']:body+=f'<a href="https://doi.org/{esc(p["doi"],quote=True)}" target="_blank" rel="noopener">DOI ↗</a>'
 if p.get('arxiv'):body+=f'<a href="https://arxiv.org/abs/{esc(p["arxiv"],quote=True)}" target="_blank" rel="noopener">arXiv ↗</a>'
 body+=f'<a href="{p["inspireUrl"]}" target="_blank" rel="noopener">INSPIRE ↗</a>'
 for doi in p['errata']:body+=f'<a href="https://doi.org/{esc(doi,quote=True)}" target="_blank" rel="noopener">Erratum ↗</a>'
 body+='</div></article>'
body+='</div></section>'
(root/'templates/publications.html').write_text(body+'\n')
(root/'assets/bibliography-content.js').write_text('/* Bibliography translations */\n'+''.join('Object.assign(window.SITE_CONTENT.translations.'+lang+', '+json.dumps(vals,ensure_ascii=False)+');\n' for lang,vals in t.items()))
print({k:v for k,v in report.items() if k in ['count','added','doiCount','statuses']})
