---
name: lit-trends
description: Analyze accumulated literature search reports and generate a trend debrief with visualizations.
user_invocable: true
---

# Literature Trend Debrief

Analyze all accumulated search reports and generate a comprehensive trend debrief with emerging topics, quantitative trends, synthesis, and visualizations.

## Instructions

1. **Read configuration.** Read `config.json` from the project root (`literature_search/config.json`).

2. **Read all search reports.** Use Glob to find all files matching `reports/searches/*.md`. Read each one using the Read tool.

   If no search reports exist, inform the user:
   > "No search reports found. Run `/lit-search <topic>` first to generate reports."
   Then stop.

3. **Extract structured data from reports.** Parse each search report and extract for every paper:
   - title, authors, date, source, focus_area
   - methods (list of algorithms/models mentioned in Key Methods)
   - keywords (key terms from title, methods, and findings)

4. **Write the extracted data as JSON.** Save to `/tmp/lit_trend_data.json` in this format:
   ```json
   {
     "papers": [
       {
         "title": "...",
         "authors": ["..."],
         "date": "YYYY-MM-DD",
         "source": "PubMed|bioRxiv|medRxiv|arXiv",
         "focus_area": "...",
         "methods": ["..."],
         "keywords": ["..."]
       }
     ]
   }
   ```

5. **Generate visualizations.** Run the plotting script:
   ```bash
   python3 scripts/generate_trend_plots.py /tmp/lit_trend_data.json reports/trends/plots YYYY-MM-DD
   ```
   (Replace YYYY-MM-DD with today's date.)

   If matplotlib/seaborn are not installed, install them first:
   ```bash
   pip3 install matplotlib seaborn
   ```

6. **Write the trend debrief report.** Analyze all papers across all search reports and produce a markdown report with these sections:

   ```markdown
   # Literature Trend Debrief — YYYY-MM-DD

   **Reports analyzed:** N search reports covering M papers
   **Date range:** earliest paper date — latest paper date
   **Focus areas:** spatial transcriptomics / multi-omics, pipeline development, DL / innovative algorithms in sequencing

   ---

   ## Executive Summary
   5-10 sentences highlighting the most significant trends, breakthroughs, and shifts observed.

   ---

   ## Emerging Topics

   ### New Methods & Tools
   - Methods/tools appearing across multiple papers that are gaining traction
   - Novel algorithm applications appearing for the first time

   ### New Datasets & Benchmarks
   - New datasets or benchmarks becoming standard in the field

   ---

   ## Quantitative Trends

   ### Publication Volume
   ![Publication Volume Over Time](plots/YYYY-MM-DD-pub-volume.png)

   | Source | Paper Count |
   |--------|-------------|
   | PubMed | N |
   | bioRxiv | N |
   | medRxiv | N |
   | arXiv | N |

   ### Sub-topic Distribution
   ![Sub-topic Distribution](plots/YYYY-MM-DD-subtopic-dist.png)

   ### Method / Algorithm Landscape
   ![Method Heatmap](plots/YYYY-MM-DD-method-heatmap.png)

   ### Most Active Labs & Groups
   ![Top Labs](plots/YYYY-MM-DD-top-labs.png)

   | Lab / Last Author | Paper Count | Primary Focus |
   |-------------------|-------------|---------------|
   | ... | ... | ... |

   ### Keyword Co-occurrence
   ![Keyword Network](plots/YYYY-MM-DD-keyword-network.png)

   ---

   ## Synthesis

   ### Converging Findings
   - Findings that multiple independent groups are arriving at

   ### Literature Gaps
   - What's missing or underexplored in the current landscape

   ### Field Direction
   - Where the field appears to be heading based on current trends

   ### Contradictions & Debates
   - Disagreements or contradictions between papers
   ```

7. **Save the report** to `reports/trends/YYYY-MM-DD-trend-debrief.md`.

8. **Clean up.** Remove `/tmp/lit_trend_data.json`.

## Error Handling

- If the plotting script fails, include the trend report without visualizations and note:
  > "Note: Visualizations could not be generated. Error: {error message}"
- If only a single search report exists, note that trend analysis is limited and skip comparative sections.
