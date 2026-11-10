"""Shared fixtures: the Edith Marsh case and fake models that never call a provider."""

from __future__ import annotations

import json
from collections.abc import Callable, Sequence
from pathlib import Path

import pytest

from clinical_env import prompts
from clinical_env.case_schema import Case
from clinical_env.roles import Message
from clinical_env.validate import load_case

CASES = Path(__file__).resolve().parents[1] / "cases" / "dev"


@pytest.fixture(scope="session")
def edith() -> Case:
    return load_case(CASES / "edith_marsh.yaml")


class FakeModel:
    """A scripted `Generate`: `reply` maps (system, last user message) to the text returned."""

    def __init__(self, reply: Callable[[str, str], str]) -> None:
        self._reply = reply
        self.calls: list[list[Message]] = []

    async def __call__(self, messages: Sequence[Message]) -> str:
        self.calls.append(list(messages))
        return self._reply(messages[0].content, messages[-1].content)


def checker_reply(
    flag_text: str | None = None, exam: dict[str, object] | None = None
) -> Callable[[str, str], str]:
    """Checker and examiner in one: flags replies containing `flag_text`; `exam` answers maps."""

    def reply(system: str, user: str) -> str:
        if system == prompts.EXAMINER_SYSTEM:
            return json.dumps(exam if exam is not None else {"ids": []})
        draft = user.rsplit("Reply to check:\n", 1)[-1]
        if flag_text and flag_text in draft:
            return json.dumps({"flags": [{"type": "invented_fact", "detail": "made up a fall"}]})
        return json.dumps({"flags": []})

    return reply
