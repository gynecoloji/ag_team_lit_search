---
name: lit-reproduce
description: Reproduce a specific figure/result from a paper — extracts the analytical pipeline, finds learning resources, and interactively teaches the hardest parts adapted to your knowledge.
user_invocable: true
argument: identifier and target — a DOI/PMID followed by " — " and the figure/table/result to reproduce (e.g., "10.1038/s41586-026-10222-2 — Figure 3a")
---

# Literature Reproduce

Given a paper identifier and a specific figure, table, or result, produce a conceptual reproduction roadmap and interactively teach the most difficult analytical steps, adapted to the user's existing knowledge.

## Instructions

1. **Parse the argument.** Split on ` — ` (space-dash-space) to get:
   - `{identifier}` — DOI, PMID, or arXiv ID (same parsing as lit-deep-dive: `10.` prefix → DOI, purely numeric → PMID, pattern like `2603.19766` → arXiv ID)
   - `{target}` — the specific figure, table, or result to reproduce (e.g., "Figure 3a", "Table 2", "the clustering analysis")

   If the target is missing (no ` — ` separator found), use AskUserQuestion to prompt:
   > "Which figure, table, or result from this paper do you want to reproduce?"

2. **Dispatch 3 parallel agents.** Use the Agent tool to launch all 3 in a single message.

   **Methods Extraction Agent prompt:**
   ````
   You are a methods extraction agent. Your job is to extract the analytical pipeline behind a specific result in a paper.

   Paper identifier: "{identifier}"
   Target to reproduce: "{target}"

   Step 1 — Fetch the paper:

   If it is a PMID:
   - Use mcp__claude_ai_PubMed__get_article_metadata with pmids: ["{identifier}"]
   - Use mcp__claude_ai_PubMed__find_related_articles with link_type="pubmed_pmc" to find PMC ID
   - If PMC ID found, use mcp__claude_ai_PubMed__get_full_text_article to get the full text

   If it is a DOI starting with "10.1101" or "10.64898" (bioRxiv/medRxiv):
   - Use mcp__claude_ai_bioRxiv__get_preprint with the DOI
   - Try both server="biorxiv" and server="medrxiv"

   If it is another DOI:
   - Use mcp__claude_ai_PubMed__search_articles with the DOI to find the PMID
   - Then use mcp__claude_ai_PubMed__get_article_metadata and attempt full text retrieval via PMC
   - Also use WebFetch on https://doi.org/{doi} with prompt: "Extract the Methods section, any supplementary methods, figure legends, and data/code availability statements."

   If it is an arXiv ID:
   - Use WebFetch to fetch https://export.arxiv.org/api/query?id_list={identifier}
     with prompt: "Extract: title, authors, abstract, full methods description."
   - Use WebFetch on the PDF or HTML version if available to extract methods details.

   Step 2 — Extract the pipeline for "{target}":
   Focus ONLY on the methods, tools, and data that produced the specified target. Extract:
   - title: paper title
   - authors: full author list
   - date: publication date
   - source: journal/preprint server
   - doi, pmid, arxiv_id: all available identifiers
   - pipeline: an ordered list of steps, where each step has:
     - step_number: integer
     - name: short name (e.g., "Quality Control", "Dimensionality Reduction")
     - description: what happens in this step (2-3 sentences)
     - tools: list of software packages/tools used (with versions if mentioned)
     - input: what data goes in (format, type)
     - output: what comes out
     - key_parameters: any thresholds, settings, or hyperparameters mentioned
     - statistical_tests: any tests applied (if applicable)
   - input_data: overall input data description (organism, platform, accessions if mentioned, number of samples/cells)
   - figure_legend: the legend/caption for the target figure/table if available

   If full text is not available, extract as much as possible from the abstract and figure legends. Note what information is missing.
   ````

   **Resource Discovery Agent prompt:**
   ````
   You are a resource discovery agent. Your job is to find the best learning resources for reproducing a specific analytical pipeline.

   Paper identifier: "{identifier}"
   Target to reproduce: "{target}"

   First, fetch the paper to identify the tools and methods used:
   - If DOI: use WebFetch on https://doi.org/{identifier} with prompt: "Extract all software tools, packages, algorithms, and methods mentioned in the Methods section. List each tool with its purpose."
   - If PMID: use mcp__claude_ai_PubMed__get_article_metadata, then check for full text
   - If arXiv: use WebFetch on the arXiv page

   Then, for EACH tool or method identified, search for learning resources:

   1. Official documentation:
      - WebFetch on the tool's documentation URL (usually found via WebSearch)
      - Look for "Getting Started", "Tutorial", or "Quickstart" pages

   2. Tutorials and vignettes:
      - For R/Bioconductor packages: WebFetch on https://bioconductor.org/packages/release/bioc/vignettes/{package}/inst/doc/
      - For Python packages: WebSearch for "{package} tutorial" or "{package} example notebook"
      - WebSearch for "{tool} {method} tutorial site:github.com" to find example notebooks

   3. Community resources:
      - WebSearch for "{tool} {method} walkthrough" or "{tool} {method} step by step"
      - WebSearch for "{tool} common errors" or "{tool} troubleshooting"

   4. Alternative implementations:
      - WebSearch for "alternative to {tool}" or "{method} other implementations"

   Return a structured list where each entry has:
   - tool_name: the software package
   - purpose: what it does in the pipeline
   - doc_url: official documentation URL
   - best_tutorial: URL and title of the most helpful tutorial
   - additional_resources: list of {title, url, type} (type = "vignette", "notebook", "blog", "video", "docs")
   - gotchas: known pitfalls or common issues (from community forums)
   - alternatives: other tools that can accomplish the same step
   ````

   **Difficulty Assessment Agent prompt:**
   ````
   You are a difficulty assessment agent. Your job is to analyze an analytical pipeline from a paper and assess the difficulty of each step for someone who wants to reproduce it.

   Paper identifier: "{identifier}"
   Target to reproduce: "{target}"

   First, fetch the paper to understand the methods:
   - If DOI: use WebFetch on https://doi.org/{identifier} with prompt: "Extract the complete Methods section including any supplementary methods. Focus on the pipeline that produced {target}."
   - If PMID: use mcp__claude_ai_PubMed__get_article_metadata, then check for full text
   - If arXiv: use WebFetch on the arXiv page

   For each step in the analytical pipeline, assess difficulty on 3 axes:

   1. **Conceptual difficulty** (Low / Medium / High):
      - Low: standard, well-known technique (e.g., PCA, basic filtering)
      - Medium: requires understanding specific statistical or mathematical concepts (e.g., negative binomial models, graph-based clustering)
      - High: requires deep understanding of advanced math, novel algorithms, or domain-specific theory (e.g., variational autoencoders, optimal transport, spatial statistics)

   2. **Technical difficulty** (Low / Medium / High):
      - Low: well-maintained package, simple API, good docs
      - Medium: requires careful configuration, dependency management, or version-specific behavior
      - High: poorly documented, complex installation, GPU requirements, or requires custom code

   3. **Data wrangling difficulty** (Low / Medium / High):
      - Low: standard formats, straightforward loading
      - Medium: format conversions needed, multiple input sources to merge
      - High: complex preprocessing, custom parsers, large-scale data handling

   For each step rated Medium or High on ANY axis, prepare explanations at 3 levels:

   **Beginner explanation:** Assumes no prior knowledge of this concept. Uses everyday analogies. Explains the "what" and "why" before the "how".

   **Intermediate explanation:** Assumes familiarity with the general domain (e.g., knows what clustering is, but not this specific algorithm). Focuses on what makes this method different from simpler alternatives.

   **Expert explanation:** Assumes strong background. Focuses on implementation nuances, parameter sensitivity, and edge cases specific to this paper's application.

   Return a structured assessment:
   - steps: list of {step_name, conceptual, technical, data_wrangling, explanations: {beginner, intermediate, expert}}
   - overall_difficulty: Low / Medium / High
   - hardest_step: which step is the biggest hurdle and why
   - prerequisites: what background knowledge is assumed
   ````

3. **Interactive teaching phase.** After all agents return, engage the user in a dialogue:

   **Step 3a — Present the pipeline.** Show the extracted analytical pipeline as a numbered list with tools and brief descriptions. Ask:
   > "Here's the analytical pipeline I extracted for {target}. Does this match your understanding of what the paper did? Anything missing or incorrect?"

   Wait for user response. Adjust the pipeline if they provide corrections.

   **Step 3b — Show the difficulty map.** Present a table:

   | Step | Conceptual | Technical | Data Wrangling |
   |------|-----------|-----------|----------------|
   | 1. ... | Low | Medium | Low |
   | 2. ... | High | Low | Medium |

   Then ask:
   > "Here's how I'd rate the difficulty of each step. Which of these are you already comfortable with? Which feel unfamiliar or would you like me to explain?"

   Wait for user response. Note which steps they want explained.

   **Step 3c — Deliver tailored explanations.** For each step the user flagged as unfamiliar, present:
   - **Intuition:** What this method does in plain terms
   - **Key insight:** The concept that makes it click
   - **Connection:** How this relates to techniques the user already knows (leverage their computational biology background)
   - **Go deeper:** The single best resource from the Resource Discovery Agent

   Use the appropriate explanation level based on what the user said they know. Default to intermediate for a computational biologist.

   After each explanation, ask:
   > "Does that make sense? Want me to go deeper on this, or shall we move on?"

   **Step 3d — Final check.** After covering all flagged steps:
   > "Anything else unclear before I generate the full reproduction guide?"

4. **Generate the reproduction report.** Compile everything into:

   ```markdown
   # Reproduction Guide: [Paper Title] — [Target]

   **Authors:** full author list
   **Source:** journal / preprint server | **Date:** YYYY-MM-DD
   **DOI:** ... | **PMID:** ... | **arXiv:** ...
   **Target:** {target}

   ---

   ## Analytical Pipeline

   ### Step 1: [Step Name]
   - **What:** Description of this step
   - **Tools:** Package/tool (version)
   - **Input:** What goes in (format, type)
   - **Output:** What comes out
   - **Key parameters:** Thresholds, settings from the paper

   ### Step 2: [Step Name]
   ...

   (repeat for all steps)

   ## Difficulty Guide

   | Step | Conceptual | Technical | Data Wrangling |
   |------|-----------|-----------|----------------|
   | 1. ... | Low | Medium | Low |
   | 2. ... | High | Low | Medium |

   **Overall difficulty:** Medium
   **Hardest step:** Step N — [reason]
   **Prerequisites:** [background knowledge assumed]

   ## Deep Explanations

   (Only steps the user flagged as unfamiliar)

   ### Understanding [Concept from Step N]
   - **Intuition:** What it does in plain terms
   - **Key insight:** The concept that makes it click
   - **Connection:** How this relates to what you already know
   - **Go deeper:** [Best resource link]

   ### Understanding [Concept from Step M]
   ...

   ## Resources

   | Step | Tool | Resource | Type | URL |
   |------|------|----------|------|-----|
   | 1 | Scanpy | Preprocessing tutorial | Vignette | ... |
   | 2 | STdeconvolve | Getting started | Docs | ... |
   | ... | ... | ... | ... | ... |

   ### Alternative Tools
   - Step N: [alternative] can be used instead of [tool] — [trade-off]

   ### Known Gotchas
   - Step N: [common pitfall and how to avoid it]

   ## Reproduction Checklist

   - [ ] Obtain input data ([accession/source])
   - [ ] Install required tools ([list with install commands])
   - [ ] Step 1: [actionable description]
   - [ ] Step 2: [actionable description]
   - [ ] ...
   - [ ] Compare output to paper's {target}
   ```

5. **Save the report** to `reports/reproductions/YYYY-MM-DD-<sanitized-title>-<sanitized-target>.md` where title and target are lowercased, spaces replaced with hyphens, special characters removed.

## Error Handling

- If full text is not available, note this and extract as much as possible from the abstract, figure legends, and the DOI landing page. Flag: "Note: Full text was not accessible. Pipeline extraction is based on abstract and available metadata. Some steps may be incomplete."
- If a specific tool/method cannot be identified for a step, note it as "Method not specified in paper" and suggest the user check supplementary materials.
- If any of the 3 parallel agents fail, proceed with results from the others. Note the gap in the report.
- If the target figure/table cannot be found in the paper, ask the user to verify and describe what the figure shows.
