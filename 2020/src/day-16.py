#!/usr/bin/python3

import argparse
import sys
import re

# Check correct usage
parser = argparse.ArgumentParser(description="Check your Train Ticket.")
parser.add_argument('input', metavar='input', type=str,
                    help='Ticket list input.')
args = parser.parse_args()

rules = {}
myticket = []
tickets = []
errors = {}


def main():
    parseInput(args.input)
    uber = uberrule()

    # Part 1
    findErrors(uber)
    total = 0
    for vals in errors.values():
        for val in vals:
            total += val
    print(total)

    # Part 2
    removeErrors()
    solve(findFields())

    # Debug
    # printTickets()


# Parse the input file
def parseInput(inp):
    global rules, myticket, tickets
    try:
        tickets_fh = open(inp, 'r')
    except IOError:
        sys.exit("Unable to open input file: " + inp)

    mode = 'rules'

    for line in tickets_fh:
        line = line.strip("\n")

        if line == 'your ticket:':
            mode = 'myticket'
        elif line == 'nearby tickets:':
            mode = 'tickets'
        else:
            if line != '':
                if mode == 'rules':
                    match = re.match(r"^([\w\s]+): (\d+)-(\d+) or (\d+)-(\d+)$", line, re.I)
                    rules[match.group(1)] = [(int(match.group(2)), int(match.group(3))),
                                             (int(match.group(4)), int(match.group(5)))]
                elif mode == 'myticket':
                    myticket = [int(i) for i in line.split(',')]
                else:
                    ticket = [int(i) for i in line.split(',')]
                    tickets.append(ticket)


# Find single set of conditions to satisfy all rules
def uberrule():
    minval = 100
    maxval = 900
    # Looking at data show the 2 groups overlap, so just need a min and max
    for rule in rules:
        for pair in rules[rule]:
            if pair[0] < minval:
                minval = pair[0]
            if pair[1] > maxval:
                maxval = pair[1]

    return (minval, maxval)


# For each pass, identify its seat
def findErrors(uber):
    global errors

    # ALL incorrect values (regardless of anything else)
    for i, ticket in enumerate(tickets):
        for val in ticket:
            if val < uber[0] or val > uber[1]:
                if i not in errors:
                    errors[i] = []
                errors[i].append(val)

    return sum(errors)


# Remove tickets if they have an error - work backwards to maintain indices
def removeErrors():
    global tickets

    badids = sorted(errors.keys(), reverse=True)

    for i in badids:
        tickets.pop(i)


# Iterate through each field over each ticket. Elminate impossible rules.
def findFields():
    options = {}

    for field in range(len(tickets[0])):
        possField = list(rules.keys())

        for ticket in tickets:
            for rule in rules:
                if (ticket[field] < rules[rule][0][0] or
                    (ticket[field] > rules[rule][0][1] and
                     ticket[field] < rules[rule][1][0]) or
                    ticket[field] > rules[rule][1][1]):
                        possField.remove(rule)

        # print(f"Field: {field}, Possibles: {possField}")

        options[field] = possField

    # Go through fields based on fewest options to determine truth
    truth = {}

    sortops = sorted(options.keys(), key=lambda x: len(options[x]))

    for i in sortops:
        for v in options[i]:
            if v not in truth:
                truth[v] = i

    return truth


# Solve puzzle for my ticket
def solve(truth):
    prod = 1

    for field in [
        "departure location",
        "departure station",
        "departure platform",
        "departure track",
        "departure date",
        "departure time"
    ]:
        prod *= myticket[truth[field]]

    print(prod)


def printTickets():
    for item in tickets:
        print(item)


if __name__ == "__main__":
    main()
