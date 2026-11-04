from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlparse, unquote
from xml.etree import ElementTree
import json, re, subprocess

root=Path(__file__).resolve().parents[1]
class Page(HTMLParser):
    def __init__(self):
        super().__init__();self.ids=[];self.refs=[];self.i18n=[];self.anchors=[];self.images=[];self.meta={};self.canonicals=[];self.h1_count=0;self.in_title=False;self.title=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'id' in a:self.ids.append(a['id'])
        if 'data-i18n' in a:self.i18n.append(a['data-i18n'])
        if tag=='h1':self.h1_count+=1
        if tag=='title':self.in_title=True
        if tag=='a':self.anchors.append(a)
        if tag=='img':self.images.append(a)
        if tag=='meta' and 'content' in a:
            key=a.get('name') or a.get('property')
            if key:self.meta[key]=a['content']
        if tag=='link' and 'canonical' in a.get('rel','').split() and 'href' in a:self.canonicals.append(a['href'])
        for attr in ['href','src']:
            if attr in a:self.refs.append(a[attr])
    def handle_endtag(self,tag):
        if tag=='title':self.in_title=False
    def handle_data(self,data):
        if self.in_title:self.title.append(data)

pages={}
for file in root.rglob('*.html'):
    if 'templates' in file.parts: continue
    source=file.read_text()
    parsed_page=Page();parsed_page.feed(source)
    for schema in re.findall(r'<script type="application/ld\+json">(.*?)</script>',source,re.S):
        json.loads(schema)
    assert len(parsed_page.ids)==len(set(parsed_page.ids)), f'Duplicate IDs: {file}'
    assert parsed_page.h1_count==1, f'Expected one H1 in {file}, found {parsed_page.h1_count}'
    assert ''.join(parsed_page.title).strip(), f'Missing title in {file}'
    assert all('alt' in image for image in parsed_page.images), f'Image without alt text in {file}'
    for anchor in parsed_page.anchors:
        parsed=urlparse(anchor.get('href',''))
        if parsed.scheme in ['http','https'] and anchor.get('target')=='_blank':
            assert 'noopener' in anchor.get('rel','').split(), f'External blank link without noopener in {file}: {anchor["href"]}'
    if file.name!='404.html':
        description=parsed_page.meta.get('description','')
        assert 50<=len(description)<=200, f'Invalid description length in {file}: {len(description)}'
        assert all(parsed_page.meta.get(key) for key in ['og:title','og:description','og:url','og:image']), f'Incomplete Open Graph metadata in {file}'
        assert len(parsed_page.canonicals)==1, f'Expected one canonical URL in {file}'
        rel=file.relative_to(root).as_posix()
        expected='https://helmoumni.github.io/'+('' if rel=='index.html' else rel)
        assert parsed_page.canonicals[0]==expected, f'Incorrect canonical URL in {file}'
        assert 'helmoumni.weebly.com' not in source, f'Legacy Weebly link in {file}'
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
js="global.window={};require('./assets/content.js');require('./assets/research-content.js');require('./assets/bibliography-content.js');console.log(JSON.stringify(window.SITE_CONTENT))"
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
sitemap=ElementTree.parse(root/'sitemap.xml')
ns={'s':'http://www.sitemaps.org/schemas/sitemap/0.9'}
sitemap_urls={loc.text for loc in sitemap.findall('s:url/s:loc',ns)}
indexable={page.canonicals[0] for file,page in pages.items() if file.name!='404.html'}
assert sitemap_urls==indexable, f'Sitemap mismatch: missing={indexable-sitemap_urls}, extra={sitemap_urls-indexable}'
assert len({''.join(page.title).strip() for page in pages.values()})==len(pages), 'Duplicate page titles'
print('Site checks passed: links, anchors, headings, metadata, sitemap, translations, publication data and teaching resource.')

