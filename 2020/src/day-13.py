#!/usr/bin/python3

import argparse
import sys
import math

# Check correct usage
parser = argparse.ArgumentParser(description="Check your Bus.")
parser.add_argument('input', metavar='input', type=str,
                    help='Bus timetable input.')
args = parser.parse_args()

busses = []
board = 0
syncStart = 0


def main():
    global busses

    parseInput(args.input)

    # Part 1
    findNextBus()

    # Part 2
    # Find t such that t * b1 = u * b2 + gap = v * b3 + gap2
    # Essentially lowest common multiples, with an offset?
    # a * 19 = b * 41 + 9 = etc.

    # Work through from first bus
    first = busses[0]
    for comp in range(1, len(busses)):
        first = findSync(first, busses[comp])
    print(syncStart)

    # Debug
    # printTimetable()


# Parse the input file
def parseInput(inp):
    global busses, board
    try:
        busses_fh = open(inp, 'r')
    except IOError:
        sys.exit("Unable to open input file: " + inp)

    board = int(busses_fh.readline().strip("\n"))

    for line in busses_fh:
        line = line.strip("\n")
        pos = 0
        for i in line.split(','):
            if i != 'x':
                busses.append((int(i), pos))
            pos += 1


# For each pass, identify its seat
def findNextBus():
    arrivals = {}
    minwait = 1000000

    for bus, _ in busses:
        nextArrival = math.ceil(board / bus) * bus
        wait = nextArrival - board
        arrivals[wait] = bus
        if wait < minwait:
            minwait = wait

    print(minwait * arrivals[minwait])


def findSync(a, b):
    global syncStart
    # print(f"Sync: {a} - {b}")
    delta = b[1] - a[1]
    # print(f"Delta: {delta}")
    match = False
    firstObs = None
    periodicity = None

    # Find 2 matches, and infer periodicity for these busses
    # print(f"Start: {syncStart}")
    while not match:
        # If in sync based on start
        if (syncStart + delta) % b[0] == 0:
            if firstObs is None:
                firstObs = syncStart
                # print(f"First: {firstObs}")
            else:
                match = True
                periodicity = syncStart - firstObs
                # print(f"Second: {syncStart}")
                # print(f"Period: {periodicity}")
        # Check next window
        syncStart += a[0]

    syncStart = firstObs
    return (periodicity, 0)


def printTimetable():
    for item in busses:
        print(item)


if __name__ == "__main__":
    main()
