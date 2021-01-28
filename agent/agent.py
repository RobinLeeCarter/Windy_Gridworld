from typing import Optional

import environment
import policy
from agent import episode, rsa, sarsa


class Agent:
    def __init__(self, environment_: environment.Environment, policy_: policy.Policy, verbose: bool = False):
        self.environment: environment.Environment = environment_
        self.policy: policy.Policy = policy_
        self.verbose: bool = verbose
        self.episode: Optional[episode.Episode] = None

        self.previous_rsa: Optional[rsa.RSA] = None
        self.state: Optional[environment.State] = None
        self.action: Optional[environment.Action] = None
        self.reward: Optional[float] = None
        self.response: Optional[environment.Response] = None

    def set_policy(self, policy_: policy.Policy):
        self.policy = policy_

    def start_episode(self):
        if self.verbose:
            print("start episode...")
        self.episode = episode.Episode()
        self.previous_rsa = None
        # start
        self.response = self.environment.start()
        self._update_from_response()
        self._add_episode_rsa()

    def take_step(self):
        #  state and action already set
        if self.state.is_terminal:
            raise Exception("Trying to act in terminal state.")
        self.response = self.environment.apply_action_to_state(self.state, self.action)
        self._update_from_response()
        self.previous_rsa = self.episode.rsa
        self._add_episode_rsa()

    def get_sarsa(self) -> sarsa.SARSA:
        if self.previous_rsa is None:
            raise Exception("Trying to get_sarsa with no previous_rsa.")
        sarsa_ = sarsa.SARSA(
            state=self.previous_rsa.state,
            action=self.previous_rsa.action,
            reward=self.previous_rsa.reward,
            next_state=self.state,
            next_action=self.action
        )
        return sarsa_

    def _add_episode_rsa(self):
        self.episode.set_rsa(reward=self.reward, state=self.state, action=self.action)
        self.episode.add_rsa()

    def _update_from_response(self):
        self.reward = self.response.reward
        self.state = self.response.state
        if self.state.is_terminal:
            self.action = None
        else:
            self.action = self.policy.get_action_given_state(self.state)
        if self.verbose:
            print("start episode:")
            print(f"state = {self.state} \t action = {self.action}")

    def generate_episode(self) -> episode.Episode:
        episode_: episode.Episode = episode.Episode()
        # start
        response = self.environment.start()
        self.state = response.state

        while not self.state.is_terminal:
            self.action = self.policy.get_action_given_state(self.state)
            if self.verbose:
                print(f"state = {self.state} \t action = {self.action}")
            self.response = self.environment.apply_action_to_state(self.state, self.action)
            episode_.add_monte_carlo_style(self.state, self.action, self.response.reward)
            self.state = self.response.state
        episode_.add_terminal(self.state)

        return episode_
