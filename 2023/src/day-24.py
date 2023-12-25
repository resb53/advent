#!/usr/bin/env python3

import argparse
import sys
from itertools import combinations
import numpy as np

# Check correct usage
parser = argparse.ArgumentParser(description="Parse some data.")
parser.add_argument('input', metavar='input', type=str,
                    help='Input data file.')
args = parser.parse_args()

hailstones = []


class Hail():
    def __init__(self, pos, vel):
        self.pos = np.array(pos)
        self.vel = np.array(vel)
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

        # Check future/past
        when = "future"
        if a.vel[0] > 0 and x0 < a.pos[0]:
            when = "past"
        elif a.vel[0] < 0 and x0 > a.pos[0]:
            when = "past"
        elif b.vel[0] > 0 and x0 < b.pos[0]:
            when = "past"
        elif b.vel[0] < 0 and x0 > b.pos[0]:
            when = "past"

        return (x0, y0, when)
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
        if i is not None and i[2] == "future" and \
            i[0] >= 200000000000000 and i[0] <= 400000000000000 and \
                i[1] >= 200000000000000 and i[1] <= 400000000000000:
            count += 1
    return count


# Solve Linear Algebra with numpy
def solveLin(a, b, c):
    A = np.array(
        [
            [b.vel[1] - a.vel[1], a.vel[0] - b.vel[0], 0, a.pos[1] - b.pos[1], b.pos[0] - a.pos[0], 0],
            [c.vel[1] - a.vel[1], a.vel[0] - c.vel[0], 0, a.pos[1] - c.pos[1], c.pos[0] - a.pos[0], 0],
            [b.vel[2] - a.vel[2], 0, a.vel[0] - b.vel[0], a.pos[2] - b.pos[2], 0, b.pos[0] - a.pos[0]],
            [c.vel[2] - a.vel[2], 0, a.vel[0] - c.vel[0], a.pos[2] - c.pos[2], 0, c.pos[0] - a.pos[0]],
            [0, b.vel[2] - a.vel[2], a.vel[1] - b.vel[1], 0, a.pos[2] - b.pos[2], b.pos[1] - a.pos[1]],
            [0, c.vel[2] - a.vel[2], a.vel[1] - c.vel[1], 0, a.pos[2] - c.pos[2], c.pos[1] - a.pos[1]],
        ]
    )

    x = [
        (a.pos[1] * a.vel[0] - b.pos[1] * b.vel[0]) - (a.pos[0] * a.vel[1] - b.pos[0] * b.vel[1]),
        (a.pos[1] * a.vel[0] - c.pos[1] * c.vel[0]) - (a.pos[0] * a.vel[1] - c.pos[0] * c.vel[1]),
        (a.pos[2] * a.vel[0] - b.pos[2] * b.vel[0]) - (a.pos[0] * a.vel[2] - b.pos[0] * b.vel[2]),
        (a.pos[2] * a.vel[0] - c.pos[2] * c.vel[0]) - (a.pos[0] * a.vel[2] - c.pos[0] * c.vel[2]),
        (a.pos[2] * a.vel[1] - b.pos[2] * b.vel[1]) - (a.pos[1] * a.vel[2] - b.pos[1] * b.vel[2]),
        (a.pos[2] * a.vel[1] - c.pos[2] * c.vel[1]) - (a.pos[1] * a.vel[2] - c.pos[1] * c.vel[2]),
    ]

    return np.linalg.solve(A, x)


# Process harder
def processMore():
    # Use 3 linearly independant hailstones
    a = hailstones[0]
    b = None
    c = None
    next = 1
    for i, x in enumerate(hailstones[next:]):
        if (a.vel / x.vel).ptp() != 0:
            b = x
            next += i + 1
            break
    for x in hailstones[next:]:
        if (a.vel / x.vel).ptp() != 0 and (b.vel / x.vel).ptp() != 0:
            c = x
            break

    # Solve linear algebra
    solution = solveLin(a, b, c)

    return sum([round(x) for x in solution])


def main():
    parseInput(args.input)

    # Part 1
    print(f"Part 1: {processData()}")

    # Part 2
    print(f"Part 2: {processMore()}")


if __name__ == "__main__":
    main()
