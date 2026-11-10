"""The clinician's plan, submitted with `submit_plan` to end a visit (docs/build-v0.md, item 3).

No forced single diagnosis: the plan is a problem list. Actions carry a rationale because the
grader gives no credit for a bare mention.
"""

from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field


class ActionType(StrEnum):
    MEDICATION_CHANGE = "medication_change"
    REFERRAL = "referral"
    CARE_PACKAGE_CHANGE = "care_package_change"
    EQUIPMENT = "equipment"
    INVESTIGATION = "investigation"
    SAFEGUARDING = "safeguarding"
    CARER_SUPPORT = "carer_support"
    ADVICE = "advice"
    FOLLOW_UP = "follow_up"
    OTHER = "other"


class Urgency(StrEnum):
    EMERGENCY = "emergency"  # 999 / immediate
    SAME_DAY = "same_day"
    WITHIN_DAYS = "within_days"
    ROUTINE = "routine"


class _Model(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)


class PlanAction(_Model):
    type: ActionType
    detail: str = Field(min_length=1)
    rationale: str = Field(min_length=1)
    urgency: Urgency


class Discrepancy(_Model):
    description: str = Field(min_length=1, description="what the sources disagreed about")
    resolution: str = Field(min_length=1, description="what you concluded and why")


class Plan(_Model):
    problems: list[str] = Field(min_length=1)
    function_summary: str = Field(min_length=1, description="mobility, falls and ADLs")
    risks: list[str] = Field(default_factory=list)
    actions: list[PlanAction] = Field(min_length=1)
    discrepancies: list[Discrepancy] = Field(default_factory=list)
    follow_up: str = Field(min_length=1)
    safety_netting: str = Field(min_length=1)


def plan_text(plan: Plan) -> str:
    """The whole plan as plain text: the clinician's notes carried to its next visit."""
    lines = ["Problems:", *[f"- {p}" for p in plan.problems]]
    lines.append(f"Function and ADLs: {plan.function_summary}")
    if plan.risks:
        lines += ["Risks:", *[f"- {r}" for r in plan.risks]]
    lines.append("Actions:")
    lines += [
        f"- {a.type.value} ({a.urgency.value}): {a.detail}. Why: {a.rationale}"
        for a in plan.actions
    ]
    if plan.discrepancies:
        lines += [
            "Discrepancies:",
            *[f"- {d.description}: {d.resolution}" for d in plan.discrepancies],
        ]
    lines += [f"Follow-up: {plan.follow_up}", f"Safety-netting: {plan.safety_netting}"]
    return "\n".join(lines)


def plan_summary(plan: Plan) -> str:
    """A short GP record entry for a plan: problems, actions and follow-up, no rationale."""
    actions = "; ".join(a.detail.rstrip(".") for a in plan.actions)
    return (
        f"Problems: {'; '.join(p.rstrip('.') for p in plan.problems)}. "
        f"Plan: {actions}. Follow-up: {plan.follow_up.rstrip('.')}."
    )
