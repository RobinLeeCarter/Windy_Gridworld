import numpy as np

import environment
import policy


class EGreedyPolicy(policy.RandomPolicy):
    def __init__(self, environment_: environment.Environment, rng: np.random.Generator,
                 greedy_policy: policy.DeterministicPolicy, epsilon: float = 0.1):
        super().__init__(environment_, rng)
        self.greedy_policy: policy.DeterministicPolicy = greedy_policy
        self.epsilon = epsilon

    def set_greedy_action(self, state_: environment.State, action_: environment.Action):
        self.greedy_policy.set_action(state_, action_)

    def get_action_given_state(self, state_: environment.State) -> environment.Action:
        if self.rng.uniform() > self.epsilon:
            return self.greedy_policy.get_action_given_state(state_)
        else:
            return policy.RandomPolicy.get_action_given_state(self, state_)
            # policy.RandomPolicy.get_action_given_state(self, state_)
            # self.set_possible_actions(state_)
            # return self.rng.choice(self.possible_actions)

    def get_probability(self, state_: environment.State, action_: environment.Action) -> float:
        self.set_possible_actions(state_)
        non_greedy_p = self.epsilon * (1.0 / len(self.possible_actions))
        greedy_action = self.greedy_policy.get_action_given_state(state_)
        if action_ == greedy_action:
            greedy_p = (1 - self.epsilon) + non_greedy_p
            return greedy_p
        else:
            return non_greedy_p
