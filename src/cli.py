from __future__ import annotations

import json
from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console
from rich.table import Table

from .crewai_runtime import run_live_case
from .datasets import load_injecagent, load_native
from .detector import RuleBasedInjectionDetector
from .evaluation import run_benchmark
from .models import DefenseProfile
from .reporting import create_charts, write_executed_results

app = typer.Typer(help="RedCrew Arena adversarial prompting benchmark")
console = Console()


@app.command()
def benchmark(
    output: Annotated[Path, typer.Option(help="Result directory")] = Path("results"),
) -> None:
    frame = run_benchmark(output)
    create_charts(output)
    write_executed_results(output)
    console.print(f"[green]Completed {len(frame):,} runs.[/green]")
    _print_summary(output / "summary.csv")


@app.command()
def report(
    results: Annotated[Path, typer.Option(help="Existing result directory")] = Path("results"),
) -> None:
    paths = create_charts(results)
    md = write_executed_results(results)
    console.print(f"Wrote {md} and {len(paths)} charts.")


@app.command()
def inspect(
    text: Annotated[str, typer.Argument(help="Text to inspect")],
    threshold: Annotated[float, typer.Option(min=0.0, max=1.0)] = 0.55,
) -> None:
    detection = RuleBasedInjectionDetector().inspect(text, threshold)
    console.print_json(detection.model_dump_json())


@app.command()
def live(
    case_id: Annotated[str, typer.Argument(help="Case ID from the bundled datasets")],
    defense: Annotated[DefenseProfile, typer.Option()] = DefenseProfile.combined,
    model: Annotated[str | None, typer.Option()] = None,
    output: Annotated[Path, typer.Option()] = Path("results/live"),
) -> None:
    cases = load_injecagent() + load_native()
    selected = next((case for case in cases if case.id == case_id), None)
    if selected is None:
        raise typer.BadParameter(f"Unknown case ID: {case_id}")
    result = run_live_case(selected, defense, model)
    output.mkdir(parents=True, exist_ok=True)
    path = output / f"{case_id}__{defense.value}.json"
    path.write_text(json.dumps(result, indent=2), encoding="utf-8")
    console.print(f"Saved live trace to {path}")


def _print_summary(path: Path) -> None:
    import pandas as pd

    frame = pd.read_csv(path)
    table = Table(title="RedCrew Arena summary")
    for column in ("defense", "SASR_percent", "utility_under_attack_percent", "clean_utility_percent"):
        table.add_column(column)
    columns = ["defense", "SASR_percent", "utility_under_attack_percent", "clean_utility_percent"]
    for _, row in frame.iterrows():
        table.add_row(*(str(row[col]) for col in columns))
    console.print(table)


if __name__ == "__main__":
    app()
