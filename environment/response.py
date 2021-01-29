from __future__ import annotations
from dataclasses import dataclass
from typing import Optional

from environment import state


@dataclass(frozen=True)
class Response:
    reward: Optional[float]
    state: state.State
