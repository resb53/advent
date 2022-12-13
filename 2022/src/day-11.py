#!/usr/bin/env python3

import argparse
import sys
import math
from collections import defaultdict
import copy

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

    monkey = {}

    for line in input_fh:
        line = line.strip("\n")

        if line.startswith("Monkey"):
            if len(monkey) != 0:
                data.append(monkey)
            monkey = {}

        if line.startswith("  Starting items"):
            monkey["items"] = [int(x) for x in line.split(": ")[1].split(", ")]

        if line.startswith("  Operation"):
            parts = line.split(" ")
            monkey["op"] = (parts[6], parts[7])

        if line.startswith("  Test"):
            monkey["test"] = int(line.split(" ")[5])

        if line.startswith("    If true"):
            monkey["true"] = int(line.split(" ")[9])

        if line.startswith("    If false"):
            monkey["false"] = int(line.split(" ")[9])

    data.append(monkey)

    return math.prod([x["test"] for x in data])


def throwAround(monkeys, activity, div=True, magic=0):
    for i, monkey in enumerate(monkeys):
        for item in monkey["items"]:
            # Calculate new worry
            if monkey["op"][0] == "+":
                item += int(monkey["op"][1])
            elif monkey["op"][1] == "old":
                item *= item
            else:
                item *= int(monkey["op"][1])
            # Part 1
            if div:
                # Bored of item
                item = math.floor(item / 3)
                # Throw item
                if item % monkey["test"] == 0:
                    monkeys[monkey["true"]]["items"].append(item)
                else:
                    monkeys[monkey["false"]]["items"].append(item)
            # Part 2
            else:
                # Throw item
                if item % monkey["test"] == 0:
                    monkeys[monkey["true"]]["items"].append(item % magic)
                else:
                    monkeys[monkey["false"]]["items"].append(item % magic)
            # Record throw
            activity[i] += 1
        # All items thrown
        monkey["items"] = []


# For each pass, identify its seat
def processData(monkeys):
    round = 1
    activity = defaultdict(int)

    while round <= 20:
        throwAround(monkeys, activity)
        round += 1

    orderedact = sorted(activity.items(), key=lambda x: x[1])
    print(f"Part 1: {orderedact[-1][1] * orderedact[-2][1]}")


# Process harder
def processMore(monkeys, magic):
    round = 1
    activity = defaultdict(int)

    while round <= 10000:
        throwAround(monkeys, activity, div=False, magic=magic)
        round += 1

    orderedact = sorted(activity.items(), key=lambda x: x[1])
    print(f"Part 2: {orderedact[-1][1] * orderedact[-2][1]}")


def main():
    magic = parseInput(args.input)

    # Part 1
    processData(copy.deepcopy(data))

    # Part 2
    processMore(copy.deepcopy(data), magic)


if __name__ == "__main__":
    main()
