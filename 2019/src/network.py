#!/usr/bin/python3

import intCode
import argparse
import sys

# Check correct usage
parser = argparse.ArgumentParser(description="Run network code.")
parser.add_argument('code', metavar='code', type=str, help='Int code file.')
args = parser.parse_args()

# Network
comp = [] # Array of computers
network = {} # List of awaiting packets for each computer

def main():
    global comp, network
    prog = intCode.Program(args.code)
    # Prep network messages
    for i in range(50):
        network[i] = i
    print(network)
    #for i in range(50):
        #comp.append(prog.run(i=instr_in, o=instr_out))


def instr_out(p):
    print(p)

def instr_in():
    print("Provide input:", flush=True)
    return int(sys.stdin.readline().strip('\n'))

if __name__ == "__main__":
    main()
