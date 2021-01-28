from typing import Generator
import numpy as np

import common
from environment import action, response, state, grid


class Environment:
    def __init__(self, grid_: grid.Grid, rng: np.random.Generator, verbose: bool = False):
        self.rng: np.random.Generator = rng
        self.verbose: bool = verbose
        self.grid_world: grid.GridWorld = grid.GridWorld(grid_, rng)

        # position
        self.min_x: int = 0
        self.max_x: int = self.grid_world.grid.max_x
        self.min_y: int = 0
        self.max_y: int = self.grid_world.grid.max_y

        # # velocity
        # self.min_vx: int = 0
        # self.max_vx: int = constants.MAX_VELOCITY
        # self.min_vy: int = 0
        # self.max_vy: int = constants.MAX_VELOCITY
        #
        # # acceleration
        # self.min_ax: int = constants.MIN_ACCELERATION
        # self.max_ax: int = constants.MAX_ACCELERATION
        # self.min_ay: int = constants.MIN_ACCELERATION
        # self.max_ay: int = constants.MAX_ACCELERATION

        self.states_shape: tuple = (self.max_x + 1, self.max_y + 1)
        # self.actions_shape: tuple = (self.max_ax - self.min_ax + 1, self.max_ay - self.min_ay + 1)
        # self.trace_ = grid.Trace = grid.Trace(self.grid_world)

        # pre-reset state (if not None it means the state has just been reset and this was the failure state)
        # self.pre_reset_state: Optional[state.State] = None

    # region Sets
    def states(self) -> Generator[state.State, None, None]:
        """set S"""
        for x in range(self.states_shape[0]):
            for y in range(self.states_shape[1]):
                position = common.XY(x=x, y=y)
                is_terminal: bool = self.grid_world.is_at_goal(position)
                yield state.State(position, is_terminal)

    def actions(self) -> Generator[action.Action, None, None]:
        """set A - same for all s"""
        # left
        yield action.Action(move=common.XY(x=-1, y=0))
        # right
        yield action.Action(move=common.XY(x=+1, y=0))
        # up
        yield action.Action(move=common.XY(x=0, y=+1))
        # down
        yield action.Action(move=common.XY(x=0, y=-1))

        # for iy in range(self.actions_shape[0]):
        #     for ix in range(self.actions_shape[1]):
        #         yield action.Action.get_action_from_index((iy, ix))

    # def current_actions(self) -> Generator[action.Action, None, None]:
    #     yield from self.actions_for_state(self.state)

    # possible need to materialise this if it's slow since it will be at the bottom of the loop
    def actions_for_state(self, state_: state.State) -> Generator[action.Action, None, None]:
        """set A(s)"""
        for action_ in self.actions():
            # if self.is_action_compatible_with_state(state_, action_):
            yield action_

    # def is_action_compatible_with_state(self, state_: state.State, action_: action.Action):
    #     new_vx = state_.vx + action_.ax
    #     new_vy = state_.vy + action_.ay
    #     if self.min_vx <= new_vx <= self.max_vx and \
    #         self.min_vy <= new_vy <= self.max_vy and \
    #             not (new_vx == 0 and new_vy == 0):
    #         return True
    #     else:
    #         return False
    # endregion

    # region Operation
    def start(self) -> response.Response:
        state_ = self.get_a_start_state()
        # if self.verbose:
        #     self.trace_.start(state_)
        return response.Response(state=state_, reward=0.0)

    def get_a_start_state(self) -> state.State:
        position: common.XY = self.grid_world.get_a_start_position()
        return state.State(position)

    def apply_action_to_state(self, state_: state.State, action_: action.Action) -> response.Response:
        # if not self.is_action_compatible_with_state(state_, action_):
        #     raise Exception(f"apply_action_to_state state {state_} incompatible with action {action_}")

        wind: common.XY = self.grid_world.get_wind(state_.position)
        combined: common.XY = common.XY(
            x=action_.move.x + wind.x,
            y=action_.move.y + wind.y
        )
        blown_position: common.XY = common.XY(
            x=state_.position.x + combined.x,
            y=state_.position.y + combined.y
        )
        projected_position: common.XY = self._project_back_to_grid(blown_position)
        is_terminal: bool = self.grid_world.is_at_goal(projected_position)
        new_state: state.State = state.State(projected_position, is_terminal)
        reward: float = -1.0
        return response.Response(reward, new_state)

    def _project_back_to_grid(self, blown_position: common.XY) -> common.XY:
        x = blown_position.x
        y = blown_position.y
        if x < 0:
            x = 0
        if y < 0:
            y = 0
        if x > self.max_x:
            x = self.max_x
        if y > self.max_y:
            y = self.max_y
        return common.XY(x=x, y=y)
    # endregion
