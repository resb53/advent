#!/usr/bin/python3

import argparse
import sys
from functools import reduce
import re

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
    
    # Add last passport
    batch.append(passport)


# Count how many passports are Present and Valid according to mandatory fields
def countValid(data):
    present = 0
    valid = 0

    for pp in data:
        #print(pp)
        result = 1
        accurate = 1
        test = fields.copy()
        correct = fields.copy()

        for item in pp:
            if item[0] in fields:
                test[item[0]] += 1

                # Check Validity of data
                #byr
                if item[0] == 'byr':
                    item[1] = int(item[1])
                    if 1920 <= item[1] and item[1] <= 2002:
                        correct[item[0]] += 1

                #iyr
                elif item[0] == 'iyr':
                    item[1] = int(item[1])
                    if 2010 <= item[1] and item[1] <= 2020:
                        correct[item[0]] += 1

                #eyr
                elif item[0] == 'eyr':
                    item[1] = int(item[1])
                    if 2020 <= item[1] and item[1] <= 2030:
                        correct[item[0]] += 1

                #hgt
                elif item[0] == 'hgt':
                    match = re.match(r"^(\d+)(in|cm)$", item[1], re.I)
                    if match:
                        hits = list(match.groups())
                        hits[0] = int(hits[0])
                        if hits[1] == 'cm':
                            if 150 <= hits[0] and hits[0] <= 193:
                                correct[item[0]] += 1
                        else:
                            if 59 <= hits[0] and hits[0] <= 76:
                                correct[item[0]] += 1

                #hcl
                elif item[0] == 'hcl':
                    match = re.match(r"^\#[0-9a-f]{6}$", item[1], re.I)
                    if match:
                        correct[item[0]] += 1

                #ecl
                elif item[0] == 'ecl':
                    if item[1] in ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']:
                        correct[item[0]] += 1

                #pid
                elif item[0] == 'pid':
                    match = re.match(r"^\d{9}$", item[1])
                    if match:
                        correct[item[0]] += 1

        #print(test)
        for check in test:
            if test[check] == 0:
                result = 0
        
        #print(correct)
        for check in correct:
            if correct[check] == 0:
                accurate = 0
        
        present += result
        valid += accurate
        #print("Valid so far: " + str(valid))

    return (present, valid)

    
# Print batch
def printBatch():
    for pp in batch:
        print(pp)
        

if __name__ == "__main__":
    main()
