#!/usr/bin/python3

import argparse
import sys
from functools import reduce

# Check correct usage
parser = argparse.ArgumentParser(description="Check your Passport.")
parser.add_argument('input', metavar='input', type=str,
                    help='Password list input.')
args = parser.parse_args()

batch = []
fields = {
    'byr': 0, 
    'iyr': 0,
    'eyr': 0,
    'hgt': 0,
    'hcl': 0,
    'ecl': 0,
    'pid': 0
    #'cid': optional
}    

def main():
    parseInput(args.input)

    # Part 1
    print(countValid(batch))

    # Part 2

    # Debug
    # printBatch()


# Parse the input file
def parseInput(inp):
    global batch
    try:
        batch_fh = open(inp, 'r')
    except IOError:
        sys.exit("Unable to open input file: " + inp)

    passport = []

    for line in batch_fh:
        line = line.strip("\n")

        # If new line, push passport onto batch file and start new record
        if len(line) == 0:
            batch.append(passport)
            passport = []

        # Parse line
        records = line.split()

        for item in records:
            kvpair = item.split(':')
            passport.append(kvpair)


# Count how many passports are valid according to mandatory fields
def countValid(data):
    valid = 0

    for pp in data:
        print(pp)
        result = 1
        test = fields.copy()

        for item in pp:
            if item[0] in test:
                test[item[0]] += 1
            
        for check in test:
            if test[check] == 0:
                print("No " + check)
                result = 0
        
        valid += result
        print("Valid so far: " + str(valid))

    return valid

    
# Print batch
def printBatch():
    for pp in batch:
        print(pp)
        

if __name__ == "__main__":
    main()
