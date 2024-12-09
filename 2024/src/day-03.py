#!/usr/bin/env python3

import argparse
import sys
import re

# Check correct usage
parser = argparse.ArgumentParser(description="Parse some data.")
parser.add_argument('input', metavar='input', type=str,
                    help='Input data file.')
args = parser.parse_args()

data = []
instr = []
instregex = r"mul\((\d{1,3})\,(\d{1,3})\)"
condregex = re.compile(r"(?:mul\((\d{1,3})\,(\d{1,3})\)|do\(\)|don\'t\(\))")

# Parse the input file
def parseInput(inp):
    try:
        input_fh = open(inp, 'r')
    except IOError:
        sys.exit("Unable to open input file: " + inp)

    for line in input_fh:
        data.append(line.rstrip())


# For each line of input, filter instructions
def processData():
    total = 0
    for line in data:
        matches = re.finditer(instregex, line)
        for x in matches:
            total += int(x[1]) * int(x[2])
    return total


# Re-process the input, including conditional statements
def processMore():
    capture = True
    total = 0
    for line in data:
        matches =  re.finditer(condregex, line)
        for x in matches:
            if x.lastindex == None:
                if x[0] == "do()":
                    capture = True
                else:
                    capture = False
            else:
                if capture:
                    total += int(x[1]) * int(x[2])
    return total


def main():
    parseInput(args.input)

    # Part 1
    print(f"Part 1: {processData()}")

    # Part 2
    print(f"Part 2: {processMore()}")


if __name__ == "__main__":
    main()
