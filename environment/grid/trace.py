from typing import Optional

import numpy as np

import common
from environment.grid import grid_world
import environment


class Trace:
    def __init__(self, grid_world_: grid_world.GridWorld):
        self.grid_world: grid_world.GridWorld = grid_world_
        self.trace: Optional[np.ndarray] = None

    def start(self, state_: environment.State):
        # self.trace = self.grid_world.track.copy()
        self.mark(state_)

    def mark(self, state_: environment.State):
        pass
        # iy, ix = self.grid_world.get_index(state_.x, state_.y)
        # self.trace[iy, ix] = enums.Square.CAR

    def output(self):
        print(self.trace)
