"""Model roles and the small generate interface the core depends on.

The core (simulators, checker, grader) only sees `Generate`: an async function from messages to
text. It never imports Inspect, so it can be wrapped for verifiers or Gymnasium later.
`inspect_layer.py` supplies the Inspect-backed implementation.
"""

from __future__ import annotations

from collections.abc import Callable, Coroutine, Sequence
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path
from typing import Any, Literal

import yaml
from pydantic import BaseModel, ConfigDict, Field, model_validator

DEFAULT_CONFIG = Path(__file__).resolve().parents[2] / "config" / "models.yaml"


class Role(StrEnum):
    CLINICIAN = "clinician"  # the model under test
    PATIENT = "patient"
    CARER = "carer"
    CHECKER = "checker"  # flags simulator drift
    GRADER = "grader"


@dataclass(frozen=True)
class Message:
    role: Literal["system", "user", "assistant"]
    content: str


Generate = Callable[[Sequence[Message]], Coroutine[Any, Any, str]]


class RoleModel(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    model: str = Field(pattern=r"^[\w.-]+/\S+$", description="Inspect model id, provider/name")
    reasoning_effort: Literal["none", "minimal", "low", "medium", "high", "xhigh", "max"] | None = (
        None
    )
    max_tokens: int | None = Field(default=None, gt=0)
    temperature: float | None = Field(default=None, ge=0)
    # Inspect retries forever by default; bound every call so a stuck provider cannot run up
    # time or cost unnoticed.
    max_retries: int = Field(default=5, ge=0)
    timeout: int = Field(default=600, gt=0, description="seconds per call, including retries")


class ModelConfig(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    roles: dict[Role, RoleModel]

    @model_validator(mode="after")
    def _every_role_assigned(self) -> ModelConfig:
        missing = [role.value for role in Role if role not in self.roles]
        if missing:
            raise ValueError(f"no model for role(s): {', '.join(missing)}")
        return self


def load_model_config(path: Path = DEFAULT_CONFIG) -> ModelConfig:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    return ModelConfig.model_validate(data)
