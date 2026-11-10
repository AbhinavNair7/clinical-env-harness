"""Patient and carer simulators, interjection, and the checker (ResidencyRL section 3.2.2).

Each person sees only their persona, their own facts at this visit and the spoken conversation.
They never see the clinician's records, examinations, tool calls or the rubric. Every reply is
checked against the speaker's script; a flagged reply is regenerated once and every flag is kept.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from typing import Literal

from pydantic import BaseModel, ConfigDict, ValidationError, field_validator

from clinical_env import prompts
from clinical_env.case_schema import Case, Disclosure, Interjection, Person, Visit
from clinical_env.locale import UK, Locale, locale_of
from clinical_env.roles import Generate, Message
from clinical_env.views import describe, facts_at, persona

GP = "GP"  # the clinician's speaker id in logs; what people read follows the locale
FlagType = Literal["invented_fact", "hidden_revealed", "over_cooperative", "checker_error"]


@dataclass(frozen=True)
class Utterance:
    speaker: str  # "GP" or the person's name
    text: str
    to: str | None = None  # whom the GP addressed


class CheckFlag(BaseModel):
    model_config = ConfigDict(extra="ignore", frozen=True)

    type: FlagType
    detail: str
    fact: str | None = None  # the kept-back fact id, for hidden_revealed

    @field_validator("fact")
    @classmethod
    def _bare_id(cls, value: str | None) -> str | None:
        # Models often echo the script's "[id]" tag; keep the bare id.
        return value.strip().strip("[]").strip() if value else value


class _CheckerReply(BaseModel):
    model_config = ConfigDict(extra="ignore")

    flags: list[CheckFlag]


class Attempt(BaseModel):
    """One drafted reply and the checker's flags on it. `text` None means stayed silent."""

    model_config = ConfigDict(frozen=True)

    text: str | None
    flags: list[CheckFlag] = []


def render_conversation(lines: list[Utterance], clinician: str = UK.clinician) -> str:
    """The spoken conversation as people read it; `clinician` labels the clinician's lines."""
    if not lines:
        return "(the consultation is just starting)"
    rendered = []
    for line in lines:
        if line.speaker == GP and line.to:
            rendered.append(f"{clinician} (to {line.to}): {line.text}")
        elif line.speaker == GP:
            rendered.append(f"{clinician}: {line.text}")
        else:
            rendered.append(f"{line.speaker}: {line.text}")
    return "\n".join(rendered)


def parse_json_object(text: str) -> object:
    """Parse the first JSON object in a model reply (models sometimes wrap it in prose)."""
    match = re.search(r"\{.*\}", text, flags=re.DOTALL)
    if match is None:
        raise ValueError("no JSON object in reply")
    return json.loads(match.group())


class Checker:
    def __init__(self, generate: Generate, loc: Locale = UK) -> None:
        self._generate = generate
        self._loc = loc

    async def check(
        self,
        name: str,
        script: str,
        conversation: list[Utterance],
        reply: str,
        earlier: str = "",
    ) -> list[CheckFlag]:
        """`earlier` is the spoken record of earlier visits the speaker was at."""
        loc = self._loc
        turn = loc.text(prompts.CHECKER_TURN).format(
            name=name,
            facts=script,
            earlier=loc.text(prompts.CHECKER_MEMORY).format(visits=earlier) if earlier else "",
            conversation=render_conversation(conversation, loc.clinician),
            reply=reply,
        )
        raw = await self._generate(
            [Message("system", loc.text(prompts.CHECKER_SYSTEM)), Message("user", turn)]
        )
        try:
            return _CheckerReply.model_validate(parse_json_object(raw)).flags
        except (ValueError, ValidationError) as exc:
            # Logged, never silent; an unreadable check does not trigger a regenerate.
            return [CheckFlag(type="checker_error", detail=f"unreadable checker reply: {exc}")]


def _blocking(flags: list[CheckFlag]) -> list[CheckFlag]:
    return [flag for flag in flags if flag.type != "checker_error"]


def _is_silent(text: str) -> bool:
    return text.strip().strip(".").upper() == "SILENT" or not text.strip()


class PersonSimulator:
    def __init__(
        self,
        case: Case,
        person: Person,
        visit: Visit,
        generate: Generate,
        checker: Checker,
        memory: str = "",
    ) -> None:
        """`memory` is the spoken record of earlier visits this person was at (case_run.py)."""
        self.person = person
        self.memory = memory
        self.persona = persona(case, person)
        self.name = self.persona.name
        self._generate = generate
        self._checker = checker
        self._facts = facts_at(case, person.value, visit.number)
        self._present = ", ".join(describe(case, p) for p in visit.present)
        self._loc = locale_of(case)
        self._setting = self._loc.setting_text[visit.setting]
        # The checker sees fact ids so it can name a kept-back fact that slipped out.
        self.script = self._script(with_ids=True)
        self.system = self._system()

    def _script(self, *, with_ids: bool = False, without: frozenset[str] = frozenset()) -> str:
        lines = []
        for fact in self._facts:
            if fact.id in without:
                continue
            disclosure = fact.disclosure or Disclosure.IF_ASKED
            if disclosure == Disclosure.HIDDEN:
                how = self._loc.text(prompts.HIDDEN_TEXT).format(
                    condition=" ".join((fact.reveal_condition or "").split())
                )
            else:
                how = prompts.DISCLOSURE_TEXT[disclosure.value]
            tag = f"[{fact.id}] " if with_ids else ""
            lines.append(f"- {tag}{fact.statement.strip()} ({how})")
        return "\n".join(lines) or "- (nothing specific)"

    def _system(self, without: frozenset[str] = frozenset()) -> str:
        about = (
            ""
            if self.person == Person.PATIENT
            else f", the patient's {self.persona.relationship or 'carer'}"
        )
        loc = self._loc
        return loc.text(prompts.PERSON_SYSTEM).format(
            name=self.name,
            about=about,
            setting=self._setting,
            present=self._present,
            cognition=self.persona.cognition,
            health_literacy=self.persona.health_literacy,
            agenda=self.persona.agenda,
            speech_style=self.persona.speech_style,
            traits="".join(
                f"- Habit: {loc.text(prompts.TRAIT_TEXT[t.value])}\n" for t in self.persona.traits
            ),
            facts=self._script(without=without),
            memory=loc.text(prompts.PERSON_MEMORY).format(visits=self.memory)
            if self.memory
            else "",
        )

    async def reply(self, conversation: list[Utterance]) -> list[Attempt]:
        turn = self._loc.text(prompts.PERSON_TURN).format(
            conversation=render_conversation(conversation, self._loc.clinician), name=self.name
        )
        return await self._checked(turn, conversation, allow_silence=False)

    async def interject(self, conversation: list[Utterance], addressed: str) -> list[Attempt]:
        """One cheap call after someone else's reply; [] when the persona never interjects."""
        if self.persona.interjection == Interjection.NEVER:
            return []
        turn = self._loc.text(prompts.INTERJECT_TURN).format(
            conversation=render_conversation(conversation, self._loc.clinician),
            addressed=addressed,
            tendency=prompts.INTERJECT_TENDENCY[self.persona.interjection.value],
        )
        return await self._checked(turn, conversation, allow_silence=True)

    async def _draft(
        self, system: str, turn: str, conversation: list[Utterance], *, allow_silence: bool
    ) -> Attempt:
        text = (await self._generate([Message("system", system), Message("user", turn)])).strip()
        if allow_silence and _is_silent(text):
            return Attempt(text=None)
        flags = await self._checker.check(
            self.name, self.script, conversation, text, earlier=self.memory
        )
        return Attempt(text=text, flags=flags)

    async def _checked(
        self, turn: str, conversation: list[Utterance], *, allow_silence: bool
    ) -> list[Attempt]:
        """First draft; one rewrite on a flag; if a kept-back fact slipped out twice, a last
        draft with that fact taken out of the script, so the clinician never gets it free."""
        first = await self._draft(self.system, turn, conversation, allow_silence=allow_silence)
        blocking = _blocking(first.flags)
        if not blocking:
            return [first]
        reasons = "; ".join(f"{flag.type}: {flag.detail}" for flag in blocking)
        system = self.system + prompts.REGENERATE_NOTE.format(reason=reasons)
        second = await self._draft(system, turn, conversation, allow_silence=allow_silence)
        known = {fact.id for fact in self._facts}
        leaked = frozenset(
            flag.fact
            for flag in second.flags
            if flag.type == "hidden_revealed" and flag.fact in known
        )
        if not leaked:
            return [first, second]
        third = await self._draft(
            self._system(without=leaked), turn, conversation, allow_silence=allow_silence
        )
        return [first, second, third]
