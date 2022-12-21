#!/usr/bin/env python3

import argparse
import sys

# Check correct usage
parser = argparse.ArgumentParser(description="Parse some data.")
parser.add_argument('input', metavar='input', type=str,
                    help='Input data file.')
args = parser.parse_args()

data = {}


# Parse the input file
def parseInput(inp):
    try:
        input_fh = open(inp, 'r')
    except IOError:
        sys.exit("Unable to open input file: " + inp)

    for line in input_fh:
        line = line.strip("\n")
        name = line[0:4]
        op = line[6:].split(" ")
        if len(op) == 1:
            data[name] = int(op[0])
        else:
            data[name] = op


# What does the monkey say?
def getAnswer(name, part):
    if name in data:
        if type(data[name]) == int:
            return data[name]
        else:
            lhs = getAnswer(data[name][0], part)
            rhs = getAnswer(data[name][2], part)

            if name == "root" and part == 2:
                return (lhs < rhs, lhs > rhs)
            if data[name][1] == "+":
                return lhs + rhs
            elif data[name][1] == "-":
                return lhs - rhs
            elif data[name][1] == "*":
                return lhs * rhs
            elif data[name][1] == "/":
                return int(lhs / rhs)


# For each pass, identify its seat
def processData():
    print(f'Part 1: {getAnswer("root", 1)}')


# Process harder
def processMore():
    upper = 0
    lower = -10000000000000
    data["humn"] = int((upper - lower) / 2)

    while (res := getAnswer("root", 2)) != (False, False):
        cur = data["humn"]
        if res[1] == True:
            upper = cur
            data["humn"] = int((upper + lower) / 2)
        else:
            lower = cur
            data["humn"] = int((upper + lower) / 2)
        if upper - lower == 1:
            data["humn"] = upper
        if data["humn"] == cur:
            break

    print(f'Part 2: {data["humn"]}')


def main():
    parseInput(args.input)

    # Part 1
    processData()

    # Part 2
    processMore()


if __name__ == "__main__":
    main()
