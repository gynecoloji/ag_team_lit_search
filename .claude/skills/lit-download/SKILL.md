---
name: lit-download
description: Download full-text PDFs for papers from a search report or a list of DOIs/PMIDs — tries PMC, bioRxiv, medRxiv, arXiv, browser-based Google navigation, Unpaywall, Semantic Scholar, Europe PMC, Google Scholar, and author lab pages.
user-invocable: true
argument-hint: source - either "latest" (use most recent search report), a report filename (e.g., "2026-04-09-kras-inhibitors.md"), or a space-separated list of DOIs/PMIDs/arXiv IDs
---

# Literature Download

Download full-text PDFs for papers from a recent search report or an explicit list of identifiers. Tries 10 routes in order — API-based OA routes first, then a human-like browser search (Google → publisher page → PDF download), then web search for author-posted and repository copies. Saves PDFs to `reports/downloads/YYYY-MM-DD-<topic>/` and produces a manifest.

## Instructions

1. **Resolve the paper list.**

   - If argument is `"latest"` or omitted: read the most recently modified file in `reports/searches/` (use Glob on `reports/searches/*.md` sorted by modification time). Extract every DOI, PMID, and arXiv ID from the report — look for lines matching `**DOI/URL:**`, `doi.org/`, `arxiv.org/abs/`, or bare `10.\d{4}/` patterns.
   - If argument is a filename (ends with `.md`): read `reports/searches/{argument}` and extract identifiers the same way.
   - If argument is a whitespace-separated list of identifiers: use them directly.

   Classify each identifier:
   - Starts with `10.1101/` or `10.64898/` → bioRxiv/medRxiv DOI
   - Starts with `10.` (other) → journal DOI → try PMC and Unpaywall
   - Purely numeric → PMID → look up PMC ID first
   - Matches `\d{4}\.\d{4,5}` → arXiv ID

2. **Ask the user to confirm** the list (summarize count per source type) before downloading. Use AskUserQuestion:
   > "Found N papers to download (X from PubMed/PMC, Y from bioRxiv/medRxiv, Z from arXiv). Proceed?"
   If user says no or wants to filter, ask which to keep.

3. **Create the output directory.** Use today's date and the report topic (or "papers" if from a raw ID list):
   `reports/downloads/YYYY-MM-DD-<topic>/`

4. **Download each paper in parallel.** Launch one agent per paper (batch in groups of 10 if >10 papers). Each agent uses this prompt template:

   ````
   You are a PDF download agent. Download the full-text PDF for this paper and save it.

   Paper identifier: "{identifier}"
   Identifier type: "{type}"  # pmid | journal_doi | biorxiv_doi | arxiv_id
   Output directory: "{output_dir}"
   Suggested filename: "{safe_title}.pdf"  # title lowercased, spaces→underscores, max 80 chars

   Try these routes IN ORDER, stopping at the first success:

   ## Route 1 — PubMed Central (for PMIDs and journal DOIs)
   If type is "pmid":
   - Use mcp__claude_ai_PubMed__find_related_articles with link_type="pubmed_pmc" to get the PMC ID.
   - If a PMC ID is found, fetch: https://www.ncbi.nlm.nih.gov/pmc/articles/{pmcid}/pdf/
     via WebFetch with prompt: "Is this a PDF download page or a redirect? Extract the direct PDF URL if visible."
   - Alternatively fetch: https://europepmc.org/backend/ptpmcrender.fcgi?accid={pmcid}&blobtype=pdf

   If type is "journal_doi":
   - Search PubMed for the DOI using mcp__claude_ai_PubMed__search_articles, get the PMID, then follow the PMID route above.

   ## Route 2 — bioRxiv / medRxiv (for biorxiv_doi)
   - The PDF URL is: https://www.biorxiv.org/content/{doi}v1.full.pdf
     (try v1, v2, v3 if earlier versions 404)
   - Use WebFetch with prompt: "Is this a valid PDF file? What is the content-type?"
   - If server is medRxiv: https://www.medrxiv.org/content/{doi}v1.full.pdf

   ## Route 3 — arXiv (for arxiv_id)
   - PDF URL: https://arxiv.org/pdf/{arxiv_id}
   - Use WebFetch with prompt: "Fetch this PDF. What is its size? Is it a valid PDF?"

   ## Route 4 — Human-like browser navigation (Google → publisher page → PDF)
   Applies to any identifier type. Uses the Playwright browser to find and download the PDF exactly as a human would.

   **Step 4a — Google the paper:**
   - Construct a search query: `"{title}" {first_author_last_name} {year} PDF`
     (use title and author from metadata retrieved in earlier routes; fall back to `"{doi}" full text PDF` if no metadata yet)
   - Call mcp__playwright__browser_navigate with URL:
     `https://www.google.com/search?q={url_encoded_query}`
   - Call mcp__playwright__browser_wait_for (2 seconds) for results to load.
   - Call mcp__playwright__browser_take_screenshot to see the results page.

   **Step 4b — Pick the best result:**
   - Call mcp__playwright__browser_snapshot to read all result links.
   - Prefer results in this order:
     1. Publisher's own article page (matches the DOI domain, e.g. `nature.com`, `cell.com`, `science.org`, `nih.gov`, `wiley.com`, etc.)
     2. PubMed Central (`ncbi.nlm.nih.gov/pmc`)
     3. Institutional repository or author lab page (`.edu`, `.ac.uk`, etc.)
     4. ResearchGate or Academia.edu author page
   - Skip any link pointing to Sci-Hub, LibGen, or similar piracy services.
   - Click the chosen result with mcp__playwright__browser_click.
   - Call mcp__playwright__browser_wait_for (3 seconds) for the page to load.
   - Call mcp__playwright__browser_take_screenshot to confirm what loaded.

   **Step 4c — Find the PDF download link on the article page:**
   - Call mcp__playwright__browser_snapshot to inspect the page.
   - Look for any of:
     - A button or link whose text includes "Download PDF", "Full Text PDF", "PDF Full Text", "View PDF", "Open PDF", "Get PDF", "Download", or "Full text"
     - A link whose `href` ends with `.pdf`
     - A link whose `href` contains `/pdf/` or `?format=pdf` or `type=printable`
   - If a paywall or login wall is detected (text like "Subscribe", "Purchase", "Sign in to access", "Institutional login") and no PDF link is visible → mark route as failed, skip to Route 5.
   - If a PDF link is found, note the current network baseline with mcp__playwright__browser_network_requests, then click the link with mcp__playwright__browser_click.
   - Call mcp__playwright__browser_wait_for (3 seconds).

   **Step 4d — Capture the PDF URL:**
   - Call mcp__playwright__browser_network_requests and look for any new request whose URL ends in `.pdf` or whose response Content-Type is `application/pdf`.
   - Call mcp__playwright__browser_tabs — if a new tab opened with a `.pdf` URL, capture it.
   - If an intermediate redirect page appeared ("You are leaving…", "Click here to continue"), call mcp__playwright__browser_snapshot, find the continuation link, click it, wait 2 seconds, and repeat this step (up to 2 more times).

   **Step 4e — Save the PDF:**
   - Use WebFetch on the captured PDF URL (prompt: "Is this a valid PDF? Return its size.").
   - If valid, save to `{output_dir}/{safe_title}.pdf` with the Write tool.
   - If WebFetch is blocked (session cookies required), call mcp__playwright__browser_evaluate with:
     `document.querySelector('a[href$=".pdf"], a[href*="/pdf/"]')?.href ?? window.location.href`
     to get the URL, note it in the manifest as "browser-session required; open manually", and mark status as "open_access_not_found".

   **Step 4f — Fallback within this route:**
   - If no PDF link was found but an HTML full-text is visible (publisher HTML reader, PMC HTML), record the page URL in the manifest with note "HTML full-text — no direct PDF link found".
   - If nothing worked, mark route as failed and continue to Route 5.

   ## Route 5 — Unpaywall (for journal DOIs with no PMC)
   - Fetch: https://api.unpaywall.org/v2/{doi}?email=researcher@lab.org
     with prompt: "Extract: is_oa (bool), best_oa_location.url_for_pdf, best_oa_location.host_type, best_oa_location.license"
   - If is_oa=true and url_for_pdf is not null, fetch that URL.

   ## Route 6 — Publisher page scrape
   - Fetch: https://doi.org/{doi}
     with prompt: "Find any open-access PDF download links. Look for 'Download PDF', 'Full Text PDF', or links ending in .pdf. Return the first direct PDF URL found, or null."
   - If a PDF URL is found, fetch it.

   ## Route 7 — Semantic Scholar
   - Fetch: https://api.semanticscholar.org/graph/v1/paper/{doi}?fields=title,authors,openAccessPdf,externalIds
     with prompt: "Extract: openAccessPdf.url (the direct PDF URL if present), authors[0].name, title."
   - If openAccessPdf.url is not null, fetch that URL.
   - If the DOI lookup fails, try: https://api.semanticscholar.org/graph/v1/paper/search?query={url_encoded_title}&fields=title,openAccessPdf
     and use the top result's openAccessPdf.url if it matches the title closely.

   ## Route 8 — Europe PMC full-text search
   - Fetch: https://www.ebi.ac.uk/europepmc/webservices/rest/search?query={doi_or_pmid}&format=json&resultType=core
     with prompt: "Extract: fullTextUrlList.fullTextUrl[] where documentStyle='pdf' and availability='Open access'. Return the first such URL."
   - If a PDF URL is found, fetch it.
   - Also check for author manuscripts: look for fullTextUrl entries where documentStyle='pdf' and site contains 'manuscript' or 'PMC'.

   ## Route 9 — Google Scholar author-posted copies
   - Fetch: https://scholar.google.com/scholar?q={url_encoded_title}
     with prompt: "Find any links labeled [PDF] on the right side of results. These point to author-posted copies on university or lab servers. Return all [PDF] URLs found (typically ending in .pdf and hosted on .edu, .ac.uk, or similar academic domains)."
   - For each PDF URL found, check if it is hosted on an academic domain (.edu, .ac.uk, .ac.jp, .uni-*.de, researchgate.net, academia.edu, or similar) — skip any that are not.
   - Fetch the first valid academic-domain PDF URL.
   - Note: do NOT follow links to Sci-Hub, LibGen, or similar piracy services even if they appear in results.

   ## Route 10 — Corresponding author lab page
   - From the paper metadata (retrieved in Route 1 or 6), extract the corresponding author's name and affiliation.
   - Construct a search query: "{author_name} {affiliation} publications" and fetch via Google Scholar or the author's likely lab page URL pattern.
   - Fetch the author's lab publications page with prompt: "Find a PDF download link for the paper titled '{title}'. Look for links ending in .pdf or labeled 'PDF', 'Preprint', or 'Download'."
   - If a direct PDF link is found on an academic domain, fetch it.

   ## Result
   Return a JSON object:
   {
     "identifier": "...",
     "title": "...",
     "route_used": "pmc|biorxiv|arxiv|browser_nav|unpaywall|publisher|semantic_scholar|europe_pmc|google_scholar|author_page|none",
     "pdf_url": "...",    # URL that yielded the PDF, or null
     "saved_path": "...", # relative path where PDF was saved, or null
     "status": "success|open_access_not_found|error",
     "note": "..."        # error message or extra info
   }

   If you successfully fetched PDF content, save it to {output_dir}/{safe_title}.pdf using the Write tool.
   If the content is HTML rather than a PDF, do NOT save it — mark status as "open_access_not_found".
   ````

5. **Compile the download manifest.** After all agents return, write `reports/downloads/YYYY-MM-DD-<topic>/manifest.md`:

   ```markdown
   # Download Manifest — {topic}
   **Date:** YYYY-MM-DD | **Source report:** {report_filename or "explicit IDs"}
   **Downloaded:** N / Total | **Not available (OA):** M

   ## Successfully Downloaded

   | # | Title | Route | File |
   |---|-------|-------|------|
   | 1 | ... | PMC / bioRxiv / arXiv / Browser nav / Unpaywall / Semantic Scholar / Europe PMC / Google Scholar / Author page | filename.pdf |

   ## Not Available (all 9 routes exhausted)

   | # | Title | Identifier | Routes tried |
   |---|-------|------------|--------------|
   | 1 | ... | doi:... | PMC ✗ · Browser nav ✗ · Unpaywall ✗ · S2 ✗ · GS ✗ · author page ✗ |

   ## Tips for Unavailable Papers
   - Request via Interlibrary Loan (ILL) through your institution
   - Email the corresponding author directly (address usually in PubMed metadata)
   - Check the author's lab page manually — it may have a recent preprint or author copy
   ```

6. **Report to the user.** Summarize: how many downloaded, how many unavailable, and where the files are saved.

## Error Handling

- If a PDF fetch returns HTML (publisher paywall or login page), mark that route as failed — do NOT save the HTML. Move to the next route.
- LibKey.io (Route 4): if the Playwright browser has no active UNM session (page shows a login prompt or redirects to the publisher without downloading), mark it as failed silently. Do NOT prompt the user to log in — that is handled out-of-band.
- If an agent errors entirely, note it in the manifest under an "Errors" section.
- Rate limiting: if arXiv, bioRxiv, or Google Scholar returns 429, wait 5 seconds and retry once before moving on.
- Google Scholar may block automated requests — if it returns a CAPTCHA page, skip Route 8 and continue to Route 9.
- For Route 8, only follow PDF links on academic domains (.edu, .ac.uk, .ac.jp, researchgate.net, academia.edu, institutional repos). Skip any link pointing to Sci-Hub, LibGen, or similar piracy services even if they appear in search results.
- Never attempt to bypass paywalls or download from Sci-Hub or similar services.
