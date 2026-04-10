# Literature Search Agent Team

Multi-agent literature search and analysis system for biology research.

## Project Structure

```
literature_search/
├── config.json                    # Search configuration (topics, focus areas, schedule)
├── scripts/                       # Python utilities (plotting, PPTX generation)
├── reports/
│   ├── searches/                  # /lit-search output (YYYY-MM-DD-<topic>.md)
│   ├── trends/                    # /lit-trends output + plots/
│   ├── deep-dives/                # /lit-deep-dive output
│   ├── comparisons/               # /lit-compare output
│   ├── reproductions/             # /lit-reproduce output
│   ├── reviews/                   # /lit-review output
│   ├── presentations/             # /lit-ppt output (.pptx)
│   └── downloads/                 # /lit-download output (PDFs + manifest.md)
└── .claude/skills/                # Skill definitions
    ├── lit-search/                # Multi-source paper search
    ├── lit-trends/                # Trend analysis + visualizations
    ├── lit-deep-dive/             # Single paper deep dive
    ├── lit-compare/               # Head-to-head method comparison
    ├── lit-reproduce/              # Reproduction guide + interactive teaching
    ├── lit-review/                # Mini-review synthesis
    ├── lit-ppt/                   # Presentation generator
    └── lit-download/              # PDF downloader (PMC, bioRxiv, arXiv, Unpaywall)
```

## Available Skills (Slash Commands)

| Command | Purpose |
|---------|---------|
| `/lit-search <topic>` | Search PubMed, bioRxiv, medRxiv, arXiv. Asks for time span (1mo/3mo/6mo/1yr). |
| `/lit-trends` | Analyze the most recent search report — trend debrief with plots. |
| `/lit-deep-dive <DOI or PMID>` | Deep dive on one paper: full text, related work, code/data check. |
| `/lit-compare <A> vs <B>` | Head-to-head comparison of methods — benchmarks, features, recs. |
| `/lit-reproduce <ID> — <target>` | Reproduce a figure/result — pipeline extraction, resources, interactive teaching. |
| `/lit-review <topic>` | Mini-review narrative from all accumulated reports. |
| `/lit-ppt [search\|trends\|review]` | Generate a PPTX presentation from a report. |
| `/lit-download [latest\|<report.md>\|<IDs...>]` | Download open-access PDFs (PMC, bioRxiv, arXiv, Unpaywall). Saves to `reports/downloads/`. |

## Typical Workflow

1. `/lit-search` → find papers on a topic
2. `/lit-trends` → identify what stands out
3. `/lit-download` → download open-access PDFs from the search results
4. `/lit-deep-dive` → drill into a specific paper
5. `/lit-reproduce` → learn how to reproduce a specific result
6. `/lit-compare` → compare competing methods
7. `/lit-review` → synthesize into a narrative
8. `/lit-ppt` → generate slides for lab meeting

## Data Sources

- **PubMed** — via MCP PubMed tools (search, metadata, full text via PMC)
- **bioRxiv/medRxiv** — via MCP bioRxiv tools (category browsing, preprint details)
- **arXiv** — via arXiv API (WebFetch on export.arxiv.org)

## Key Conventions

- Reports are saved as Markdown with date-prefixed filenames (YYYY-MM-DD-<topic>.md)
- `/lit-trends` analyzes only the most recent search report, not historical ones
- `/lit-search` asks the user for time span before searching
- `config.json` holds tracked topics, focus areas, and search parameters
- The `scripts/` directory holds reusable Python utilities (plotting, PPTX building)
- Python dependencies: `matplotlib`, `seaborn`, `python-pptx` (installed on demand)

## User Context

The primary user is a biomedical researcher focused on disease mechanisms, therapeutic targets, drug discovery, and translational research. Reports should be tailored to this expertise level.
