#!/usr/bin/env python3

import argparse
import sys
from collections import defaultdict
from random import choices
import string

# Check correct usage
parser = argparse.ArgumentParser(description="Parse some data.")
parser.add_argument('input', metavar='input', type=str,
                    help='Input data file.')
args = parser.parse_args()

stack = defaultdict(dict)
bricks = []


class Brick():
    def __init__(self, start, finish):
        # Set name
        while True:
            name = "".join(choices(string.ascii_uppercase + string.digits, k=3))
            if name not in [x.name for x in bricks]:
                break
        self.name = name

        # Initialise
        self.supports = set()  # Blocks that currently support this one
        self.suspends = set()  # Blocks that this supports

        # Get dimension
        delta = None
        for i in range(3):
            if start[i] != finish[i]:
                delta = i
                break
        # Load positions
        match delta:
            case 0:
                self.orientation = "horizontal"
                self.pos = [(x, start[1], start[2])
                            for x in range(min((start[0], finish[0])), max((start[0], finish[0])) + 1)]
            case 1:
                self.orientation = "horizontal"
                self.pos = [(start[0], y, start[2])
                            for y in range(min((start[1], finish[1])), max((start[1], finish[1])) + 1)]
            case 2:
                self.orientation = "vertical"
                self.pos = [(start[0], start[1], z)
                            for z in range(min((start[2], finish[2])), max((start[2], finish[2])) + 1)]
            case _:
                self.orientation = "vertical"
                self.pos = [(start[0], start[1], start[2])]

        # Update world
        self.insert()
        bricks.append(self)

    def __str__(self):
        return f"{self.name}: {self.pos[0]} -> {self.pos[-1]}"

    def __repr__(self):
        return self.name

    def __lt__(self, other):
        lowzself = min([pos[2] for pos in self.pos])
        lowzother = min([pos[2] for pos in other.pos])
        return lowzself < lowzother

    def insert(self):
        for (x, y, z) in self.pos:
            if complex(x, y) not in stack[z]:
                stack[z][complex(x, y)] = self

    def update(self):
        self.supports.clear()
        self.suspends.clear()
        if self.orientation == "vertical":
            self.pos.sort(key=lambda x: x[2])
            if complex(self.pos[0][0], self.pos[0][1]) in stack[self.pos[0][2] - 1]:
                self.supports.add(stack[self.pos[0][2] - 1][complex(self.pos[0][0], self.pos[0][1])])
            if complex(self.pos[-1][0], self.pos[-1][1]) in stack[self.pos[-1][2] + 1]:
                self.suspends.add(stack[self.pos[-1][2] + 1][complex(self.pos[-1][0], self.pos[-1][1])])
        else:
            for (x, y, z) in self.pos:
                if complex(x, y) in stack[z - 1]:
                    self.supports.add(stack[z - 1][complex(x, y)])
                if complex(x, y) in stack[z + 1]:
                    self.suspends.add(stack[z + 1][complex(x, y)])

    def drop(self):
        if len(self.supports) == 0:
            if self.orientation == "vertical":
                x = self.pos[0][0]
                y = self.pos[0][1]
                lowz = min([pos[2] for pos in self.pos])
                for z in range(lowz - 1, 0, -1):
                    if complex(x, y) in stack[z]:
                        self.descend(lowz - z - 1)
                        return
                self.descend(lowz - 1)
            else:
                for z in range(self.pos[0][2] - 1, 0, -1):
                    for pos in self.pos:
                        if complex(pos[0], pos[1]) in stack[z]:
                            self.descend(pos[2] - z - 1)
                            return
                self.descend(self.pos[0][2] - 1)

    def descend(self, dist):
        if dist > 0:
            for (x, y, z) in self.pos:
                try:
                    stack[z].pop(complex(x, y))
                except KeyError:
                    sys.exit(f"Block {(x, y, z)} not found in Stack.")
            for i, (x, y, z) in enumerate(self.pos):
                if z - dist < 1:
                    raise ValueError(f"Cannot descend to {(x, y, z - dist)}")
                self.pos[i] = (x, y, z - dist)
            self.insert()
            for brick in bricks:
                brick.update()


# Parse the input file
def parseInput(inp):
    try:
        input_fh = open(inp, 'r')
    except IOError:
        sys.exit("Unable to open input file: " + inp)

    for line in input_fh:
        line = line.rstrip()
        start, finish = [[int(x) for x in y.split(",")] for y in line.split("~")]
        _ = Brick(start, finish)

    for brick in bricks:
        brick.update()


# For each pass, identify its seat
def processData():
    bricks.sort()
    for brick in bricks:
        brick.drop()
    # Count bricks that support nothing, or support a brick with other supports
    count = 0
    for brick in bricks:
        if len(brick.suspends) == 0:
            count += 1
        else:
            for sus in brick.suspends:
                if len(sus.supports) > 1:
                    count += 1
                    break
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
