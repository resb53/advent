#!/usr/bin/env python3

import argparse
import sys

# Check correct usage
parser = argparse.ArgumentParser(description="Parse some data.")
parser.add_argument('input', metavar='input', type=str,
                    help='Input data file.')
args = parser.parse_args()

instr = []


# Parse the input file
def parseInput(inp):
    try:
        input_fh = open(inp, 'r')
    except IOError:
        sys.exit("Unable to open input file: " + inp)

    for line in input_fh:
        instr.append(line.strip("\n").split(" "))


# For each pass, identify its seat
def processData():
    tick = 0
    ptr = 0
    exe = None
    dur = {
        "noop": 1,
        "addx": 2
    }
    cycle = [1]
    sprite = [0, 1, 2]

    while ptr < len(instr) or exe is not None:
        if exe is None:
            exe = instr[ptr]
            exe.insert(0, dur[exe[0]])
            ptr += 1
        exe[0] -= 1

        # Draw a pixel during this cycle
        if tick in sprite:
            print("#", end="")
        else:
            print(".", end="")
        # New row?
        if tick == 39:
            print("")
            tick = -1

        # End of cycle
        tick += 1
        if exe[0] == 0:
            # Complete action
            if exe[1] == "noop":
                cycle.append(cycle[-1])
                sprite = [cycle[-1] - 1, cycle[-1], cycle[-1] + 1]
            elif exe[1] == "addx":
                cycle.append(cycle[-1] + int(exe[2]))
                sprite = [cycle[-1] - 1, cycle[-1], cycle[-1] + 1]
            exe = None
        else:
            # No action this tick
            cycle.append(cycle[-1])
            sprite = [cycle[-1] - 1, cycle[-1], cycle[-1] + 1]

    # During 20th cycle always = end of 19th cycle
    signal = 20 * cycle[19] \
        + 60 * cycle[59] \
        + 100 * cycle[99] \
        + 140 * cycle[139] \
        + 180 * cycle[179] \
        + 220 * cycle[219]

    print(f"Part 1: {signal}")


# Process harder
def processMore():
    return False


def main():
    parseInput(args.input)
    processData()


if __name__ == "__main__":
    main()
