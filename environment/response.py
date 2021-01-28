from __future__ import annotations
from dataclasses import dataclass

from environment import state


@dataclass(frozen=True)
class Response:
    reward: float
    state: state.State
