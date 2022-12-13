#!/usr/bin/env python3

import argparse
import sys
import json
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

    for line in input_fh:
        line = line.strip("\n")
        if line:
            data.append(json.loads(line))


def comparePair(left, right):
    # print(f"Comparing {left} and {right}...")
    while True:
        if len(left) == 0 and len(right) == 0:
            # print("Nothing to separate, move on...")
            return None
        elif len(left) == 0:
            # print("Left empty")
            return True
        elif len(right) == 0:
            # print("Right empty")
            return False

        lcmp = left.pop(0)
        rcmp = right.pop(0)

        if type(lcmp) == int and type(rcmp) == int:
            if lcmp < rcmp:
                # print("Left < Right")
                return True
            elif rcmp < lcmp:
                # print("Right < Left")
                return False
        else:
            if type(lcmp) == int:
                lcmp = [lcmp]
            if type(rcmp) == int:
                rcmp = [rcmp]
            lookDeeper = comparePair(lcmp, rcmp)
            if lookDeeper is not None:
                return lookDeeper


# For each pass, identify its seat
def processData(input):
    index = 0
    correct = []

    while len(input) > 0:
        index += 1
        if comparePair(input.pop(0), input.pop(0)):
            correct.append(index)

    print(f"Part 1: {sum(correct)}")


# Process harder
def processMore(input):

    print(input)

    return False


def main():
    parseInput(args.input)

    # Part 1
    processData(copy.deepcopy(data))

    # Part 2
    processMore(copy.deepcopy(data))


if __name__ == "__main__":
    main()
