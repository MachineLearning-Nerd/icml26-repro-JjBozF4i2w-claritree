"""Generate the five evidence figures used by the CLARITree report."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


OUT = Path(__file__).parent / "images"
OUT.mkdir(parents=True, exist_ok=True)
INK = "#17213b"
BLUE = "#2878b5"
ORANGE = "#f28e2b"
GREEN = "#2a9d68"
AMBER = "#d99b22"
GRID = "#d9deea"


def finish(fig: plt.Figure, name: str) -> None:
    fig.savefig(OUT / name, dpi=180, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def coverage() -> None:
    fig, ax = plt.subplots(figsize=(11, 4.8))
    ax.axis("off")
    claims = [
        ("C1", "Algorithm", "Aligned", GREEN),
        ("C2", "Complexity", "Aligned*", GREEN),
        ("C3", "Dominance", "Aligned", GREEN),
        ("C4", "California", "Aligned", GREEN),
        ("C5", "Synthetic", "Partial", AMBER),
        ("C6", "Completion", "Partial", AMBER),
    ]
    for i, (claim, label, status, color) in enumerate(claims):
        x = 0.02 + i * 0.163
        ax.add_patch(
            plt.Rectangle((x, 0.21), 0.145, 0.43, transform=ax.transAxes,
                          facecolor="#f7f9fc", edgecolor=color, linewidth=2)
        )
        ax.text(x + 0.0725, 0.54, claim, transform=ax.transAxes, ha="center",
                fontsize=15, fontweight="bold", color=INK)
        ax.text(x + 0.0725, 0.42, label, transform=ax.transAxes, ha="center",
                fontsize=10, color=INK)
        ax.text(x + 0.0725, 0.29, status, transform=ax.transAxes, ha="center",
                fontsize=10, fontweight="bold", color=color)
    ax.text(0.5, 0.86, "12 / 12 evidence points", transform=ax.transAxes,
            ha="center", fontsize=24, fontweight="bold", color=INK)
    ax.text(0.5, 0.74, "All six claims received a paper target and an observed, scoped assessment",
            transform=ax.transAxes, ha="center", fontsize=11, color="#4f5b75")
    ax.text(0.5, 0.08, "* C2 checks source + formula consequences; it is not a fresh asymptotic proof",
            transform=ax.transAxes, ha="center", fontsize=9, color="#667085")
    finish(fig, "headline_coverage.png")


def california() -> None:
    fig, ax = plt.subplots(figsize=(8, 4.8))
    labels = ["CLARITree\nrelease (5-fold)", "CLARITree\nfresh outer-4", "STreeD\nrelease (5-fold)"]
    values = [0.7499375138, 0.7431327225, 0.7048454540]
    bars = ax.bar(labels, values, color=[BLUE, GREEN, ORANGE], width=0.62)
    ax.set_ylim(0.67, 0.77)
    ax.set_ylabel("Test $R^2$")
    ax.set_title("California Housing: the released advantage survives a fresh source run",
                 color=INK, fontweight="bold")
    ax.grid(axis="y", color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)
    for bar, value in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width() / 2, value + 0.002,
                f"{value:.3f}", ha="center", fontweight="bold", color=INK)
    ax.text(0.5, 0.035, "fresh = release row to 1.2e-15", transform=ax.transAxes,
            ha="center", fontsize=9, color="#4f5b75")
    finish(fig, "california_r2.png")


def synthetic() -> None:
    greedy = np.array([4.2817508333, 5.1594863179, 3.9130133202, 4.9960598921, 5.2617571989])
    clari = np.array([4.1954450170, 5.0481816222, 3.8306324355, 4.9960598921, 5.0783655305])
    fig, ax = plt.subplots(figsize=(8, 4.8))
    for i in range(5):
        ax.plot([0, 1], [greedy[i], clari[i]], color="#aab3c5", linewidth=1.5)
        ax.scatter([0], [greedy[i]], color=ORANGE, s=55, zorder=3)
        ax.scatter([1], [clari[i]], color=BLUE, s=55, zorder=3)
        ax.text(-0.06, greedy[i], str(i), ha="right", va="center", fontsize=8, color="#667085")
    ax.set_xticks([0, 1], ["Greedy", "CLARITree"])
    ax.set_xlim(-0.25, 1.25)
    ax.set_ylabel("Test MSE (lower is better)")
    ax.set_title("Independent Figure 1 reconstruction: 4 wins, 1 tie",
                 color=INK, fontweight="bold")
    ax.grid(axis="y", color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)
    ax.text(0.5, 0.025, "mean 4.722 → 4.630 (−0.093)", transform=ax.transAxes,
            ha="center", fontsize=10, fontweight="bold", color=INK,
            bbox={"facecolor": "white", "edgecolor": "none", "pad": 2})
    finish(fig, "synthetic_paired_mse.png")


def dominance() -> None:
    slack = [0.0, 0.9128634, 1.7707346, 5.3169086, 0.0, 8.2312902, 0.0, 0.0, 0.0, 0.0]
    fig, ax = plt.subplots(figsize=(8, 4.8))
    ax.bar(np.arange(10), slack, color=[GREEN if value > 0 else "#b8c1d1" for value in slack])
    ax.axhline(0, color=INK, linewidth=1)
    ax.set_xticks(np.arange(10))
    ax.set_xlabel("Deterministic seed")
    ax.set_ylabel("Greedy objective − CLARITree objective")
    ax.set_title("Objective dominance: no negative slack in 10 trials",
                 color=INK, fontweight="bold")
    ax.grid(axis="y", color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)
    ax.text(9, 7.7, "4 strict improvements\n6 ties", ha="right", va="top",
            fontsize=10, color=INK)
    finish(fig, "dominance_slack.png")


def completion() -> None:
    fig, ax = plt.subplots(figsize=(8, 4.8))
    x = np.arange(2)
    width = 0.34
    paper = [95, 60]
    release = [100, 70]
    b1 = ax.bar(x - width / 2, paper, width, label="Paper (rounded)", color="#9aa6bd")
    b2 = ax.bar(x + width / 2, release, width, label="Released plot input", color=[BLUE, ORANGE])
    ax.set_xticks(x, ["CLARITree", "STreeD"])
    ax.set_ylim(0, 110)
    ax.set_ylabel("Completed runs at time budget (%)")
    ax.set_title("Completion advantage aligns; exact endpoints differ",
                 color=INK, fontweight="bold")
    ax.legend(frameon=False, loc="lower left")
    ax.grid(axis="y", color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)
    ax.bar_label(b1, fmt="%.0f%%", padding=3)
    ax.bar_label(b2, fmt="%.0f%%", padding=3, fontweight="bold")
    finish(fig, "completion_rates.png")


if __name__ == "__main__":
    coverage()
    california()
    synthetic()
    dominance()
    completion()
