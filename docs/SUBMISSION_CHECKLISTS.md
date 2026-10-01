# Submission checklists — exact values to enter, per venue

*Prepared for Pranjul Rathour. Everything below is free. Account creation and the final "publish/submit" click are yours; I never log in or enter credentials. Where a field asks whether AI tools were used, answer truthfully according to the venue's definition. Re-check each venue's current rules on the day: they changed several times in 2025–2026.*

Identity to use everywhere (keep it byte-identical so Google and Scholar merge the records):

| Field | Value |
|---|---|
| Name | Pranjul Rathour |
| Affiliation | Independent researcher, Kanpur, India |
| Email | pranjulrathour41@gmail.com |
| Website | https://pranjulrathour.scult.in |
| Code | https://github.com/Pranjulrathour/research |
| ORCID | create first at orcid.org (free, 2 minutes); then paste the same ORCID into every venue |

## 0. Order of operations (do these first, in this order)

1. **ORCID** (orcid.org): register; add employment "Independent researcher"; add website and GitHub links; set record public.
2. **Google Scholar profile** (scholar.google.com/citations): create with the Gmail; name exactly "Pranjul Rathour"; affiliation "Independent researcher"; homepage pranjulrathour.scult.in; make profile public. Papers will attach automatically after indexing (Preprints.org and SSRN are indexed; typically 1–4 weeks).
3. **Push the repo** to github.com/Pranjulrathour/research (public). Every paper's "Data and code availability" points there.
4. **Zenodo** (zenodo.org, log in with GitHub): enable the research repo under "GitHub" so each GitHub release gets a DOI automatically. Make release `v1.0-p1` after the first paper is final, and so on. Zenodo DOIs are the permanent archive of each paper's code, results and data provenance (the data themselves are not redistributed; `papers/fetch_data.py` re-downloads them and checks the recorded hashes).
5. **ISBN** (isbn.gov.in, Raja Rammohun Roy National Agency): register as an author-publisher, apply for ISBNs for both books (eBook format). Free; 7–15 working days typical. Needed for Google Play Books; not needed for Kindle or Leanpub, so publish those first.

## 1. Papers

### Preprints.org (primary for P1, P2, P4, P5) — preprints.org

Free; Crossref DOI; screening in under 24 hours in practice; indexed by Google Scholar, Europe PMC, Scilit. Accepts papers not yet submitted to a journal.

| Field | P1 | P2 | P4 | P5 |
|---|---|---|---|---|
| Title | Fat Tails and the Failure of Gaussian Risk Models: Out-of-Sample Value-at-Risk Evidence from NIFTY 50 and S&P 500, 2010–2026 | Do Machine-Learning Return Predictors Beat Linear Baselines Out of Sample? A Small-Scale Walk-Forward Replication on Public Equity Data | Recall–Latency Frontiers of Approximate Nearest-Neighbour Indexes on Public Datasets | Card-Fraud Detection Under Extreme Class Imbalance: A Time-Aware, Cost-Sensitive Benchmark on Public Data |
| Subject area | Business, Economics & Management → Finance | Business, Economics & Management → Finance (or Computer Science → AI) | Computer Science & Mathematics → Data Structures / Information Retrieval | Computer Science & Mathematics → Artificial Intelligence / Machine Learning |
| Keywords | from the paper's front matter (5–8) | same | same | same |
| Abstract | paste from paper.md | same | same | same |
| File | PDF (built from paper.md, single column) | same | same | same |
| Supplementary | link to GitHub folder + Zenodo DOI | same | same | same |
| Funding | None | None | None | None |
| Conflicts | None declared | None | None | None |
| Data availability | "Code, results and data provenance at https://github.com/Pranjulrathour/research/tree/main/papers/<folder>; the public data are re-downloaded and hash-checked by papers/fetch_data.py; archived at Zenodo DOI <…>" | same | same | same |
| Licence | CC BY 4.0 (default) | same | same | same |
| AI-use statement (if asked) | paste the "Use of AI tools" sentence from the paper's Declarations, and make sure it matches what you actually did; the venues (MDPI/Preprints.org, IEEE/TechRxiv, Elsevier/SSRN) require a disclosure of this kind | same | same | same |

### TechRxiv (secondary for P3, P4) — techrxiv.org (IEEE)

Free; DOI; moderation about 4 business days; the natural home for the two systems papers. Use the IEEE two-column PDF build. Fields as above; category "Computing and Processing". Can be *in addition to* Preprints.org only if both venues' terms allow (Preprints.org allows prior preprints; TechRxiv asks that the work not already be published in a journal, which is satisfied). If in doubt, put P3 on TechRxiv and P4 on Preprints.org and do not double-post.

### SSRN (secondary for P1, P2) — ssrn.com

Free; the standard preprint server for finance and economics; indexed by Scholar; "SSRN" on a CV is recognised by quant recruiters. Submit P1 and P2 to the Financial Economics Network (FEN) with JEL codes from each paper (P1: C58, G17, G32; P2: C45, C53, G11, G17). Fields as above. SSRN allows the same paper to be on another preprint server; state the Preprints.org DOI in the "Notes" field.

### Not used, and why

- **arXiv**: CS categories require an endorser with ≥5 recent arXiv papers in the category since January 2026, and since 31 October 2025 CS rejects review/position papers without prior peer review. P1–P5 are empirical, not reviews, but endorsement is the blocker. Revisit after a first peer-reviewed publication.
- **Journals / conferences**: the 20 October deadline rules out peer review for this round. The honest wording on the CV and the portfolio is "preprint" or "working paper", never "published in" or "peer-reviewed". A later round can submit P1 to a finance journal and P3/P4 to a systems venue.

## 2. Books

### Amazon KDP (both books, eBook) — kdp.amazon.com

Free; no ISBN required for Kindle (Amazon assigns an ASIN); worldwide; royalty 70% in the ₹99–₹449 band for India with KDP Select, or 35% otherwise.

| Field | The AGI Transition | Systems That Scale |
|---|---|---|
| Language | English | English |
| Book title | The AGI Transition | Systems That Scale |
| Subtitle | A Field Guide for the Next Decade | The Engineering Judgment Behind Reliable, Low-Latency Software |
| Series | (leave blank) | (leave blank) |
| Edition | 1 | 1 |
| Author | Pranjul Rathour | Pranjul Rathour |
| Description | from `books/build_book.py` META description, expanded to 2–3 paragraphs from the preface | same |
| Publishing rights | I own the copyright and hold the necessary publishing rights | same |
| Primary audience | Not for children; no sexually explicit content | same |
| Keywords (7) | artificial intelligence, AGI, future of work, AI careers, technology policy, India technology, AI education | system design, distributed systems, software architecture, latency, reliability engineering, system design interview, scalability |
| Categories (3) | Computers › Artificial Intelligence; Business & Economics › Industries › Computers & IT; Education › Higher | Computers › Software Development & Engineering › Systems Analysis & Design; Computers › Networking › Distributed Systems; Computers › Programming |
| AI-generated content question | Answer truthfully per Amazon's current definition (Amazon distinguishes "AI-generated" from "AI-assisted"; read the definitions on the form that day) | same |
| Manuscript | `books/agi-transition/build/agi-transition.epub` | `books/systems-that-scale/build/systems-that-scale.epub` |
| Cover | `books/agi-transition/cover/cover.png` (1600×2560) | `books/systems-that-scale/cover/cover.png` |
| ISBN | leave blank (Kindle does not need one) | leave blank |
| DRM | No | No |
| Territories | All | All |
| Pricing | ₹299 India / $4.99 US (70% band) or set free-promo via KDP Select later | same |
| KDP Select | Your choice: it gives 70% in India and promo tools but requires Kindle exclusivity for 90 days, which conflicts with Leanpub/Google Play. For the Knowledge Panel goal, breadth beats exclusivity: **do not enrol**, accept 35% in India. | same |

Also create an **Amazon Author Central** profile (author.amazon.com) with the same name, photo and bio as the books; link the website. This page is a strong entity signal.

### Leanpub (both books) — leanpub.com

Free to publish; upload EPUB/PDF directly ("Bring your own book"); set minimum price ₹0/$0 and suggested price, or free. Author page with bio and links. Books can be updated without limit, which suits a "field guide" that will be revised.

### Google Play Books (both books, after ISBNs arrive) — play.google.com/books/publish

Free; requires an ISBN per book; India payments supported. Upload EPUB and cover; fill the same metadata; set price or free. Google Play Books listings feed Google's book entity data, which is directly relevant to the Knowledge Panel.

### Archive copies

- **Zenodo**: upload each book's PDF as a separate record with type "Book", licence "All rights reserved" (or CC BY-NC-ND if you want free sharing), and get a DOI. Cite the DOI on the portfolio.
- **Internet Archive** (archive.org): optional, free, permanent; adds another authoritative URL for the same title.

## 3. After publishing

1. **Portfolio** (pranjul-portfolio, profile.ts): add a "Publications" section with the two books (cover, link to each store, DOI) and the five papers (title, venue, DOI, code link). Add each book's ISBN/ASIN and each paper's DOI to the Person schema `sameAs`/`subjectOf` where appropriate.
2. **GitHub Pages SEO site**: a `/publications/` page with the same list and `ScholarlyArticle` / `Book` JSON-LD; add Scholar, ORCID and SSRN author URLs to the Person `sameAs`.
3. **Resume block**:

   > **Publications (2026; books self-published, papers are preprints)**
   > Rathour, P. (2026). *The AGI Transition: A Field Guide for the Next Decade.* Kindle/Leanpub/Google Play. ISBN ….
   > Rathour, P. (2026). *Systems That Scale: The Engineering Judgment Behind Reliable, Low-Latency Software.* Kindle/Leanpub/Google Play. ISBN ….
   > Rathour, P. (2026). Fat tails and the failure of Gaussian risk models: out-of-sample VaR evidence from NIFTY 50 and S&P 500, 2010–2026. *Preprints.org / SSRN*, doi:….
   > Rathour, P. (2026). Do machine-learning return predictors beat linear baselines out of sample? A walk-forward replication on public equity data. *Preprints.org / SSRN*, doi:….
   > Rathour, P. (2026). Tail latency under load: an empirical comparison of threaded, async and hybrid API server designs. *TechRxiv*, doi:….
   > Rathour, P. (2026). Recall–latency frontiers of approximate nearest-neighbour indexes on public datasets. *Preprints.org*, doi:….
   > Rathour, P. (2026). Card-fraud detection under extreme class imbalance: a time-aware, cost-sensitive benchmark on public data. *Preprints.org*, doi:….
   > Code and data for all papers: github.com/Pranjulrathour/research.

4. **Wording discipline**: "preprint", "working paper", "self-published" are the words. Never "peer-reviewed", never "published in [journal]". Recruiters at the target firms check, and the honest version is still far more than most candidates have.
5. **Brand-engine**: one LinkedIn post per publication (not a burst), each linking the DOI or store page, spaced over October–November; Blogger long-form summary of each paper with the figures; the books' "What to do this year" sections make natural carousel content.
