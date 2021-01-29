from typing import List

import numpy as np

import constants
import environment
import policy
import agent
from algorithm import state_action_function


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
        assert isinstance(self.agent.policy, policy.EGreedyPolicy), "agent.policy not EGreedyPolicy"
        self.policy: policy.EGreedyPolicy = self.agent.policy
        self.gamma = gamma
        self.alpha = alpha
        self.verbose = verbose

        self.Q = state_action_function.StateActionFunction(self.environment)
        self.initialise_policy()
        self.learning_iteration: int = 0

        # samples = int(constants.LEARNING_EPISODES / constants.PERFORMANCE_SAMPLE_FREQUENCY)
        # self.sample_iteration: np.ndarray = np.zeros(shape=samples+1, dtype=int)
        # self.average_return: np.ndarray = np.zeros(shape=samples+1, dtype=float)
        # self.average_return[0] = constants.INITIAL_Q_VALUE*2

    def initialise_policy(self):
        for state_ in self.environment.states():
            # self.policy[state_] = self.Q.state_argmax(state_)
            target_action = self.Q.state_argmax(state_)
            self.policy.set_greedy_action(state_, target_action)

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
