from pathlib import Path
import hashlib

import redcrew_arena.datasets as datasets
from redcrew_arena.datasets import data_root, load_clean_controls, load_injecagent, load_native, project_root


def test_injecagent_cardinality() -> None:
    cases = load_injecagent()
    assert len(cases) == 2108
    assert sum(case.setting == "base" for case in cases) == 1054
    assert sum(case.setting == "enhanced" for case in cases) == 1054


def test_native_cardinality() -> None:
    assert len(load_native()) == 72


def test_clean_controls_and_data_locations(tmp_path: Path) -> None:
    controls = load_clean_controls()
    assert len(controls) == 29
    assert all(not case.is_attack for case in controls)

    repository_root = project_root()
    assert data_root(repository_root) == repository_root / "data"
    bare_root = tmp_path / "bare"
    bare_root.mkdir()
    assert data_root(bare_root) == bare_root

    package_data = Path(datasets.__file__).resolve().parent / "data"
    repository_data = repository_root / "data"
    for relative in (
        Path("public/injecagent_users.jsonl"),
        Path("public/injecagent_attackers.jsonl"),
        Path("native/tasks.jsonl"),
        Path("native/attacks.jsonl"),
    ):
        left = hashlib.sha256((package_data / relative).read_bytes()).hexdigest()
        right = hashlib.sha256((repository_data / relative).read_bytes()).hexdigest()
        assert left == right


def test_public_categories() -> None:
    cases = load_injecagent()
    assert {case.attack_family for case in cases} == {"direct_harm", "data_stealing"}
