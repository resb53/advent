#!/usr/bin/python3

import sys

# Check correct usage
if (len(sys.argv) != 2):
    sys.exit("USAGE: " + sys.argv[0] + " inputs_filename")

# Parse memory
try:
    instr_fh = open(sys.argv[1],'r')
except IOError:
    sys.exit("Unable to open input file: " + sys.argv[1])

def main():
    # Parse instructions in file. Allow for multiline just in case future need.
    for line in instr_fh:
        rng = line.rsplit()[0]

        # Split command string into list of instructions
        [rmin, rmax] = rng.split('-') #min and max range for codes
        rmin = int(rmin)
        rmax = int(rmax)

        print(countOccurences(rmin,rmax))

def countOccurences(a,b):
    count = 0;

    for i in range(a,b+1):
        # Boolean checks
        twoSame = 0 # set true if right
        nevDec = 1 #set false if wrong

        # Parse digits
        digits = list(str(i))

        for x in range(1,len(digits)):
            if (digits[x] == digits[x-1]):
                twoSame = 1
                # Check not part of larger group
                if (x > 1):
                    if (digits[x] == digits[x-2]):
                        twoSame = 0

            if (digits[x] < digits[x-1]):
                nevDec = 0

        # Check
        if twoSame and nevDec:
            print(i)
            count += 1

    return count

main()
