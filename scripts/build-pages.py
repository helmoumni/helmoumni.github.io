from pathlib import Path
import json,re
root=Path(__file__).resolve().parents[1]
shell=(root/'templates/page.html').read_text()
pages=json.loads((root/'templates/pages.json').read_text())
for path,(en,fr,body) in pages.items():
    if path in ('research.html', 'publications.html'):
        body = (root/'templates'/path).read_text()
    prefix='../' if path.startswith('teaching/') else ''
    page=shell.replace('{{CONTENT}}',body)
    # Assets always live in the root assets folder.
    page=re.sub(r'(href|src)="assets/',lambda m:m[1]+'="'+prefix+'assets/',page)
    # Shell navigation and footer links are relative to root.
    for tag in ['header','footer']:
        pattern=r'<'+tag+r'\b.*?</'+tag+'>'
        def fix(m):
            text=m[0]
            text=re.sub(r'href="(?!https?:|mailto:|#)([^"]+)"',lambda a:'href="'+prefix+a[1]+'"',text)
            text=text.replace('href="'+prefix+path+'"','href="'+prefix+path+'" aria-current="page"')
            return text
        page=re.sub(pattern,fix,page,flags=re.S)
    if path!='index.html':
        page=page.replace('<body>','<body class="inner-page" data-title-en="'+en+'" data-title-fr="'+fr+'">')
        breadcrumb='<div class="container breadcrumb"><a href="'+prefix+'index.html" data-i18n="navHome">Home</a> / '
        if path.startswith('teaching/') and path!='teaching/index.html':
            breadcrumb+='<a href="index.html" data-i18n="navTeaching">Teaching</a> / '
        breadcrumb+=fr+'</div>'
        page=page.replace('<main id="main">','<main id="main">'+breadcrumb)
        page=re.sub(r'<title>.*?</title>','<title>'+en+' — Hasan El Moumni</title>',page)
        page=re.sub(r'(<link rel="canonical" href=")[^"]+',r'\g<1>https://helmoumni.github.io/'+path,page)
        page=re.sub(r'(<meta property="og:url" content=")[^"]+',r'\g<1>https://helmoumni.github.io/'+path,page)
        page=re.sub(r'(<meta property="og:title" content=")[^"]+',r'\g<1>'+en+' — Hasan El Moumni',page)
        page=page.replace('href="#publications"','href="publications.html"')
    else:
        page=page.replace('</main>','<div class="container section-links"><a class="text-link" href="teaching/index.html" data-i18n="browseCourses">Browse courses</a></div></main>')
    if path in ('research.html', 'publications.html'):
        extra = 'research-content.js' if path == 'research.html' else 'bibliography-content.js'
        page = page.replace('<script src="assets/content.js"></script>', '<script src="assets/content.js"></script><script src="assets/' + extra + '"></script>')
        def minimal_schema(match):
            data = json.loads(match[1])
            data.pop('email', None)
            return '<script type="application/ld+json">' + json.dumps(data, ensure_ascii=False) + '</script>'
        page = re.sub(r'<script type="application/ld\+json">(.*?)</script>', minimal_schema, page)
    if path == 'publications.html':
        page = page.replace('</head>', '<link rel="stylesheet" href="assets/bibliography.css"></head>')
        page = page.replace('</body>', '<script src="assets/bibliography-filters.js"></script></body>')
    (root/path).parent.mkdir(exist_ok=True,parents=True)
    (root/path).write_text(page)
urls=['https://helmoumni.github.io/'+('' if p=='index.html' else p) for p in pages]+['https://helmoumni.github.io/teaching/pendule.html']
(root/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join('<url><loc>'+u+'</loc></url>' for u in urls)+'</urlset>\n')
print('Generated',len(pages),'pages.')
