#!/usr/bin/env python3

import argparse
import sys
import json

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
    while True:
        if len(left) == 0 and len(right) == 0:
            return None
        elif len(left) == 0:
            return True
        elif len(right) == 0:
            return False

        lcmp = left.pop(0)
        rcmp = right.pop(0)

        if type(lcmp) == int and type(rcmp) == int:
            if lcmp < rcmp:
                return True
            elif rcmp < lcmp:
                return False
        else:
            if type(lcmp) == int:
                lcmp = [lcmp]
            if type(rcmp) == int:
                rcmp = [rcmp]
            lookDeeper = comparePair(lcmp, rcmp)
            if lookDeeper is not None:
                return lookDeeper

        return True


# For each pass, identify its seat
def processData():
    index = 0
    correct = []

    while len(data) > 0:
        index += 1
        if comparePair(data.pop(0), data.pop(0)):
            correct.append(index)

    print(correct)


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
