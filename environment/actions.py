from environment import action

import common


class Actions:
    action_list = [
        # left
        action.Action(move=common.XY(x=-1, y=0)),
        # right
        action.Action(move=common.XY(x=+1, y=0)),
        # up
        action.Action(move=common.XY(x=0, y=+1)),
        # down
        action.Action(move=common.XY(x=0, y=-1))
    ]
    actions_shape = (len(action_list), )
    action_dict = {action_: i for i, action_ in enumerate(action_list)}

    @staticmethod
    def get_action_from_index(index: int) -> action.Action:
        return Actions.action_list[index]

    @staticmethod
    def get_index_from_action(action_: action.Action) -> int:
        return Actions.action_dict[action_]
