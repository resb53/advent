#!/usr/bin/env python3

import argparse
import sys
import json

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
    for entity in dir["contents"]:
        if entity["type"] == "f":
            size += entity["size"]
        else:
            size += dirSize(entity)
    dir["size"] = size
    print(f'Size of {dir["name"]} is {dir["size"]}')
    return dir["size"]


# Calculate total size for all directories
def processData():
    dirSize(data)


# Process harder
def processMore():
    return False


def main():
    parseInput(args.input)

    # Part 1
    processData()

    # Part 2
    processMore()


if __name__ == "__main__":
    main()
