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
        data.append(json.loads(line.strip("\n")))


# Work through snail numbers and add them together
def processData():
    result = data[0]
    for snumber in data[1:]:
        result = sadd(result, snumber)

    print(result)


# Add snail numbers
def sadd(left, right):
    return reduce([left, right])


def reduce(snumber):
    return snumber


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
