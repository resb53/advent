#!/usr/bin/python3

import argparse
import sys

# Check correct usage
parser = argparse.ArgumentParser(description="Check seat patterns.")
parser.add_argument('input', metavar='input', type=str,
                    help='Seat position input.')
args = parser.parse_args()

seats = {}
maxrow = 0
maxcol = 0


def main():
    parseInput(args.input)

    # Part 1
    changed = 1
    while changed > 0:
        changed = fillSeats()
    print(occupied())

    # Part 2

    # Debug
    # printSeats()


# Parse the input file
def parseInput(inp):
    global seats, maxrow, maxcol
    try:
        seats_fh = open(inp, 'r')
    except IOError:
        sys.exit("Unable to open input file: " + inp)

    row = 0

    for line in seats_fh:
        line = line.strip("\n")
        col = 0
        for seat in line:
            if seat == 'L':
                seats[row + col * 1j] = False
            else:
                seats[row + col * 1j] = seat
            col += 1
        row += 1
        maxcol = col

    maxrow = row


# For each pass, identify its seat
def fillSeats():
    global seats
    change = set()  # Dict for any seats that change state this iteration

    for r in range(maxrow):
        for c in range(maxcol):
            seat = r + c * 1j
            state = seats[seat]

            if state != '.':
                adj = checkAdjacent(r + c * 1j)
                # print(f"Seat: {r + c * 1j}, Status: {seat}, Adj: {adj}")

                # If empty and nobody adjacent, fill
                if not state and adj == 0:
                    change.add(seat)

                # If filled and 4 or more adjacent, empty
                if state and adj >= 4:
                    change.add(seat)

    # For changing seats, update seats
    for seat in change:
        seats[seat] = not seats[seat]

    return len(change)


def checkAdjacent(seat):
    count = 0
    adjacent = [seat - 1 - 1j, seat - 1, seat - 1 + 1j,
                seat - 1j,                 seat + 1j,
                seat + 1 - 1j, seat + 1, seat + 1 + 1j]

    for s in adjacent:
        if s.real >= 0 and s.real < maxrow and s.imag >= 0 and s.imag < maxcol:
            if seats[s] != '.' and seats[s]:
                count += 1

    return count


def occupied():
    count = 0

    for r in range(maxrow):
        for c in range(maxcol):
            if seats[r + c * 1j] != '.' and seats[r + c * 1j]:
                count += 1

    return count


def printSeats():
    for r in range(maxrow):
        for c in range(maxcol):
            seat = seats[r + c * 1j]
            if seat == '.':
                print(seat, end="")
            elif seat:
                print('#', end="")
            else:
                print('L', end="")
        print("")


if __name__ == "__main__":
    main()
