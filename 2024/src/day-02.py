#!/usr/bin/env python3

import argparse
import sys

# Check correct usage
parser = argparse.ArgumentParser(description="Parse some data.")
parser.add_argument('input', metavar='input', type=str,
                    help='Input data file.')
args = parser.parse_args()

data = []


# Parse the input file
def parseInput(inp):
    try:
        input_fh = open(inp, 'r')
    except IOError:
        sys.exit("Unable to open input file: " + inp)

    for line in input_fh:
        data.append([int(x) for x in line.rstrip().split()])


# For each report, scan the levels to see if they're safe
def processData():
    safep1 = 0
    safep2 = 0
    for report in data:
        scan = []
        for lvl in range(len(report) - 1):
            scan.append(report[lvl] - report[lvl + 1])
        # Check the scan
        if checkScan(scan):
            safep1 += 1
            safep2 += 1
        # Try any unsafe reports if allowing for dampening
        else:
            if dampen(report):
                safep2 += 1
    return safep1, safep2


# Check a scan of a report and return true if safe, false if not
def checkScan(scan):
    # Check if always decreasing and no 0's
    if all(x < 0 for x in scan) or all(x > 0 for x in scan):
        # Check if all absolute values less than or equal to 3
        if all(abs(x) <= 3 for x in scan):
            return True
    return False


# Recheck scan, but allow for dampening - i.e. drop each value until one returns true, else return false
def dampen(rpt):
    for i in range(len(rpt)):
        test = rpt.copy()
        test.pop(i)
        # Scan new report
        scan = []
        for lvl in range(len(test) - 1):
            scan.append(test[lvl] - test[lvl + 1])
        if checkScan(scan):
            return True
    return False


def main():
    parseInput(args.input)

    # Part 1
    p1, p2 = processData()
    print(f"Part 1: {p1}")

    # Part 2
    print(f"Part 2: {p2}")


if __name__ == "__main__":
    main()
