#!/usr/bin/env python3
"""Generate trend visualization plots from literature search data.

Usage:
    python generate_trend_plots.py <input_json> <output_dir> <date_label>

Input JSON format:
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
"""

import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


def load_data(input_path: str) -> dict:
    with open(input_path) as f:
        return json.load(f)


def plot_publication_volume(papers: list, output_dir: Path, date_label: str):
    """Stacked bar chart: paper count per week by source."""
    from datetime import datetime

    source_week = defaultdict(lambda: defaultdict(int))
    for p in papers:
        dt = datetime.strptime(p["date"], "%Y-%m-%d")
        week = dt.strftime("%Y-W%U")
        source_week[week][p["source"]] += 1

    weeks = sorted(source_week.keys())
    sources = ["PubMed", "bioRxiv", "medRxiv", "arXiv"]
    colors = ["#2196F3", "#4CAF50", "#FF9800", "#9C27B0"]

    fig, ax = plt.subplots(figsize=(10, 5))
    bottoms = np.zeros(len(weeks))
    for source, color in zip(sources, colors):
        vals = [source_week[w].get(source, 0) for w in weeks]
        ax.bar(weeks, vals, bottom=bottoms, label=source, color=color)
        bottoms += np.array(vals)

    ax.set_xlabel("Week")
    ax.set_ylabel("Number of Papers")
    ax.set_title("Publication Volume Over Time")
    ax.legend()
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(output_dir / f"{date_label}-pub-volume.png", dpi=150)
    plt.close()


def plot_subtopic_distribution(papers: list, output_dir: Path, date_label: str):
    """Horizontal bar chart: papers per focus area."""
    area_counts = Counter(p["focus_area"] for p in papers)
    areas = list(area_counts.keys())
    counts = [area_counts[a] for a in areas]

    fig, ax = plt.subplots(figsize=(10, 5))
    colors = sns.color_palette("viridis", len(areas))
    ax.barh(areas, counts, color=colors)
    ax.set_xlabel("Number of Papers")
    ax.set_title("Sub-topic Distribution")
    plt.tight_layout()
    plt.savefig(output_dir / f"{date_label}-subtopic-dist.png", dpi=150)
    plt.close()


def plot_method_heatmap(papers: list, output_dir: Path, date_label: str):
    """Heatmap: methods vs focus areas."""
    method_area = defaultdict(lambda: defaultdict(int))
    all_methods = set()
    all_areas = set()
    for p in papers:
        for m in p.get("methods", []):
            method_area[m][p["focus_area"]] += 1
            all_methods.add(m)
            all_areas.add(p["focus_area"])

    if not all_methods or not all_areas:
        return

    methods = sorted(all_methods)
    areas = sorted(all_areas)
    matrix = np.array([[method_area[m][a] for a in areas] for m in methods])

    # Show top 15 methods by total count
    totals = matrix.sum(axis=1)
    top_idx = np.argsort(totals)[-15:]
    matrix = matrix[top_idx]
    methods = [methods[i] for i in top_idx]

    fig, ax = plt.subplots(figsize=(10, max(6, len(methods) * 0.4)))
    sns.heatmap(matrix, xticklabels=areas, yticklabels=methods,
                annot=True, fmt="d", cmap="YlOrRd", ax=ax)
    ax.set_title("Method / Algorithm × Focus Area")
    plt.tight_layout()
    plt.savefig(output_dir / f"{date_label}-method-heatmap.png", dpi=150)
    plt.close()


def plot_top_labs(papers: list, output_dir: Path, date_label: str):
    """Bar chart: most frequently appearing author groups."""
    # Use last author as proxy for lab/group
    lab_counts = Counter()
    for p in papers:
        if p.get("authors"):
            last_author = p["authors"][-1]
            lab_counts[last_author] += 1

    top = lab_counts.most_common(15)
    if not top:
        return

    labs, counts = zip(*top)

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(list(reversed(labs)), list(reversed(counts)), color="#3F51B5")
    ax.set_xlabel("Number of Papers")
    ax.set_title("Top Active Labs / Groups (by Last Author)")
    plt.tight_layout()
    plt.savefig(output_dir / f"{date_label}-top-labs.png", dpi=150)
    plt.close()


def plot_keyword_network(papers: list, output_dir: Path, date_label: str):
    """Network plot: keyword co-occurrence."""
    cooccurrence = defaultdict(int)
    keyword_count = Counter()

    for p in papers:
        kws = sorted(set(p.get("keywords", [])))
        for kw in kws:
            keyword_count[kw] += 1
        for i, kw1 in enumerate(kws):
            for kw2 in kws[i + 1:]:
                pair = tuple(sorted([kw1, kw2]))
                cooccurrence[pair] += 1

    # Top 20 keywords by frequency
    top_kws = {kw for kw, _ in keyword_count.most_common(20)}
    if len(top_kws) < 3:
        return

    # Filter co-occurrences to top keywords
    edges = [(k1, k2, c) for (k1, k2), c in cooccurrence.items()
             if k1 in top_kws and k2 in top_kws and c >= 1]

    if not edges:
        return

    fig, ax = plt.subplots(figsize=(10, 10))

    # Simple circular layout
    nodes = sorted(top_kws)
    n = len(nodes)
    angles = np.linspace(0, 2 * np.pi, n, endpoint=False)
    pos = {node: (np.cos(a), np.sin(a)) for node, a in zip(nodes, angles)}

    # Draw edges
    max_weight = max(c for _, _, c in edges)
    for k1, k2, c in edges:
        x = [pos[k1][0], pos[k2][0]]
        y = [pos[k1][1], pos[k2][1]]
        alpha = 0.2 + 0.8 * (c / max_weight)
        width = 0.5 + 3 * (c / max_weight)
        ax.plot(x, y, color="#90A4AE", alpha=alpha, linewidth=width)

    # Draw nodes
    for node in nodes:
        size = 100 + 500 * (keyword_count[node] / keyword_count.most_common(1)[0][1])
        ax.scatter(*pos[node], s=size, c="#1976D2", zorder=5, edgecolors="white", linewidth=1.5)
        ax.annotate(node, pos[node], fontsize=8, ha="center", va="center",
                    xytext=(0, 12), textcoords="offset points")

    ax.set_title("Keyword Co-occurrence Network")
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.5, 1.5)
    ax.axis("off")
    plt.tight_layout()
    plt.savefig(output_dir / f"{date_label}-keyword-network.png", dpi=150)
    plt.close()


def main():
    if len(sys.argv) != 4:
        print("Usage: python generate_trend_plots.py <input_json> <output_dir> <date_label>")
        sys.exit(1)

    input_path = sys.argv[1]
    output_dir = Path(sys.argv[2])
    date_label = sys.argv[3]

    output_dir.mkdir(parents=True, exist_ok=True)

    data = load_data(input_path)
    papers = data["papers"]

    if not papers:
        print("No papers to plot.")
        sys.exit(0)

    plot_publication_volume(papers, output_dir, date_label)
    plot_subtopic_distribution(papers, output_dir, date_label)
    plot_method_heatmap(papers, output_dir, date_label)
    plot_top_labs(papers, output_dir, date_label)
    plot_keyword_network(papers, output_dir, date_label)

    print(f"Generated plots in {output_dir}")


if __name__ == "__main__":
    main()
