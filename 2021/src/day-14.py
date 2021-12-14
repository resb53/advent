#!/usr/bin/env python3

import argparse
import sys
from collections import defaultdict
from types import NoneType

# Check correct usage
parser = argparse.ArgumentParser(description="Parse some data.")
parser.add_argument('input', metavar='input', type=str,
                    help='Input data file.')
args = parser.parse_args()

recipe = defaultdict(dict)
counter = defaultdict(int)


class Node:
    def __init__(self, dataval=None):
        self.data = dataval
        self.next = None


class SLL:
    def __init__(self):
        self.head = None

    def print(self):
        val = self.head
        while val is not None:
            print(val.data, end="")
            val = val.next


# Parse the input file
def parseInput(inp):
    try:
        input_fh = open(inp, 'r')
    except IOError:
        sys.exit("Unable to open input file: " + inp)

    pattern = input_fh.readline().strip("\n")
    _ = input_fh.readline()

    for line in input_fh:
        (pair, result) = line.strip("\n").split(" -> ")
        recipe[pair[0]][pair[1]] = result

    polymer = SLL()
    lastnode = None

    for x in pattern:
        counter[x] += 1
        if polymer.head is None:
            polymer.head = Node(x)
            lastnode = polymer.head
        else:
            y = Node(x)
            lastnode.next = y
            lastnode = y

    return polymer


# For each pass, identify its seat
def stepThrough(polymer):
    startnode = polymer.head
    nextnode = startnode.next

    while nextnode is not None:
        newval = recipe[startnode.data][nextnode.data]
        counter[newval] += 1
        newnode = Node(newval)
        startnode.next = newnode
        newnode.next = nextnode

        startnode = nextnode
        nextnode = startnode.next


def main():
    poly = parseInput(args.input)

    # Part 1
    for _ in range(10):
        stepThrough(poly)

    print(f"Solution to part 1: {max(counter.values()) - min(counter.values())}")

    # Part 2
    return


if __name__ == "__main__":
    main()
