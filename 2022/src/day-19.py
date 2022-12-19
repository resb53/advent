#!/usr/bin/env python3

import argparse
import sys
import re
import copy

# Check correct usage
parser = argparse.ArgumentParser(description="Parse some data.")
parser.add_argument('input', metavar='input', type=str,
                    help='Input data file.')
args = parser.parse_args()

data = {}
types = ["O", "C", "B", "G"]


# Parse the input file
def parseInput(inp):
    try:
        input_fh = open(inp, 'r')
    except IOError:
        sys.exit("Unable to open input file: " + inp)

    robots = (
        r"^Blueprint (\d+): .+? (\d+) ore\. .+? (\d+) ore\. .+? (\d+) ore"
        r" and (\d+) clay. .+? (\d+) ore and (\d+) obsidian."
    )

    for line in input_fh:
        match = re.match(robots, line)
        if match is not None:
            data[int(match[1])] = [
                [int(match[2])],  # Ore (Ore)
                [int(match[3])],  # Clay (Ore)
                [int(match[4]), int(match[5])],  # Obsidian (Ore, Clay)
                [int(match[6]), int(match[7])]   # Geode (Ore, Obsidian)
            ]


class Factory():
    def __init__(self, past: str, target: int, res: list, bots: list, cost: list):
        self.history = past
        self.target = target
        self.resources = copy.copy(res)
        self.bots = copy.copy(bots)
        self.cost = cost

    def __str__(self):
        return str([self.history, self.target, self.resources, self.bots])

    def accumulate(self):
        for i in range(4):
            self.resources[i] += self.bots[i]

    def build(self):
        if self.target == 0:
            if self.resources[0] >= self.cost[self.target][0]:
                self.resources[0] -= self.cost[self.target][0]
                return self.target
        elif self.target == 1:
            if self.resources[0] >= self.cost[self.target][0]:
                self.resources[0] -= self.cost[self.target][0]
                return self.target
        elif self.target == 2:
            if self.resources[0] >= self.cost[self.target][0] and self.resources[1] >= self.cost[self.target][1]:
                self.resources[0] -= self.cost[self.target][0]
                self.resources[1] -= self.cost[self.target][1]
                return self.target
        elif self.target == 3:
            if self.resources[0] >= self.cost[self.target][0] and self.resources[2] >= self.cost[self.target][1]:
                self.resources[0] -= self.cost[self.target][0]
                self.resources[2] -= self.cost[self.target][1]
                return self.target
        return None

    def complete(self):
        if self.target is not None:
            self.bots[self.target] += 1
            self.history += types[self.target]
            self.target = None
        else:
            sys.exit("No target to complete...")


# Simulate 24 minutes of bot building geode harvesting fun
def preOrdained(bp):
    rounds = 24

    # Specify Build order
    buildOrder = [1, 1, 1, 2, 1, 2, 3, 3]

    # Run sim, BFS
    #                                       O  C  oB G    O  C  oB G
    state = Factory("", buildOrder.pop(0), [0, 0, 0, 0], [1, 0, 0, 0], bp)

    for _ in range(rounds):
        # Build next robot
        built = state.build()

        # Collect resources
        state.accumulate()

        # Complete builds
        if built is not None:
            state.complete()
            # Update current state with next bot
            if len(buildOrder) > 0:
                state.target = buildOrder.pop(0)

        print(state)

    return state.resources[3]


def simulateBots(bp):
    rounds = 24

    states = [        # O  C  oB G    O  C  oB G
        Factory("", 0, [0, 0, 0, 0], [1, 0, 0, 0], bp),
        Factory("", 1, [0, 0, 0, 0], [1, 0, 0, 0], bp),
    ]

    for _ in range(rounds):
        newstates = []

        for state in states:
            # Build next bot
            built = state.build()

            # Collect resources
            state.accumulate()

            # Complete builds
            if built is not None:
                state.complete()
                # Update current state with next bot
                constructs = chooseBot(state)
                if len(constructs) > 0:
                    state.target = constructs.pop(0)
                    for construct in constructs:
                        newstates.append(
                            Factory(state.history, construct, state.resources, state.bots, bp),
                        )
            # print(state.history)

        states.extend(newstates)

    return max([x.resources[3] for x in states])


def chooseBot(state: Factory):
    choices = []
    # Never more than 4 ore bots
    if state.bots[0] < 4:
        choices.append(0)
    # Clay Bots
    choices.append(1)
    # Obsidian Bots
    if state.bots[1] > 0:
        choices.append(2)
    if state.bots[2] > 0:
        choices.append(3)

    return choices


# For each blueprint, run the building program
def processData():
    results = {}
    for blueprint in data:
        results[blueprint] = simulateBots(data[blueprint])
        print(f"{blueprint}: {results[blueprint]}")

    print(f"Part 1: {sum([x * results[x] for x in results])}")


# Process harder
def processMore():
    return False


def main():
    parseInput(args.input)

    # Part 1
    processData()

    # Part 2
    processMore()


if __name__ == "__main__":
    main()
