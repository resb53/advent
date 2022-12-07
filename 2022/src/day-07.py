#!/usr/bin/env python3

import argparse
import sys
from collections import defaultdict

# Check correct usage
parser = argparse.ArgumentParser(description="Parse some data.")
parser.add_argument('input', metavar='input', type=str,
                    help='Input data file.')
args = parser.parse_args()


class File:
    def __init__(self, name: str, size: int, parent: 'Dir' = None) -> 'File':
        self.name = name
        self.size = size
        self.parent = parent


class Dir:
    def __init__(self, name: str, parent: 'Dir' = None) -> 'Dir':
        self.name = name
        self.size = 0
        self.parent = parent
        self.contents = []

    def add(self, entity: File) -> None:
        if type(entity) == File:
            self.contents.append(entity)
            entity.parent = self
            self.updateSize(entity.size)
        elif type(entity) == Dir:
            self.contents.append(entity)
            entity.parent = self

    def updateSize(self, size: int) -> None:
        self.size += size
        if self.parent is not None:
            self.parent.updateSize(size)


# Parse the input file
def parseInput(inp):
    try:
        input_fh = open(inp, 'r')
    except IOError:
        sys.exit("Unable to open input file: " + inp)

    root = Dir("/")
    pwd = root

    for line in input_fh:
        line = line.strip("\n")

        if line.startswith("$"):
            cmd = line.split(" ")

            if cmd[1] == "cd":
                if cmd[2] == "/":
                    pwd = root
                elif cmd[2] == "..":
                    pwd = pwd.parent
                else:
                    for dir in pwd.contents:
                        if cmd[2] == dir.name and type(dir) == Dir:
                            pwd = dir
                            break
                    else:
                        sys.exit("Unable to find directory")

        # Else we're in an ls for the current directory
        else:
            listing = line.split(" ")

            if listing[0] == "dir":
                pwd.add(Dir(listing[1]))
            else:
                pwd.add(File(listing[1], int(listing[0])))

    return root


# Collect total size of directories
def dirSize(dir, sizes):
    sizes[dir.name].append(dir.size)

    for entity in dir.contents:
        if type(entity) == Dir:
            dirSize(entity, sizes)

    return sizes


# Calculate total size for all directories
def processData(dirSizes):
    sumLessTarget = 0

    for dir in dirSizes:
        for size in dirSizes[dir]:
            if size <= 100000:
                sumLessTarget += size

    print(f"Part 1: {sumLessTarget}")


# Find smallest directory that frees up 30000000 space out of 70000000
def processMore(dirSizes):
    smallest = dirSizes["/"][0]

    for dir in dirSizes:
        for size in dirSizes[dir]:
            if dirSizes["/"][0] - size <= 40000000:
                if size < smallest:
                    smallest = size

    print(f"Part 2: {smallest}")


def main():
    rootfs = parseInput(args.input)
    dirSizes = defaultdict(list)
    dirSizes = dirSize(rootfs, dirSizes)

    # Part 1
    processData(dirSizes)

    # Part 2
    processMore(dirSizes)


if __name__ == "__main__":
    main()
