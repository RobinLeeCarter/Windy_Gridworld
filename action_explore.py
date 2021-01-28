from __future__ import annotations
from dataclasses import dataclass

import common


@dataclass(frozen=True)
class Action:
    # move before wind
    move: common.XY

    @property
    def index(self) -> int:
        return Actions.get_index_from_action(self)

    # @staticmethod
    # def get_action_from_index(index: tuple) -> Action:
    #     ix, iy = index
    #     ax = ix + constants.MIN_ACCELERATION
    #     ay = iy + constants.MIN_ACCELERATION
    #     return Action(ax, ay)


class Actions:
    action_list = [
        # left
        Action(move=common.XY(x=-1, y=0)),
        # right
        Action(move=common.XY(x=+1, y=0)),
        # up
        Action(move=common.XY(x=0, y=+1)),
        # down
        Action(move=common.XY(x=0, y=-1))
    ]
    actions_shape = (len(action_list), )
    action_dict = {action_: i for i, action_ in enumerate(action_list)}
    _test_action = Action(common.XY(-1, 0))

    @staticmethod
    def get_action_from_index(index: int) -> Action:
        return Actions.action_list[index]

    @staticmethod
    def get_index_from_action(action_: Action) -> int:
        return Actions.action_dict[action_]


_test_action2 = Action(common.XY(+1, 0))
