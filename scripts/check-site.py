from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlparse, unquote
import json, subprocess

root=Path(__file__).resolve().parents[1]
class Page(HTMLParser):
    def __init__(self): super().__init__();self.ids=[];self.refs=[];self.i18n=[];self.links=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'id' in a:self.ids.append(a['id'])
        if 'data-i18n' in a:self.i18n.append(a['data-i18n'])
        for attr in ['href','src']:
            if attr in a:self.refs.append(a[attr])

pages={}
for file in root.rglob('*.html'):
    if 'templates' in file.parts: continue
    parsed_page=Page();parsed_page.feed(file.read_text())
    assert len(parsed_page.ids)==len(set(parsed_page.ids)), f'Duplicate IDs: {file}'
    pages[file.resolve()]=parsed_page
for file,parsed_page in pages.items():
    for ref in parsed_page.refs:
        parsed=urlparse(ref)
        if parsed.scheme or ref.startswith('//'):continue
        target=((root/unquote(parsed.path).lstrip('/')) if parsed.path.startswith('/') else (file.parent/unquote(parsed.path))).resolve() if parsed.path else file
        if target.is_dir(): target=target/'index.html'
        assert target.is_file(), f'Missing file in {file}: {ref}'
        if parsed.fragment and target in pages:
            assert parsed.fragment in pages[target].ids, f'Missing anchor in {file}: {ref}'
page=pages[(root/'index.html').resolve()]
js="global.window={};require('./assets/content.js');console.log(JSON.stringify(window.SITE_CONTENT))"
content=json.loads(subprocess.check_output(['node','-e',js],cwd=root,text=True))
for language in ['en','fr']:
    missing={key for parsed_page in pages.values() for key in parsed_page.i18n}-set(content['translations'][language])
    assert not missing, f'Missing {language} translation: {missing}'
pubs=content['publications']
assert len({p['id'] for p in pubs})==len(pubs), 'Duplicate publication IDs'
assert len({p['doi'] for p in pubs})==len(pubs), 'Duplicate DOIs'
assert all(p['category'] in ['thermodynamics','shadows','qpo'] for p in pubs)
assert all(p['year']<=2026 for p in pubs), 'Unverified future publications'
assert all('H. El Moumni' in p['authors'] for p in pubs)
assert (root/'assets/selected-publications.bib').read_text().count('@article{')==len(pubs)
book=(root/'teaching/pendule.html').read_text()
assert 'data-offline="true"' in book and 'PendulumPhysics' in book, 'Incomplete mechanics resource'
assert 'script src=' not in book, 'Mechanics resource should remain standalone'
assert (root/'assets/hasan-el-moumni.png').is_file()
print('Site checks passed: local links, anchors, translations, publication metadata and standalone teaching resource.')

