#!/usr/bin/python3

import argparse
import sys

# Check correct usage
parser = argparse.ArgumentParser(description="Check your Mathematics.")
parser.add_argument('input', metavar='input', type=str,
                    help='Maths problem input.')
args = parser.parse_args()

probs = []
ops = ["*", "+"]
nums = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

def main():
    parseInput(args.input)

    # Part 1
    answer = 0
    for prob in probs:
        print(findSolutions(prob))

    # Part 2

    # Debug
    # printProbs()


# Parse the input file
def parseInput(inp):
    global probs
    try:
        probs_fh = open(inp, 'r')
    except IOError:
        sys.exit("Unable to open input file: " + inp)

    for line in probs_fh:
        probs.append(line.strip("\n").replace(" ", ""))


# Iterate through problem
def findSolutions(line):
    # Find parenthese depth
    strdep = ""
    curdep = 0
    maxdep = 0

    for cha in line:
        if cha == "(":
            curdep += 1
            if curdep > maxdep:
                maxdep = curdep
            strdep += "x"
        elif cha == ")":
            curdep = curdep - 1
            strdep += "x"
        else:
            strdep += str(curdep)

    print(line)
    print(strdep)

    # If parsing parentheses
    if maxdep > 0:
        chunks = []
        catch = False
        breaks = []

        for i, p in enumerate(strdep):
            if p == str(maxdep) and catch is False:
                catch = True
                breaks.append(i)
                chunks.append('')
                chunks[-1] += line[i]
            elif p == str(maxdep) and catch is True:
                chunks[-1] += line[i]
            elif p != str(maxdep) and catch is True:
                catch = False
                breaks.append(i)

        for i, chunk in enumerate(chunks):
            chunks[i] = solve(chunk)

        newstr = ""
        start = 0

        while len(breaks) > 0:
            newstr += line[start:breaks.pop(0)-1]
            newstr += str(chunks.pop(0))
            start = breaks.pop(0)+1

        newstr += line[start:]

        return findSolutions(newstr)

    else:
        return solve(line)


def solve(line):
    lhs = ''
    rhs = ''
    op = ''
    stop = 0
    soln = 0

    for i, cha in enumerate(line):
        if op not in ops and cha in nums:
            lhs += cha
        elif op not in ops and cha in ops:
            op = cha
        elif op in ops and cha in nums:
            rhs += cha
        elif op in ops and cha in ops:
            stop = i
            break

    if op == '*':
        soln = int(lhs) * int(rhs)
    elif op == '+':
        soln = int(lhs) + int(rhs)

    if stop != 0:
        line = str(soln) + line[stop:]
        return solve(line)
    else:
        return soln


def printProbs():
    for item in probs:
        print(item)


if __name__ == "__main__":
    main()
