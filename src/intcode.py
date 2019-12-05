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
        cmd = line.rsplit()[0]

        # Split command string into list of instructions
        initmem = cmd.split(',')
        initmem = [int(x) for x in initmem]

        # Reset after alarm
        #noun = 12
        #verb = 2

        # Set inputs and run
        #for noun in range(100):
        #    for verb in range(100):
        #        mem = initmem.copy() #reinitisalise
        #        mem[1] = noun
        #        mem[2] = verb
        #        operate(mem)
        #        print("Noun: " + str(noun) + ", Verb: " + str(verb) + ", Output: " + str(mem[0]))

        operate(initmem)

def operate(mem):
    # Iterate through list
    i = 0;

    while (mem[i] != 99):
        #print("i:" + str(i) + "; mem:" + str(mem))
        # Decide operation based of value in first field
        if (mem[i] == 1):
            # Add values
            mem[mem[i+3]] = mem[mem[i+1]] + mem[mem[i+2]]
            i += 4
        elif (mem[i] == 2):
            # Multiply values
            mem[mem[i+3]] = mem[mem[i+1]] * mem[mem[i+2]]
            i += 4
        elif (mem[i] == 3):
            # Read input from STDIN. Save it to the address given.
            print('Provide input: ', end='', flush=True)
            inp = int(sys.stdin.readline().rsplit()[0])
            mem[mem[i+1]] = inp
            i += 2
        elif (mem[i] == 4):
            print(mem[mem[i+1]], end='')
            i += 2
        else:
            sys.exit("Invalid operator in position " + str(i) + ": " + str(mem[i]))

main()
