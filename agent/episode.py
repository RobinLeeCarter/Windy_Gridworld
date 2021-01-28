from typing import List, Optional

import environment
from agent import rsa


class Episode:
    """Just makes a record laid out in the standard way with Reward, State, Action for each t"""
    def __init__(self):
        self.trajectory: List[rsa.RSA] = []
        self.rsa: rsa.RSA = rsa.RSA(None, None, None)
        self.previous_reward: Optional[float] = None

    def set_rsa(self,
                reward: Optional[float],
                state: Optional[environment.State],
                action: Optional[environment.Action]):
        self.rsa.reward = reward
        self.rsa.state = state
        self.rsa.action = action

    def add_rsa(self):
        # S0, A0, R1, S1, A1, R2 ... S(T-1), A(T-1), R(T)
        self.trajectory.append(self.rsa)

    def add_monte_carlo_style(self, state: environment.State, action: environment.Action, reward: float):
        # S0, A0, R1, S1, A1, R2 ... S(T-1), A(T-1), R(T)
        rsa_ = rsa.RSA(self.previous_reward, state, action)
        self.trajectory.append(rsa_)
        self.previous_reward = reward

    def add_terminal(self, state: environment.State):
        rsa_ = rsa.RSA(self.previous_reward, state, None)
        self.trajectory.append(rsa_)
