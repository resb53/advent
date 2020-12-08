#!/usr/bin/python3

import sys


class Handheld:
    'A class for running Handheld assembly'

    def __init__(self, incode=[]):
        self.code = incode
        self.acc = 0
        self.ptr = 0
        self.exo = []

    def load(self, newcode):
        self.code = newcode
        return 0

    # For each pass, identify its seat
    def execute(self, start=0):
        self.acc = 0
        self.ptr = start
        self.exo = []

        while self.ptr not in self.exo:
            self.exo.append(self.ptr)

            # Exit gracefully
            if self.ptr == len(self.code):
                return 0

            op = self.code[self.ptr][0]
            arg = self.code[self.ptr][1]

            # Execute step
            if op == 'acc':
                self.acc += arg
                self.ptr += 1

            elif op == 'jmp':
                self.ptr += arg

            elif op == 'nop':
                self.ptr += 1

            else:
                print(f"Unknown argument at pointer {self.ptr}: {arg}",
                      file=sys.stderr)
                return 1

        print(f"Infinite loop at pointer {self.ptr}, acc: {self.acc}",
              file=sys.stderr)
        return 2
