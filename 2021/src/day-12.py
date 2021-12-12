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
            newplot = list(plot)
            newplot.append(next)
            newplots.append(newplot)
        elif next in plot and next.isupper():
            newplot = list(plot)
            newplot.append(next)
            newplots.append(newplot)
        elif next in plot[0] and plot.count(next) < 2:
            newplot = list(plot)
            newplot.append(next)
            newplots.append(newplot)

    for newplot in newplots:
        plots.add(tuple(newplot))

    for x in newplots:
        findRoutes(x, plots)


def main():
    parseInput(args.input)

    # Part 1
    plots = set()
    for x in routes["start"]:
        plots.add(("*", "start", x))

    journeys = plots.copy()
    for plot in journeys:
        findRoutes(plot, plots)

    count = 0
    for route in plots:
        if route[-1] == "end":
            count += 1
    print(f"Solution to part 1: {count}")

    # Part 2
    plots = set()
    smalls = []
    for loc in routes:
        if loc.islower() and loc != "start" and loc != "end":
            smalls.append(loc)

    for x in routes["start"]:
        for double in smalls:
            plots.add((double + "*", "start", x))

    journeys = plots.copy()

    for plot in journeys:
        findRoutes(plot, plots)

    uniset = set()
    for route in plots:
        if route[-1] == "end":
            uniset.add(route[1:])
    print(f"Solution to part 2: {len(uniset)}")


if __name__ == "__main__":
    main()
