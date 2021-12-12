#!/usr/bin/env python3

import argparse
import sys
from collections import defaultdict

# Check correct usage
parser = argparse.ArgumentParser(description="Parse some data.")
parser.add_argument('input', metavar='input', type=str,
                    help='Input data file.')
args = parser.parse_args()

routes = defaultdict(list)


# Parse the input file
def parseInput(inp):
    try:
        input_fh = open(inp, 'r')
    except IOError:
        sys.exit("Unable to open input file: " + inp)

    for line in input_fh:
        (a, b) = line.strip("\n").split("-")
        routes[a].append(b)
        routes[b].append(a)


# For each pass, identify its seat
def findRoutes(plot, plots):
    newplots = []
    for next in routes[plot[-1]]:
        if next not in plot:
            newplot = plot.copy()
            newplot.append(next)
            newplots.append(newplot)
        elif next in plot and next.isupper():
            newplot = plot.copy()
            newplot.append(next)
            newplots.append(newplot)
    plots.extend(newplots)

    for x in newplots:
        findRoutes(x, plots)


# Process harder
def processMore():
    return False


def main():
    parseInput(args.input)

    # Part 1
    plots = []
    for x in routes["start"]:
        plots.append(["start", x])

    journeys = plots.copy()
    for plot in journeys:
        findRoutes(plot, plots)

    count = 0
    for route in plots:
        if route[-1] == "end":
            count += 1
    print(f"Solution to part 1: {count}")

    # Part 2
    processMore()


if __name__ == "__main__":
    main()
