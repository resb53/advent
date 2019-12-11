#!/usr/bin/python3

import os
import sys
import argparse

# Check correct usage
parser = argparse.ArgumentParser(description="Ship's intcode computer.")
parser.add_argument('-n', metavar='name', type=str, help='Optionally name the process for error messages.')
parser.add_argument('-p', metavar='phase', type=int, help='Optionally specify the phase for the program.')
parser.add_argument('run', metavar='programme_file', type=str, help='Specify the program for the computer run.')
args = parser.parse_args()

# Globals
mem = []     # Internal memory
prog_inputs = 0 # Counts inputs received
pnt = 0         # Program pointer
rel = [0]       # Program rel pointer

def main():
    global mem, pnt, rel
    # Initialise
    initialise(args.run)
    run()


def initialise(fh):
    global mem
    # Parse memory
    try:
        instr_fh = open(fh,'r')
    except IOError:
        sys.exit("Unable to open input file: " + sys.argv[1])

    # Parse instructions in file. Allow for multiline just in case future need.
    for line in instr_fh:
        cmd = line.rsplit()[0]

        # Split command string into list of instructions
        mem = cmd.split(',')
        mem = [int(x) for x in mem]

def run():
    global mem, pnt, rel

    while (mem[pnt] != 99):
        opcode = mem[pnt]
        # Setup parameter mode array pad with a number of leading zeroes
        pmode = list(str(opcode))
        opcode = int(''.join(pmode[-2:]))
        pmode = pmode[0:-2]
        # Switch back to int
        pmode = [int(x) for x in pmode]
        # Pad with zeroes
        while len(pmode) < op[opcode][1]:
            pmode.insert(0,0)
        # Process instruction based on opcode
        if opcode in op:
            pnt = operate(opcode,pmode)
        else:
            sys.exit("Invalid operator in position " + str(pnt) + ": " + str(mem[pnt]))

def operate(opc,prm):
    global mem, pnt, rel
    # Check parameter mode for this opcode and use values appropriately
    params = []

    for j in range(1,len(prm)+1):
        # write to the field specified
        if op[opc][2][j-1] == 'w':
            extmem(pnt+j)
            if prm[len(prm)-j] != 2:
                params.append(mem[pnt+j])
            else:
                params.append(rel[0]+mem[pnt+j])
        # else pull correct value
        elif prm[len(prm)-j] == 0: # position mode
            extmem(mem[pnt+j])
            params.append(mem[mem[pnt+j]])
        elif prm[len(prm)-j] == 1: # immediate mode
            extmem(pnt+j)
            params.append(mem[pnt+j])
        elif prm[len(prm)-j] == 2: # relative mode
            extmem(rel[0]+mem[pnt+j])
            params.append(mem[rel[0]+mem[pnt+j]])
        else:
            sys.exit("Invalid parameter mode in: " + str(prm))

    return op[opc][0](params)

def extmem(v): # Extend memory up to an including index v
    global mem
    while v >= len(mem):
        mem.append(0)
    

def op01(param): # Add 2 parameters, place in 3rd
    global mem, pnt
    extmem(param[2])
    mem[param[2]] = param[0] + param[1] 
    return pnt+4

def op02(param): # Multiply 2 parameters, place in 3rd
    global mem, pnt
    extmem(param[2])
    mem[param[2]] = param[0] * param[1]
    return pnt+4

def op03(param): # Take input, place in parameter
    global mem, pnt, prog_inputs
    if os.isatty(0):
        print('Provide input: ', end='', flush=True)
    if prog_inputs == 0 and args.p is not None:
        inp = args.p
    else:
        inp = int(sys.stdin.readline().rsplit()[0])
    prog_inputs += 1
    extmem(param[0])
    mem[param[0]] = inp
    # print(args.n + ': inp(' + str(prog_inputs) + ') <- ' + str(inp), file=sys.stderr) #debug
    return pnt+2

def op04(param): # Output parameter
    global pnt
    print(param[0], flush=True)
    #print(args.n + ': ' + str(param[0]), file=sys.stderr) #debug
    return pnt+2

def op05(param): # Jump to 2nd parameter if first is non-zero else do nothing
    global pnt
    if param[0] == 0:
        return pnt+3
    else:
        return param[1]

def op06(param): # Jump to 2nd parameter if first is zero else do nothing
    global pnt
    if param[0] == 0:
        return param[1]
    else:
        return pnt+3

def op07(param): # If 1st param less than 2nd, store 1 in position given by 3rd, else store 0
    global mem, pnt
    extmem(param[2])
    if param[0] < param[1]:
        mem[param[2]] = 1
    else:
        mem[param[2]] = 0
    return pnt+4

def op08(param): # If 1st param equals 2nd, store 1 in position given by 3rd, else store 0
    global mem, pnt
    extmem(param[2])
    if param[0] == param[1]:
        mem[param[2]] = 1
    else:
        mem[param[2]] = 0
    return pnt+4

def op09(param): # Adjust relative base by value of parameter
    global pnt, rel
    rel[0] += param[0]
    return pnt+2

# Declare opcodes, and how many parameters they take
op = {
        1: [op01,3,['r','r','w']],
        2: [op02,3,['r','r','w']],
        3: [op03,1,['w']],
        4: [op04,1,['r']],
        5: [op05,2,['r','r']],
        6: [op06,2,['r','r']],
        7: [op07,3,['r','r','w']],
        8: [op08,3,['r','r','w']],
        9: [op09,1,['r']]
}

if __name__ == "__main__":
    main()
    sys.exit(0)
