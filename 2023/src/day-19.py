#!/usr/bin/env python3

import argparse
import sys
import re

# Check correct usage
parser = argparse.ArgumentParser(description="Parse some data.")
parser.add_argument('input', metavar='input', type=str,
                    help='Input data file.')
args = parser.parse_args()

instr = {}
data = []


# Parse the input file
def parseInput(inp):
    try:
        input_fh = open(inp, 'r')
    except IOError:
        sys.exit("Unable to open input file: " + inp)

    dmode = False
    for line in input_fh:
        line = line.rstrip()
        if not dmode:
            if len(line) > 0:
                name, content = line.rstrip("}").split("{")
                instr[name] = []
                for check in content.split(","):
                    parts = re.match(r"^([xmas])(.)(\d+):(\S+)$", check)
                    if parts:
                        instr[name].append([parts[1], parts[2], int(parts[3]), parts[4]])
                    else:
                        instr[name].append(check)
            else:
                dmode = True
        else:
            line = line.strip("{}")
            values = line.split(",")
            data.append({})
            for val in values:
                k, v = val.split("=")
                data[-1][k] = int(v)


# Run through the test algorithm
def testPart(part):
    check = "in"
    while check not in "RA":
        for step in instr[check]:
            if type(step) is list:
                if step[1] == "<":
                    if part[step[0]] < step[2]:
                        check = step[3]
                        break
                else:
                    if part[step[0]] > step[2]:
                        check = step[3]
                        break
            else:
                check = step
    return check


# For each pass, identify its seat
def processData():
    ratings = 0
    for x in data:
        if testPart(x) == "A":
            ratings += sum(x.values())

    return ratings


# Process harder
def processMore():
    return False


def main():
    parseInput(args.input)

    # Part 1
    print(f"Part 1: {processData()}")

    # Part 2
    print(f"Part 2: {processMore()}")


if __name__ == "__main__":
    main()
