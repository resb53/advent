#!/usr/bin/python3

# intcode.py but with Class!

import os
import sys
import argparse

class Program:
    def __init__(self, fh, args=''):
        # Globals
        self.mem = []        # Internal memory
        self.prog_inputs = 0 # Counts inputs received
        self.pnt = 0         # Program pointer
        self.rel = [0]       # Program rel pointer
        self.iom = {}         # input/output method dict
        self.args = args
        # Init
        self.init(fh)

    def init(self, fh):
        # Parse memory
        try:
            instr_fh = open(fh, 'r')
        except IOError:
            sys.exit("Unable to open input file: " + fh)

        # Parse instructions in file. Allow for multiline just in case future need.
        for line in instr_fh:
            cmd = line.rsplit()[0]

            # Split command string into list of instructions
            self.mem = cmd.split(',')
            self.mem = [int(x) for x in self.mem]

    def __readin(self): # Define input reading behaviour
        if os.isatty(0):
            print('Provide input: ', end='', flush=True)
        if prog_inputs == 0 and args.p is not None:
            inp = args.p
        else:
            inp = int(sys.stdin.readline().rsplit()[0])
        return inp

    def __printout(self, p): # Define output reading behaviour
        print(p, flush=True)

    def run(self, i=__readin, o=__printout):
        self.iom['input'] = i
        self.iom['output'] = o

        while (self.mem[self.pnt] != 99):
            opcode = self.mem[self.pnt]
            # Setup parameter mode array pad with a number of leading zeroes
            pmode = list(str(opcode))
            opcode = int(''.join(pmode[-2:]))
            pmode = pmode[0:-2]
            # Switch back to int
            pmode = [int(x) for x in pmode]
            # Pad with zeroes
            while len(pmode) < self.__op[opcode][1]:
                pmode.insert(0,0)
            # Process instruction based on opcode
            if opcode in self.__op:
                self.pnt = self.__operate(opcode,pmode)
            else:
                sys.exit("Invalid operator in position " + str(self.pnt) + ": " + str(self.mem[self.pnt]))

    def __operate(self, opc, prm):
        # Check parameter mode for this opcode and use values appropriately
        params = []

        for j in range(1,len(prm)+1):
            # write to the field specified
            if self.__op[opc][2][j-1] == 'w':
                self.__extmem(self.pnt+j)
                if prm[len(prm)-j] != 2:
                    params.append(self.mem[self.pnt+j])
                else:
                    params.append(self.rel[0]+self.mem[self.pnt+j])
            # else pull correct value
            elif prm[len(prm)-j] == 0: # position mode
                self.__extmem(self.mem[self.pnt+j])
                params.append(self.mem[self.mem[self.pnt+j]])
            elif prm[len(prm)-j] == 1: # immediate mode
                self.__extmem(self.pnt+j)
                params.append(self.mem[self.pnt+j])
            elif prm[len(prm)-j] == 2: # relative mode
                self.__extmem(self.rel[0]+self.mem[self.pnt+j])
                params.append(self.mem[self.rel[0]+self.mem[self.pnt+j]])
            else:
                sys.exit("Invalid parameter mode in: " + str(prm))

        return self.__op[opc][0](self, params)

    def __extmem(self, v): # Extend memory up to an including index v
        while v >= len(self.mem):
            self.mem.append(0)
    

    def __op01(self, param): # Add 2 parameters, place in 3rd
        self.__extmem(param[2])
        self.mem[param[2]] = param[0] + param[1] 
        return self.pnt+4

    def __op02(self, param): # Multiply 2 parameters, place in 3rd
        self.__extmem(param[2])
        self.mem[param[2]] = param[0] * param[1]
        return self.pnt+4

    def __op03(self, param): # Take input, place in parameter
        self.prog_inputs += 1
        self.__extmem(param[0])
        self.mem[param[0]] = self.iom['input']()
        return self.pnt+2

    def __op04(self, param): # Output parameter
        self.iom['output'](param[0])
        return self.pnt+2

    def __op05(self, param): # Jump to 2nd parameter if first is non-zero else do nothing
        if param[0] == 0:
            return self.pnt+3
        else:
            return param[1]

    def __op06(self, param): # Jump to 2nd parameter if first is zero else do nothing
        if param[0] == 0:
            return param[1]
        else:
            return self.pnt+3

    def __op07(self, param): # If 1st param less than 2nd, store 1 in position given by 3rd, else store 0
        self.__extmem(param[2])
        if param[0] < param[1]:
            self.mem[param[2]] = 1
        else:
            self.mem[param[2]] = 0
        return self.pnt+4

    def __op08(self, param): # If 1st param equals 2nd, store 1 in position given by 3rd, else store 0
        self.__extmem(param[2])
        if param[0] == param[1]:
            self.mem[param[2]] = 1
        else:
            self.mem[param[2]] = 0
        return self.pnt+4

    def __op09(self, param): # Adjust relative base by value of parameter
        self.rel[0] += param[0]
        return self.pnt+2

    # Declare opcodes, and how many parameters they take
    __op = {
            1: [__op01,3,['r','r','w']],
            2: [__op02,3,['r','r','w']],
            3: [__op03,1,['w']],
            4: [__op04,1,['r']],
            5: [__op05,2,['r','r']],
            6: [__op06,2,['r','r']],
            7: [__op07,3,['r','r','w']],
            8: [__op08,3,['r','r','w']],
            9: [__op09,1,['r']]
    }

def main(args):
    prog = Program(args.run, args)
    prog.run()

if __name__ == "__main__":
    # Check correct usage
    parser = argparse.ArgumentParser(description="Ship's intcode computer.")
    parser.add_argument('-n', metavar='name', type=str, help='Optionally name the process for error messages.')
    parser.add_argument('-p', metavar='phase', type=int, help='Optionally specify the phase for the program.')
    parser.add_argument('run', metavar='programme_file', type=str, help='Specify the program for the computer run.')
    args = parser.parse_args()

    main(args)
