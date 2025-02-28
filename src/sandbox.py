from __future__ import annotations

from dataclasses import dataclass, field

from .models import ActionPlan


@dataclass
class AuditSandbox:
    """Records approved actions without performing external side effects."""

    events: list[dict] = field(default_factory=list)

    def execute(self, plan: ActionPlan, approved: bool) -> list[dict]:
        if not approved or plan.aborted:
            self.events.append({"event": "rejected", "case_id": plan.case_id})
            return self.events
        for call in plan.tool_calls:
            self.events.append(
                {
                    "event": "simulated_tool_call",
                    "case_id": plan.case_id,
                    "tool": call.name,
                    "arguments": call.arguments,
                    "side_effect": "none",
                }
            )
        return self.events
