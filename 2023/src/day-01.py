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

firstDigit = r'^.*?(\d)'
lastDigit = r'^.*(\d)'


# Parse the input file
def parseInput(inp):
    try:
        input_fh = open(inp, 'r')
    except IOError:
        sys.exit("Unable to open input file: " + inp)

    for line in input_fh:
        data.append(line.strip("\n"))


# For each line, identify first and last digits
def processData():
    total = 0

    for line in data:
        value = ''

        if (getFirst := re.match(firstDigit, line)) is not None:
            value += getFirst.group(1)
        else:
            sys.exit(f"Error: firstDigit not found in {line}.")

        if (getLast := re.match(lastDigit, line)) is not None:
            value += getLast.group(1)
        else:
            sys.exit(f"Error: firstDigit not found in {line}.")

        # print(value)
        total += int(value)

    return total


# Replace text with digits then redo part 1
def processMore():
    total = 0

    for line in data:
        value = ''
        index = 0

        while len(value) == 0:
            if line[index] in "123456789":
                value += line[index]
            elif line[index:index+3] == "one":
                value += "1"
            elif line[index:index+3] == "two":
                value += "2"
            elif line[index:index+5] == "three":
                value += "3"
            elif line[index:index+4] == "four":
                value += "4"
            elif line[index:index+4] == "five":
                value += "5"
            elif line[index:index+3] == "six":
                value += "6"
            elif line[index:index+5] == "seven":
                value += "7"
            elif line[index:index+5] == "eight":
                value += "8"
            elif line[index:index+4] == "nine":
                value += "9"
            index += 1

        index = len(line)
        while len(value) == 1:
            if line[index-1] in "123456789":
                value += line[index-1]
            elif line[index-3:index] == "one":
                value += "1"
            elif line[index-3:index] == "two":
                value += "2"
            elif line[index-5:index] == "three":
                value += "3"
            elif line[index-4:index] == "four":
                value += "4"
            elif line[index-4:index] == "five":
                value += "5"
            elif line[index-3:index] == "six":
                value += "6"
            elif line[index-5:index] == "seven":
                value += "7"
            elif line[index-5:index] == "eight":
                value += "8"
            elif line[index-4:index] == "nine":
                value += "9"
            index -= 1

        total += int(value)

    return total


def main():
    parseInput(args.input)

    # Part 1
    print(f"Part 1: {processData()}")

    # Part 2
    print(f"Part 2: {processMore()}")


if __name__ == "__main__":
    main()
