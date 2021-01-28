from __future__ import annotations
from dataclasses import dataclass

import common


@dataclass(frozen=True)
class Action:
    # move before wind
    move: common.XY

    # @property
    # def index(self) -> tuple:
    #     # ax = ix - constants.MAX_ACCELERATION
    #     # ay = constants.MAX_ACCELERATION - iy
    #     ix = self.ax - constants.MIN_ACCELERATION
    #     iy = self.ay - constants.MIN_ACCELERATION
    #     return ix, iy

    # @staticmethod
    # def get_action_from_index(index: tuple) -> Action:
    #     ix, iy = index
    #     ax = ix + constants.MIN_ACCELERATION
    #     ay = iy + constants.MIN_ACCELERATION
    #     return Action(ax, ay)
