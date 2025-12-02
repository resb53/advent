#!/usr/bin/env python3

import argparse
import sys

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
        line = line.rstrip()
        for rng in line.split(","):
            data.append(rng.split("-"))


# Check for a pattern indicating an invalid code
def checkInvalid(x):
    a, b = x[:len(x)//2], x[len(x)//2:]

    if a == b:
        return int(x)
    else:
        return 0


# Generator divisors of the length of code
def generateDivisors(n):
    for i in range(1, int(n**0.5) + 1):
        if n % i == 0:
            yield i
            if i != n // i:
                yield n // i


# Check for a pattern indicating a more complex invalid code
def checkComplex(x):
    for d in generateDivisors(len(x)):
        if d != len(x):
            units = [x[i:i+d] for i in range(0, len(x), d)]
            # Compare all other units with the first
            matches = True
            for chk in units[1:]:
                if chk != units[0]:
                    matches = False
                    break
            if matches:
                return int(x)

    return 0


# For each range find invalid codes
def processData():
    sum_invalids = 0

    for rng in data:
        for x in range(int(rng[0]), int(rng[1])+1):
            x = str(x)
            if len(x) % 2 != 1:
                sum_invalids += checkInvalid(x)

    return sum_invalids


# For each range find complex codes
def processMore():
    sum_complex = 0

    for rng in data:
        for x in range(int(rng[0]), int(rng[1])+1):
            sum_complex += checkComplex(str(x))

    return sum_complex


def main():
    parseInput(args.input)

    # Part 1
    print(f"Part 1: {processData()}")

    # Part 2
    print(f"Part 2: {processMore()}")


if __name__ == "__main__":
    main()
