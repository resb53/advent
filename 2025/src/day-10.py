#!/usr/bin/env python3

import argparse
import sys
from copy import deepcopy

# Check correct usage
parser = argparse.ArgumentParser(description="Parse some data.")
parser.add_argument('input', metavar='input', type=str,
                    help='Input data file.')
args = parser.parse_args()

data = []


# Parse the input file
def parseInput(inp):
    try:
        input_fh = open(inp, 'r')
    except IOError:
        sys.exit("Unable to open input file: " + inp)

    for line in input_fh:
        chunks = line.rstrip().split()

        if chunks[0][0] != "[" or chunks[-1][0] != "{":
            sys.exit(f"Unexpected order on: {line}")

        target = chunks[0][1:-1].replace(".", "0").replace("#", "1")
        goal = int(target[::-1], 2)

        jolt = [int(x) for x in chunks[-1][1:-1].split(",")][::-1]

        switches = []

        for chunk in chunks[1:-1]:
            switch = 0
            for n in [int(x) for x in chunk[1:-1].split(",")]:
                switch += 2**n
            switches.append(switch)

        data.append([goal, switches, jolt])


# Update state for a button press
def pressSwitch(state, button):
    newstate = deepcopy(state)
    newstate[0] ^= button
    newstate[1].append(button)

    return newstate


# Find the machine initialisation procedures
def processData():
    presses = 0

    for machine in data:
        curStates = [[0, []]]
        fastestState = {0: []}

        while machine[0] not in fastestState:
            newStates = []
            for state in curStates:
                for switch in machine[1]:
                    newStates.append(pressSwitch(state, switch))

            curStates = []

            for state in newStates:
                if state[0] not in fastestState:
                    fastestState[state[0]] = state[1]
                    curStates.append(state)

        presses += len(fastestState[machine[0]])

    return presses


# Update joltage for a button press
def updateJoltage(state, button):
    newstate = deepcopy(state)
    for i, x in enumerate(f"{{0:0{len(state[0])}b}}".format(button)):
        newstate[0][i] += int(x)
    newstate[1].append(button)

    return newstate


# Process harder
def processMore():
    presses = 0

    for machine in data:
        curStates = [[[0] * len(machine[2]), []]]

        while len(curStates) > 0:
            newStates = []

            for state in curStates:
                for switch in machine[1]:
                    newState = updateJoltage(state, switch)

                    valid = True
                    for i, joltage in enumerate(newState[0]):
                        if joltage > machine[2][i]:
                            valid = False

                    if valid:
                        if newState[0] == machine[2]:
                            presses += len(newState[1])
                        else:
                            newStates.append(newState)

            curStates = newStates

    return presses


def main():
    parseInput(args.input)

    # Part 1
    print(f"Part 1: {processData()}")

    # Part 2
    print(f"Part 2: {processMore()}")


if __name__ == "__main__":
    main()
