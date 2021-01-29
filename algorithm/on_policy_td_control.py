from typing import List

import numpy as np

import constants
import environment
import policy
import agent


class OnPolicyTdControl:
    def __init__(self,
                 environment_: environment.Environment,
                 agent_: agent.Agent,
                 gamma: float = 1.0,
                 alpha: float = 0.5,
                 verbose: bool = False
                 ):
        self.environment: environment.Environment = environment_
        self.agent: agent.Agent = agent_
        assert isinstance(self.agent.policy, policy.EGreedyPolicy),\
            "agent.policy not EGreedyPolicy"
        self.policy: policy.EGreedyPolicy = self.agent.policy
        self.gamma = gamma
        self.alpha = alpha
        self.verbose = verbose

        q_shape = self.environment.states_shape + self.environment.actions_shape
        self.Q: np.ndarray = np.zeros(shape=q_shape, dtype=float)
        self.initialise_q()
        self.initialise_policy()
        self.learning_iteration: int = 0

        # samples = int(constants.LEARNING_EPISODES / constants.PERFORMANCE_SAMPLE_FREQUENCY)
        # self.sample_iteration: np.ndarray = np.zeros(shape=samples+1, dtype=int)
        # self.average_return: np.ndarray = np.zeros(shape=samples+1, dtype=float)
        # self.average_return[0] = constants.INITIAL_Q_VALUE*2

    def initialise_q(self):
        # incompatible actions must never be selected
        self.Q.fill(np.NINF)
        # so that a successful trajectory is always better
        for state_ in self.environment.states():
            for action_ in self.environment.actions_for_state(state_):
                q_index = state_.index + action_.index
                if state_.is_terminal:
                    self.Q[q_index] = 0.0
                else:
                    self.Q[q_index] = constants.INITIAL_Q_VALUE

    def initialise_policy(self):
        for state_ in self.environment.states():
            target_action = self.consistent_argmax_q(state_)
            self.policy.set_greedy_action(state_, target_action)

    def consistent_argmax_q(self, state_: environment.State) -> environment.Action:
        """set target_policy to argmax over a of Q breaking ties consistently"""
        # state_index = self.get_index_from_state(state_)
        # print(f"state_index {state_index}")
        q_slice = state_.index + np.s_[:]
        q_state: np.ndarray = self.Q[q_slice]
        # print(f"q_state.shape {q_state.shape}")

        # argmax
        best_q: float = np.max(q_state)
        # print(f"best_q {best_q}")
        best_q_bool: np.ndarray = (q_state == best_q)
        # print(f"best_q_bool.shape {best_q_bool.shape}")
        best_flat_indexes: np.ndarray = np.flatnonzero(best_q_bool)
        consistent_best_flat_index: int = best_flat_indexes[0]
        # print(f"consistent_best_flat_index {consistent_best_flat_index}")
        unravelled_index: tuple[np.ndarray] = np.unravel_index(consistent_best_flat_index, shape=q_state.shape)
        # unravelled_index actually returns tuple[np.int64]
        assert np.isscalar(unravelled_index[0])
        best_index: tuple[int] = tuple([int(i) for i in unravelled_index])

        # unravelled_index: tuple = best_index_tuple_array[0][0]
        # print(f"unravelled_index {unravelled_index}")
        best_action = environment.Actions.get_action_from_index(best_index)
        # best_action = self.get_action_from_index(unravelled_index)
        # print(f"best_action {best_action}")
        return best_action

    # noinspection PyPep8Naming
    def run(self):
        self.learning_iteration: int = 0
        while self.learning_iteration <= constants.LEARNING_EPISODES:
            if self.verbose:
                print(f"iteration = {self.learning_iteration}")
            else:
                if self.learning_iteration % 10000 == 0:
                    print(f"iteration = {self.learning_iteration}")
            # if self.learning_iteration >= constants.PERFORMANCE_SAMPLE_START and \
            #         self.learning_iteration % constants.PERFORMANCE_SAMPLE_FREQUENCY == 0:
            #     self.sample_target()

            episode: agent.Episode = self.behaviour_agent.generate_episode()
            trajectory: List[agent.RSA] = episode.trajectory
            G: float = 0.0
            W: float = 1.0
            # reversed_non_terminated = reversed(trajectory_.episode[:-1])
            T: int = len(trajectory) - 1
            # print(f"T = {T}")
            for t in reversed(range(T)):
                # if t < T-1:
                #     print(f"t = {t}")
                R_t_plus_1 = trajectory[t+1].reward
                S_t = trajectory[t].state
                A_t = trajectory[t].action
                G = self.gamma * G + R_t_plus_1
                s_a = S_t.index + A_t.index
                # print(f"s_a = {s_a}")
                self.C[s_a] += W
                self.Q[s_a] += (W / self.C[s_a]) * (G - self.Q[s_a])
                target_action = self.consistent_argmax_q(S_t)
                self.target_policy.set_action(S_t, target_action)
                # print(f"S_t={S_t} -> new_a={target_action}")
                if A_t.index != target_action.index:
                    break
                W /= self.behaviour_agent.policy.get_probability(S_t, A_t)
            self.learning_iteration += 1

        # print(self.sample_iteration)
        # print(self.average_return)

    # noinspection PyPep8Naming
    # def sample_target(self):
    #     sample_number = int(self.learning_iteration / constants.PERFORMANCE_SAMPLE_FREQUENCY)
    #     # print(sample_number)
    #     sample_iteration: int = 1
    #     average_G: float = 0.0
    #     while sample_iteration <= constants.PERFORMANCE_SAMPLES:
    #         if self.verbose:
    #             print(f"sample_iteration = {sample_iteration}")
    #
    #         episode: agent.Episode = self.target_agent.generate_episode()
    #         G: float = 0.0
    #         for reward_state_action in reversed(episode.trajectory):
    #             if reward_state_action.reward is not None:
    #                 G = self.gamma * G + reward_state_action.reward
    #         average_G += (1/sample_iteration) * (G - average_G)
    #         sample_iteration += 1
    #     self.sample_iteration[sample_number] = self.learning_iteration
    #     self.average_return[sample_number] = average_G
