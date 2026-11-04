# Content sources

Verified on 2 November 2026. The homepage contains a selected bibliography, not a live citation dashboard. Public professional information and the author's supplied teaching context were used; personal phone numbers and unpublished work were omitted.

- **Name, current rank, affiliation, professional email and identifier:** [ORCID 0000-0001-7408-0910](https://orcid.org/0000-0001-7408-0910). Full Professor at Ibn Zohr University is the current role; the outdated rank on the former website was not retained.
- **Academic background:** [Author's previous biography](https://helmoumni.weebly.com/bio.html), for the 2014 PhD at Cadi Ayyad University and 2018 habilitation at Ibn Zohr University. No current head-of-team or editorial title was inferred from this older page.
- **Teaching archive:** [Author's teaching page](https://helmoumni.weebly.com/teaching.html). These links are labelled as archives and do not imply validation of every external file or current semester requirement.
- **Professional profile:** [ResearchGate](https://www.researchgate.net/profile/Hasan-El-Moumni-2).
- **Modified Unruh thermodynamics:** [APS issue record](https://journals.aps.org/prresearch/issues/8/1), Physical Review Research 8, 013260 (2026), [DOI 10.1103/mnm4-mylh](https://doi.org/10.1103/mnm4-mylh).
- **Bayesian QPO constraints:** [Publisher record](https://www.sciencedirect.com/science/article/pii/S2212686426001007), Physics of the Dark Universe 52, 102311 (2026), DOI 10.1016/j.dark.2026.102311.
- **Rényi microstructure:** [Publisher record](https://www.sciencedirect.com/science/article/pii/S0550321325004456), Nuclear Physics B 1022, 117239 (2026), DOI 10.1016/j.nuclphysb.2025.117239; arXiv:2508.07357.
- **HF-QPOs and CDM halos:** [Springer record](https://link.springer.com/article/10.1140/epjc/s10052-025-14830-6), European Physical Journal C 85, 1090 (2025), DOI 10.1140/epjc/s10052-025-14830-6; arXiv:2507.11139.
- **Accelerating black-hole shadows:** [Publisher record](https://www.sciencedirect.com/science/article/abs/pii/S2212686424003145), Physics of the Dark Universe 47, 101731 (2025), DOI 10.1016/j.dark.2024.101731; arXiv:2409.02594. The website uses a neutral description of the subject, without a claim of observational detection of supersymmetry.
- **Born–Infeld-AdS topology:** [Bibliographic record](https://inspirehep.net/literature/2785036), Annals of Physics 465, 169679 (2024), DOI 10.1016/j.aop.2024.169679; arXiv:2306.11212. The full four-author list and published title were retained.

The portrait is the author's supplied professional portrait. The thematic drawings are original schematic SVGs, not research results. The mechanics chapter is the existing standalone prototype created for this project; it is included without content changes.

## Stage 3 — 4 November 2026
Home academic links and About employment, education and CERN visit come from the Weebly archive captured on 2 November 2026. Current Full Professor rank is retained from the existing site. Undated former responsibilities are not presented as current. INSPIRE and arXiv links are name searches, not verified author identifiers. Web of Science uses ResearcherID T-6745-2019 recorded in the archive. External platforms may require login. CV and postal-address publication remain pending.

## Stage 4 — Research, 4 November 2026
Four research directions synthesize the archived Home topics and Research & Publications bibliography, retaining the current site’s QPO and observational themes. Representative citations reuse the six records already in assets/content.js; arXiv:2301.08321 is explicitly recorded in the archive. QNM, Hawking radiation, higher-dimensional and holographic heat-engine themes are documented in the archived bibliography. This stage does not claim an exhaustive or newly verified bibliography; full import and metadata updates belong to stages 5A and 5B. No unpublished projects are disclosed.

## Stage 5A — Bibliography import, 4 November 2026
The 57 ordered bibliography entries in the archived research-publications.html were extracted to data/weebly-publications.json, with source ordinal and original normalized details. The source HTML SHA-256 is retained. Six existing selected records are merged by DOI, arXiv identifier, then normalized title. One duplicate (arXiv:2306.11212) retains the existing published Annals of Physics record. All 57 source records map to the resulting 62 distinct entries in data/bibliography-import-report.json. Whitespace, TeX nonbreaking spaces and the Rényi accent are normalized; archival metadata are not independently corrected. A displayed year is taken from the archived publication statement, or from the preprint information when unavailable. INSPIRE links are explicitly labelled title searches. Full status verification is deferred to stage 5B. Regenerate with python3 scripts/import-bibliography.py then python3 scripts/build-pages.py.
