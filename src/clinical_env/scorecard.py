"""A grade report as readable Markdown: per visit and per case, verdicts beside their evidence."""

from __future__ import annotations

from clinical_env.grader import CaseScore, GradeReport, Verdict, VisitScore


def _pct(value: float | None) -> str:
    return "n/a" if value is None else f"{value:.0%}"


def _cell(text: str) -> str:
    return text.replace("|", "/").replace("\n", " ").strip()


def _verdict(v: Verdict) -> str:
    if v.met is None:
        return "NOT GRADED" + (" ⚑ quote not found" if not v.evidence_verified else "")
    if not v.applicable:
        return "n/a"
    if v.kind == "must_not_do":
        return "**HAPPENED**" if v.met else "avoided"
    text = "met" if v.met else "**not met**"
    if v.overridden:
        text += f" (judge said met; {v.overridden})"
    return text


def _criticals(value: bool | None) -> str:
    return {True: "all met", False: "MISSED", None: "n/a"}[value]


def _visit(v: VisitScore) -> list[str]:
    f = v.log_facts
    lines = [
        f"### Visit {v.visit}: score {_pct(v.score)}",
        "",
        f"- Earned {v.earned:g} of {v.possible:g}; deductions {v.deductions:g}. "
        f"Criticals: {_criticals(v.criticals_met)}. "
        f"Consultation {v.consultation_earned:g} of {v.consultation_possible:g}.",
        f"- Log: {f.turns_used} of {f.turn_budget} turns, ended by {f.ended}; "
        f"read {', '.join(f.records_read) or 'nothing'}"
        f" ({len(f.records_before_talking)} before speaking, "
        f"{len(f.records_after_greeting)} before its questions); "
        f"not read: {', '.join(f.records_not_read) or 'none'}; "
        f"spoke to {', '.join(f'{p} ×{n}' for p, n in f.spoke_to.items()) or 'no one'}; "
        f"{f.multi_question_turns} turns with 2+ questions; {f.invalid_actions} invalid actions.",
        f"- Examined: {', '.join(f.examined) or 'nothing'}.",
    ]
    lines += [f"- ⚑ {e}" for e in v.errors]
    groups = [
        (
            "Case rubric",
            [x for x in v.verdicts if x.group in ("critical", "must_do", "must_not_do")],
        ),
        ("Consultation", [x for x in v.verdicts if x.group == "consultation"]),
    ]
    for title, verdicts in groups:
        if not verdicts:
            continue
        lines += [
            "",
            f"**{title}**",
            "",
            "| Item | Weight | Verdict | Evidence | Reason |",
            "|---|---|---|---|---|",
        ]
        for x in verdicts:
            name = f"{x.id} (critical)" if x.critical else x.id
            evidence = f"“{_cell(x.evidence)}”" if x.evidence else ""
            lines.append(
                f"| {name} | {x.weight:g} | {_verdict(x)} | {evidence} | {_cell(x.reason)} |"
            )
    if v.penalties:
        lines += [
            "",
            "**Penalties**",
            "",
            "| Type | Points | Quote | Reason |",
            "|---|---|---|---|",
        ]
        for p in v.penalties:
            flag = " ⚑ quote not found, not counted" if not p.evidence_verified else ""
            lines.append(
                f"| {p.type} | -{p.weight:g} | “{_cell(p.quote)}”{flag} | {_cell(p.reason)} |"
            )
    return lines


def _case(score: CaseScore, primary: bool) -> list[str]:
    misses = ", ".join(score.critical_misses)
    lines = [
        f"## Judge {score.judge}{' (primary)' if primary else ''}",
        "",
        f"- **Case score:** {_pct(score.score)}",
        f"- **Criticals:** {_criticals(score.criticals_met)}" + (f" ({misses})" if misses else ""),
        f"- **Consultation score:** {_pct(score.consultation_score)}",
    ]
    if score.ungraded:
        lines.append(f"- ⚑ **Not graded:** {', '.join(score.ungraded)}")
    for visit in score.visits:
        lines += ["", *_visit(visit)]
    return lines


def render_scorecard(report: GradeReport) -> str:
    lab = {
        "other_lab": "",
        "same_lab": " (same lab as the clinician: development only)",
        "unknown": " (clinician's lab not recorded)",
    }[report.primary_lab]
    lines = [
        f"# Grade: {report.case_id}",
        "",
        f"- **Run:** {report.run}",
        f"- **Clinician:** {report.clinician or 'not recorded'}",
        f"- **Primary judge:** {report.primary}{lab}",
    ]
    for a in report.agreement:
        lines.append(
            f"- **Agreement {a.judges[0]} vs {a.judges[1]}:** {a.agreed}/{a.items} items, "
            f"{a.critical_agreed}/{a.critical_items} criticals"
        )
    ordered = sorted(report.scores, key=lambda s: s.judge != report.primary)
    for score in ordered:
        lines += ["", *_case(score, score.judge == report.primary)]
    return "\n".join(lines) + "\n"
