---
name: lit-search
description: Search recent publications across PubMed, bioRxiv, medRxiv, and arXiv on a given topic and produce a structured summary report.
user_invocable: true
argument: topic - the research topic to search for (e.g., "spatial transcriptomics deep learning")
---

# Literature Search

Search publications across PubMed, bioRxiv, medRxiv, and arXiv for a given topic within a user-specified time span. Produce a structured summary report with detailed analysis cards.

## Instructions

1. **Read configuration.** Read `config.json` from the project root (`literature_search/config.json`) to get focus areas, categories, and limits.

2. **Ask the user for the search time span.** Use AskUserQuestion to prompt:
   > "What time span should this search cover?"
   Options:
   - "Last 1 month" (default / recommended)
   - "Last 3 months"
   - "Last 6 months"
   - "Last 1 year"

   Compute `{search_days}` from the selected option (30, 90, 180, or 365 days). Compute `{date_from}` as today minus `{search_days}` in YYYY-MM-DD and YYYY/MM/DD formats, and `{date_to}` as today.

3. **Dispatch 4 parallel search agents.** Use the Agent tool to launch all 4 in parallel in a single message. Each agent must return results as a structured list with fields: title, authors, date, source, doi_or_url, abstract. **All agents must use the user-selected time span** (`{search_days}` / `{date_from}` / `{date_to}`) instead of a hardcoded 30 days.

   **PubMed Agent prompt:**
   ````
   You are a PubMed search agent. Search for publications related to: "{topic}"

   Use the mcp__claude_ai_PubMed__search_articles tool with:
   - query: "{topic}" combined with relevant terms from the focus areas
   - date_from: "{date_from_slash}" (YYYY/MM/DD format)
   - date_to: "{date_to_slash}" (YYYY/MM/DD format)
   - max_results: 50
   - sort: "pub_date"

   For each result, use mcp__claude_ai_PubMed__get_article_metadata to get full metadata.

   For the top 5 most relevant results, check if full text is available:
   - Use mcp__claude_ai_PubMed__find_related_articles with link_type="pubmed_pmc" to find PMC IDs
   - If available, use mcp__claude_ai_PubMed__get_full_text_article to get the full text

   Return ALL results as a structured list. For each paper include:
   - title, authors (list), date (YYYY-MM-DD), source ("PubMed"), doi, pmid, abstract
   - full_text_excerpt: first 500 words of full text if available, otherwise null
   ````

   **bioRxiv Agent prompt:**
   ````
   You are a bioRxiv search agent. Search for preprints related to: "{topic}"

   IMPORTANT: The bioRxiv search tool does NOT support keyword search. You must search by category and date, then filter results by relevance.

   Search these categories one at a time using mcp__claude_ai_bioRxiv__search_preprints:
   - category: "bioinformatics", server: "biorxiv", recent_days: {search_days}, limit: 100
   - category: "genomics", server: "biorxiv", recent_days: {search_days}, limit: 100
   - category: "systems biology", server: "biorxiv", recent_days: {search_days}, limit: 100

   For each result, check if the title and abstract are relevant to: "{topic}"
   and the focus areas: spatial transcriptomics/multi-omics, pipeline development, DL/algorithms in sequencing.

   For relevant results, use mcp__claude_ai_bioRxiv__get_preprint to get full details.

   Also check mcp__claude_ai_bioRxiv__search_published_preprints with recent_days: {search_days}
   to note which preprints have been published in journals.

   Return only RELEVANT results as a structured list. For each paper include:
   - title, authors (list), date (YYYY-MM-DD), source ("bioRxiv"), doi, abstract
   - published_doi: if the preprint has been published in a journal, include the journal DOI
   ````

   **medRxiv Agent prompt:**
   ````
   You are a medRxiv search agent. Search for preprints related to: "{topic}"

   IMPORTANT: The medRxiv search tool does NOT support keyword search. You must search by category and date, then filter results by relevance.

   Search using mcp__claude_ai_bioRxiv__search_preprints with:
   - server: "medrxiv", recent_days: {search_days}, limit: 100

   Note: medRxiv has fewer category options relevant to computational biology.
   Search without category filter to get all recent medRxiv preprints, then filter by relevance.

   For each result, check if the title and abstract are relevant to: "{topic}"
   and the focus areas: spatial transcriptomics/multi-omics, pipeline development, DL/algorithms in sequencing.

   For relevant results, use mcp__claude_ai_bioRxiv__get_preprint with server="medrxiv" to get full details.

   Return only RELEVANT results as a structured list. For each paper include:
   - title, authors (list), date (YYYY-MM-DD), source ("medRxiv"), doi, abstract
   ````

   **arXiv Agent prompt:**
   ````
   You are an arXiv search agent. Search for preprints related to: "{topic}"

   Use the WebFetch tool to query the arXiv API. Make separate requests for each category:

   For each category in [q-bio, cs.LG, stat.ML]:
     URL: https://export.arxiv.org/api/query?search_query=cat:{category}+AND+all:{url_encoded_topic}&start=0&max_results=50&sortBy=submittedDate&sortOrder=descending
     Prompt: "Extract all papers from this Atom XML feed. For each paper return: title, authors, date (published), arxiv_id, abstract, categories. Only include papers from the last {search_days} days (after {date_from})."

   Filter results for relevance to: "{topic}"
   and focus areas: spatial transcriptomics/multi-omics, pipeline development, DL/algorithms in sequencing.

   Return only RELEVANT results as a structured list. For each paper include:
   - title, authors (list), date (YYYY-MM-DD), source ("arXiv"), arxiv_id, url (https://arxiv.org/abs/{id}), abstract
   ````

3. **Deduplicate results.** After all agents return, merge results:
   - Match by DOI when available
   - Fall back to fuzzy title matching (titles that are >90% similar after lowercasing)
   - When a paper appears on multiple sources, prefer the published version (PubMed > bioRxiv/medRxiv > arXiv)
   - Note all sources in the merged entry

4. **Generate structured analysis cards.** For each paper (up to the `detailed_summary_limit` from config), produce:

   ```markdown
   ## [Paper Title]
   **Authors:** Author1, Author2, ...
   **Source:** PubMed / bioRxiv / medRxiv / arXiv | **Date:** YYYY-MM-DD
   **DOI/URL:** ...

   ### Summary
   2-3 sentence overview of the paper's contribution.

   ### Key Methods
   - Algorithms/models used
   - Computational framework/pipeline details
   - Datasets analyzed

   ### Main Findings
   - Key results and claims

   ### Strengths & Limitations
   - What the approach does well
   - Caveats, scalability concerns, missing benchmarks

   ### Related Work
   - How this fits with other papers in this batch
   - Comparison to known methods

   ### Relevance to Your Work
   - Which focus area this applies to
   - Potential applications to existing pipelines
   ```

5. **Group by focus area** and write a **top-level executive summary** (5-10 sentences).

6. **If more than `detailed_summary_limit` papers**, provide a condensed table for the remainder:

   ```markdown
   ## Additional Papers

   | Title | Source | Date | Focus Area |
   |-------|--------|------|------------|
   | ...   | ...    | ...  | ...        |
   ```

7. **Save the report** to `reports/searches/YYYY-MM-DD-<sanitized-topic>.md` where the topic is lowercased, spaces replaced with hyphens, special characters removed. Include the search time span in the report header (e.g., "Search Window: {date_from} to {date_to} ({search_days} days)").

8. **Offer to add topic to tracked list.** If the searched topic is not already in `config.json` topics, ask:
   > "Would you like to add '{topic}' to your tracked topics for periodic searches?"
   If yes, update `config.json`.

## Error Handling

- If a source agent fails, proceed with results from the other agents. Note the failure in the report header:
  > "Note: {source} was unavailable during this search. Results may be incomplete."
- If no results are found across all sources, report this and suggest alternative search terms.
- If the arXiv API returns an error or rate limit, wait 3 seconds and retry once.
