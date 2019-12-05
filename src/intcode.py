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

        # Iterate through memory
        pnt = 0

        while (initmem[pnt] != 99):
            opcode = initmem[pnt]
            # Setup parameter mode array pad with a number of leading zeroes
            pmode = list('00000000' + str(opcode))
            opcode = int(pmode[-2] + pmode[-1])
            # Process instruction based on opcode
            if opcode in opcs:
                pnt = opcs[opcode](initmem,pnt,pmode)
            else:
                sys.exit("Invalid operator in position " + str(pnt) + ": " + str(initmem[pnt]))

def op1(mem,i,prm): # Add 2 parameters, place in 3rd
     # Check parameter mode for this opcode and use values appropriately
    a = mem[i+1]
    b = mem[i+2]
    if prm[-3] == '0':
        a = mem[mem[i+1]]
    if prm[-4] == '0':
        b = mem[mem[i+2]]
    if prm[-5] == '1':
        sys.exit("Opcode 1 can write in immediate mode. Update.")
    # Add values
    mem[mem[i+3]] = a + b 
    return i+4

def op2(mem,i,prm): # Multiply 2 parameters, place in 3rd
     # Check parameter mode for this opcode and use values appropriately
    a = mem[i+1]
    b = mem[i+2]
    if prm[-3] == '0':
        a = mem[mem[i+1]]
    if prm[-4] == '0':
        b = mem[mem[i+2]]
    if prm[-5] == '1':
        sys.exit("Opcode 2 can write in immediate mode. Update.")
    # Multiply values
    mem[mem[i+3]] = a * b
    return i+4

def op3(mem,i,prm): # Take input, place in parameter
    # Check parameter mode for this opcode and use values appropriately
    if prm[-3] == '1':
        sys.exit("Opcode 3 can write in immediate mode. Update.")
    # Read input from STDIN. Save it to the address given.
    print('Provide input: ', end='', flush=True)
    inp = int(sys.stdin.readline().rsplit()[0])
    mem[mem[i+1]] = inp
    return i+2

def op4(mem,i,prm): # Output parameter
    # Check parameter mode for this opcode and use values appropriately
    if prm[-3] == '1':
        print(mem[i+1], end=' ')
    else:
        print(mem[mem[i+1]], end=' ') 
    return i+2

# Declare opcodes
opcs = {
        1: op1,
        2: op2,
        3: op3,
        4: op4
}

if __name__ == "__main__":
    main()
