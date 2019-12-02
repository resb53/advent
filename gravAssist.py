#!/usr/bin/python3

import sys

# Check correct usage
if (len(sys.argv) != 2):
    sys.exit("USAGE: " + sys.argv[0] + " inputs_filename")

# Parse input
try:
    instr_fh = open(sys.argv[1],'r')
except IOError:
    sys.exit("Unable to open input file: " + sys.argv[1])

# Parse instructions in file. Allow for multiline just in case future need.
for line in instr_fh:
    cmd = line.rsplit()[0]

    # Split command string into list of instructions
    instr = cmd.split(',')
    instr = [int(x) for x in instr]
    print("Input: " + str(instr))

    # Reset after alarm
    instr[1] = 12
    instr[2] = 2
    print("Reset: " + str(instr))

    # Iterate through list
    i = 0;

    while (instr[i] != 99):
        print("i=" + str(i))
        print(instr[i:i+4])
        # Decide operation based of value in first field
        if (instr[i] == 1):
            # Add values
            instr[instr[i+3]] = instr[instr[i+1]] + instr[instr[i+2]]
        elif (instr[i] == 2):
            # Multiply values
            instr[instr[i+3]] = instr[instr[i+1]] * instr[instr[i+2]]
        else:
            sys.exit("Invalid operator in position " + str(i) + ": " + instr[i])
        i += 4

    print("Output: " + str(instr))
