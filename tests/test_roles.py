"""Model roles: config loading and the Inspect-backed generate layer, using Inspect's mock model."""

from __future__ import annotations

import asyncio
from pathlib import Path

import pytest
from inspect_ai.model import ChatMessage, GenerateConfig, ModelOutput, get_model
from inspect_ai.tool import ToolChoice, ToolInfo
from pydantic import ValidationError

from clinical_env.inspect_layer import generate_config, inspect_generate, role_models
from clinical_env.roles import DEFAULT_CONFIG, Message, ModelConfig, Role, load_model_config

MOCK = "mockllm/model"


def test_repo_config_assigns_every_role() -> None:
    config = load_model_config(DEFAULT_CONFIG)
    assert set(config.roles) == set(Role)
    # Development runs on OpenAI only until the pilot (DECISIONS.md, staged keys).
    assert all(spec.model.startswith("openai/") for spec in config.roles.values())


def test_missing_role_is_rejected(tmp_path: Path) -> None:
    path = tmp_path / "models.yaml"
    path.write_text(
        "roles:\n"
        "  clinician: {model: openai/a}\n"
        "  patient: {model: openai/b}\n"
        "  carer: {model: openai/b}\n"
        "  checker: {model: openai/b}\n"
    )
    with pytest.raises(ValidationError, match="no model for role\\(s\\): grader"):
        load_model_config(path)


@pytest.mark.parametrize(
    "spec",
    [
        {"model": "gpt-6-luna"},  # no provider prefix
        {"model": "openai/x", "reasoning_effort": "extreme"},
        {"model": "openai/x", "temperture": 0.2},
        {"model": "openai/x", "max_tokens": 0},
    ],
)
def test_bad_role_spec_is_rejected(spec: dict[str, object]) -> None:
    roles: dict[str, dict[str, object]] = {role.value: {"model": "openai/x"} for role in Role}
    roles["patient"] = spec
    with pytest.raises(ValidationError):
        ModelConfig.model_validate({"roles": roles})


def test_role_settings_become_generate_config() -> None:
    config = ModelConfig.model_validate(
        {
            "roles": {
                role.value: {"model": MOCK, "reasoning_effort": "low", "max_tokens": 300}
                for role in Role
            }
        }
    )
    models = role_models(config)
    assert set(models) == {role.value for role in Role}
    spec = config.roles[Role.PATIENT]
    generated = generate_config(spec)
    assert (generated.reasoning_effort, generated.max_tokens, generated.temperature) == (
        "low",
        300,
        None,
    )
    assert models["patient"].config.reasoning_effort == "low"
    # Retries are always bounded (Inspect otherwise retries forever).
    assert (generated.max_retries, generated.timeout) == (5, 600)


def test_inspect_generate_sends_messages_and_returns_text() -> None:
    seen: list[list[ChatMessage]] = []

    def reply(
        messages: list[ChatMessage],
        tools: list[ToolInfo],
        tool_choice: ToolChoice,
        config: GenerateConfig,
    ) -> ModelOutput:
        seen.append(messages)
        return ModelOutput.from_content(model=MOCK, content="Oh I'm fine, love.")

    model = get_model(MOCK, custom_outputs=reply, memoize=False)
    generate = inspect_generate(model)
    text = asyncio.run(
        generate(
            [
                Message("system", "You are Edith."),
                Message("assistant", "Hello Edith."),
                Message("user", "How are you?"),
            ]
        )
    )
    assert text == "Oh I'm fine, love."
    [sent] = seen
    assert [(m.role, m.text) for m in sent] == [
        ("system", "You are Edith."),
        ("assistant", "Hello Edith."),
        ("user", "How are you?"),
    ]
