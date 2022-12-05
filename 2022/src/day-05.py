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

data = []
crates = [[] for _ in range(9)]


# Parse the input file
def parseInput(inp):
    try:
        input_fh = open(inp, 'r')
    except IOError:
        sys.exit("Unable to open input file: " + inp)

    setup = []
    for _ in range(10):
        setup.append(input_fh.readline())

    for i in range(7, -1, -1):
        match = re.match(r"^(.{3}) (.{3}) (.{3}) (.{3}) (.{3}) (.{3}) (.{3}) (.{3}) (.{3})$", setup[i])

        if match is not None:
            for j in range(1, 10):
                if match[j] != "   ":
                    crates[j-1].append(match[j][1])

    for line in input_fh:
        match = re.match(r"^move (\d+) from (\d+) to (\d+)", line)

        if match is not None:
            data.append({
                "move": int(match[1]),
                "from": int(match[2]),
                "to": int(match[3])
            })


# Process crate instructions
def processData(cratelist):
    for instr in data:
        for _ in range(instr["move"]):
            cratelist[instr["to"] - 1].append(cratelist[instr["from"] - 1].pop())

    print("Part 1: ")
    for stack in cratelist:
        print(stack[-1], end="")
    print("")


# Process harder
def processMore(cratelist):
    for instr in data:
        cratelist[instr["to"] - 1].extend(cratelist[instr["from"] - 1][-1 * instr["move"]:])
        cratelist[instr["from"] - 1] = cratelist[instr["from"] - 1][:-1 * instr["move"]]

    print("Part 2: ")
    for stack in cratelist:
        print(stack[-1], end="")
    print("")


def main():
    parseInput(args.input)

    # Part 1
    processData(copy.deepcopy(crates))

    # Part 2
    processMore(copy.deepcopy(crates))


if __name__ == "__main__":
    main()
