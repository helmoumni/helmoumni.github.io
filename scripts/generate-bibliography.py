from pathlib import Path
import json, subprocess
root=Path(__file__).resolve().parents[1]
js="global.window={};require('./assets/content.js');console.log(JSON.stringify(window.SITE_CONTENT.publications))"
pubs=json.loads(subprocess.check_output(['node','-e',js],cwd=root,text=True))
entries=[]
for p in pubs:
    fields=[('title',p['bibTitle']),('author',p['bibAuthors']),('journal',p['journal']),('year',p['year']),('volume',p['volume']),('pages',p['pages']),('doi',p['doi'])]
    if p.get('arxiv'): fields += [('eprint',p['arxiv']),('archivePrefix','arXiv')]
    entries.append('@article{'+p['id']+',\n'+',\n'.join('  '+k+' = {'+str(v)+'}' for k,v in fields)+'\n}')
(root/'assets/selected-publications.bib').write_text('\n\n'.join(entries)+'\n')
print(f'{len(entries)} BibTeX entries generated.')
