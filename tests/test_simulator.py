from redcrew_arena.datasets import load_native
from redcrew_arena.models import DefenseProfile
from redcrew_arena.simulator import DeterministicAttackFollowingOracle


def select(attack_type: str):
    return next(case for case in load_native() if case.attack_type == attack_type)


def test_baseline_follows_attack() -> None:
    record = DeterministicAttackFollowingOracle().run(select("tool_misuse"), DefenseProfile.baseline)
    assert record.security_attack_success


def test_tool_policy_blocks_external_tool() -> None:
    record = DeterministicAttackFollowingOracle().run(select("tool_misuse"), DefenseProfile.tool_policy)
    assert not record.security_attack_success
    assert record.clean_task_success


def test_combined_catches_secret_exfiltration() -> None:
    record = DeterministicAttackFollowingOracle().run(select("secret_exfiltration"), DefenseProfile.combined)
    assert not record.security_attack_success


def test_combined_retains_documented_stealth_gap() -> None:
    record = DeterministicAttackFollowingOracle().run(select("stealth_goal_hijack"), DefenseProfile.combined)
    assert record.security_attack_success
