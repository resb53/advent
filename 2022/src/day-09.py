#!/usr/bin/env python3

import argparse
import sys

# Check correct usage
parser = argparse.ArgumentParser(description="Parse some data.")
parser.add_argument('input', metavar='input', type=str,
                    help='Input data file.')
args = parser.parse_args()

data = []
direction = {
    "U": 1j,
    "R": 1,
    "D": -1j,
    "L": -1
}


# Parse the input file
def parseInput(inp):
    try:
        input_fh = open(inp, 'r')
    except IOError:
        sys.exit("Unable to open input file: " + inp)

    for line in input_fh:
        dir, mag = line.strip("\n").split(" ")
        data.append([dir, int(mag)])


def singleMove(dir, pos, visits=None):
    # Move the head
    pos[0] += direction[dir]
    # Check the tail
    diff = pos[0] - pos[1]
    if abs(diff.real) > 1 or abs(diff.imag) > 1:
        # Horizontal / Vertical
        if diff.real == 0 or diff.imag == 0:
            pos[1] += diff/2
        # Diagonal
        else:
            if abs(diff.real) > 1:
                pos[1] += diff.real/2 + diff.imag * 1j
            else:
                pos[1] += diff.real + diff.imag/2 * 1j
        # Add new tail position
        if visits:
            visits.add(pos[1])

    return pos


# Tail follows the head
def processData():
    headtail = [0j, 0j]
    visits = {headtail[1]}

    for move in data:
        for _ in range(move[1]):
            singleMove(move[0], headtail, visits)

    print(f"Part 1: {len(visits)}")


# Process harder
def processMore():
    headtail = [0j] * 10
    visits = {headtail[9]}

    for move in data:
        for _ in range(move[1]):
            # For each adjacent pair of knots (Head to 8)
            for i in range(9):
                (headtail[i], headtail[i+1]) = singleMove(move[0], [headtail[i], headtail[i+1]])
                print(f"After part: {headtail}")
            # For the last pair of knots (8 and 9)
            (headtail[8], headtail[9]) = singleMove(move[0], [headtail[8], headtail[9]], visits)
            print(f"After Move: {headtail} - {visits}")

    print(f"Part 2: {len(visits)}")


def main():
    parseInput(args.input)

    # Part 1
    processData()

    # Part 2
    processMore()


if __name__ == "__main__":
    main()
