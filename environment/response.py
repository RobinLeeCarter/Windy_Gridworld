from __future__ import annotations
from dataclasses import dataclass

from environment import state


@dataclass
class Response:
    reward: float
    state: state.State
