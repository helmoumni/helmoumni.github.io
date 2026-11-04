"""Merge the archived bibliography with the existing selected records.
No remote metadata inference: archival years and publication statements are retained.
"""
from pathlib import Path
from urllib.parse import quote
import json,re,subprocess,unicodedata,html
root=Path(__file__).resolve().parents[1]
source=json.loads((root/'data/weebly-publications.json').read_text())
selected=json.loads(subprocess.check_output(['node','-e',"global.window={};require('./assets/content.js');console.log(JSON.stringify(window.SITE_CONTENT.publications))"],cwd=root,text=True))
def key(s):
 return re.sub(r'[^a-z0-9]','',unicodedata.normalize('NFKD',s).encode('ascii','ignore').decode().lower())
def ids(p):
 return [('doi',p['doi'].lower())] if p.get('doi') else []
def identities(p):
 return ids(p)+([('arxiv',p['arxiv'])] if p.get('arxiv') else [])+[('title',key(p['title']))]
records=[];index={};merges=[];mapping=[]
for p in selected:
 record={**p,'details':p['authors']+' — '+p['journal']+' '+p['volume']+', '+p['pages']+f" ({p['year']})",'source':'existing-selection','url':'https://doi.org/'+p['doi'],'linkType':'doi','sourceOrdinals':[],'yearBasis':'existing-record'}
 records.append(record)
 for identity in identities(record):index[identity]=record
for p in source['records']:
 detail=p['details'];a=re.search(r'arXiv:\s*(\d{4}\.\d{4,5})',detail)
 doi=next((u.split('doi.org/',1)[1] for u in p['links'] if 'doi.org/' in u),None)
 pub=re.split(r'Published(?:\s+in)?\s*:?\s*',detail,maxsplit=1)
 years=re.findall(r'\b(?:19|20)\d{2}\b',pub[-1] if len(pub)>1 else detail)
 year=int(years[-1]) if years else (2000+int(a[1][:2]) if a else None)
 record={'id':f"weebly-{p['sourceOrdinal']:02d}",'title':p['title'].replace('$','').rstrip(' ,'),'details':detail,'year':year,'yearBasis':'archived-publication' if len(pub)>1 and years else 'archived-preprint','source':'weebly-archive','sourceOrdinals':[p['sourceOrdinal']]}
 if a:record['arxiv']=a[1]
 if doi:record['doi']=doi
 match=next(((identity,index[identity]) for identity in identities(record) if identity in index),None)
 if match:
  identity,existing=match;existing['sourceOrdinals'].append(p['sourceOrdinal'])
  merges.append({'sourceOrdinal':p['sourceOrdinal'],'sourceTitle':p['title'],'retainedId':existing['id'],'matchedBy':identity[0],'value':identity[1]})
  mapping.append({'sourceOrdinal':p['sourceOrdinal'],'recordId':existing['id']});continue
 record['url']='https://doi.org/'+doi if doi else ('https://arxiv.org/abs/'+a[1] if a else 'https://inspirehep.net/literature?q='+quote('find title "'+record['title']+'"'))
 record['linkType']='doi' if doi else ('arxiv' if a else 'search')
 records.append(record);mapping.append({'sourceOrdinal':p['sourceOrdinal'],'recordId':record['id']})
 for identity in identities(record):index[identity]=record
records.sort(key=lambda p:-(p['year'] or 0))
assert len(mapping)==len(source['records'])
assert len({p['id'] for p in records})==len(records)
assert len({key(p['title']) for p in records})==len(records)
for field in ['doi','arxiv']:
 values=[p[field] for p in records if p.get(field)];assert len(values)==len(set(values)),field
report={'archiveCount':len(source['records']),'existingCount':len(selected),'mergedCount':len(merges),'outputCount':len(records),'merges':merges,'sourceMapping':mapping,'verification':'Archive import only. Bibliographic status and externally inferred metadata are deferred to stage 5B.'}
(root/'assets/bibliography.json').write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n')
(root/'data/bibliography-import-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
t={'en':{},'fr':{}}
def tr(k,en,fr,tag='span',attrs=''):
 t['en'][k]=en;t['fr'][k]=fr
 return f'<{tag} data-i18n="{k}" {attrs}>{en}</{tag}>'
esc=html.escape
body='<section class="section" id="publications"><div class="container">'+tr('b5label','Research · Bibliography','Recherche · Bibliographie','p','class="eyebrow"')+tr('b5title','Publications & preprints','Publications et prépublications','h1')+tr('b5intro',f'{len(records)} distinct references combining the existing selection and the archived bibliography, spanning 2011–2026.',f'{len(records)} références distinctes réunissant la sélection existante et la bibliographie archivée, de 2011 à 2026.','p')+tr('b5note','Weebly records retain the bibliographic information available in the archive of 2 November 2026. Some preprints may since have been published; their status and metadata will be updated separately. INSPIRE search links are title searches, not verified article records.','Les notices Weebly conservent les informations bibliographiques de la sauvegarde du 2 novembre 2026. Certaines prépublications peuvent avoir été publiées depuis ; leurs statuts et métadonnées seront actualisés séparément. Les liens de recherche INSPIRE sont des recherches par titre, pas des notices d’article vérifiées.','p','class="archive-note"')+'<div class="academic-profiles"><a class="text-link" href="assets/bibliography.json" download>'+tr('b5json','Download all 62 records (JSON)','Télécharger les 62 notices (JSON)')+'</a><a class="text-link" href="assets/selected-publications.bib" download>'+tr('b5bib','BibTeX · 6 selected publications','BibTeX · 6 publications sélectionnées')+'</a></div><nav class="academic-profiles" aria-label="Publication years">'
for year in sorted({p['year'] for p in records},reverse=True):body+=f'<a class="text-link" href="#year-{year}">{year}</a>'
body+='</nav>'
for year in sorted({p['year'] for p in records},reverse=True):
 body+=f'<section id="year-{year}" aria-labelledby="heading-{year}"><h2 id="heading-{year}">{year}</h2>'
 for p in [p for p in records if p['year']==year]:
  body+=f'<article class="publication" id="{p["id"]}"><div class="publication-year">{year}</div><div class="publication-content"><h3 class="publication-title">{esc(p["title"])}</h3><p class="publication-authors">{esc(p["details"])}</p>'
  body+=tr('b5sourceRecent','Existing selection','Sélection existante','p','class="publication-note"') if p['source']=='existing-selection' else tr('b5sourceArchive','Weebly archive · metadata to be updated','Archive Weebly · métadonnées à actualiser','p','class="publication-note"')
  body+='</div><div class="publication-links"><a href="'+esc(p['url'],quote=True)+'" target="_blank" rel="noopener">'+(tr('b5search','Search INSPIRE','Rechercher sur INSPIRE') if p['linkType']=='search' else tr('b5article','Read article','Consulter l’article'))+' ↗</a></div></article>'
 body+='</section>'
body+='</div></section>'
(root/'templates/publications.html').write_text(body+'\n')
(root/'assets/bibliography-content.js').write_text('/* Bibliography page translations */\n'+''.join('Object.assign(window.SITE_CONTENT.translations.'+lang+', '+json.dumps(vals,ensure_ascii=False)+');\n' for lang,vals in t.items()))
print(json.dumps({k:v for k,v in report.items() if k not in ['sourceMapping','verification']},ensure_ascii=False,indent=2))
