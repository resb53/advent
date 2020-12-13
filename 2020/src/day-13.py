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

def main():
    parseInput(args.input)

    # Part 1
    findNextBus()

    # Part 2
    # Find t such that t * b1 = u * b2 + gap = v * b3 + gap2

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
        for i in line.split(','):
            if i != 'x':
                busses.append(int(i))


# For each pass, identify its seat
def findNextBus():
    arrivals = {}
    minwait = 1000000

    for bus in busses:
        nextArrival = math.ceil(board / bus) * bus
        wait = nextArrival - board
        arrivals[wait] = bus
        if wait < minwait:
            minwait = wait
    
    print(minwait * arrivals[minwait])


def printTimetable():
    for item in busses:
        print(item)


if __name__ == "__main__":
    main()
