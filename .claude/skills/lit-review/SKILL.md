---
name: lit-review
description: Generate a mini-review/perspective from accumulated search reports — a narrative synthesis suitable for lab meetings, grant intros, or review paper sections.
user-invocable: true
argument-hint: topic - the topic to synthesize a review for (e.g., "CAR-T cell therapy in solid tumors")
---

# Literature Mini-Review

Synthesize all available search reports into a narrative mini-review on a given topic. The output should be suitable for a lab meeting presentation, grant introduction, or a section of a review paper.

Produces **three outputs** for every run:
1. `YYYY-MM-DD-<topic>.md` — academic citation style (numbered `[1]` in-text, full reference list at end)
2. `YYYY-MM-DD-<topic>-linked.md` — same content, but every citation is an inline hyperlink `[Author et al., YYYY](https://doi.org/...)` directly in the body
3. `YYYY-MM-DD-<topic>-diagram.pptx` — editable scientific overview diagram (taxonomy / concept map) *(generated if at least 5 relevant papers are found)*

## Instructions

1. **Read configuration.** Read `config.json` from the project root (`literature_search/config.json`).

2. **Read all search reports.** Use Glob to find all files matching `reports/searches/*.md`. Read each one. Also read any deep-dive reports from `reports/deep-dives/*.md` and comparison reports from `reports/comparisons/*.md` if they exist.

   If no search reports exist, inform the user:
   > "No search reports found. Run `/lit-search <topic>` first to build a literature base."
   Then stop.

3. **Filter for relevance.** From all reports, extract only papers relevant to the given `{topic}`. A paper is relevant if:
   - Its title, abstract, or methods mention terms related to `{topic}`
   - Its focus area overlaps with `{topic}`
   - It is cited or compared in the context of `{topic}` in deep-dive or comparison reports

   Build a **master reference list** — a numbered array of all relevant papers sorted alphabetically by first author:
   ```
   [1] Last, F. et al. (YYYY). Title. Journal. DOI: https://doi.org/...
   [2] ...
   ```
   Every citation used in the review body must map to an entry in this list. Assign numbers `[1]`, `[2]`, … in alphabetical order at this step so they are consistent across both output files.

4. **Dispatch 3 parallel agents** to build the review sections. Pass the master reference list (with numbers already assigned) to each agent so in-text citation numbers are consistent.

   **Background Agent prompt:**
   ````
   You are a literature background agent. Given the following numbered reference list and papers related to "{topic}", write a background section for a mini-review.

   Reference list (use these numbers exactly for in-text citations):
   {numbered reference list}

   Papers (titles, authors, dates, abstracts):
   {list of relevant papers}

   Write 3-5 paragraphs covering:
   1. The problem: What is {topic} and why does it matter?
   2. Historical context: How has the field evolved? What were the key earlier methods or milestones?
   3. Current state: What are the dominant approaches as of the most recent papers?
   4. Why a review is needed now.

   Use numbered in-text citations exactly as [N] (e.g., [1], [3,4]). Write for an audience of biomedical researchers familiar with molecular biology but not necessarily experts in {topic}.
   ````

   **Methods Landscape Agent prompt:**
   ````
   You are a methods landscape agent. Given the following numbered reference list and papers related to "{topic}", create a structured analysis of the current methodological landscape.

   Reference list (use these numbers exactly):
   {numbered reference list}

   Papers (titles, authors, dates, methods, key findings):
   {list of relevant papers}

   Produce:
   1. **Taxonomy of approaches:** Group methods into categories. Create a classification table.
   2. **Technical comparison:** For each category, describe the core approach, strengths, and limitations.
   3. **Benchmark summary:** Where papers share datasets or metrics, compile a comparison.
   4. **Emerging trends:** New patterns appearing in the field.

   Use numbered in-text citations as [N]. Write technically but accessibly.
   ````

   **Gaps & Future Agent prompt:**
   ````
   You are a literature gaps and future directions agent. Given the following numbered reference list and papers related to "{topic}", identify gaps and predict future directions.

   Reference list (use these numbers exactly):
   {numbered reference list}

   Papers (titles, authors, dates, abstracts, methods, findings):
   {list of relevant papers}

   Produce:
   1. **Open problems:** What questions remain unanswered? What limitations do most methods share?
   2. **Missing benchmarks/datasets:** What evaluation infrastructure does the field need?
   3. **Underexplored connections:** Adjacent fields or methods not yet applied.
   4. **Predicted directions:** Where is the field heading in the next 1-2 years?
   5. **Opportunities for your lab:** Given focus on disease mechanisms, therapeutic targets, drug discovery, and translational research, where are the highest-impact opportunities?

   Use numbered in-text citations as [N]. Be specific and actionable.
   ````

5. **Assemble the review body.** Combine agent outputs into a single cohesive body (shared across both output files):

   ```
   ## Abstract
   150-250 word summary — problem, current state, key findings, gaps, and outlook.

   ---

   ## 1. Background
   {Background Agent output}

   ## 2. Current Methods Landscape

   ### 2.1 Taxonomy of Approaches
   {Classification table}

   ### 2.2 Technical Comparison
   {Per-category analysis}

   ### 2.3 Benchmark Summary
   {Comparison tables where available}

   ### 2.4 Emerging Trends
   {New patterns and architectural innovations}

   ## 3. Open Problems & Future Directions

   ### 3.1 Unresolved Challenges
   ### 3.2 Missing Infrastructure
   ### 3.3 Opportunities
   ### 3.4 Outlook

   ## 4. Key Papers Reference Table

   | # | Paper | Authors | Year | Source | Category | Key Contribution |
   |---|-------|---------|------|--------|----------|-----------------|
   | 1 | ... | ... | ... | ... | ... | ... |
   ```

6. **Write File 1 — Academic citation format** (`reports/reviews/YYYY-MM-DD-<topic>.md`):

   Prepend the header block and append the reference list at the end:

   ```markdown
   # Mini-Review: {Topic}

   **Generated:** YYYY-MM-DD
   **Based on:** N search reports, M papers
   **Scope:** {date range of papers}
   **Citation style:** numbered [N]

   ---

   {assembled review body — in-text citations as [1], [3,4], etc.}

   ---

   ## References

   [1] Last, F., Second, A., & Third, B. (YYYY). Title of paper. *Journal Name*, volume(issue), pages. https://doi.org/...
   [2] ...

   ---
   *Mini-review generated: YYYY-MM-DD | Literature search agent team*
   ```

   **Reference formatting rules (strict):**
   - Author list: Last, F.I. style; list all authors up to 6, then "et al." if more
   - Year in parentheses after authors
   - Title in sentence case (capitalize only first word and proper nouns)
   - Journal in italics (`*Journal Name*`)
   - Include volume, issue, pages where available
   - DOI as a full URL `https://doi.org/...` — if no DOI, use PubMed URL or arXiv URL
   - Sort alphabetically by first author last name

7. **Write File 2 — Inline hyperlink format** (`reports/reviews/YYYY-MM-DD-<topic>-linked.md`):

   Same header and body, but replace every `[N]` citation in the body text with a Markdown inline hyperlink:
   `[Author et al., YYYY](https://doi.org/...)` (or the best available URL if no DOI).

   - For a single author: `[Smith et al., 2024](https://doi.org/...)`
   - For exactly two authors: `[Smith & Jones, 2024](https://doi.org/...)`
   - Multiple consecutive citations that were `[3,4]` become `[Brown et al., 2023](url3), [Chen et al., 2022](url4)`

   The References section at the end still appears (same as File 1) so the document is self-contained. Append a note at the top:

   ```markdown
   > **Note:** Citations in this version are inline hyperlinks — click any `[Author et al., YYYY]` to open the paper. A full reference list is included at the end.
   ```

8. **Generate the PPTX diagram** (`reports/reviews/YYYY-MM-DD-<topic>-diagram.pptx`).

   Skip this step if fewer than 5 relevant papers were found.

   Write a Python script to `scripts/gen_review_diagram.py` (overwrite if it exists) and run it with Bash. The script uses `python-pptx` to produce an editable slide with a scientific concept/taxonomy diagram. Install `python-pptx` first if needed (`pip install python-pptx`).

   **Diagram content:** derive from the Methods Landscape agent output:
   - Extract the taxonomy categories (top-level groups of methods/approaches)
   - Extract up to 3 representative papers per category (title + year)
   - Extract 2-3 key shared themes or trends as cross-cutting annotations

   **Diagram layout — use one of the following based on the number of categories:**
   - **≤ 4 categories → hub-and-spoke:** central oval labeled "{Topic} Landscape", spokes to category boxes, sub-bullets inside each box for representative papers
   - **5-8 categories → horizontal swimlane:** rows = categories, columns = Approach / Key papers / Strength / Limitation
   - **> 8 categories → matrix grid:** 3-column grid of rounded rectangles, one per category

   **python-pptx construction rules:**
   - Slide size: 13.33 × 7.5 inches (widescreen 16:9)
   - Background: white (`RGBColor(255, 255, 255)`)
   - Title text box at top: bold, 24pt, dark navy (`RGBColor(31, 56, 100)`)
   - Category boxes: rounded rectangles (`MSO_SHAPE_TYPE.ROUNDED_RECTANGLE` / `PP_ALIGN`), fill with a palette cycling through these colors: `[(70,130,180), (95,170,95), (210,140,50), (180,80,80), (120,90,180), (60,160,160)]`
   - Text inside boxes: 11pt, white, bold for category name, 9pt regular for bullet items
   - Add a footer text box: "Generated by lit-review | {date}" in 8pt gray
   - All shapes must be individually addressable (no grouped objects) so the user can edit them in PowerPoint

   **Script template** (adapt content from the actual review):
   ```python
   from pptx import Presentation
   from pptx.util import Inches, Pt, Emu
   from pptx.dml.color import RGBColor
   from pptx.enum.text import PP_ALIGN
   from pptx.util import Inches, Pt
   import sys

   # ── DATA (filled in by the agent from the review content) ──────────────────
   TOPIC = "{topic}"
   DATE  = "{YYYY-MM-DD}"
   CATEGORIES = [
       {
           "name": "Category Name",
           "papers": ["Smith et al., 2024 — key finding", "Lee et al., 2023 — key finding"],
           "strength": "...",
           "limitation": "...",
       },
       # ... one dict per category
   ]
   TRENDS = ["Trend 1", "Trend 2", "Trend 3"]
   # ───────────────────────────────────────────────────────────────────────────

   PALETTE = [
       RGBColor(70,130,180), RGBColor(95,170,95),  RGBColor(210,140,50),
       RGBColor(180,80,80),  RGBColor(120,90,180), RGBColor(60,160,160),
   ]
   NAVY   = RGBColor(31, 56, 100)
   WHITE  = RGBColor(255,255,255)
   GRAY   = RGBColor(120,120,120)
   BG     = RGBColor(255,255,255)

   prs = Presentation()
   prs.slide_width  = Inches(13.33)
   prs.slide_height = Inches(7.5)
   slide = prs.slides.add_slide(prs.slide_layouts[6])  # blank layout

   # White background
   bg = slide.background
   fill = bg.fill
   fill.solid()
   fill.fore_color.rgb = BG

   def add_textbox(slide, left, top, width, height, text, bold=False, size=11,
                   color=NAVY, align=PP_ALIGN.LEFT, wrap=True):
       txb = slide.shapes.add_textbox(Inches(left), Inches(top), Inches(width), Inches(height))
       txb.word_wrap = wrap
       tf = txb.text_frame
       tf.word_wrap = wrap
       p = tf.paragraphs[0]
       p.alignment = align
       run = p.add_run()
       run.text = text
       run.font.bold = bold
       run.font.size = Pt(size)
       run.font.color.rgb = color
       return txb

   def add_rounded_rect(slide, left, top, width, height, color, text_lines, title_size=11, body_size=9):
       from pptx.util import Pt
       from pptx.enum.shapes import MSO_SHAPE_TYPE
       shape = slide.shapes.add_shape(
           1,  # MSO_SHAPE_TYPE.ROUNDED_RECTANGLE = 5, but add_shape uses autoshape type int
           Inches(left), Inches(top), Inches(width), Inches(height)
       )
       shape.adjustments[0] = 0.05  # corner rounding
       shape.fill.solid()
       shape.fill.fore_color.rgb = color
       shape.line.color.rgb = color
       tf = shape.text_frame
       tf.word_wrap = True
       for i, line in enumerate(text_lines):
           if i == 0:
               p = tf.paragraphs[0]
           else:
               p = tf.add_paragraph()
           p.alignment = PP_ALIGN.LEFT
           run = p.add_run()
           run.text = line
           run.font.size = Pt(title_size if i == 0 else body_size)
           run.font.bold = (i == 0)
           run.font.color.rgb = WHITE
       return shape

   # Title
   add_textbox(slide, 0.3, 0.15, 12.7, 0.6,
               f"{TOPIC} — Methods & Concepts Landscape",
               bold=True, size=20, color=NAVY, align=PP_ALIGN.CENTER)

   # Layout: determine grid based on number of categories
   n = len(CATEGORIES)
   cols = min(3, n)
   rows = (n + cols - 1) // cols
   box_w = 12.0 / cols - 0.2
   box_h = (6.0 / rows) - 0.2
   x0, y0 = 0.4, 0.9

   for i, cat in enumerate(CATEGORIES):
       col = i % cols
       row = i // cols
       x = x0 + col * (box_w + 0.2)
       y = y0 + row * (box_h + 0.2)
       color = PALETTE[i % len(PALETTE)]
       lines = [cat["name"]] + [f"• {p}" for p in cat.get("papers", [])]
       if cat.get("strength"):
           lines.append(f"✓ {cat['strength']}")
       if cat.get("limitation"):
           lines.append(f"✗ {cat['limitation']}")
       add_rounded_rect(slide, x, y, box_w, box_h, color, lines)

   # Trends annotation at bottom if room
   if TRENDS:
       trend_text = "  |  ".join(f"▶ {t}" for t in TRENDS)
       add_textbox(slide, 0.3, 7.0, 12.7, 0.35,
                   f"Key trends: {trend_text}",
                   bold=False, size=9, color=GRAY, align=PP_ALIGN.CENTER)

   # Footer
   add_textbox(slide, 0.3, 7.3, 12.7, 0.2,
               f"Generated by lit-review | {DATE}",
               bold=False, size=8, color=GRAY, align=PP_ALIGN.RIGHT)

   out = f"reports/reviews/{DATE}-{TOPIC.lower().replace(' ','_')[:40]}-diagram.pptx"
   prs.save(out)
   print(f"Saved: {out}")
   ```

   After writing and running the script, confirm the `.pptx` was created. If `python-pptx` is not installed, install it with `pip install python-pptx` and retry.

9. **Report to the user.** Summarize:
   - Path to File 1 (academic citations)
   - Path to File 2 (inline hyperlinks)
   - Path to the diagram PPTX (or note if skipped due to insufficient papers)
   - Paper count, date range, and any warnings (e.g., if topic was broad and review is selective)

## Error Handling

- If fewer than 5 relevant papers are found, warn the user, suggest `/lit-search {topic}`, and skip the PPTX diagram.
- If no deep-dive or comparison reports exist, proceed with search reports only.
- If the topic is very broad (>50 relevant papers), focus on the most recent and highest-impact papers and note the review is selective.
- If a DOI is missing for a paper, use its PubMed URL (`https://pubmed.ncbi.nlm.nih.gov/{pmid}/`) or arXiv URL as the hyperlink target in File 2.
- If `python-pptx` fails, note the error in the summary and skip the diagram — do not block the two markdown files.
