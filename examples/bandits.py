import random


def main():
    print("bandits")

    # Initialise the gambling machines
    num_machines = 3
    machines = [GamblingMachine() for i in range(num_machines)]
    print("{} machines to select from.".format(num_machines))

    loop(machines)

    best_payout = 0.0
    best_index = 0
    for i, machine in enumerate(machines):
        if machine.payout > best_payout:
            best_payout = machine.payout
            best_index = i

    print("Best machine is number {}, which pays out {}.".format(best_index+1, best_payout))

def loop(machines):
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
        

class GamblingMachine:
    def __init__(self):
        self.payout = random.random()

    def gamble(self, amount=1.0):
        trial = random.random()
        if trial > self.payout:
            return amount * 2.0
        else:
            return 0.0

if __name__ == "__main__":
    main()
