---
name: lit-compare
description: Head-to-head comparison of two or more competing methods/tools — benchmarks, architectures, datasets, and recommendations.
user_invocable: true
argument: methods - two or more method names or DOIs to compare (e.g., "REMAP vs COSIE" or "10.1234/abc 10.5678/def")
---

# Literature Method Comparison

Compare two or more competing methods/tools head-to-head. Pull paper details for each, extract benchmarks, architectures, and datasets, and produce a structured comparison with recommendations.

## Instructions

1. **Parse the argument.** Extract method names or identifiers from the input. Handle formats:
   - "method1 vs method2" or "method1 vs method2 vs method3"
   - Space-separated DOIs or PMIDs
   - Method names (will be searched)

2. **Dispatch parallel agents to retrieve each paper.** Launch one agent per method in parallel.

   **Per-method Agent prompt:**
   ````
   You are a paper retrieval agent. Find the primary paper for: "{method_name_or_id}"

   If it is a DOI or PMID, retrieve it directly:
   - DOI starting with "10.1101" or "10.64898": use mcp__claude_ai_bioRxiv__get_preprint
   - Other DOI: use mcp__claude_ai_PubMed__search_articles with the DOI, then mcp__claude_ai_PubMed__get_article_metadata
   - PMID: use mcp__claude_ai_PubMed__get_article_metadata

   If it is a method name:
   - Search mcp__claude_ai_PubMed__search_articles with query: "{method_name}" sorted by relevance, max_results: 10
   - Search mcp__claude_ai_bioRxiv__search_preprints in "bioinformatics" category, recent_days: 365, limit: 100, then filter by title containing "{method_name}"
   - Pick the best matching paper

   Once found, retrieve full metadata. If PMID available, check for PMC full text:
   - Use mcp__claude_ai_PubMed__find_related_articles with link_type="pubmed_pmc"
   - If PMC ID found, use mcp__claude_ai_PubMed__get_full_text_article

   Also check for code availability:
   - Use WebFetch on the DOI URL (https://doi.org/{doi}) with prompt: "Find GitHub/GitLab URLs, data availability statements, and any benchmark result tables. Extract all URLs and any quantitative performance numbers."

   Return a structured report:
   - title, authors, date, source, doi, abstract
   - full_text_excerpt (first 1000 words if available)
   - methods_detail: algorithms, architectures, loss functions, key hyperparameters
   - datasets_used: list of datasets with sizes
   - benchmarks: any quantitative results (metrics, values, baselines compared against)
   - code_url: GitHub/GitLab URL or null
   - computational_requirements: runtime, GPU, memory if mentioned
   ````

3. **Generate the comparison report.** After all agents return, analyze the results and produce:

   ```markdown
   # Method Comparison: {Method1} vs {Method2} [vs {Method3}]

   **Date:** YYYY-MM-DD
   **Methods compared:** N

   ---

   ## Overview

   | | {Method1} | {Method2} |
   |---|-----------|-----------|
   | **Paper** | title | title |
   | **Source** | journal/preprint | journal/preprint |
   | **Date** | YYYY-MM-DD | YYYY-MM-DD |
   | **DOI** | ... | ... |

   ## Approach Comparison

   ### {Method1}
   2-3 sentence description of the core approach.

   ### {Method2}
   2-3 sentence description of the core approach.

   ### Key Architectural Differences
   - What fundamentally differs between the approaches
   - Different assumptions, inductive biases, or design choices

   ## Benchmark Comparison

   ### Shared Benchmarks
   If both methods report results on the same datasets or metrics, create a comparison table:

   | Dataset | Metric | {Method1} | {Method2} | Winner |
   |---------|--------|-----------|-----------|--------|
   | ... | ... | ... | ... | ... |

   ### Non-overlapping Benchmarks
   Results reported by one method but not the other.

   ### Benchmark Caveats
   - Different evaluation protocols, train/test splits, or preprocessing
   - Self-reported vs independently reproduced results

   ## Feature Comparison

   | Feature | {Method1} | {Method2} |
   |---------|-----------|-----------|
   | **Input data** | ... | ... |
   | **Output** | ... | ... |
   | **Platforms supported** | ... | ... |
   | **Scalability** | ... | ... |
   | **GPU required** | ... | ... |
   | **Code available** | Yes/No (URL) | Yes/No (URL) |
   | **Package** | PyPI/Bioc/None | PyPI/Bioc/None |
   | **License** | ... | ... |
   | **Reference data needed** | Yes/No | Yes/No |

   ## Strengths & Weaknesses

   ### {Method1}
   **Strengths:**
   - ...

   **Weaknesses:**
   - ...

   ### {Method2}
   **Strengths:**
   - ...

   **Weaknesses:**
   - ...

   ## Recommendation

   ### When to use {Method1}
   - Specific scenarios, data types, or requirements where this method is preferred

   ### When to use {Method2}
   - Specific scenarios, data types, or requirements where this method is preferred

   ### For your work specifically
   - Given your focus on spatial transcriptomics, multi-omics, and pipeline development, which method fits better and why
   ```

4. **Save the report** to `reports/comparisons/YYYY-MM-DD-<method1>-vs-<method2>.md`.

## Error Handling

- If a method paper cannot be found, note this and compare based on available information only.
- If no shared benchmarks exist, state this explicitly and compare qualitative features instead.
- If more than 3 methods are requested, proceed but warn that comparison complexity increases and recommend pairwise comparisons for depth.
