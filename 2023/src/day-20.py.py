#!/usr/bin/env python3

import argparse
import sys
from collections import Counter

# Check correct usage
parser = argparse.ArgumentParser(description="Parse some data.")
parser.add_argument('input', metavar='input', type=str,
                    help='Input data file.')
args = parser.parse_args()

switches = {}
connections = {}
pulses = Counter()


class Switch():
    def __init__(self, name):
        self.name = name
        self.type = "Switch"
        self.state = None
        self.inputs = []
        self.outputs = []

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def addInput(self, input):
        if self.inputs is not None:
            self.inputs.append(input)
        else:
            raise ValueError(f"Unable to add inputs to switches of type: {self.type}.")

    def addOutput(self, output):
        self.outputs.append(output)

    def receive(self, signal, source):
        # print(f"{self.name} received {"low" if not signal else "high"} from {source}")
        pass

    def send(self):
        if len(self.outputs) > 0:
            print(f"{self.name} -{"low" if not self.state else "high"}-> {self.outputs}")
        for switch in self.outputs:
            pulses[self.state] += 1
            switch.receive(self.state, self)
        return self.outputs


class Broadcast(Switch):
    def __init__(self, name):
        self.name = name
        self.type = "Broadcast"
        self.state = False
        self.inputs = None
        self.outputs = []

    def receive(self, signal):
        self.state = signal


class Flip(Switch):
    def __init__(self, name):
        self.name = name
        self.type = "Flip-Flop"
        self.state = False  # Off = low pulse
        self.inputs = []
        self.outputs = []

    def receive(self, signal, source):
        if source not in self.inputs:
            sys.exit(f"Attempted send from switch not in inputs: {source} -> {self}")
        else:
            if not signal:
                self.state = not self.state


class Conj(Switch):
    def __init__(self, name):
        self.name = name
        self.type = "Flip-Flop"
        self.state = True  # All inputs high = low pulse, else high pulse
        self.memory = []
        self.inputs = []
        self.outputs = []

    def addInput(self, input):
        self.inputs.append(input)
        self.memory.append(False)

    def receive(self, signal, source):
        if source not in self.inputs:
            sys.exit(f"Attempted send from switch not in inputs: {source} -> {self}")
        else:
            i = self.inputs.index(source)
            self.memory[i] = signal
            for x in self.memory:
                if not x:
                    self.state = True
                    return
            self.state = False


# Parse the input file
def parseInput(inp):
    try:
        input_fh = open(inp, 'r')
    except IOError:
        sys.exit("Unable to open input file: " + inp)

    for line in input_fh:
        line = line.rstrip()
        lhs, rhs = line.split(" -> ")
        outputs = rhs.split(", ")
        switch = None
        match lhs[0]:
            case "b":
                switch = Broadcast("broadcaster")
            case "%":
                switch = Flip(lhs[1:])
            case "&":
                switch = Conj(lhs[1:])
            case _:
                sys.exit(f"Invalid switch parsed: {lhs}")

        switches[switch.name] = switch
        connections[switch.name] = outputs

    for source in connections:
        for output in connections[source]:
            if output not in switches:
                switches[output] = Switch(output)
                print(f"Output: {output}")
            switches[output].addInput(switches[source])
            switches[source].addOutput(switches[output])


# For each pass, identify its seat
def processData():
    for _ in range(4):
        print("===============")
        pulses[False] += 1
        switches["broadcaster"].receive(False)
        nextswitches = set(switches["broadcaster"].send())
        while len(nextswitches) > 0:
            print("---------------")
            iterate = set()
            for switch in nextswitches:
                iterate.update(switch.send())
            nextswitches = iterate
    return pulses


# Process harder
def processMore():
    return False


def main():
    parseInput(args.input)

    # Part 1
    print(f"Part 1: {processData()}")

    # Part 2
    print(f"Part 2: {processMore()}")


if __name__ == "__main__":
    main()
