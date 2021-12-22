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
        box = {}
        (state, instr) = line.strip("\n").split(" ")
        instr = instr.split(",")
        for r in instr:
            (d, vals) = r.split("=")
            vals = vals.split("..")
            box[d] = (int(vals[0]), int(vals[1]))
        data.append([state, box])


# Run through reactor startup instructions
def startReactor():
    cores = set()

    for switch in data[0:20]:
        for z in range(switch[1]["z"][0], switch[1]["z"][1] + 1):
            for y in range(switch[1]["y"][0], switch[1]["y"][1] + 1):
                for x in range(switch[1]["x"][0], switch[1]["x"][1] + 1):
                    if switch[0] == "on":
                        cores.add((x, y, z))
                    else:
                        if (x, y, z) in cores:
                            cores.remove((x, y, z))

    return len(cores)


def main():
    parseInput(args.input)

    # Part 1
    print(f"Solution to part 1: {startReactor()}")




if __name__ == "__main__":
    main()
