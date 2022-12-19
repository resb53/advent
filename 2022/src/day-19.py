#!/usr/bin/env python3

import argparse
import sys
import re

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
            data[match[1]] = [
                [int(match[2])],  # Ore (Ore)
                [int(match[3])],  # Clay (Ore)
                [int(match[4]), int(match[5])],  # Obsidian (Ore, Clay)
                [int(match[6]), int(match[7])]   # Geode (Ore, Obsidian)
            ]


class Factory():
    def __init__(self, past: str, target: int, res: list, bots: list, cost: list):
        self.history = past
        self.target = target
        self.resources = res
        self.bots = bots
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
        else:
            sys.exit("No target to build...")
        return None

    def complete(self):
        if self.target is not None:
            self.bots[self.target] += 1
            self.history += types[self.target]
            self.target = None
        else:
            sys.exit("No target to complete...")


# Simulate 24 minutes of bot building geode harvesting fun
def simulateBots(bp):
    rounds = 24

    # Run sim, BFS
    states = {                               # O  C  oB G            O  C  oB G
        Factory("", 0, [0, 0, 0, 0], [1, 0, 0, 0], bp)
    }
    for _ in range(rounds):
        for state in states:
            # Build next robot
            built = state.build()

            # Collect resources
            state.accumulate()

            # Complete builds
            if built is not None:
                state.complete()
                # Update current state with new Ore Bot
                state.target = 0
                # Create new states for relevant other targets

            print(state)


# For each blueprint, run the building program
def processData():
    for blueprint in data:
        simulateBots(data[blueprint])


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
