#!/usr/bin/python3

import os
import sys
import argparse

# Check correct usage
parser = argparse.ArgumentParser(description="Asteroid effectiveness calculator.")
parser.add_argument('map', metavar='map', type=str, help='Asteroid map filename.')
args = parser.parse_args()

# Parse memory
try:
    map_fh = open(args.map,'r')
except IOError:
    sys.exit("Unable to open input file: " + sys.argv[1])

def main():
    # Prepare map
    asteroids = []
    # Parse instructions in file. Allow for multiline just in case future need.
    for line in map_fh:
        line = line.rsplit()[0]
        asteroids.append(list(line))

    print(asteroids)


if __name__ == "__main__":
    main()
