from collections.abc import Callable
import numpy as np

class Environment:
    """
    Returns a observation given an action.

    This is a bare-bones class. Programmer is responsible for defining the 
    state and the function that converts actions into observations given 
    the state. 
    """

    def __init__(self, initial_state, observation_from_actions : Callable[[np.array], np.array]):
        self.state = initial_state
        self.observation_from_action = observation_from_actions
        self.time = 0


