#!/usr/bin/env python3

import argparse
import sys
from collections import defaultdict

# Check correct usage
parser = argparse.ArgumentParser(description="Parse some data.")
parser.add_argument('input', metavar='input', type=str,
                    help='Input data file.')
args = parser.parse_args()

data = {
    "type": "d",
    "name": "/",
    "contents": [],
    "parent": None
}

dirSizes = defaultdict(list)


# Parse the input file
def parseInput(inp):
    try:
        input_fh = open(inp, 'r')
    except IOError:
        sys.exit("Unable to open input file: " + inp)

    pwd = data

    for line in input_fh:
        line = line.strip("\n")

        if line.startswith("$"):
            cmd = line.split(" ")

            if cmd[1] == "cd":
                if cmd[2] == "/":
                    pwd = data
                elif cmd[2] == "..":
                    pwd = pwd["parent"]
                else:
                    done = False
                    for dir in pwd["contents"]:
                        if cmd[2] == dir["name"]:
                            pwd = dir
                            done = True
                    if not done:
                        pwd["contents"].append({
                            "type": "d",
                            "name": cmd[2],
                            "contents": [],
                            "parent": pwd
                        })
                        pwd = pwd["contents"][-1]

        # Else we're in an ls for the current directory
        else:
            listing = line.split(" ")

            if listing[0] == "dir":
                pwd["contents"].append({
                    "type": "d",
                    "name": listing[1],
                    "contents": [],
                    "parent": pwd
                })
            else:
                pwd["contents"].append({
                    "type": "f",
                    "name": listing[1],
                    "size": int(listing[0]),
                    "parent": pwd
                })


# Calculate total size of a directory
def dirSize(dir):
    size = 0
    global sumLessTarget
    for entity in dir["contents"]:
        if entity["type"] == "f":
            size += entity["size"]
        else:
            size += dirSize(entity)
    dir["size"] = size
    dirSizes[dir["name"]].append(size)

    return dir["size"]


# Calculate total size for all directories
def processData():
    dirSize(data)

    sumLessTarget = 0
    for dir in dirSizes:
        for size in dirSizes[dir]:
            if size <= 100000:
                sumLessTarget += size

    print(f"Part 1: {sumLessTarget}")


# Find smallest directory that frees up 30000000 space out of 70000000
def processMore():
    smallest = dirSizes["/"][0]

    for dir in dirSizes:
        for size in dirSizes[dir]:
            if dirSizes["/"][0] - size <= 40000000:
                if size < smallest:
                    smallest = size

    print(f"Part 2: {smallest}")


def main():
    parseInput(args.input)

    # Part 1
    processData()

    # Part 2
    processMore()


if __name__ == "__main__":
    main()
