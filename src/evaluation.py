from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from .datasets import iter_all_cases
from .models import DefenseProfile, RunRecord
from .simulator import DeterministicAttackFollowingOracle

PROFILES = list(DefenseProfile)


def run_benchmark(output: Path, project_root: Path | None = None) -> pd.DataFrame:
    output.mkdir(parents=True, exist_ok=True)
    oracle = DeterministicAttackFollowingOracle()
    records: list[RunRecord] = []
    cases = list(iter_all_cases(project_root))
    for profile in PROFILES:
        for case in cases:
            records.append(oracle.run(case, profile))
    frame = pd.DataFrame([record.model_dump() for record in records])
    frame.to_json(output / "runs.jsonl", orient="records", lines=True)
    frame.to_csv(output / "runs.csv", index=False)
    summarize(frame, output)
    manifest = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "engine": "DeterministicAttackFollowingOracle-v1",
        "profiles": [p.value for p in PROFILES],
        "case_count": len(cases),
        "attack_case_count": int(sum(c.is_attack for c in cases)),
        "clean_control_count": int(sum(not c.is_attack for c in cases)),
        "run_count": len(frame),
        "dataset_fingerprint": dataset_fingerprint(cases),
        "limitations": [
            "Offline results evaluate deterministic control-plane defenses, not a live LLM.",
            "The public InjecAgent adapter uses an exact task-tool allow-list, which structurally favors least-privilege defenses.",
            "Live model results must be produced separately with pinned model identifiers and raw traces.",
        ],
    }
    (output / "run_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return frame


def dataset_fingerprint(cases: list) -> str:
    payload = "\n".join(case.model_dump_json() for case in cases).encode()
    return hashlib.sha256(payload).hexdigest()


def pct(series: pd.Series) -> float:
    return round(float(series.mean() * 100), 2) if len(series) else 0.0


def summarize(frame: pd.DataFrame, output: Path) -> None:
    rows: list[dict] = []
    for defense, group in frame.groupby("defense", sort=False):
        attacks = group[group.is_attack]
        clean = group[~group.is_attack]
        rows.append({
            "defense": defense,
            "attacked_cases": len(attacks),
            "clean_controls": len(clean),
            "BASR_percent": pct(attacks.behavioral_influence),
            "SASR_percent": pct(attacks.security_attack_success),
            "CSASR_percent": pct(attacks.clearly_attributable_success),
            "VOR_percent": pct(attacks.vulnerability_occurrence),
            "utility_under_attack_percent": pct(attacks.utility_under_attack),
            "clean_utility_percent": pct(clean.clean_task_success),
            "detector_recall_percent": pct(attacks.detector_detected),
            "detector_false_positive_percent": pct(clean.detector_detected),
            "blocked_percent": pct(attacks.blocked),
        })
    summary = pd.DataFrame(rows)
    baseline_sasr = float(summary.loc[summary.defense == "baseline", "SASR_percent"].iloc[0])
    summary["defense_effectiveness_absolute_pp"] = (baseline_sasr - summary.SASR_percent).round(2)
    summary["defense_effectiveness_relative_percent"] = (
        (baseline_sasr - summary.SASR_percent) / baseline_sasr * 100
    ).round(2)
    summary.to_csv(output / "summary.csv", index=False)

    by_suite = (
        frame[frame.is_attack]
        .groupby(["defense", "suite", "setting"], as_index=False)
        .agg(
            cases=("case_id", "count"),
            BASR_percent=("behavioral_influence", lambda s: round(s.mean() * 100, 2)),
            SASR_percent=("security_attack_success", lambda s: round(s.mean() * 100, 2)),
            VOR_percent=("vulnerability_occurrence", lambda s: round(s.mean() * 100, 2)),
            utility_under_attack_percent=("utility_under_attack", lambda s: round(s.mean() * 100, 2)),
        )
    )
    by_suite.to_csv(output / "by_suite.csv", index=False)

    by_family = (
        frame[frame.is_attack]
        .groupby(["defense", "attack_family", "attack_type"], as_index=False)
        .agg(
            cases=("case_id", "count"),
            SASR_percent=("security_attack_success", lambda s: round(s.mean() * 100, 2)),
            BASR_percent=("behavioral_influence", lambda s: round(s.mean() * 100, 2)),
        )
    )
    by_family.to_csv(output / "by_attack_family.csv", index=False)
