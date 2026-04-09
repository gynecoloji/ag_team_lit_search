---
name: lit-trends
description: Analyze the most recent literature search report and generate a trend debrief with visualizations.
user_invocable: true
---

# Literature Trend Debrief

Analyze the most recent search report and generate a comprehensive trend debrief with emerging topics, quantitative trends, synthesis, and visualizations.

## Instructions

1. **Read configuration.** Read `config.json` from the project root (`literature_search/config.json`).

2. **Read the two most recent search reports.** Use Glob to find all files matching `reports/searches/*.md`. Sort by filename (which embeds the date) and read the **two most recent reports**. The most recent is the "current" report; the second most recent is the "previous" report used only for trajectory comparison.

   If no search reports exist, inform the user:
   > "No search reports found. Run `/lit-search <topic>` first to generate reports."
   Then stop.

   If only one report exists, skip trajectory comparison and note:
   > "Only one search report found — trajectory tags will not be available."

3. **Extract structured data from the report.** Parse the current search report and extract for every paper:
   - title, authors, date, source, focus_area
   - methods (list of algorithms/models mentioned in Key Methods)
   - keywords (key terms from title, methods, and findings)

   Also extract the same fields from the previous report (if available) to enable trajectory comparison.

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
         "keywords": ["..."],
         "trajectory": "new|ongoing|fading"
       }
     ],
     "previous_report_date": "YYYY-MM-DD or null"
   }
   ```

   Assign `trajectory` by comparing the current report against the previous one:
   - `"new"` — topic/method/paper did not appear in the previous report
   - `"ongoing"` — topic/method appeared in the previous report and remains prominent
   - `"fading"` — topic/method appeared in the previous report but is less prominent now
   - If no previous report exists, set all to `"new"`

5. **Generate visualizations.** Run the plotting script:
   ```bash
   python3 scripts/generate_trend_plots.py /tmp/lit_trend_data.json reports/trends/plots YYYY-MM-DD
   ```
   (Replace YYYY-MM-DD with today's date.)

   If matplotlib/seaborn are not installed, install them first:
   ```bash
   pip3 install matplotlib seaborn
   ```

6. **Write the trend debrief report.** Analyze all papers from the current search report and produce a markdown report with these sections:

   ```markdown
   # Literature Trend Debrief — YYYY-MM-DD

   **Report analyzed:** search report filename
   **Papers covered:** M papers
   **Date range:** earliest paper date — latest paper date
   **Focus areas:** disease mechanisms, therapeutic targets, drug discovery, translational and clinical research

   ---

   ## Executive Summary
   5-10 sentences highlighting the most significant trends, breakthroughs, and shifts observed.

   ---

   ## Emerging Topics

   ### New Methods & Tools
   Each item must include a trajectory tag and the specific papers it appeared in:
   - `[NEW]` MethodName — brief description — seen in: Paper A, Paper B
   - `[ONGOING]` MethodName — brief description — seen in: Paper C (also in previous report)
   - `[FADING]` MethodName — brief description — prominent last period, less so now

   ### New Datasets & Benchmarks
   - New datasets or benchmarks becoming standard in the field (tag as `[NEW]` or `[ONGOING]`)

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

   ---

   ## Priority Reading List

   Rank the top 5 papers from the current report by actionability to the user's work (disease mechanisms, therapeutic targets, drug discovery, translational research). For each, give a concrete reason — not just the topic, but *why it matters now*.

   | Rank | Paper (Authors, Year) | DOI/URL | Why Read It |
   |------|-----------------------|---------|-------------|
   | 1 | ... | ... | Directly applicable: new method for X in your pipeline |
   | 2 | ... | ... | Challenges current assumption about Y |
   | 3 | ... | ... | Benchmark your tool should be compared against |
   | 4 | ... | ... | Dataset useful for validation |
   | 5 | ... | ... | Emerging direction worth monitoring |

   ---

   ## Suggested Next Steps

   Based on the trends above, recommend specific follow-on skill invocations. Be concrete — name the paper, method, or topic, not a generic suggestion.

   ```
   /lit-deep-dive <DOI>          — [Paper title]: [one sentence why]
   /lit-compare <A> vs <B>       — [two competing methods that appeared]: [what to resolve]
   /lit-reproduce <ID> — <fig>   — [specific result]: [why it's reproducible/relevant]
   /lit-search <refined topic>   — [why the topic should be narrowed or broadened]
   /lit-review <topic>           — [if enough reports have accumulated on a theme]
   ```

   Only include items that are genuinely warranted by what appeared in the report. Omit any that don't apply.
   ```

7. **Save the report** to `reports/trends/YYYY-MM-DD-trend-debrief.md`.

8. **Clean up.** Remove `/tmp/lit_trend_data.json`.

## Error Handling

- If the plotting script fails, include the trend report without visualizations and note:
  > "Note: Visualizations could not be generated. Error: {error message}"
- The analysis always operates on the most recent report. The previous report is read only for trajectory comparison — do not include its papers in counts or synthesis.
