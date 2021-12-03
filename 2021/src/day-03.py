#!/usr/bin/env python3

import argparse
import sys

# Check correct usage
parser = argparse.ArgumentParser(description="Parse some data.")
parser.add_argument('input', metavar='input', type=str,
                    help='Input data file.')
args = parser.parse_args()

data = []
bincount = []


# Parse the input file
def parseInput(inp):
    try:
        input_fh = open(inp, 'r')
    except IOError:
        sys.exit("Unable to open input file: " + inp)

    for line in input_fh:
        data.append(line.strip("\n"))


# For each pass, identify its seat
def processData():
    # Prepare bincount array
    for _ in range(len(data[0])):
        bincount.append({'0': 0, '1': 0})

    for element in data:
        for i, bit in enumerate(element):
            bincount[i][bit] += 1

    gamma = ''
    epsilon = ''

    for count in bincount:
        if count['0'] > count['1']:
            gamma += '0'
            epsilon += '1'
        else:
            gamma += '1'
            epsilon += '0'

    gammadec = int(gamma, 2)
    epsilondec = int(epsilon, 2)

    print(f"Gamma: {gammadec}, Epsilon {epsilondec}")
    print(f"Solution 1: {gammadec * epsilondec}")

    return (gamma, epsilon)


# Process harder
def processMore(gamma, epsilon):
    oxy = data.copy()
    co2 = data.copy()

    # Oxygen
    oxydel = []
    for i, bit in enumerate(gamma):
        if (len(oxy) > 1):
            for j, val in enumerate(oxy):
                if (val[i] != bit):
                    oxydel.append(j)
            for k in range(len(oxydel)-1, -1, -1):
                oxy.pop(oxydel[k])
            oxydel = []
    
    # CO2 Scrubbing
    co2del = []
    for i, bit in enumerate(epsilon):
        if (len(co2) > 1):
            for j, val in enumerate(co2):
                if (val[i] != bit):
                    co2del.append(j)
            for k in range(len(co2del)-1, -1, -1):
                co2.pop(co2del[k])
            co2del = []
    
    oxydec = int(oxy[0], 2)
    co2dec = int(co2[0], 2)

    print(f"Oxygen: {oxydec}, CO2 Scrubbing: {co2dec}")
    print(f"Solution 2: {oxydec * co2dec}")



def main():
    parseInput(args.input)

    # Part 1
    (g, e) = processData()

    # Part 2
    processMore(g, e)


if __name__ == "__main__":
    main()
