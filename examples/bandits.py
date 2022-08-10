from importlib.metadata import distribution
import random
import numpy as np
from scipy.stats import beta

def main():
    print("bandits")

    # Initialise the gambling machines and the RL agent. 
    num_machines = 50
    machines = [GamblingMachine() for _ in range(num_machines)]
    agent = Agent(num_machines)

    print("{} machines to select from.".format(num_machines))

    # loop_human(machines)
    num_iterations = num_machines * 10
    loop_agent(machines, agent, num_iterations)

    best_payout = 0.0
    best_index = 0
    for i, machine in enumerate(machines):
        if machine.payout > best_payout:
            best_payout = machine.payout
            best_index = i

    print("Best machine is number {}, which pays out {}.".format(best_index+1, best_payout))
    print("The agent selected machine number {}".format(agent.best_machine()+1))
    print("Machines: ")
    for i, machine in enumerate(machines):
        print("    {}, payout = {}".format(i, machine.payout))

def loop_human(machines):
    if len(machines) < 1:
        return

    while True:

        action_is_valid = False
        while not action_is_valid:
            action = input("Select machine to play, from 1 to {}:".format(len(machines)))

            if action == 'q':
                return

            if int(action) > 0 and int(action) <= len(machines):
                action_is_valid = True
                action = int(action)
            else:
                print("Invalid input.")

        print("Gambled using machine {}.".format(action))
        bet = 1.0
        result = machines[action-1].gamble()
        print("Bet {}, received {}.".format(bet, result))

def loop_agent(machines, agent, num_iterations = 100):
    for _ in range(num_iterations):
        machine_inx = agent.action()
        success = bool(machines[machine_inx].gamble())
        agent.update(success, machine_inx)
        

class GamblingMachine:
    def __init__(self):
        self.payout = random.random()

    def gamble(self, amount=1.0):
        trial = random.random()
        if trial > (1 - self.payout):
            return amount * 2.0
        else:
            return 0.0

class BetaDistribution:
    def __init__(self):
        # alpha and beta are the shape parameters of the beta distribution .
        # Alph counts the sucesses. Beta counts the failures. 
        self.alpha = 1 
        self.beta = 1 

    def sample(self) -> float:
        return beta.rvs(self.alpha, self.beta) # Does this do what I think it does?


class Agent:
    """
    Agent uses thompson sampling to determine the best gambling machine.
    action : returns the index of the gambling machine to play. Samples the 
    beta distribution of the machines and takes the greedy result. 
    """
    def __init__(self, num_machines):
        self.information_state = [BetaDistribution() for _ in range(num_machines)]

    def action(self) -> int:
        samples = [machine.sample() for machine in self.information_state]
        max_index = samples.index(max(samples))
        return max_index

    def update(self, success: bool, selected_action: int):
        if success:
            self.information_state[selected_action].alpha += 1
        else:
            self.information_state[selected_action].beta += 1

    def best_machine(self):
        expected_returns = [beta.stats(machine.alpha, machine.beta, moments='m') \
            for machine in self.information_state]
        best_machine_inx = expected_returns.index(max(expected_returns))
        return best_machine_inx

if __name__ == "__main__":
    main()
