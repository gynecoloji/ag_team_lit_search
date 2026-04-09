# Literature Search Agent Team

A multi-agent system for biomedical literature search, analysis, and synthesis — built on Claude Code skills and designed for biomedical research in disease mechanisms, therapeutic targets, drug discovery, and translational research.

---

## How It Works

Each slash command invokes a **skill** that acts as a lead agent. Most skills dispatch **parallel sub-agents** to gather information simultaneously, then synthesize the results. Communication between the lead and sub-agents is one-directional: the lead sends a full briefing via the `Agent` tool, sub-agents return structured results, and the lead synthesizes.

```
User
 └─ /skill command
     └─ Lead Agent (skill instructions)
         ├─ Sub-agent 1  (parallel)
         ├─ Sub-agent 2  (parallel)
         └─ Sub-agent 3  (parallel)
              └─ Results merged → Report saved to reports/
```

---

## Skills Overview

### `/lit-search <topic>`
**Purpose:** Search recent publications across 4 sources and produce a structured summary report.

**Sub-agents dispatched (4, in parallel):**
| Agent | Source | Method |
|-------|--------|--------|
| PubMed Agent | PubMed + PMC | MCP PubMed tools |
| bioRxiv Agent | bioRxiv | MCP bioRxiv tools (category filter + relevance) |
| medRxiv Agent | medRxiv | MCP bioRxiv tools (server=medrxiv) |
| arXiv Agent | arXiv | arXiv API via WebFetch |

**Key behaviors:**
- Asks user for time span before searching (1mo / 3mo / 6mo / 1yr)
- Deduplicates across sources by DOI, then fuzzy title match
- Produces per-paper analysis cards: summary, key methods, findings, strengths/limitations, relevance to your work
- Groups papers by focus area with an executive summary
- Offers to add the topic to `config.json` tracked list

**Output:** `reports/searches/YYYY-MM-DD-<topic>.md`

---

### `/lit-trends`
**Purpose:** Analyze the most recent search report and produce a trend debrief with visualizations.

**Sub-agents dispatched:** None — runs as a single agent.

**Key behaviors:**
- Reads the **two** most recent search reports: current for analysis, previous for trajectory comparison
- Tags every method/tool as `[NEW]`, `[ONGOING]`, or `[FADING]` based on comparison with the previous report
- Generates 5 plots via `scripts/generate_trend_plots.py`: publication volume, sub-topic distribution, method heatmap, top labs, keyword co-occurrence
- **Priority Reading List:** top 5 papers ranked by actionability with a concrete reason per paper
- **Suggested Next Steps:** ready-to-paste skill invocations (`/lit-deep-dive`, `/lit-compare`, etc.) based on what actually appeared in the report

**Output:** `reports/trends/YYYY-MM-DD-trend-debrief.md` + `reports/trends/plots/`

---

### `/lit-deep-dive <DOI or PMID>`
**Purpose:** Exhaustive analysis of a single paper — full text, related work, code/data availability, reproducibility assessment.

**Sub-agents dispatched (3, in parallel):**
| Agent | Responsibility |
|-------|---------------|
| Paper Metadata Agent | Full text retrieval, all identifiers, abstract |
| Related Papers Agent | PubMed related articles + recent context papers |
| Code & Data Agent | GitHub/GitLab, GEO/SRA accessions, PyPI/Bioconductor packages |

**Key behaviors:**
- Handles DOI, PMID, and arXiv IDs
- Reproducibility assessment table: code, data, package, pre-trained models
- Frames findings in terms of relevance to your disease mechanisms / therapeutic target research

**Output:** `reports/deep-dives/YYYY-MM-DD-<title>.md`

---

### `/lit-compare <A> vs <B>`
**Purpose:** Head-to-head comparison of two or more competing methods.

**Sub-agents dispatched:** One per method (in parallel).

**Key behaviors:**
- Each agent fetches the primary paper and checks code availability
- Produces a feature comparison table (input/output, platforms, scalability, GPU, license, package availability)
- Shared benchmark table when methods report on the same datasets; flags evaluation protocol differences
- Personalized recommendation: when to use each method given your focus on disease mechanisms, therapeutic targets, and translational research

**Output:** `reports/comparisons/YYYY-MM-DD-<method1>-vs-<method2>.md`

---

### `/lit-reproduce <ID> — <figure>`
**Purpose:** Extract the analytical pipeline for a specific figure/result and interactively teach the hardest steps.

**Sub-agents dispatched (3, in parallel):**
| Agent | Responsibility |
|-------|---------------|
| Methods Extraction Agent | Ordered pipeline steps, tools, parameters, inputs/outputs |
| Resource Discovery Agent | Docs, tutorials, vignettes, known gotchas per tool |
| Difficulty Assessment Agent | Per-step ratings (conceptual / technical / data wrangling) at 3 levels |

**Key behaviors:**
- **Interactive teaching phase** after sub-agents return: confirms pipeline with user, shows difficulty map, delivers tailored explanations (beginner / intermediate / expert) for flagged steps
- Generates a Reproduction Checklist with actionable steps and install commands

**Output:** `reports/reproductions/YYYY-MM-DD-<title>-<target>.md`

---

### `/lit-review <topic>`
**Purpose:** Synthesize all accumulated reports into a narrative mini-review (suitable for grant intros, lab meetings, or review paper sections).

**Sub-agents dispatched (3, in parallel):**
| Agent | Responsibility |
|-------|---------------|
| Background Agent | Problem framing, historical context, current state |
| Methods Landscape Agent | Taxonomy table, technical comparison, benchmarks, emerging trends |
| Gaps & Future Agent | Open problems, missing benchmarks, lab opportunities, predicted directions |

**Key behaviors:**
- Reads all search reports + any deep-dive and comparison reports
- Filters for relevance to the given topic before dispatching agents
- Outputs a structured mini-review with abstract, background, methods landscape, open problems, key papers table, and references

**Output:** `reports/reviews/YYYY-MM-DD-<topic>.md`

---

### `/lit-ppt [search|trends|review]`
**Purpose:** Generate a PowerPoint presentation from any report type.

**Sub-agents dispatched:** None — runs as a single agent.

**Key behaviors:**
- Asks user for presentation style: Lab meeting (15-20 slides) / Journal club (10-15 slides) / Quick update (5-8 slides)
- Writes `scripts/build_presentation.py` using `python-pptx`, then runs it
- Design: white backgrounds throughout, dark navy headings, no text truncation
- Embeds trend plot images when generating from a trends report
- Falls back to a Markdown slide outline if `python-pptx` is unavailable

**Output:** `reports/presentations/YYYY-MM-DD-<topic>.pptx`

---

## Typical Workflow

```
/lit-search <topic>          # find papers
/lit-trends                  # identify what stands out + get next-step suggestions
/lit-deep-dive <DOI>         # drill into a specific paper
/lit-reproduce <ID> — Fig 3  # learn to reproduce a key result
/lit-compare <A> vs <B>      # resolve a method choice
/lit-review <topic>          # synthesize into a narrative
/lit-ppt trends              # generate slides for lab meeting
```

---

## Data Sources

| Source | Access method | Notes |
|--------|---------------|-------|
| PubMed | MCP PubMed tools | Full text via PMC when available |
| bioRxiv | MCP bioRxiv tools | Category-based browsing + relevance filter |
| medRxiv | MCP bioRxiv tools | `server=medrxiv` |
| arXiv | arXiv API (WebFetch) | Categories: q-bio, cs.LG, stat.ML |

---

## Project Structure

```
literature_search/
├── config.json                    # Tracked topics, focus areas, search parameters
├── scripts/
│   ├── generate_trend_plots.py    # Matplotlib/Seaborn plots for /lit-trends
│   └── build_presentation.py      # python-pptx builder for /lit-ppt (generated on demand)
├── reports/
│   ├── searches/                  # /lit-search output
│   ├── trends/                    # /lit-trends output + plots/
│   ├── deep-dives/                # /lit-deep-dive output
│   ├── comparisons/               # /lit-compare output
│   ├── reproductions/             # /lit-reproduce output
│   ├── reviews/                   # /lit-review output
│   └── presentations/             # /lit-ppt output (.pptx)
└── .claude/skills/                # Skill definitions (one SKILL.md per command)
```

---

## Dependencies

Installed on demand by the skills themselves:

```bash
pip3 install matplotlib seaborn   # required by /lit-trends
pip3 install python-pptx          # required by /lit-ppt
```
