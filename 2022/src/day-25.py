#!/usr/bin/env python3

import argparse
import sys

# Check correct usage
parser = argparse.ArgumentParser(description="Parse some data.")
parser.add_argument('input', metavar='input', type=str,
                    help='Input data file.')
args = parser.parse_args()

data = []
snafu = {
    "=": "-2",
    "-": "-1"
}


# Parse the input file
def parseInput(inp):
    try:
        input_fh = open(inp, 'r')
    except IOError:
        sys.exit("Unable to open input file: " + inp)

    for line in input_fh:
        data.append(line.strip("\n"))


# Convert snafu to decimal
def snafuToDec(value):
    parts = [int(snafu.get(x, x)) for x in value]
    mx = 1
    for i in range(len(parts) - 1, -1, -1):
        parts[i] *= mx
        mx *= 5
    return sum(parts)


# Convert decimal to snafu
def decToSnafu(value):
    parts = []
    if value == 0:
        parts.append("0")
    else:
        while value:
            value, rem = divmod(value, 5)
            parts.append(rem)

    # Carry over
    extra = None
    for i, x in enumerate(parts):
        if x > 2:
            if x == 3:
                parts[i] = "="
            elif x == 4:
                parts[i] = "-"
            elif x == 5:
                parts[i] = "0"
            if i == len(parts) - 1:
                extra = 1
            else:
                parts[i + 1] += 1
        else:
            parts[i] = str(x)
    if extra is not None:
        parts.append(str(extra))

    parts.reverse()

    return str.join("", parts)


# For each pass, convert from snafu and add up
def processData():
    total = 0

    for amount in data:
        total += snafuToDec(amount)

    print(f"Part 1: {decToSnafu(total)}")


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
