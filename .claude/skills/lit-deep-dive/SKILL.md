---
name: lit-deep-dive
description: Deep-dive analysis of a single paper by DOI or PMID — full text, citing/related papers, code/data availability, and reproducibility assessment.
user_invocable: true
argument: identifier - a DOI (e.g., "10.1038/s41586-026-10222-2") or PMID (e.g., "41850247")
---

# Literature Deep Dive

Given a single paper identifier (DOI or PMID), produce an exhaustive analysis including full text review, related/citing papers, code and data availability, and a reproducibility assessment.

## Instructions

1. **Parse the identifier.** Determine whether the argument is a DOI or PMID:
   - If it starts with `10.` or contains `doi.org` → DOI
   - If it is purely numeric → PMID
   - If it looks like an arXiv ID (e.g., `2603.19766`) → arXiv ID

2. **Dispatch 3 parallel agents** to gather information simultaneously.

   **Paper Metadata Agent prompt:**
   ````
   You are a paper metadata agent. Retrieve full details for this paper: "{identifier}"

   If it is a PMID:
   - Use mcp__claude_ai_PubMed__get_article_metadata with pmids: ["{identifier}"]
   - Use mcp__claude_ai_PubMed__find_related_articles with link_type="pubmed_pmc" to find PMC ID
   - If PMC ID found, use mcp__claude_ai_PubMed__get_full_text_article to get the full text

   If it is a DOI starting with "10.1101" or "10.64898" (bioRxiv/medRxiv):
   - Use mcp__claude_ai_bioRxiv__get_preprint with the DOI
   - Try both server="biorxiv" and server="medrxiv"
   - Use mcp__claude_ai_bioRxiv__search_published_preprints to check if it has been published in a journal

   If it is another DOI:
   - Use mcp__claude_ai_PubMed__search_articles with the DOI to find the PMID
   - Then use mcp__claude_ai_PubMed__get_article_metadata and attempt full text retrieval via PMC

   If it is an arXiv ID:
   - Use WebFetch to fetch https://export.arxiv.org/api/query?id_list={identifier}
     with prompt: "Extract: title, authors, abstract, categories, published date, updated date, DOI if present"

   Return: title, authors (full list), date, journal/source, abstract, full_text (if available), DOI, PMID, all identifiers found.
   ````

   **Related Papers Agent prompt:**
   ````
   You are a related papers agent. Find papers related to: "{identifier}"

   Step 1 — Find related papers:
   - If you have a PMID, use mcp__claude_ai_PubMed__find_related_articles with link_type="pubmed_pubmed", max_results=20
   - For each related PMID, use mcp__claude_ai_PubMed__get_article_metadata to get title, authors, date, abstract

   Step 2 — Search for papers that cite this work or address the same problem:
   - Extract the paper title and key method name from the identifier
   - Use mcp__claude_ai_PubMed__search_articles to search for the method name or key terms, sort by "pub_date", max_results=20
   - Use mcp__claude_ai_bioRxiv__search_preprints with relevant categories, recent_days=90, to find preprints on the same topic

   Return two lists:
   1. "related_papers": papers computationally similar (from PubMed related articles)
   2. "recent_context": recent papers addressing the same problem or using similar methods
   For each paper include: title, authors, date, source, doi/pmid, abstract (first 200 words)
   ````

   **Code & Data Agent prompt:**
   ````
   You are a code and data availability agent. Check reproducibility resources for: "{identifier}"

   Step 1 — Check for code repositories:
   - Use WebFetch on the paper's DOI URL (https://doi.org/{doi}) with prompt: "Find any links to GitHub, GitLab, Bitbucket, Zenodo, Figshare, or code/data availability statements. Extract all repository URLs, data accession numbers (GEO GSE*, SRA SRP*, etc.), and any 'Data Availability' or 'Code Availability' sections."
   - If a GitHub URL is found, use WebFetch on that GitHub URL with prompt: "Extract: repo description, last commit date, number of stars, primary language, whether it has a README, installation instructions, license, and any listed dependencies."

   Step 2 — Check for datasets:
   - Look for GEO accession numbers (GSE*), SRA accessions (SRP*/SRR*), ArrayExpress (E-MTAB-*), Zenodo DOIs
   - If GEO accessions found, use WebFetch on https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc={accession} with prompt: "Extract: title, organism, platform, number of samples, submission date, summary."

   Step 3 — Check for package availability:
   - Search PyPI: WebFetch on https://pypi.org/search/?q={method_name} with prompt: "Is there a package matching this method? Extract: name, version, last updated, downloads."
   - Search Bioconductor: WebFetch on https://bioconductor.org/packages/release/bioc/html/{method_name}.html with prompt: "Does this Bioconductor package exist? Extract: title, version, last updated."

   Return a structured report:
   - code_url: GitHub/GitLab URL or null
   - code_status: {last_commit, stars, language, license, installs_cleanly: unknown}
   - datasets: list of {accession, type, organism, samples, url}
   - package: {pypi: true/false, bioconductor: true/false, conda: unknown}
   - data_availability_statement: quoted text from paper or null
   ````

3. **Synthesize the deep-dive report.** After all agents return, produce:

   ```markdown
   # Deep Dive: [Paper Title]

   **Authors:** full author list
   **Source:** journal / preprint server | **Date:** YYYY-MM-DD
   **DOI:** ... | **PMID:** ... | **arXiv:** ...

   ---

   ## Paper Overview
   3-5 paragraph summary of the paper based on abstract and full text (if available).
   Cover: motivation, approach, key results, and conclusions.

   ## Detailed Methods
   - Algorithms and models (with technical detail)
   - Datasets used (with sizes and platforms)
   - Evaluation metrics and baselines
   - Computational requirements mentioned

   ## Key Results
   - Main quantitative results (with numbers)
   - Key figures/tables summarized
   - Statistical significance noted where available

   ## Critical Assessment

   ### Strengths
   - What the paper does well

   ### Limitations
   - Methodological concerns
   - Missing comparisons or baselines
   - Scalability or generalization concerns

   ### Open Questions
   - What the paper leaves unanswered

   ## Reproducibility Assessment

   | Resource | Status | Details |
   |----------|--------|---------|
   | Code | Available / Not found | URL, language, last updated |
   | Data | Available / Not found | Accessions, sizes |
   | Package | PyPI / Bioconductor / None | Version |
   | Pre-trained models | Available / Not found | URL |

   ### Reproducibility Notes
   - Can this work be reproduced with available resources?
   - What would be needed to adapt it to your pipelines?

   ## Related Work Context

   ### Most Similar Papers
   Top 5 related papers with 1-sentence comparison to this work.

   ### Recent Developments
   Papers from the last 3 months addressing the same problem — how does this paper compare?

   ## Relevance to Your Work
   - Which focus areas this applies to
   - Specific integration opportunities with your pipelines
   - Recommended next steps (read further, try the tool, adapt the method, etc.)
   ```

4. **Save the report** to `reports/deep-dives/YYYY-MM-DD-<sanitized-title>.md`.

## Error Handling

- If full text is not available, note this and base analysis on abstract only.
- If no code/data resources are found, state this clearly in the reproducibility section.
- If the identifier is not found in any source, inform the user and suggest checking the identifier.
