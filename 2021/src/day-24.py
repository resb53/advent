#!/usr/bin/env python3

import argparse
import sys

# Check correct usage
parser = argparse.ArgumentParser(description="Parse some data.")
parser.add_argument('input', metavar='input', type=str,
                    help='Input data file.')
args = parser.parse_args()

vars = ["w", "x", "y", "z"]


# Parse the input file
def parseInput(inp):
    instr = []

    try:
        input_fh = open(inp, 'r')
    except IOError:
        sys.exit("Unable to open input file: " + inp)

    for line in input_fh:
        args = line.strip("\n").split(" ")
        if len(args) > 2:
            if args[2] not in vars:
                args[2] = int(args[2])
        instr.append(args)

    return instr


def simplifyInput(instr):
    analyse = instr.copy()
    simplified = []
    while len(analyse) > 0:
        block, analyse = analyse[0:18], analyse[18:]
        simplified.append([block[4][2], block[5][2], block[15][2]])

    return simplified


def runSimply(instr, input):
    instr = instr.copy()
    z = 0

    for val in input:
        vars = instr.pop(0)
        remainder = z % 26
        z = z // vars[0]
        if remainder + vars[1] != val:
            z = ((26 * z) + val + vars[2])

    return z


def traceStates(instr):
    zeds = {}
    for f in range(1, 10):
        z = runSimply(instr, [f])
        zeds[z] = f

    for n in range(2, 15):
        print(f"Processing for digit {n}...")
        zeds = addInput(zeds, instr)

    return zeds[0]


def addInput(zeds, instr):
    newzeds = {}

    for f in zeds.values():
        for g in range(1, 10):
            val = int(str(f) + str(g))
            vals = [int(i) for i in list(str(val))]
            z = runSimply(instr, vals)
            if z in newzeds:
                if val < newzeds[z]:
                    newzeds[z] = val
            else:
                newzeds[z] = val

    return newzeds


def main():
    instr = parseInput(args.input)
    simpl = simplifyInput(instr)

    # Part 1
    print(f"Solution to part 2: {traceStates(simpl)}")


if __name__ == "__main__":
    main()
