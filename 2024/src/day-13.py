#!/usr/bin/env python3

import argparse
import sys
from sympy import Eq, solve, symbols, core

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

    parts = {}
    for line in input_fh:
        line = line.rstrip()
        if len(line) == 0:
            continue
        type, values = line.split(": ")
        values = values.split(", ")
        quot = []
        if type == "Button A":
            parts.clear()
            for q in values:
                quot.append(int(q.split("+")[1]))
            parts["A"] = quot
        elif type == "Button B":
            for q in values:
                quot.append(int(q.split("+")[1]))
            parts["B"] = quot
        elif type == "Prize":
            for q in values:
                quot.append(int(q.split("=")[1]))
            parts["Target"] = quot
            data.append(parts.copy())


# For each machine, identify cheapest solution
def processData():
    cost = 0
    for machine in data:
        x, y = symbols("x y")
        sim = solve([Eq(machine["A"][0] * x + machine["B"][0] * y, machine["Target"][0]),
                     Eq(machine["A"][1] * x + machine["B"][1] * y, machine["Target"][1])])
        if isinstance(sim[x], core.numbers.Integer) and isinstance(sim[y], core.numbers.Integer):
            cost += 3 * sim[x] + sim[y]
    return cost


# Process harder
def processMore():
    cost = 0
    for machine in data:
        x, y = symbols("x y")
        sim = solve([Eq(machine["A"][0] * x + machine["B"][0] * y, machine["Target"][0] + 10000000000000),
                     Eq(machine["A"][1] * x + machine["B"][1] * y, machine["Target"][1] + 10000000000000)])
        if isinstance(sim[x], core.numbers.Integer) and isinstance(sim[y], core.numbers.Integer):
            cost += 3 * sim[x] + sim[y]
    return cost


def main():
    parseInput(args.input)

    # Part 1
    print(f"Part 1: {processData()}")

    # Part 2
    print(f"Part 2: {processMore()}")


if __name__ == "__main__":
    main()
