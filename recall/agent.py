import numpy as np

from environment import Environment

class Agent:
    """
    An agent's goal is to maximise the culumative reward by selecting an action
    at each time step. The action is selected based on a policy, which is 
    the learned based on the reward given the history of actions and rewards.

    An agent can have multiple actions (outputs). Each action is a scalar.
    """
    def __init__(self, num_actions):
        self.cumulative_reward = 0.0 
        self.num_actions = num_actions
        # does this need to be callable? should it be a set of weights / distributions? Selected action also needs to depend on the environment
        self.policy = 0.0
        self.time = 0

    def get_action(self, environment: Environment) -> np.array:
        return np.zeros(1)

    def get_reward(self, observation: np.array) -> float:
        return 0.0

    def accumulate(self, reward: float):
        self.cumulative_reward += reward