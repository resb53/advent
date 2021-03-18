#!/usr/bin/python3

import intCodeClass
import argparse
import sys

# Check correct usage
parser = argparse.ArgumentParser(description="Test tractor beam.")
parser.add_argument('code', metavar='code', type=str, help='Int code file.')
args = parser.parse_args()

def main():
    prog = intCodeClass.Program(args.code)
    prog.run(i=instr_in, o=instr_out)

def instr_out(p):
    print(p)

def instr_in():
    print("Provide input:", flush=True)
    return int(sys.stdin.readline().strip('\n'))

if __name__ == "__main__":
    main()
