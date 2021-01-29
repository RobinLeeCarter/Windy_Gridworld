from __future__ import annotations

from dataclasses import dataclass

import common


@dataclass(frozen=True)
class Action:
    # move before wind
    move: common.XY

    @property
    def index(self) -> tuple[int]:
        return Actions.get_index_from_action(self)


class Actions:
    action_list = [
        # left
        Action(move=common.XY(-1, 0)),
        # right
        Action(move=common.XY(1, 0)),
        # up
        Action(move=common.XY(0, +1)),
        # down
        Action(move=common.XY(0, -1))
    ]
    shape = (len(action_list),)
    _action_to_index = {action_: i for i, action_ in enumerate(action_list)}

    @staticmethod
    def get_action_from_index(index: tuple[int]) -> Action:
        return Actions.action_list[index[0]]

    @staticmethod
    def get_index_from_action(action_: Action) -> tuple[int]:
        index = (Actions._action_to_index[action_], )
        return index
