from __future__ import annotations
from dataclasses import dataclass

import common


@dataclass(frozen=True)
class Action:
    # move before wind
    move: common.XY

    @property
    def index(self) -> int:
        from environment import actions
        return actions.Actions.get_index_from_action(self)

    # @staticmethod
    # def get_action_from_index(index: tuple) -> Action:
    #     ix, iy = index
    #     ax = ix + constants.MIN_ACCELERATION
    #     ay = iy + constants.MIN_ACCELERATION
    #     return Action(ax, ay)
