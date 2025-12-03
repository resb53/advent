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
        data.append([int(x) for x in line.rstrip()])


# Find highest pairing of batteries without changing order
def pairBatteries(batteries: list, n: int) -> int:
    if n in batteries:
        # Leftmost pos of n:
        pos = batteries.index(n)
        if pos < len(batteries) - 1:
            two = max(batteries[pos+1:])
            return int(str(n) + str(two))

    return None


# Find highest value for n batteries
def nBatteries(batteries: list, n: int, val: str):
    if n > 0:
        end = len(batteries)
        if n > 1:
            end = -1*(n-1)
        target = batteries[0:end]
        m = max(target)
        val += str(m)
        pos = batteries.index(m)
        newBatteries = batteries[pos+1:]

        return nBatteries(newBatteries, n-1, val)

    else:
        return int(val)


# Turn on exactly 2 batteries, maximise joltage
def processData():
    joltage = 0
    for row in data:
        # Look for 9s, find highest to the right
        n = 9
        while n >= 0:
            check = pairBatteries(row, n)
            if check is not None:
                joltage += check
                break
            else:
                n -= 1

    return joltage


# Process for 12 batteries per row
def processMore():
    joltage = 0
    for row in data:
        joltage += nBatteries(row, 12, "")

    return joltage


def main():
    parseInput(args.input)

    # Part 1
    print(f"Part 1: {processData()}")

    # Part 2
    print(f"Part 2: {processMore()}")


if __name__ == "__main__":
    main()
