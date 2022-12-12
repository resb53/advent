#!/usr/bin/env python3

import argparse
import sys
import math
from collections import defaultdict

# Check correct usage
parser = argparse.ArgumentParser(description="Parse some data.")
parser.add_argument('input', metavar='input', type=str,
                    help='Input data file.')
args = parser.parse_args()

monkeys = []
activity = defaultdict(int)


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
                monkeys.append(monkey)
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

    monkeys.append(monkey)


def throwAround(div):
    for i, monkey in enumerate(monkeys):
        for item in monkey["items"]:
            # Calculate new worry
            if monkey["op"][0] == "+":
                item += int(monkey["op"][1])
            elif monkey["op"][1] == "old":
                item *= item
            else:
                item *= int(monkey["op"][1])
            # Bored of item
            if div:
                item = math.floor(item / 3)
            # Throw item
            # Store only the result of the modulus: x * y % n = (x % n) * y % n
            if item % monkey["test"] == 0:
                monkeys[monkey["true"]]["items"].append(item % monkey["test"])
            else:
                monkeys[monkey["false"]]["items"].append(item % monkey["test"])
            # Record throw
            activity[i] += 1
        # All items thrown
        monkey["items"] = []


# For each pass, identify its seat
def processData():
    round = 1

    while round <= 20:
        throwAround(True)
        # print(f"After round {round}:")
        # for i, monkey in enumerate(monkeys):
        #     print(f'Monkey {id}: {monkey["items"]}')
        round += 1

    orderedact = sorted(activity.items(), key=lambda x: x[1])
    print(f"Part 1: {orderedact[-1][1] * orderedact[-2][1]}")


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
