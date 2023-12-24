#!/usr/bin/env python3

import argparse
import sys
from itertools import combinations

# Check correct usage
parser = argparse.ArgumentParser(description="Parse some data.")
parser.add_argument('input', metavar='input', type=str,
                    help='Input data file.')
args = parser.parse_args()

hailstones = []


class Hail():
    def __init__(self, pos, vel):
        self.pos = pos
        self.vel = vel
        self.xyline = self.xytraj()

    def __str__(self):
        return f"{{p{self.pos}, v{self.vel}}}"

    def __repr__(self):
        return f"{{p{self.pos}, v{self.vel}}}"

    def xytraj(self):
        # Convert to form y = mx + c
        p1 = (self.pos[0], self.pos[1])
        p2 = (self.pos[0] + self.vel[0], self.pos[1] + self.vel[1])

        deltaY = p2[1] - p1[1]
        deltaX = p2[0] - p1[0]

        m = deltaY / deltaX
        c = p1[1] - (m * p1[0])

        # Return in form mx + y + c = 0
        return (-m, -c)


def getIntersect(a: Hail, b: Hail):
    #             c2-c1   c1m2-c2m1
    # (x0, y0) = (----- , ---------)
    #             m1-m2     m1-m2
    base = a.xyline[0] - b.xyline[0]
    if base != 0:
        x0 = (b.xyline[1] - a.xyline[1]) / (a.xyline[0] - b.xyline[0])
        y0 = (a.xyline[1] * b.xyline[0] - b.xyline[1] * a.xyline[0]) / (a.xyline[0] - b.xyline[0])

        return (x0, y0)
    else:
        return None


# Parse the input file
def parseInput(inp):
    try:
        input_fh = open(inp, 'r')
    except IOError:
        sys.exit("Unable to open input file: " + inp)

    for line in input_fh:
        line = line.rstrip()
        pos, vel = line.split(" @ ")
        pos = tuple([int(x) for x in pos.split(", ")])
        vel = tuple([int(x) for x in vel.split(", ")])
        hailstones.append(Hail(pos, vel))


# For each pass, identify its seat
def processData():
    count = 0
    for a, b in combinations(hailstones, 2):
        i = getIntersect(a, b)
        if i is not None and \
            i[0] >= 200000000000000 and i[0] <= 400000000000000 and \
                i[1] >= 200000000000000 and i[1] <= 400000000000000:
            count += 1
    return count


# Process harder
def processMore():
    return False


def main():
    parseInput(args.input)

    # Part 1
    print(f"Part 1: {processData()}")

    # Part 2
    print(f"Part 2: {processMore()}")


if __name__ == "__main__":
    main()
