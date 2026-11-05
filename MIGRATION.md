# Migration Weebly → GitHub

Stages 1 and 2 completed. Stage 3 partially published on 4 November 2026:
- Home: academic profile links and full biography link.
- About: historical employment, four qualifications, dissertation topics and CERN visit (2–15 September 2018).
- English/French translations added; current Full Professor rank preserved.
- Portrait, teaching pages, publication records and pendulum unchanged.

CV excluded at the author’s request. Contact/address update left pending; stage 4 does not modify it.

Validation: static links, anchors, translations and JavaScript syntax pass. Browser rendering could not be tested because Chromium socket creation is restricted.

## Stage 4 — Research
Four expanded research directions in English and French, section navigation, and seven representative article links. Existing homepage selection and publication records retained. Static links, anchors, translations and JavaScript syntax checked.

Next: stage 5A, import and deduplicate the archived bibliography; stage 5B, update and verify its metadata.

## Stage 5A — Bibliography import
57 archived notices plus six selected records, with one arXiv duplicate merged: 62 distinct entries. All source entries are accounted for in the import report. Publication page has year navigation, bilingual labels, direct identifiers when known and explicit INSPIRE title-search links otherwise. The homepage’s six selected publications and BibTeX file are unchanged.
Next: stage 5B — verify publication statuses, enrich metadata and add filters.

## Stage 5B — Metadata and filters
69 references: 62 matched uniquely in INSPIRE, seven additional records. 63 DOI links; 64 journal records, three preprints, one forthcoming 2027 issue and one unresolved version. The M-theory publisher candidate 2765745 is held out to avoid likely double counting with arXiv:2301.08321. Year 2015 for DOI 10.1142/S0219887815500176 is corrected using publisher-deposited Crossref dates. Added search, year/theme/status filters, reset, bilingual result counts, full BibTeX export and erratum link.
Regenerate with python3 scripts/update-bibliography.py and python3 scripts/build-pages.py. The original import script alone restores stage 5A metadata and should not be used as the final build step.
Validation: static links, translation coverage, unique identifiers, all 69 rendered cards/BibTeX entries, accent-insensitive search and combined filter logic pass. Browser launch failed in this environment; visual desktop/mobile verification remains pending.

## Stage 6 — Teaching portal and statistical physics
Portal refreshed with a featured statistics library and course-level navigation. Statistical physics now lists 48 unique MEGA documents, five numbered course videos and two complementary resources (55 working URL references, external availability not checked). Earlier course versions (17) and 2025–2026 notes (13) remain distinct; six TD links and 12 exam/resit correction links retain their source associations. Video 3 is explicitly missing its URL. The two labels “Annales” and “Polycopié de TD” share one source link, displayed once. Homepage statistics link now points to the migrated page. Next lot: quantum mechanics, relativity and nuclear practicals.

## Stage 7 — Quantum mechanics, relativity and nuclear practicals
Three course pages now expose 14 MEGA documents and six quantum mechanics videos. Quantum corrections preserve series/problem associations and the distinct 2017–2018 / 2019–2020 periods. Series 4 problem 2 has no capture/video URLs in the archive and is explicitly marked. Relativity retains the Master S3 2021–2024 context; nuclear practicals retain SMP-S5 2021–2022 and manipulation 3. Portal cards and homepage relativity link updated. Next lot: tools and simulations.

## Stage 8 — Tools and simulations
Expanded the tools page with the existing pendulum laboratory, its preparation/measurement/analysis workflow, and three archived external resources. No simulation code changed. The Nantes two-body link returned HTTP 404 on 2026-11-04 and is explicitly unavailable; Zenodo could not be retrieved, and YouTube availability is unchecked. Next lot: academic activities.

## Stage 9 — Academic activities
The former placeholder is replaced by a bilingual activities page covering dated research leadership, editorial and peer-review service, doctoral supervision, archived collaborators, the CERN visit, and three events referenced by the archived site. The 2024 “Black holes inside and out” poster is restored as a downloadable PDF. The ASP and ICS3EIS entries explicitly state that the archive does not establish personal participation. Historical appointments are labelled as archival rather than current.

## Stage 10 — Final audit
Added unique bilingual descriptions for all generated pages, Open Graph/Twitter metadata, canonical and social metadata for the standalone pendulum laboratory, richer scholarly profile links in Person structured data, and noindex metadata for the 404 page. Corrected the About and Contact heading hierarchy so every public page has exactly one H1. The site checker now enforces heading, metadata, canonical, sitemap, image-alt, external-link safety and legacy-link rules in addition to its earlier checks.

## Research podcast
Restored the archived Spotify show as a dedicated bilingual “Giving physics a voice” section on the Research page. The official Spotify embed is lazy-loaded, titled for assistive technology and paired with a direct show link. The surrounding design follows the site’s graphite, green and orange visual identity.
