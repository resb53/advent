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

# Count inputs received
prog_inputs = 0

# Parse memory
try:
    instr_fh = open(args.run,'r')
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
            pmode = list(str(opcode))
            opcode = int(''.join(pmode[-2:]))
            pmode = pmode[0:-2]
            # Pad with zeroes
            while len(pmode) < op[opcode][1]:
                pmode.insert(0,'0')
            # Process instruction based on opcode
            if opcode in op:
                pnt = run(opcode,initmem,pnt,pmode)
            else:
                sys.exit("Invalid operator in position " + str(pnt) + ": " + str(initmem[pnt]))

def run(opc,mem,i,prm):
    # Check parameter mode for this opcode and use values appropriately
    params = []

    #print(str(mem))
    #print("i:" + str(i) + "; prm:" + str(prm))

    j = 1
    for j in range(1,len(prm)+1):
        # write to the field specified
        if op[opc][2][j-1] == 'w':
            params.append(mem[i+j])
        # else pull correct value
        elif prm[len(prm)-j] == '0':
            params.append(mem[mem[i+j]])
        elif prm[len(prm)-j] == '1':
            params.append(mem[i+j])
        j += 1

    #print("opcode:" + str(opc) + "; params:" + str(params))

    return op[opc][0](mem,i,params)

def op01(mem,i,param): # Add 2 parameters, place in 3rd
    mem[param[2]] = param[0] + param[1] 
    return i+4

def op02(mem,i,param): # Multiply 2 parameters, place in 3rd
    mem[param[2]] = param[0] * param[1]
    return i+4

def op03(mem,i,param): # Take input, place in parameter
    global prog_inputs
    if os.isatty(0):
        print('Provide input: ', end='', flush=True)
    if prog_inputs == 0 and args.p is not None:
        inp = args.p
    else:
        inp = int(sys.stdin.readline().rsplit()[0])
    prog_inputs += 1
    mem[param[0]] = inp
    #print(args.n + ': inp(' + str(prog_inputs) + ') <- ' + str(inp), file=sys.stderr) #debug
    return i+2

def op04(mem,i,param): # Output parameter
    print(param[0], flush=True)
    #print(args.n + ': ' + str(param[0]), file=sys.stderr) #debug
    return i+2

def op05(mem,i,param): # Jump to 2nd parameter if first is non-zero else do nothing
    if param[0] == 0:
        return i+3
    else:
        return param[1]

def op06(mem,i,param): # Jump to 2nd parameter if first is zero else do nothing
    if param[0] == 0:
        return param[1]
    else:
        return i+3

def op07(mem,i,param): # If 1st param less than 2nd, store 1 in position given by 3rd, else store 0
    if param[0] < param[1]:
        mem[param[2]] = 1
    else:
        mem[param[2]] = 0
    return i+4

def op08(mem,i,param): # If 1st param equals 2nd, store 1 in position given by 3rd, else store 0
    if param[0] == param[1]:
        mem[param[2]] = 1
    else:
        mem[param[2]] = 0
    return i+4

# Declare opcodes, and how many parameters they take
op = {
        1: [op01,3,['r','r','w']],
        2: [op02,3,['r','r','w']],
        3: [op03,1,['w']],
        4: [op04,1,['r']],
        5: [op05,2,['r','r']],
        6: [op06,2,['r','r']],
        7: [op07,3,['r','r','w']],
        8: [op08,3,['r','r','w']]
}

if __name__ == "__main__":
    main()
    sys.exit(0)
