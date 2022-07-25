from agent import Agent
from environment import Environment

def learn(agent: Agent, environment: Environment, max_time_steps: int) -> Agent:
    """
    Update the agent policy to maximise the cumulative reward. Break when after
    reaching the maximum time steps, or after reaching some stopping criteria.
    """

    t = 0
    for t in range(t):
        action = agent.action(environment)
        observation = environment.observation_from_action(action)
        reward = agent.reward(observation)
        agent.accumulate(reward)

    return agent