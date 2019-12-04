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
        onlyTwo = 0 # at least one set of digits must only occur twice

        # Parse digits
        digits = list(str(i))
        countDig = {}

        for x in range(1,len(digits)):
            if (digits[x] == digits[x-1]):
                twoSame = 1
            if (digits[x] < digits[x-1]):
                nevDec = 0
            # number of occurences, (at least) one digit must occur only twice (due to increasing or same only rule)
            if digits[x] in countDig:
                countDig[digits[x]] += 1
            else:
                countDig[digits[x]] = 1

        # Check
        for c in countDig:
            if countDig[c] == 2:
                onlyTwo = 1
        

        if twoSame and nevDec and onlyTwo:
            print(i)
            count += 1

    return count

main()
