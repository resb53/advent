#!/usr/bin/env python3

import argparse
import sys

# Check correct usage
parser = argparse.ArgumentParser(description="Parse some data.")
parser.add_argument('input', metavar='input', type=str,
                    help='Input data file.')
args = parser.parse_args()

data = []
bincount = []


# Parse the input file
def parseInput(inp):
    try:
        input_fh = open(inp, 'r')
    except IOError:
        sys.exit("Unable to open input file: " + inp)

    for line in input_fh:
        data.append(line.strip("\n"))


# For each pass, identify its seat
def processData():
    # Prepare bincount array
    for _ in range(len(data[0])):
        bincount.append({'0': 0, '1': 0})

    for element in data:
        for i, bit in enumerate(element):
            bincount[i][bit] += 1

    gamma = ''
    epsilon = ''

    for count in bincount:
        if count['0'] > count['1']:
            gamma += '0'
            epsilon += '1'
        else:
            gamma += '1'
            epsilon += '0'

    gamma = int(gamma, 2)
    epsilon = int(epsilon, 2)

    print(f"Gamma: {gamma}, Epsilon {epsilon}")
    print(f"Solution 1: {gamma * epsilon}")


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
