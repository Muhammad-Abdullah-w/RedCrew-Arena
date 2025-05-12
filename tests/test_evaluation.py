from pathlib import Path

import pandas as pd

from redcrew_arena.evaluation import run_benchmark


def test_end_to_end_benchmark(tmp_path: Path) -> None:
    frame = run_benchmark(tmp_path)
    assert len(frame) == (2108 + 72 + 29) * 6
    assert (tmp_path / "summary.csv").exists()
    summary = pd.read_csv(tmp_path / "summary.csv")
    assert set(summary.defense) == {
        "baseline", "prompt_hardening", "detector_abort", "tool_policy",
        "independent_reviewer", "combined"
    }
    baseline = summary.loc[summary.defense == "baseline", "SASR_percent"].iloc[0]
    combined = summary.loc[summary.defense == "combined", "SASR_percent"].iloc[0]
    assert combined < baseline
