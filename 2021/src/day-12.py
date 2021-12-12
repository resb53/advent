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
        elif next in plot[0] and plot.count(next) < 2:
            newplot = plot.copy()
            newplot.append(next)
            newplots.append(newplot)

    # Check for repeat routes
    for check in newplots:
        repeat = False
        for validate in plots:
            if check[1:] == validate[1:]:
                repeat = True
        if not repeat:
            plots.append(check)

    for x in newplots:
        findRoutes(x, plots)


def main():
    parseInput(args.input)

    # Part 1
    plots = []
    for x in routes["start"]:
        plots.append(["*", "start", x])

    journeys = plots.copy()
    for plot in journeys:
        findRoutes(plot, plots)

    count = 0
    for route in plots:
        if route[-1] == "end":
            count += 1
    print(f"Solution to part 1: {count}")

    # Part 2
    plots = []
    smalls = []
    for loc in routes:
        if loc.islower() and loc != "start" and loc != "end":
            smalls.append(loc)

    for x in routes["start"]:
        for double in smalls:
            plots.append([double + "*", "start", x])

    journeys = plots.copy()

    for plot in journeys:
        findRoutes(plot, plots)       

    count = 0
    for route in plots:
        if route[-1] == "end":
            count += 1
    print(f"Solution to part 2: {count}")


if __name__ == "__main__":
    main()
