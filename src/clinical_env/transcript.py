"""A visit log as readable Markdown: what a clinician reviewer reads to judge realism."""

from __future__ import annotations

from clinical_env.case_run import CaseLog
from clinical_env.plan import Plan
from clinical_env.simulators import Attempt
from clinical_env.visit import Event, VisitLog


def _flags(attempts: list[Attempt]) -> list[str]:
    lines = []
    for number, attempt in enumerate(attempts, start=1):
        for flag in attempt.flags:
            lines.append(f"> ⚑ checker, draft {number}: **{flag.type}**: {flag.detail}")
        if number < len(attempts):
            lines.append(f"> rejected draft {number}: _{attempt.text}_")
    return lines


def _plan(plan: Plan) -> list[str]:
    lines = ["**Problems**", *[f"- {p}" for p in plan.problems]]
    lines += ["", f"**Function and ADLs:** {plan.function_summary}"]
    if plan.risks:
        lines += ["", "**Risks**", *[f"- {r}" for r in plan.risks]]
    lines += ["", "**Actions**", "", "| Type | Detail | Rationale | Urgency |", "|---|---|---|---|"]
    for action in plan.actions:
        cells = [action.type.value, action.detail, action.rationale, action.urgency.value]
        lines.append(
            "| " + " | ".join(c.replace("|", "/").replace("\n", " ") for c in cells) + " |"
        )
    if plan.discrepancies:
        lines += ["", "**Discrepancies**"]
        lines += [f"- {d.description} → {d.resolution}" for d in plan.discrepancies]
    lines += [
        "",
        f"**Follow-up:** {plan.follow_up}",
        "",
        f"**Safety-netting:** {plan.safety_netting}",
    ]
    return lines


def _event(event: Event, names: dict[str, str]) -> list[str]:
    turn = f"`{event.turn:>2}`"
    match event.kind:
        case "say":
            return [f"{turn} **GP → {names.get(event.to or '', event.to)}:** {event.text}"]
        case "reply":
            return [f"{turn} **{names[event.actor]}:** {event.text}", *_flags(event.attempts)]
        case "interjection":
            name = names[event.actor]
            if event.text is None:
                if len(event.attempts) < 2:
                    return []
                return [
                    f"{turn} **{name} (stays silent after a rejected draft)**",
                    *_flags(event.attempts),
                ]
            return [f"{turn} **{name} (adds):** {event.text}", *_flags(event.attempts)]
        case "read_record":
            body = (event.text or "").replace("\n", "\n> ")
            return [f"{turn} _GP reads `{event.request}`_", f"> {body}"]
        case "examine":
            hit = f" [{', '.join(event.finding_ids)}]" if event.finding_ids else ""
            error = f" ⚑ {event.error}" if event.error else ""
            return [f"{turn} _GP examines: {event.request}_ → {event.text}{hit}{error}"]
        case "invalid":
            return [f"{turn} _invalid action: {event.error}_"]
        case "plan":
            return [f"{turn} _GP submits plan_"]


def _visit_lines(log: VisitLog, names: dict[str, str], level: int) -> list[str]:
    """One visit's summary, briefing, consultation and plan, headed at `level`."""
    silent = sum(1 for e in log.events if e.kind == "interjection" and e.text is None)
    flagged = sum(
        1 for e in log.events for a in e.attempts if any(f.type != "checker_error" for f in a.flags)
    )
    regenerated = sum(1 for e in log.events if len(e.attempts) > 1)
    heading = "#" * level
    lines = [
        f"- **Turns:** {log.turns_used} used of a {log.turn_budget}-turn budget "
        f"(hard cap {log.hard_cap}); ended by {log.ended}",
        f"- **Checker:** {flagged} flagged drafts, {regenerated} regenerated; "
        f"{silent} interjection calls stayed silent",
        "",
        f"{heading} What the GP was told",
        "",
        "```text",
        log.briefing,
        "```",
        "",
        f"{heading} Consultation",
        "",
    ]
    for event in log.events:
        rendered = _event(event, names)
        if rendered:
            lines += [*rendered, ""]
    lines += [f"{heading} Plan", ""]
    lines += _plan(log.plan) if log.plan else ["_No plan submitted (hard cap reached)._"]
    if log.results:
        lines += ["", f"{heading} Tests ordered (in the chart by the next visit)", ""]
        for match in log.results:
            flag = f" ⚑ {match.error}" if match.error else ""
            lines.append(f"- {match.text}{flag}")
    return lines


def _header(header: dict[str, str]) -> list[str]:
    return [f"- **{key}:** {value}" for key, value in header.items()]


def render_markdown(log: VisitLog, names: dict[str, str], header: dict[str, str]) -> str:
    """One visit. `names` maps 'patient'/'carer' to display names; `header` adds run details."""
    lines = [f"# {log.case_id}, visit {log.visit}", "", *_header(header)]
    return "\n".join(lines + _visit_lines(log, names, level=2)) + "\n"


def render_case_markdown(
    log: CaseLog, names: dict[str, str], header: dict[str, str], headings: dict[int, str]
) -> str:
    """Every visit of a case run, in order. `headings` names each visit (date and setting)."""
    lines = [f"# {log.case_id}", "", *_header(header), f"- **Clinician memory:** {log.memory}"]
    for visit in log.visits:
        lines += ["", f"## {headings.get(visit.visit, f'Visit {visit.visit}')}", ""]
        lines += _visit_lines(visit, names, level=3)
    return "\n".join(lines) + "\n"
