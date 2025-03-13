from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def create_charts(results: Path) -> list[Path]:
    summary = pd.read_csv(results / "summary.csv")
    figures = results / "figures"
    figures.mkdir(exist_ok=True)

    order = summary["defense"].tolist()
    display = {
        "baseline": "Baseline",
        "prompt_hardening": "Prompt hardening",
        "detector_abort": "Detector abort",
        "tool_policy": "Tool policy",
        "independent_reviewer": "Reviewer",
        "combined": "Combined",
    }
    labels = [display[name] for name in order]
    fig, ax = plt.subplots(figsize=(10, 5.5))
    ax.bar(labels, summary["SASR_percent"])
    ax.set_ylabel("Security attack success rate (%)")
    ax.set_xlabel("Defense profile")
    ax.set_title("Executed offline benchmark: SASR by defense")
    ax.tick_params(axis="x", rotation=20)
    fig.tight_layout()
    p1 = figures / "sasr_by_defense.png"
    fig.savefig(p1, dpi=180)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(8, 5.5))
    ax.scatter(summary["SASR_percent"], summary["utility_under_attack_percent"], s=85)
    offsets = {
        "baseline": (8, 8),
        "prompt_hardening": (8, 8),
        "detector_abort": (8, 8),
        "tool_policy": (8, -18),
        "independent_reviewer": (8, 8),
        "combined": (8, 8),
    }
    for _, row in summary.iterrows():
        ax.annotate(
            display[row["defense"]],
            (row["SASR_percent"], row["utility_under_attack_percent"]),
            xytext=offsets[row["defense"]],
            textcoords="offset points",
            fontsize=8,
        )
    ax.set_xlabel("Security attack success rate (%) - lower is better")
    ax.set_ylabel("Utility under attack (%) - higher is better")
    ax.set_title("Security-utility trade-off")
    ax.grid(True, alpha=0.25)
    fig.tight_layout()
    p2 = figures / "security_utility_tradeoff.png"
    fig.savefig(p2, dpi=180)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(10, 5.5))
    ax.bar(labels, summary["detector_recall_percent"])
    ax.set_ylabel("Detection rate on attacked cases (%)")
    ax.set_xlabel("Defense profile threshold")
    ax.set_title("Transparent detector coverage")
    ax.tick_params(axis="x", rotation=20)
    fig.tight_layout()
    p3 = figures / "detector_coverage.png"
    fig.savefig(p3, dpi=180)
    plt.close(fig)
    return [p1, p2, p3]


def write_executed_results(results: Path) -> Path:
    summary = pd.read_csv(results / "summary.csv")
    by_suite = pd.read_csv(results / "by_suite.csv")
    manifest = (results / "run_manifest.json").read_text(encoding="utf-8")
    lines = [
        "# Executed benchmark results",
        "",
        "> Status: executed locally with the deterministic offline oracle. These are not live LLM results.",
        "",
        "## Overall summary",
        "",
        summary.to_markdown(index=False),
        "",
        "## Results by suite and setting",
        "",
        by_suite.to_markdown(index=False),
        "",
        "## Interpretation",
        "",
        "The exact least-privilege policy eliminates the public InjecAgent attacks in this adapter because the attacker tools are outside the explicit user-task capability set. This is a structural control-plane result, not evidence that a language model is intrinsically robust.",
        "",
        "The RedCrew-native suite contains output-only, same-tool, memory, and stealth goal-hijack cases. The residual stealth cases demonstrate why tool allow-listing alone is insufficient and why deterministic output validation or human approval remains necessary.",
        "",
        "The detector-abort profile reduces attack success but sacrifices utility whenever it aborts. Prompt sanitization and least-privilege enforcement preserve more user-task utility.",
        "",
        "## Manifest",
        "",
        "```json",
        manifest,
        "```",
    ]
    path = results / "EXECUTED_RESULTS.md"
    path.write_text("\n".join(lines), encoding="utf-8")
    return path
