from __future__ import annotations

from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class DefenseProfile(str, Enum):
    baseline = "baseline"
    prompt_hardening = "prompt_hardening"
    detector_abort = "detector_abort"
    tool_policy = "tool_policy"
    independent_reviewer = "independent_reviewer"
    combined = "combined"


class ToolCall(BaseModel):
    name: str
    arguments: dict[str, Any] = Field(default_factory=dict)
    source: str = "user"


class BenchmarkCase(BaseModel):
    id: str
    suite: str
    setting: str = "base"
    user_instruction: str
    user_tool: str
    untrusted_content: str = ""
    is_attack: bool = True
    attack_family: str = "none"
    attack_type: str = "none"
    attacker_instruction: str = ""
    attacker_tools: list[str] = Field(default_factory=list)
    success_marker: str = ""
    stealth: bool = False
    content_freedom: str = "unknown"
    metadata: dict[str, Any] = Field(default_factory=dict)


class Detection(BaseModel):
    score: float
    detected: bool
    reasons: list[str] = Field(default_factory=list)


class ActionPlan(BaseModel):
    case_id: str
    tool_calls: list[ToolCall] = Field(default_factory=list)
    final_text: str = ""
    followed_untrusted_instruction: bool = False
    aborted: bool = False
    notes: list[str] = Field(default_factory=list)


class ReviewDecision(BaseModel):
    approved: bool
    reasons: list[str] = Field(default_factory=list)


class RunRecord(BaseModel):
    case_id: str
    suite: str
    setting: str
    defense: str
    is_attack: bool
    attack_family: str
    attack_type: str
    detector_score: float
    detector_detected: bool
    blocked: bool
    clean_task_success: bool
    behavioral_influence: bool
    vulnerability_occurrence: bool
    security_attack_success: bool
    clearly_attributable_success: bool
    utility_under_attack: bool
    executed_tools: list[str]
    reasons: list[str] = Field(default_factory=list)
