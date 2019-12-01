#!/usr/bin/python3

import sys

# Check correct usage
if (len(sys.argv) != 2):
    sys.exit("USAGE: " + sys.argv[0] + " inputs_filename")

# Parse input
try:
    masses_fh = open(sys.argv[1],'r')
except IOError:
    sys.exit("Unable to open input file: " + sys.argv[1])

masses = []

for line in masses_fh:
    masses.append(int(line.rsplit()[0]))

# Calculate fuel requirement based on day 1 task 1 rules
total_fuel = 0;

for mass in masses:
    while ((int(mass / 3) - 2) > 0): #div by 3, round down, subtract 2
        mass = int(mass / 3) - 2
        total_fuel += mass

print('Total fuel required: ' + str(total_fuel))
