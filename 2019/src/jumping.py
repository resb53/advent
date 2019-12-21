#!/usr/bin/python3

import intCode
import argparse
import sys

# Check correct usage
parser = argparse.ArgumentParser(description="Test tractor beam.")
parser.add_argument('code', metavar='code', type=str, help='Int code file.')
args = parser.parse_args()

# Prepare io
output = []
instr = list('NOT A J\nNOT B T\nOR T J\nNOT C T\nOR T J\nAND D J\n')
instr.extend(list('WALK\n'))

# Robot will jump 4 spaces forwards. Need to ensure this is not a hole. AND D J final command
# If hole in 3, 2 or 1, and 4 is safe, jump now.
def main():
    prog = intCode.Program(args.code)
    prog.run(i=instr_in, o=instr_out)

def instr_out(p):
    global output
    if p == 10:
        print(''.join(output))
        output = []
    elif p > 127:
        print(p)
    else:
        output.append(chr(p))

def instr_in():
    global instr
    return ord(instr.pop(0))

if __name__ == "__main__":
    main()
