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
        opcode = mem[i]
        # Setup parameter mode array pad with a number of leading zeroes
        prm = list('00000000' + str(opcode))
        opcode = int(prm[-2] + prm[-1])
        #print("\ni:" + str(i) + "; opcode:" + str(opcode) + "; param: " + str(prm))

        # Decide operation based of value of opcode
        if (opcode == 1):
            #print("0:" + str(mem[i]) + "; 1:" + str(mem[i+1]) + "; 2:" + str(mem[i+2]) + "; 3:" + str(mem[i+3]), end='')
            # Check parameter mode for this opcode and use values appropriately
            a = mem[i+1]
            b = mem[i+2]
            if prm[-3] == '0':
                a = mem[mem[i+1]]
                #print ("; p1: " + str(mem[mem[i+1]]), end='')
            if prm[-4] == '0':
                b = mem[mem[i+2]]
                #print ("; p2: " + str(mem[mem[i+2]]), end='')
            if prm[-5] == '1':
                sys.exit("Opcode 1 can be in immediate mode. Update.")
            # Add values
            #print("\nAdding " + str(a) + " and " + str(b) + " and putting in " +  str(mem[i+3]))
            mem[mem[i+3]] = a + b 
            i += 4
        elif (opcode == 2):
            #print("0:" + str(mem[i]) + "; 1:" + str(mem[i+1]) + "; 2:" + str(mem[i+2]) + "; 3:" + str(mem[i+3]), end='')
            # Check parameter mode for this opcode and use values appropriately
            a = mem[i+1]
            b = mem[i+2]
            if prm[-3] == '0':
                a = mem[mem[i+1]]
                #print ("; p1: " + str(mem[mem[i+1]]), end='')
            if prm[-4] == '0':
                b = mem[mem[i+2]]
                #print ("; p2: " + str(mem[mem[i+2]]), end='')
            if prm[-5] == '1':
                sys.exit("Opcode 2 can be in immediate mode. Update.")
            # Multiply values
            #print("\nMultiplying " + str(a) + " and " + str(b) + " and putting in " +  str(mem[i+3]))
            mem[mem[i+3]] = a * b
            i += 4
        elif (opcode == 3):
            # Check parameter mode for this opcode and use values appropriately
            if prm[-3] == '1':
                sys.exit("Opcode 3 can be in immediate mode. Update.")
            # Read input from STDIN. Save it to the address given.
            print('Provide input: ', end='', flush=True)
            inp = int(sys.stdin.readline().rsplit()[0])
            mem[mem[i+1]] = inp
            i += 2
        elif (opcode == 4):
            # Check parameter mode for this opcode and use values appropriately
            if prm[-3] == '1':
                print(mem[i+1], end=' ')
            else:
                print(mem[mem[i+1]], end=' ') 
            i += 2
        else:
            sys.exit("Invalid operator in position " + str(i) + ": " + str(mem[i]))

main()
