---
name: lit-review
description: Generate a mini-review/perspective from accumulated search reports — a narrative synthesis suitable for lab meetings, grant intros, or review paper sections.
user_invocable: true
argument: topic - the topic to synthesize a review for (e.g., "spatial transcriptomics deconvolution methods")
---

# Literature Mini-Review

Synthesize all available search reports into a narrative mini-review on a given topic. The output should be suitable for a lab meeting presentation, grant introduction, or a section of a review paper.

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

4. **Dispatch 3 parallel agents** to build the review sections.

   **Background Agent prompt:**
   ````
   You are a literature background agent. Given the following list of papers related to "{topic}", write a background section for a mini-review.

   Papers:
   {list of relevant papers with titles, authors, dates, abstracts}

   Write 3-5 paragraphs covering:
   1. The problem: What is {topic} and why does it matter? What biological/computational questions does it address?
   2. Historical context: How has the field evolved? What were the key earlier methods or milestones (reference from the papers where possible)?
   3. Current state: What are the dominant approaches as of the most recent papers?
   4. Why a review is needed: What has changed recently that makes synthesis valuable?

   Use in-text citations as (Author et al., YYYY). Write for an audience of computational biologists familiar with genomics but not necessarily experts in {topic}.
   ````

   **Methods Landscape Agent prompt:**
   ````
   You are a methods landscape agent. Given the following papers related to "{topic}", create a structured analysis of the current methodological landscape.

   Papers:
   {list of relevant papers with titles, authors, dates, methods, key findings}

   Produce:
   1. **Taxonomy of approaches:** Group methods into categories (e.g., by architecture, by input data type, by task). Create a classification table.
   2. **Technical comparison:** For each category, describe the core approach, strengths, and limitations.
   3. **Benchmark summary:** Where papers share datasets or metrics, compile a comparison. Note which benchmarks are self-reported vs independently validated.
   4. **Emerging architectural trends:** What new patterns are appearing (e.g., foundation model adaptation, graph neural networks, diffusion models)?

   Write technically but accessibly. Use (Author et al., YYYY) citations.
   ````

   **Gaps & Future Agent prompt:**
   ````
   You are a literature gaps and future directions agent. Given the following papers related to "{topic}", identify gaps and predict future directions.

   Papers:
   {list of relevant papers with titles, authors, dates, abstracts, methods, findings}

   Produce:
   1. **Open problems:** What questions remain unanswered? What limitations do most methods share?
   2. **Missing benchmarks/datasets:** What evaluation infrastructure does the field need?
   3. **Underexplored connections:** Are there adjacent fields or methods that could be applied but haven't been?
   4. **Predicted directions:** Based on current trends, where is the field heading in the next 1-2 years?
   5. **Opportunities for your lab:** Given focus areas in spatial transcriptomics, multi-omics, and DL/algorithms in sequencing, where are the highest-impact opportunities?

   Be specific and actionable. Use (Author et al., YYYY) citations.
   ````

5. **Assemble the mini-review.** Combine agent outputs into a cohesive document:

   ```markdown
   # Mini-Review: {Topic}

   **Generated:** YYYY-MM-DD
   **Based on:** N search reports, M papers
   **Scope:** {date range of papers considered}

   ---

   ## Abstract
   150-250 word summary of the entire review — problem, current state, key findings, gaps, and outlook.

   ---

   ## 1. Background
   {Background Agent output, edited for coherence}

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
   {Open problems}

   ### 3.2 Missing Infrastructure
   {Benchmarks, datasets, standards needed}

   ### 3.3 Opportunities
   {Underexplored connections and high-impact opportunities}

   ### 3.4 Outlook
   {Where the field is heading}

   ## 4. Key Papers Reference Table

   | # | Paper | Authors | Year | Source | Category | Key Contribution |
   |---|-------|---------|------|--------|----------|-----------------|
   | 1 | ... | ... | ... | ... | ... | ... |

   ---

   ## References
   Full citation list in (Author et al., YYYY) format, sorted alphabetically.

   ---

   *Mini-review generated: YYYY-MM-DD | Literature search agent team*
   ```

6. **Save the report** to `reports/reviews/YYYY-MM-DD-<sanitized-topic>.md`.

## Error Handling

- If fewer than 5 relevant papers are found, warn the user that the review will be limited and suggest running `/lit-search {topic}` first to build a broader literature base.
- If no deep-dive or comparison reports exist, proceed with search reports only.
- If the topic is very broad (>50 relevant papers), focus on the most recent and highest-impact papers and note that the review is selective.
