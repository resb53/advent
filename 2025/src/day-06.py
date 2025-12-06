#!/usr/bin/env python3

import argparse
import sys
from math import prod


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
        data.append(line.strip("\n"))


# Flip Data
def flipdata(inp):
    d = []
    for x in inp:
        d.append(x.split())

    flipped = []

    maxn = len(d) - 1

    for i in range(len(d[0])):
        calc = []

        for n in range(len(d)):
            if n < maxn:
                calc.append(int(d[n][i]))
            else:
                calc.insert(0, d[n][i])

        flipped.append(calc)

    return flipped


# Do cephlapod maths
def processData():
    grandtotal = 0
    flipped = flipdata(data)

    for calc in flipped:
        if calc[0] == "+":
            grandtotal += sum(calc[1:])
        else:
            grandtotal += prod(calc[1:])

    return grandtotal


# Do real cephlapod maths
def processMore():
    grandtotal = 0

    calc = []
    maxn = len(data) - 1

    val = []
    sign = ""
    for i in range(len(data[0])):
        num = ""
        for n in range(maxn, -1, -1):
            if n == maxn:
                if data[n][i] in ["+", "*"]:
                    if sign == "":
                        sign = data[n][i]
                    else:
                        calc.append(val)
                        calc[-1].insert(0, sign)

                        val = []
                        sign = data[n][i]
            else:
                num += data[n][i]
        val.append(num)

    calc.append(val)
    calc[-1].insert(0, sign)

    # Flip, trip and calculate
    for x in calc:
        equ = []
        for val in x[1:]:
            num = val[::-1].strip()
            if len(num) > 0:
                equ.append(int(num))

        if x[0] == "+":
            grandtotal += sum(equ)
        else:
            grandtotal += prod(equ)

    return grandtotal


def main():
    parseInput(args.input)

    # Part 1
    print(f"Part 1: {processData()}")

    # Part 2
    print(f"Part 2: {processMore()}")


if __name__ == "__main__":
    main()
