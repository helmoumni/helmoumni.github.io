# Hasan El Moumni — Personal academic website

Static website for [helmoumni.github.io](https://helmoumni.github.io/), with an English/French presentation and French teaching resources. Initial version: 2 November 2026.

## Content

- About and academic background.
- Three research themes: horizon thermodynamics, spacetime geometry and observations, particle dynamics and QPOs.
- Six selected publications, with thematic filters, DOI/arXiv links and BibTeX citations.
- Teaching resources and an existing interactive mechanics pilot.
- University email, ORCID and ResearchGate profile links.

The teaching archive is linked explicitly as an archive. The pendulum chapter is a pedagogical prototype, not a replacement for all experimental skills. No unpublished research projects or confidential documents are included.

## Updating the site

- Main copy and bibliography: `assets/content.js`.
- Layout and teaching content: `index.html`.
- Visual style: `assets/style.css`.
- Portrait: `assets/hasan-el-moumni.png`. The original supplied portrait is copied without pixel modification.
- Standalone mechanics chapter: `teaching/pendule.html`.
- Selected bibliography: regenerate with `python3 scripts/generate-bibliography.py` after editing the publication data (requires Node.js).

No framework, dependency installation or build step is needed. Run `python3 -m http.server 8000` in this directory and open `http://localhost:8000` to preview locally.

GitHub Pages publication: branch `main`, source folder `/ (root)`. The `.nojekyll` file requests plain static hosting.

## Checks

Run `node --check assets/content.js`, `node --check assets/main.js` and `python3 scripts/check-site.py`.

The website has no contact-form backend, analytics or third-party JavaScript. Language preference and the mechanics notebook use browser-local storage. External academic services open only when a visitor follows a link.

Content provenance is documented in [SOURCES.md](SOURCES.md). This initial version carries no explicit reuse license; a license can be added when the author has chosen the intended reuse terms.


## Multipage structure — stage 2 (3 November 2026)

The twelve editorial pages share templates/page.html and templates/pages.json.
Regenerate after editing these sources with python3 scripts/build-pages.py.
assets/content.js remains the single source for translations and selected publications.
The homepage retains its historical section anchors; teaching/pendule.html is unchanged.
Run python3 scripts/check-site.py and node --check assets/main.js after regeneration.
New course pages currently link to the existing archives. Full content migration is planned in later stages.
