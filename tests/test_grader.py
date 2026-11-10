"""The grader: log facts decided in code, judge replies validated, evidence checked, scores."""

from __future__ import annotations

import asyncio
import json
import re
from collections.abc import Sequence
from pathlib import Path
from typing import Any

import pytest
import yaml
from conftest import CASES, FakeModel
from test_visit import PLAN

from clinical_env import prompts
from clinical_env.case_run import CaseLog, Memory
from clinical_env.case_schema import Case, CriticalType, Person
from clinical_env.cli import main
from clinical_env.grader import (
    CaseScore,
    GradeReport,
    Penalty,
    Verdict,
    agreement,
    grade_case,
    load_consultation_rubric,
    log_facts,
    primary_judge,
    quote_found,
    score_case,
    score_visit,
)
from clinical_env.plan import Plan
from clinical_env.roles import Message
from clinical_env.scorecard import render_scorecard
from clinical_env.validate import validate_paths
from clinical_env.views import get_visit
from clinical_env.visit import Event, VisitLog

CONSULTATION = load_consultation_rubric()
SAID = "What have you actually seen at home, Janet?"
STOP = "Stop furosemide; ask pharmacy to remove it from the dosette"


def _log(case: Case, number: int, events: list[Event], *, plan: bool = True) -> VisitLog:
    visit = get_visit(case, number)
    return VisitLog(
        case_id=case.id,
        visit=number,
        setting=visit.setting,
        present=list(visit.present),
        turn_budget=visit.turn_budget,
        hard_cap=visit.turn_budget * 2,
        clinician_system="system",
        briefing="briefing",
        events=events,
        plan=Plan.model_validate(PLAN) if plan else None,
        turns_used=max((e.turn for e in events), default=0),
        ended="plan" if plan else "hard_cap",
    )


def _visit1_events(postural: bool = True) -> list[Event]:
    exams = ["x_postural_bp", "x_gait"] if postural else ["x_gait"]
    events = [
        Event(turn=1, kind="read_record", actor="clinician", request="gp_record", text="..."),
        Event(turn=2, kind="say", actor="clinician", to="carer", text=SAID),
        Event(turn=2, kind="reply", actor="carer", text="She's not eating, doctor."),
        Event(turn=3, kind="read_record", actor="clinician", request="care_agency_notes"),
        Event(turn=4, kind="say", actor="clinician", to="patient", text="Any pain? Or dizziness?"),
        Event(turn=4, kind="reply", actor="patient", text="No, dear."),
    ]
    events += [
        Event(turn=5 + i, kind="examine", actor="clinician", request=x, text="f", finding_ids=[x])
        for i, x in enumerate(exams)
    ]
    events.append(
        Event(turn=8, kind="examine", actor="clinician", request="obs", finding_ids=["x_obs"])
    )
    events.append(Event(turn=9, kind="invalid", actor="clinician", error="bad"))
    return events


def _ids(user: str) -> list[str]:
    section = user.split("\nItems:\n", 1)[1]
    return re.findall(r"^- ([a-z0-9_]+): ", section, flags=re.MULTILINE)


class Judge(FakeModel):
    """A judge that says every asked item is met (must-nots avoided) with a real quote, unless
    told otherwise per id; `penalties` go in each safety reply."""

    def __init__(
        self,
        override: dict[str, dict[str, Any]] | None = None,
        penalties: dict[str, list[dict[str, str]]] | None = None,
        raw: list[str] | None = None,
    ) -> None:
        self.override = override or {}
        self.penalties = penalties or {}
        self.raw = list(raw or [])
        super().__init__(self._reply)

    async def __call__(self, messages: Sequence[Message]) -> str:
        # On a retry the items are still in the first user message.
        self.calls.append(list(messages))
        return self._reply(messages[0].content, messages[1].content)

    def _reply(self, system: str, user: str) -> str:
        if self.raw:
            return self.raw.pop(0)
        safety = "must NOT do" in user
        items = []
        for item_id in _ids(user):
            default = {"met": not safety, "evidence": "" if safety else STOP}
            items.append(
                {"id": item_id, "reason": "r", **default, **self.override.get(item_id, {})}
            )
        reply: dict[str, Any] = {"items": items}
        if safety:
            reply.update(self.penalties)
        return json.dumps(reply)


def _grade(case: Case, log: CaseLog, judge: FakeModel) -> CaseScore:
    return asyncio.run(grade_case(case, log, judge, "openai/judge", CONSULTATION))


def _case_log(case: Case, visits: list[VisitLog]) -> CaseLog:
    return CaseLog(case_id=case.id, memory=Memory.NOTES, visits=visits)


# --- log facts ------------------------------------------------------------------------------


def test_log_facts_come_from_the_events(edith: Case) -> None:
    facts = log_facts(_log(edith, 1, _visit1_events()), get_visit(edith, 1))
    assert facts.records_read == ["gp_record", "care_agency_notes"]
    assert facts.records_before_talking == ["gp_record"]
    assert facts.records_after_greeting == ["gp_record", "care_agency_notes"]
    assert "discharge_summary" in facts.records_not_read
    assert facts.spoke_to == {"carer": 1, "patient": 1}
    # A set's id stands for its parts.
    assert {"x_postural_bp", "x_gait", "x_obs", "x_pulse", "x_sats"} <= set(facts.examined)
    assert facts.multi_question_turns == 1 and facts.invalid_actions == 1
    assert facts.turns_used == 9


# --- one visit graded -----------------------------------------------------------------------


def test_all_met_scores_full_marks_and_the_judge_sees_the_truth(edith: Case) -> None:
    judge = Judge()
    score = _grade(edith, _case_log(edith, [_log(edith, 1, _visit1_events())]), judge)
    [visit] = score.visits
    assert visit.errors == [] and visit.penalties == []
    assert visit.score == 1.0 and visit.criticals_met is True
    assert score.criticals_met is True and score.critical_misses == []
    # Four groups at visit 1 (critical, must_do, must_not_do, consultation), one call each.
    assert len(judge.calls) == 4
    user = judge.calls[0][1].content
    assert "Hidden truth" in user and "d_furosemide" in user and STOP in user
    assert judge.calls[0][0].content == prompts.GRADER_SYSTEM


def test_judge_met_without_the_required_examination_is_overruled(edith: Case) -> None:
    log = _case_log(edith, [_log(edith, 1, _visit1_events(postural=False))])
    score = _grade(edith, log, Judge())
    verdict = next(v for v in score.visits[0].verdicts if v.id == "v1_falls_function")
    assert verdict.met is False and verdict.overridden == "did not examine x_postural_bp"
    assert score.criticals_met is False and score.critical_misses == ["v1_falls_function"]


def test_ask_daughter_needs_her_spoken_to_and_the_agency_notes_read(edith: Case) -> None:
    events = [e for e in _visit1_events() if e.request != "care_agency_notes"]
    score = _grade(edith, _case_log(edith, [_log(edith, 1, events)]), Judge())
    verdict = next(v for v in score.visits[0].verdicts if v.id == "v1_ask_daughter")
    assert verdict.met is False and verdict.overridden == "did not read care_agency_notes"


def test_a_made_up_quote_gets_one_retry_then_is_left_ungraded(edith: Case) -> None:
    judge = Judge(override={"v1_reconcile_meds": {"evidence": "Stopped digoxin today"}})
    score = _grade(edith, _case_log(edith, [_log(edith, 1, _visit1_events())]), judge)
    verdict = next(v for v in score.visits[0].verdicts if v.id == "v1_reconcile_meds")
    # Neither credited nor counted as a miss; the case has no score until someone looks.
    assert verdict.met is None and verdict.evidence_verified is False
    assert score.ungraded == ["v1_reconcile_meds"] and score.score is None
    assert score.criticals_met is None and score.visits[0].criticals_met is None
    assert any("evidence not found" in e for e in score.visits[0].errors)
    assert len(judge.calls) == 5  # the critical group was asked twice
    [retry] = [c[-1].content for c in judge.calls if "could not be used" in c[-1].content]
    assert "not an exact quote: 'Stopped digoxin today'" in retry


CRITICALS = ["v1_reconcile_meds", "v1_falls_function", "v1_care_package"]


def _criticals_reply(made_up: list[str]) -> str:
    return json.dumps(
        {
            "items": [
                {"id": i, "met": True, "evidence": "invented words" if i in made_up else STOP}
                for i in CRITICALS
            ]
        }
    )


def test_a_worse_retry_never_replaces_a_better_first_reply(edith: Case) -> None:
    class Worse(Judge):
        def __init__(self) -> None:
            super().__init__()
            self.critical_calls = 0

        def _reply(self, system: str, user: str) -> str:
            if "v1_reconcile_meds" in _ids(user):
                self.critical_calls += 1
                if self.critical_calls == 1:
                    return _criticals_reply(["v1_care_package"])
                return _criticals_reply(["v1_care_package", "v1_reconcile_meds"])
            return super()._reply(system, user)

    judge = Worse()
    score = _grade(edith, _case_log(edith, [_log(edith, 1, _visit1_events())]), judge)
    verdicts = {v.id: v.met for v in score.visits[0].verdicts if v.critical}
    assert judge.critical_calls == 2
    assert verdicts == {
        "v1_reconcile_meds": True,
        "v1_falls_function": True,
        "v1_care_package": None,
    }


def test_a_provider_error_leaves_the_group_ungraded_and_the_rest_graded(edith: Case) -> None:
    class Failing(Judge):
        def _reply(self, system: str, user: str) -> str:
            if "must NOT do" in user:
                raise RuntimeError("context length exceeded")
            return super()._reply(system, user)

    judge = Failing()
    score = _grade(edith, _case_log(edith, [_log(edith, 1, _visit1_events())]), judge)
    visit = score.visits[0]
    assert {v.id for v in visit.verdicts if v.met is None} == {
        "v1_midodrine",
        "v1_bppv",
        "v1_continue_furosemide",
        "v1_care_home",
    }
    assert any("judge call failed: RuntimeError" in e for e in visit.errors)
    assert visit.score is None and score.criticals_met is True
    assert len(judge.calls) == 4  # no retry after a provider error


def test_duplicate_ids_are_retried(edith: Case) -> None:
    items = [{"id": i, "met": True, "evidence": STOP} for i in [CRITICALS[0], *CRITICALS]]
    judge = Judge(raw=[json.dumps({"items": items})])
    score = _grade(edith, _case_log(edith, [_log(edith, 1, _visit1_events())]), judge)
    assert score.ungraded == [] and len(judge.calls) == 5


def test_an_unfound_penalty_quote_is_listed_but_not_deducted(edith: Case) -> None:
    found = {"quote": "She has had a stroke last year", "reason": "x"}
    judge = Judge(penalties={"invented_facts": [found]})
    score = _grade(edith, _case_log(edith, [_log(edith, 1, _visit1_events())]), judge)
    [penalty] = score.visits[0].penalties
    assert penalty.evidence_verified is False and score.visits[0].deductions == 0


def test_a_penalty_must_quote_the_clinician_not_the_patient(edith: Case) -> None:
    judge = Judge(
        penalties={"invented_facts": [{"quote": "She's not eating, doctor", "reason": "x"}]}
    )
    score = _grade(edith, _case_log(edith, [_log(edith, 1, _visit1_events())]), judge)
    assert score.visits[0].penalties[0].evidence_verified is False


def test_consultation_ids_must_not_clash_with_the_case_rubric(edith: Case) -> None:
    clash = [CONSULTATION[0].model_copy(update={"id": "v1_reconcile_meds"})]
    with pytest.raises(ValueError, match="share ids"):
        asyncio.run(grade_case(edith, _case_log(edith, []), Judge(), "j", clash))


def test_earlier_visits_from_another_log_are_context(edith: Case) -> None:
    judge = Judge()
    v2 = [Event(turn=1, kind="say", actor="clinician", to="carer", text="How is Mum?")]
    earlier = [_log(edith, 1, _visit1_events())]
    log = _case_log(edith, [_log(edith, 2, v2)])
    asyncio.run(grade_case(edith, log, judge, "j", CONSULTATION, earlier))
    users = [c[1].content for c in judge.calls]
    assert all("plans at earlier visits" in u for u in users)
    assert not any("Visit 1, home visit" in u for u in users)  # visit 1 itself is not graded


def test_an_unreadable_judge_leaves_items_ungraded_never_met(edith: Case) -> None:
    judge = Judge(raw=["no json here", "still no json"])
    score = _grade(edith, _case_log(edith, [_log(edith, 1, _visit1_events())]), judge)
    ungraded = [v for v in score.visits[0].verdicts if v.met is None]
    assert ungraded and score.ungraded == [v.id for v in ungraded]
    assert any("judge failed after a retry" in e for e in score.visits[0].errors)
    # The group that failed did not earn anything.
    assert score.visits[0].earned < score.visits[0].possible


def test_a_retry_that_fixes_the_reply_is_used(edith: Case) -> None:
    judge = Judge(raw=["not json"])
    score = _grade(edith, _case_log(edith, [_log(edith, 1, _visit1_events())]), judge)
    assert score.ungraded == [] and score.visits[0].errors == []
    assert len(judge.calls) == 5


def test_wrong_ids_are_retried(edith: Case) -> None:
    bad = json.dumps({"items": [{"id": "made_up", "met": True, "evidence": STOP}]})
    judge = Judge(raw=[bad])
    score = _grade(edith, _case_log(edith, [_log(edith, 1, _visit1_events())]), judge)
    assert score.ungraded == []
    [retry] = [c[-1].content for c in judge.calls if len(c) > 2]
    assert "give exactly one entry for each of" in retry and "you gave ['made_up']" in retry


def test_penalties_and_must_not_dos_are_deducted(edith: Case) -> None:
    judge = Judge(
        override={"v1_continue_furosemide": {"met": True, "evidence": STOP}},
        penalties={
            "invented_facts": [{"quote": "Falls with postural hypotension", "reason": "x"}],
            "over_provision": [{"quote": "Call 999 after a fall with injury", "reason": "y"}],
        },
    )
    score = _grade(edith, _case_log(edith, [_log(edith, 1, _visit1_events())]), judge)
    visit = score.visits[0]
    assert [p.type for p in visit.penalties] == ["invented_fact", "over_provision"]
    assert visit.deductions == 3 + 2 + 1  # must-not-do weight 3, invented 2, over-provision 1
    assert visit.score == (visit.earned - 6) / visit.possible


def test_a_critical_must_not_do_that_happened_is_a_critical_miss(edith: Case) -> None:
    rubric = [
        r.model_copy(update={"critical": True, "critical_type": CriticalType.CLINICAL_ACTION})
        if r.id == "v1_care_home"
        else r
        for r in edith.rubric
    ]
    case = edith.model_copy(update={"rubric": rubric})
    for happened, misses in ((False, []), (True, ["v1_care_home"])):
        judge = Judge(override={"v1_care_home": {"met": happened, "evidence": STOP}})
        score = _grade(case, _case_log(case, [_log(case, 1, _visit1_events())]), judge)
        assert score.critical_misses == misses and score.criticals_met is (not happened)
        safety = [c[1].content for c in judge.calls if "must NOT do" in c[1].content]
        assert len(safety) == 1 and "- v1_care_home:" in safety[0]


def test_over_provision_is_listed_in_full_but_capped(edith: Case) -> None:
    quote = {"quote": "Call 999 after a fall with injury", "reason": "y"}
    judge = Judge(penalties={"over_provision": [quote] * 5})
    score = _grade(edith, _case_log(edith, [_log(edith, 1, _visit1_events())]), judge)
    visit = score.visits[0]
    assert len(visit.penalties) == 5 and visit.deductions == 3


def test_over_budget_is_a_penalty_from_the_log(edith: Case) -> None:
    events = [*_visit1_events(), Event(turn=41, kind="plan", actor="clinician")]
    score = _grade(edith, _case_log(edith, [_log(edith, 1, events)]), Judge())
    [penalty] = score.visits[0].penalties
    assert penalty.type == "over_budget" and penalty.quote.startswith("41 turns used of a 40")


def test_read_first_is_decided_in_code(edith: Case) -> None:
    greet = Event(turn=0, kind="say", actor="clinician", to="patient", text="Hello Edith")
    greeting_first = [greet, *_visit1_events()]
    two_first = [greet, greet, *_visit1_events()]
    cases = ((_visit1_events(), True), (greeting_first, True), (two_first, False))
    for events, met in cases:
        score = _grade(edith, _case_log(edith, [_log(edith, 1, events)]), Judge())
        verdict = next(v for v in score.visits[0].verdicts if v.id == "c_read_first")
        assert verdict.met is met and verdict.reason.startswith("from the log")


def test_consultation_items_follow_their_setting_and_applicability(edith: Case) -> None:
    judge = Judge(override={"c_rephrase": {"met": False, "applicable": False}})
    v2 = [Event(turn=1, kind="say", actor="clinician", to="carer", text="How is Mum?")]
    log = _case_log(edith, [_log(edith, 1, _visit1_events()), _log(edith, 2, v2)])
    score = _grade(edith, log, judge)
    one, two = score.visits
    assert "c_permission_home" in [v.id for v in one.verdicts]
    assert "c_permission_home" not in [v.id for v in two.verdicts]  # a phone call
    assert "c_follow_up_plan" not in [v.id for v in one.verdicts]  # follow-up visits only
    assert "c_follow_up_plan" in [v.id for v in two.verdicts]
    rephrase = next(v for v in one.verdicts if v.id == "c_rephrase")
    assert rephrase.applicable is False
    weights = {c.id: c.weight for c in CONSULTATION}
    expected = sum(weights.values()) - weights["c_rephrase"] - weights["c_follow_up_plan"]
    assert one.consultation_possible == expected


def test_visit_2_grading_sees_the_earlier_plan_as_context(edith: Case) -> None:
    judge = Judge()
    v2 = [Event(turn=1, kind="say", actor="clinician", to="carer", text="How is Mum?")]
    log = _case_log(edith, [_log(edith, 1, _visit1_events()), _log(edith, 2, v2)])
    _grade(edith, log, judge)
    v2_calls = [
        c[1].content for c in judge.calls if "Visit 2, telephone consultation" in c[1].content
    ]
    assert v2_calls and all("plans at earlier visits" in u for u in v2_calls)
    assert all("Visit 1:\nProblems:" in u for u in v2_calls)
    assert all("Since the last visit:" in u for u in v2_calls)


def test_a_lone_later_visit_says_earlier_visits_are_missing(edith: Case) -> None:
    judge = Judge()
    v2 = [Event(turn=1, kind="say", actor="clinician", to="carer", text="How is Mum?")]
    _grade(edith, _case_log(edith, [_log(edith, 2, v2)]), judge)
    assert "Earlier visits are not in this run log" in judge.calls[0][1].content


def test_no_plan_is_said_and_graded(edith: Case) -> None:
    judge = Judge(override={"v1_reconcile_meds": {"met": False, "evidence": ""}})
    score = _grade(edith, _case_log(edith, [_log(edith, 1, _visit1_events(), plan=False)]), judge)
    assert "No plan was submitted" in judge.calls[0][1].content
    assert score.critical_misses == ["v1_reconcile_meds"]


def test_a_run_of_another_case_is_refused(edith: Case) -> None:
    log = CaseLog(case_id="someone_else", memory=Memory.NOTES)
    with pytest.raises(ValueError, match="someone_else"):
        _grade(edith, log, Judge())


# --- pieces ---------------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("quote", "found"),
    [
        (STOP, True),
        (f'"{STOP.upper()}."', True),
        ("Stop furosemide ... remove it from the dosette", True),
        ("Stop furosemide … remove it from the dosette", True),
        ("Stop digoxin", False),
        ("Stop furosemide ... start digoxin", False),
        ("", False),
        ("...", False),
    ],
)
def test_quote_found(quote: str, found: bool) -> None:
    assert quote_found(quote, f"Actions:\n- {STOP}.  Why: it’s fine") is found


def test_curly_quotes_and_spacing_are_forgiven() -> None:
    assert quote_found("it's  fine for now", "Why: it’s fine for now")


@pytest.mark.parametrize("quote", ["a", "GP to", "Stop ... dosette", "[turn 2]"])
def test_short_pieces_never_count_as_evidence(quote: str) -> None:
    assert not quote_found(quote, f"[turn 2] GP to Edith: {STOP}")


def _verdict(
    item: str, met: bool | None, *, critical: bool = False, group: Any = "must_do"
) -> Verdict:
    return Verdict(id=item, group=group, kind="must_do", weight=2, critical=critical, met=met)


def test_score_floors_at_zero_and_criticals(edith: Case) -> None:
    facts = log_facts(_log(edith, 1, []), get_visit(edith, 1))
    penalty = Penalty(type="wrong_fact_action", quote="q", reason="r", weight=3)
    visit = score_visit(
        1, [_verdict("a", True), _verdict("b", False, critical=True)], [penalty] * 2, facts, []
    )
    assert visit.score == 0.0 and visit.criticals_met is False
    case = score_case("c", "j", [visit])
    assert case.score == 0.0 and case.critical_misses == ["b"]


def test_an_ungraded_critical_is_unknown_but_a_miss_still_decides(edith: Case) -> None:
    facts = log_facts(_log(edith, 1, []), get_visit(edith, 1))
    unknown = score_visit(1, [_verdict("a", None, critical=True)], [], facts, [])
    assert unknown.criticals_met is None and score_case("c", "j", [unknown]).criticals_met is None
    missed = score_visit(2, [_verdict("b", False, critical=True)], [], facts, [])
    assert score_case("c", "j", [unknown, missed]).criticals_met is False
    mixed = [_verdict("a", None, critical=True), _verdict("b", False, critical=True)]
    both = score_visit(1, mixed, [], facts, [])
    assert both.criticals_met is False and both.score is None


def test_agreement_and_primary_judge(edith: Case) -> None:
    facts = log_facts(_log(edith, 1, []), get_visit(edith, 1))
    a = score_case(
        "c",
        "openai/a",
        [score_visit(1, [_verdict("x", True, critical=True), _verdict("y", True)], [], facts, [])],
    )
    b = score_case(
        "c",
        "google/b",
        [score_visit(1, [_verdict("x", True, critical=True), _verdict("y", False)], [], facts, [])],
    )
    [pair] = agreement([a, b])
    assert (pair.items, pair.agreed, pair.critical_items, pair.critical_agreed) == (2, 1, 1, 1)
    assert primary_judge(["openai/a", "google/b"], "openai/clin") == ("google/b", "other_lab")
    assert primary_judge(["openai/a"], "openai/clin") == ("openai/a", "same_lab")
    assert primary_judge(["openai/a"], None) == ("openai/a", "unknown")
    assert primary_judge(["openai/a"], "human") == ("openai/a", "unknown")


def test_scorecard_shows_misses_evidence_and_flags(edith: Case) -> None:
    log = _case_log(edith, [_log(edith, 1, _visit1_events(postural=False))])
    score = _grade(edith, log, Judge())
    report = GradeReport(
        case_id=edith.id,
        run="runs/x.json",
        clinician="openai/clin",
        primary="openai/judge",
        primary_lab="same_lab",
        scores=[score],
        agreement=[],
    )
    text = render_scorecard(report)
    assert "**Criticals:** MISSED (v1_falls_function)" in text
    assert "judge said met; did not examine x_postural_bp" in text
    assert f"“{STOP}”" in text and "development only" in text


# --- case files and the command line --------------------------------------------------------


def test_requires_must_name_real_findings_records_and_people(tmp_path: Path) -> None:
    text = (CASES / "edith_marsh.yaml").read_text(encoding="utf-8")
    text = text.replace("examined: [x_postural_bp, x_gait]", "examined: [x_nope]")
    text = text.replace(
        "    description: Starts midodrine",
        "    requires: {spoke_to: [patient]}\n    description: Starts midodrine",
    )
    path = tmp_path / "edith_marsh.yaml"
    path.write_text(text, encoding="utf-8")
    [result] = validate_paths([path])
    assert (
        "rubric v1_falls_function: requires examined x_nope: no such finding at visit 1"
        in result.errors
    )
    assert "rubric v1_midodrine: requires is only for must_do or red_flag items" in result.errors


def test_requires_at_a_phone_visit_cannot_examine(tmp_path: Path) -> None:
    text = (CASES / "edith_marsh.yaml").read_text(encoding="utf-8")
    text = text.replace(
        "    description: Requests an urgent",
        "    requires: {spoke_to: [patient]}\n    description: Requests an urgent",
    )
    path = tmp_path / "edith_marsh.yaml"
    path.write_text(text, encoding="utf-8")
    [result] = validate_paths([path])
    assert (
        "rubric v2_urgent_care: requires spoke_to patient: not present at visit 2" in result.errors
    )
    assert Person.PATIENT.value == "patient"


def test_grade_command_refuses_a_run_of_another_case(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    run = tmp_path / "run.json"
    run.write_text(CaseLog(case_id="other", memory=Memory.NOTES).model_dump_json())
    assert main(["grade", str(CASES / "edith_marsh.yaml"), str(run)]) == 1
    assert "is a run of other, not edith_marsh" in capsys.readouterr().out


def test_grade_command_writes_a_scorecard_and_never_counts_a_failed_judge(
    edith: Case, tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    # Inspect's mock model replies with plain text, so every group fails to parse: the run is
    # written with items ungraded, and nothing is counted as met.
    run = tmp_path / "run.json"
    log = _case_log(edith, [_log(edith, 1, _visit1_events())])
    log.clinician = "openai/clin"
    run.write_text(log.model_dump_json())
    assert (
        main(["grade", str(CASES / "edith_marsh.yaml"), str(run), "--judge", "mockllm/model"]) == 0
    )
    out = capsys.readouterr().out
    assert "score n/a" in out and "not graded:" in out and "mockllm/model: 8 calls" in out
    report = GradeReport.model_validate_json((tmp_path / "run.grade.json").read_text())
    assert report.primary == "mockllm/model" and report.primary_lab == "other_lab"
    assert report.scores[0].score is None
    assert report.scores[0].visits[0].earned == 0
    assert "NOT GRADED" in (tmp_path / "run.grade.md").read_text()


# --- the live grader eval's offline parts ---------------------------------------------------


def test_grader_eval_variants_and_misses(edith: Case) -> None:
    from clinical_env.live_evals import ROOT, _variant, grade_misses

    spec = yaml.safe_load((ROOT / "evals" / "grader.yaml").read_text(encoding="utf-8"))
    log = CaseLog.model_validate_json((ROOT / spec["fixture"]).read_text(encoding="utf-8"))
    items = {i["name"]: i for i in spec["items"]}
    kept = _variant(log, items["furosemide_kept"]).visits[0].plan
    assert kept is not None
    assert [a.detail for a in kept.actions if "furosemide" in a.detail.lower()] == [
        "Continue furosemide 40 mg each morning as on the GP repeat list"
    ]
    padded = _variant(log, items["padding"]).visits[0].plan
    assert padded is not None and len(padded.actions) == 1
    assert log.visits[0].plan is not None and len(log.visits[0].plan.actions) > 1  # unchanged

    score = _grade(edith, _case_log(edith, [_log(edith, 1, _visit1_events())]), Judge())
    assert grade_misses(score, {"met": {"v1_reconcile_meds": True}}) == []
    [miss] = grade_misses(score, {"met": {"v1_reconcile_meds": False}, "no_penalties": ["x"]})
    assert miss.startswith("v1_reconcile_meds: expected False, got True")
    assert grade_misses(score, {"penalties": {"over_provision": 1}}) == [
        "expected at least 1 over_provision, got []"
    ]
