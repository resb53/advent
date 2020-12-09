#!/usr/bin/python3

import argparse
import sys
from itertools import combinations

# Check correct usage
parser = argparse.ArgumentParser(description="Check your Datastream.")
parser.add_argument('input', metavar='input', type=str,
                    help='Data input.')
args = parser.parse_args()

data = []


def main():
    parseInput(args.input)

    # Part 1
    print(findFirstError())

    # Part 2

    # Debug
    # printSeats()


# Parse the input file
def parseInput(inp):
    global data
    try:
        data_fh = open(inp, 'r')
    except IOError:
        sys.exit("Unable to open input file: " + inp)

    for line in data_fh:
        data.append(int(line.strip("\n")))


# For each pass, identify its seat
def findFirstError():
    # Step through windows of 25 numbers
    for i in range(25, len(data)):
        window = data[i-25:i]

        # Sum until finding a match
        combs = list(combinations(window, 2))
        match = False

        while match is False and len(combs) > 0:
            check = combs.pop(0)

            if sum(check) == data[i]:
                match = True

        if match is False:
            return data[i]



def printSeats():
    for item in data:
        print(item)


if __name__ == "__main__":
    main()
