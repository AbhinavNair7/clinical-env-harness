"""Thin Inspect AI layer: turns the role config into Inspect models and `Generate` callables.

Every model call in the project goes through here, so the provider is chosen by config, and
Inspect records tokens, cost and the transcript for each call.
"""

from __future__ import annotations

from collections.abc import Sequence

from inspect_ai.model import (
    ChatMessage,
    ChatMessageAssistant,
    ChatMessageSystem,
    ChatMessageUser,
    GenerateConfig,
    Model,
    ModelUsage,
    get_model,
)

from clinical_env.roles import Generate, Message, ModelConfig, Role, RoleModel


def generate_config(spec: RoleModel) -> GenerateConfig:
    return GenerateConfig(
        reasoning_effort=spec.reasoning_effort,
        max_tokens=spec.max_tokens,
        temperature=spec.temperature,
        max_retries=spec.max_retries,
        timeout=spec.timeout,
    )


def role_models(config: ModelConfig) -> dict[str, Model]:
    """One Inspect model per role; also usable as `inspect_ai.eval(model_roles=...)`."""
    return {
        role.value: get_model(spec.model, config=generate_config(spec))
        for role, spec in config.roles.items()
    }


def to_inspect(message: Message) -> ChatMessage:
    if message.role == "system":
        return ChatMessageSystem(content=message.content)
    if message.role == "assistant":
        return ChatMessageAssistant(content=message.content)
    return ChatMessageUser(content=message.content)


def inspect_generate(model: Model, usage: list[ModelUsage] | None = None) -> Generate:
    """Wrap an Inspect model as the core's plain `Generate` callable. Outside an Inspect eval
    nothing records tokens, so a caller may pass `usage` to collect each call's usage."""

    async def generate(messages: Sequence[Message]) -> str:
        output = await model.generate([to_inspect(m) for m in messages])
        if usage is not None and output.usage is not None:
            usage.append(output.usage)
        return output.completion

    return generate


def role_generators(config: ModelConfig) -> dict[Role, Generate]:
    models = role_models(config)
    return {role: inspect_generate(models[role.value]) for role in config.roles}
