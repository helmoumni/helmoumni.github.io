from pathlib import Path
import json,re
from html import escape
root=Path(__file__).resolve().parents[1]
shell=(root/'templates/page.html').read_text()
pages=json.loads((root/'templates/pages.json').read_text())
descriptions={
    'index.html':('Hasan El Moumni, Full Professor of theoretical physics at Ibn Zohr University. Research on black holes, gravitation, generalized entropy and strong-gravity phenomenology.','Hasan El Moumni, professeur de physique théorique à l’Université Ibn Zohr. Recherches sur les trous noirs, la gravitation, les entropies généralisées et la gravitation forte.'),
    'about.html':('Biography, academic career, education, research visit and scholarly profiles of theoretical physicist Hasan El Moumni.','Biographie, parcours universitaire, formation, séjour scientifique et profils académiques du physicien théoricien Hasan El Moumni.'),
    'research.html':('Research directions of Hasan El Moumni: black-hole thermodynamics, generalized entropy, shadows, lensing, particle dynamics and quasi-periodic oscillations.','Axes de recherche de Hasan El Moumni : thermodynamique des trous noirs, entropies généralisées, ombres, lentilles, dynamique des particules et QPO.'),
    'publications.html':('Bibliography of Hasan El Moumni in black-hole physics, gravitation, high-energy physics, generalized thermodynamics and astrophysical phenomenology.','Bibliographie de Hasan El Moumni en physique des trous noirs, gravitation, hautes énergies, thermodynamique généralisée et phénoménologie astrophysique.'),
    'contact.html':('University contact details for Hasan El Moumni, Full Professor of theoretical physics at Ibn Zohr University in Agadir, Morocco.','Coordonnées universitaires de Hasan El Moumni, professeur de physique théorique à l’Université Ibn Zohr, Agadir, Maroc.'),
    'activities.html':('Academic activities of Hasan El Moumni: research leadership, doctoral supervision, editorial service, peer review, collaborations, visits and scientific events.','Activités académiques de Hasan El Moumni : responsabilité scientifique, encadrement doctoral, édition, évaluation, collaborations, séjours et événements.'),
    'teaching/index.html':('Teaching portal of Hasan El Moumni: statistical physics, quantum mechanics, relativity, nuclear physics and simulations.','Portail des enseignements de Hasan El Moumni : physique statistique, mécanique quantique, relativité, physique nucléaire et simulations.'),
    'teaching/physique-statistique.html':('Cours, TD, corrections d’examens et vidéos de physique statistique, classés par année et par type de ressource.','Cours, TD, corrections d’examens et vidéos de physique statistique, classés par année et par type de ressource.'),
    'teaching/mecanique-quantique.html':('Travaux dirigés, corrections, captures du tableau et vidéos de mécanique quantique, organisés par série et par exercice.','Travaux dirigés, corrections, captures du tableau et vidéos de mécanique quantique, organisés par série et par exercice.'),
    'teaching/relativite-cosmologie.html':('Supports archivés de relativité générale et cosmologie : polycopié, diaporama et annales du Master Matière et Rayonnement.','Supports archivés de relativité générale et cosmologie : polycopié, diaporama et annales du Master Matière et Rayonnement.'),
    'teaching/physique-nucleaire.html':('Polycopié de travaux pratiques de physique nucléaire et correction de la manipulation 3 pour le semestre 5.','Polycopié de travaux pratiques de physique nucléaire et correction de la manipulation 3 pour le semestre 5.'),
    'teaching/outils-simulations.html':('Outils pédagogiques et simulations : livre laboratoire sur le pendule, effet tunnel, problème à deux corps et physique au cinéma.','Outils pédagogiques et simulations : livre laboratoire sur le pendule, effet tunnel, problème à deux corps et physique au cinéma.')
}
for path,(en,fr,body) in pages.items():
    if path in ('research.html', 'publications.html', 'activities.html', 'teaching/index.html', 'teaching/physique-statistique.html', 'teaching/mecanique-quantique.html', 'teaching/relativite-cosmologie.html', 'teaching/physique-nucleaire.html', 'teaching/outils-simulations.html'):
        body = (root/'templates'/path).read_text()
    if path == 'about.html':
        body = body.replace('<h2 id="aboutTitle"', '<h1 id="aboutTitle"', 1).replace('</h2>', '</h1>', 1)
    if path == 'contact.html':
        body = body.replace('<h2 id="contactTitle"', '<h1 id="contactTitle"', 1).replace('</h2>', '</h1>', 1)
    prefix='../' if path.startswith('teaching/') else ''
    desc_en,desc_fr=descriptions[path]
    page=shell.replace('{{CONTENT}}',body)
    page=re.sub(r'(<meta name="description" content=")[^"]+',lambda m:m[1]+escape(desc_en,quote=True),page)
    page=re.sub(r'(<meta property="og:description" content=")[^"]+',lambda m:m[1]+escape(desc_en,quote=True),page)
    if path in ('index.html', 'about.html'):
        profile_end = 'Web of Science · T-6745-2019 ↗</a>'
        assert profile_end in page
        page = page.replace(profile_end, profile_end + '<a class="text-link" href="https://www.scopus.com/authid/detail.uri?authorId=55866171000" target="_blank" rel="noopener">Scopus ↗</a>')
    if path == 'index.html':
        page = page.replace('href="https://helmoumni.weebly.com/teaching.html" target="_blank" rel="noopener"', 'href="teaching/physique-statistique.html"', 1)
        page = page.replace('href="https://helmoumni.weebly.com/teaching.html" target="_blank" rel="noopener"', 'href="teaching/relativite-cosmologie.html"', 1)
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
        page=page.replace('<body>','<body class="inner-page" data-title-en="'+escape(en,quote=True)+'" data-title-fr="'+escape(fr,quote=True)+'" data-description-en="'+escape(desc_en,quote=True)+'" data-description-fr="'+escape(desc_fr,quote=True)+'">')
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
        page=page.replace('<body>','<body data-description-en="'+escape(desc_en,quote=True)+'" data-description-fr="'+escape(desc_fr,quote=True)+'">')
        page=page.replace('</main>','<div class="container section-links"><a class="text-link" href="teaching/index.html" data-i18n="browseCourses">Browse courses</a></div></main>')
    if path in ('research.html', 'publications.html'):
        extra = 'research-content.js' if path == 'research.html' else 'bibliography-content.js'
        page = page.replace('<script src="assets/content.js"></script>', '<script src="assets/content.js"></script><script src="assets/' + extra + '"></script>')
        def minimal_schema(match):
            data = json.loads(match[1])
            data.pop('email', None)
            return '<script type="application/ld+json">' + json.dumps(data, ensure_ascii=False) + '</script>'
        page = re.sub(r'<script type="application/ld\+json">(.*?)</script>', minimal_schema, page)
    if path in ('teaching/index.html', 'teaching/physique-statistique.html', 'teaching/mecanique-quantique.html', 'teaching/relativite-cosmologie.html', 'teaching/physique-nucleaire.html', 'teaching/outils-simulations.html'):
        page = page.replace('</head>', '<link rel="stylesheet" href="../assets/teaching-resources.css"></head>')
    if path == 'research.html':
        page = page.replace('</head>', '<link rel="stylesheet" href="assets/arabic-writing.css"></head>')
    if path == 'activities.html':
        page = page.replace('</head>', '<link rel="stylesheet" href="assets/activities.css"></head>')
    if path == 'publications.html':
        page = page.replace('</head>', '<link rel="stylesheet" href="assets/bibliography.css"></head>')
        page = page.replace('</body>', '<script src="assets/bibliography-filters.js"></script></body>')
    (root/path).parent.mkdir(exist_ok=True,parents=True)
    (root/path).write_text(page)
urls=['https://helmoumni.github.io/'+('' if p=='index.html' else p) for p in pages]+['https://helmoumni.github.io/teaching/pendule.html']
(root/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join('<url><loc>'+u+'</loc></url>' for u in urls)+'</urlset>\n')
print('Generated',len(pages),'pages.')
