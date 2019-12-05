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

    j = i + 1
    for k in range(0,len(prm))[::-1]:
        # write to the field specified
        if op[opc][2][j-i-1] == 'w':
            params.append(mem[j])
        # else pull correct value
        elif prm[k] == '0':
            params.append(mem[mem[j]])
        elif prm[k] == '1':
            params.append(mem[j])
        j += 1

    #print("opcode:" + str(opc) + "; params:" + str(params))

    return op[opc][0](mem,i,params)

def op1(mem,i,param): # Add 2 parameters, place in 3rd
    mem[param[2]] = param[0] + param[1] 
    return i+4

def op2(mem,i,param): # Multiply 2 parameters, place in 3rd
    mem[param[2]] = param[0] * param[1]
    return i+4

def op3(mem,i,param): # Take input, place in parameter
    print('Provide input: ', end='', flush=True)
    inp = int(sys.stdin.readline().rsplit()[0])
    mem[param[0]] = inp
    return i+2

def op4(mem,i,param): # Output parameter
    print(param[0], end=' ')
    return i+2

# Declare opcodes, and how many parameters they take
op = {
        1: [op1,3,['r','r','w']],
        2: [op2,3,['r','r','w']],
        3: [op3,1,['w']],
        4: [op4,1,['r']]
}

if __name__ == "__main__":
    main()
