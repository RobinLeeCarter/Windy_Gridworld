import numpy as np

import common
from environment.grid import grid


class GridWorld:
    def __init__(self, grid_: grid.Grid, rng: np.random.Generator):
        self.grid: grid.Grid = grid_
        self.rng: np.random.Generator = rng

    def get_a_start_position(self) -> common.XY:
        return self.grid.start

    def is_at_goal(self, grid_position: common.XY) -> bool:
        return grid_position == self.grid.goal

    # noinspection PyUnusedLocal
    def get_wind(self, x: int, y: int) -> common.XY:
        return common.XY(x=0, y=self.grid.upward_wind[x])
