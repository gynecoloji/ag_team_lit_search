---
name: lit-ppt
description: Generate a presentation (PPTX) from the most recent literature search, trend debrief, or review report — ready for lab meetings or journal clubs.
user_invocable: true
argument: source (optional) - which report to present. Options "search", "trends", "review", or a specific report filename. Defaults to the most recent search report.
---

# Literature Presentation Generator

Generate a PowerPoint (PPTX) presentation from literature search results, trend debriefs, or mini-reviews. Outputs a professional slide deck suitable for lab meetings, journal clubs, or group presentations.

## Instructions

1. **Determine the source report.** Based on the argument:
   - `"search"` or no argument → read the most recent file from `reports/searches/*.md`
   - `"trends"` → read the most recent file from `reports/trends/*.md`
   - `"review"` → read the most recent file from `reports/reviews/*.md`
   - A specific filename → read that file directly

   If the report does not exist, inform the user:
   > "No report found. Run the appropriate skill first (`/lit-search`, `/lit-trends`, or `/lit-review`)."
   Then stop.

2. **Ask the user for presentation style.** Use AskUserQuestion:
   > "What style of presentation do you need?"
   Options:
   - "Lab meeting (15-20 slides, detailed)" (recommended)
   - "Journal club (10-15 slides, focused on 3-5 key papers)"
   - "Quick update (5-8 slides, highlights only)"

3. **Install python-pptx if needed.**
   ```bash
   pip3 install python-pptx
   ```

4. **Generate the PPTX builder script.** Write a Python script to `scripts/build_presentation.py` that uses `python-pptx` to build the slide deck. The script should accept arguments:
   ```bash
   python3 scripts/build_presentation.py <input_json> <output_pptx>
   ```

   The script must create slides with these design specs:
   - **Color scheme:** White/simple backgrounds throughout, dark navy (#1B2A4A) for title bars and headings only, accent color (#E74C3C) for highlights
   - **Fonts:** Title slides use 28pt bold, content headers 22pt bold, body 16pt, table text 12pt
   - **Layout:** Title + content layout for most slides; two-column where appropriate
   - **Text:** Never truncate or crop text — always show the full content even if long

5. **Extract structured data from the report** and write to `/tmp/lit_ppt_data.json`:

   For a **search report**, extract:
   ```json
   {
     "type": "search",
     "title": "Literature Search: {topic}",
     "date": "YYYY-MM-DD",
     "search_window": "...",
     "total_papers": N,
     "sources": {"PubMed": N, "bioRxiv": N, "medRxiv": N, "arXiv": N},
     "executive_summary": "...",
     "papers_by_focus_area": {
       "area1": [
         {
           "title": "...",
           "authors_short": "First et al.",
           "date": "YYYY-MM-DD",
           "source": "...",
           "summary": "2-3 sentences",
           "key_methods": ["..."],
           "main_findings": ["..."],
           "relevance": "..."
         }
       ]
     },
     "additional_papers": [{"title": "...", "source": "...", "date": "...", "focus_area": "..."}]
   }
   ```

   For a **trends report**, extract:
   ```json
   {
     "type": "trends",
     "title": "Trend Debrief: {topic}",
     "date": "YYYY-MM-DD",
     "total_papers": N,
     "executive_summary": "...",
     "emerging_topics": {"methods": ["..."], "datasets": ["..."]},
     "source_counts": {"PubMed": N, "bioRxiv": N, "medRxiv": N, "arXiv": N},
     "converging_findings": ["..."],
     "literature_gaps": ["..."],
     "field_direction": ["..."],
     "contradictions": ["..."],
     "plot_paths": ["path1.png", "path2.png"]
   }
   ```

   For a **review report**, extract:
   ```json
   {
     "type": "review",
     "title": "Mini-Review: {topic}",
     "date": "YYYY-MM-DD",
     "total_papers": N,
     "abstract": "...",
     "background_summary": "...",
     "method_categories": [{"name": "...", "methods": ["..."], "description": "..."}],
     "open_problems": ["..."],
     "opportunities": ["..."],
     "outlook": "...",
     "key_papers_table": [{"title": "...", "authors": "...", "year": "...", "category": "...", "contribution": "..."}]
   }
   ```

6. **Build the presentation script.** The script (`scripts/build_presentation.py`) should generate slides as follows:

   **For search reports — Lab meeting style:**
   - Slide 1: Title slide — topic, date, search window, total papers
   - Slide 2: Executive summary (key bullet points)
   - Slide 3: Source breakdown (bar chart or table: PubMed/bioRxiv/medRxiv/arXiv counts)
   - Slides 4-N: One slide per focus area header, then 1-2 slides per top paper:
     - Paper title + authors + source
     - Key methods (bullets)
     - Main findings (bullets)
     - Relevance to our work
   - Slide N+1: Additional papers table (condensed)
   - Final slide: Key takeaways (3-5 bullets synthesizing the search)

   **For search reports — Journal club style:**
   - Slide 1: Title slide
   - Slide 2: Overview — what was searched, how many papers, top themes
   - Slides 3-12: 2 slides per paper for the top 5 papers (methods + findings)
   - Slide 13: Landscape summary — how papers relate to each other
   - Final slide: Discussion questions

   **For search reports — Quick update style:**
   - Slide 1: Title slide
   - Slide 2: One-slide executive summary
   - Slides 3-6: One slide per top highlight (title + 3 bullet findings)
   - Slide 7: What to watch — emerging themes
   - Final slide: Links/DOIs for follow-up

   **For trends reports:**
   - Slide 1: Title slide
   - Slide 2: Executive summary
   - Slide 3: Publication volume (embed plot image if available)
   - Slide 4: Sub-topic distribution (embed plot image if available)
   - Slide 5: Method landscape (embed plot image if available)
   - Slide 6: Emerging topics — new methods & tools
   - Slide 7: Emerging topics — new datasets
   - Slide 8: Converging findings
   - Slide 9: Literature gaps
   - Slide 10: Field direction & outlook
   - Final slide: Key takeaways

   **For review reports:**
   - Slide 1: Title slide
   - Slide 2: Abstract / overview
   - Slide 3-4: Background (condensed)
   - Slide 5-6: Methods taxonomy (table + key descriptions)
   - Slide 7: Benchmark summary (if available)
   - Slide 8: Emerging trends
   - Slide 9: Open problems
   - Slide 10: Opportunities for our lab
   - Slide 11: Key papers reference table
   - Final slide: Outlook & next steps

7. **Run the script:**
   ```bash
   python3 scripts/build_presentation.py /tmp/lit_ppt_data.json reports/presentations/YYYY-MM-DD-<sanitized-topic>.pptx
   ```

8. **Clean up.** Remove `/tmp/lit_ppt_data.json`.

9. **Report to the user:**
   > "Presentation saved to `reports/presentations/YYYY-MM-DD-<topic>.pptx` ({N} slides, {style} format)."

## Error Handling

- If `python-pptx` fails to install, fall back to generating a detailed Markdown outline of the presentation in `reports/presentations/YYYY-MM-DD-<topic>-outline.md` and inform the user:
  > "Could not generate PPTX (python-pptx unavailable). Saved a slide outline to `reports/presentations/YYYY-MM-DD-<topic>-outline.md` that you can copy into your presentation tool."
- If plot images are referenced but missing, skip those slides and note the omission.
- If the source report has fewer than 3 papers, warn that the presentation will be sparse and suggest running a broader search first.
