#!/usr/bin/env python3

import argparse
import sys
import networkx as nx

# Check correct usage
parser = argparse.ArgumentParser(description="Parse some data.")
parser.add_argument('input', metavar='input', type=str,
                    help='Input data file.')
args = parser.parse_args()

G = nx.DiGraph()
sys.setrecursionlimit(20000)


# Parse the input file
def parseInput(inp):
    try:
        input_fh = open(inp, 'r')
    except IOError:
        sys.exit("Unable to open input file: " + inp)

    # Setup nodes
    y = 0
    for line in input_fh:
        line = line.rstrip()
        for x, val in enumerate(line):
            if val in ".^>v<":
                G.add_node(complex(x, y), type=val)
        y += 1

    # Setup edges
    adj = [-1j, 1, 1j, -1]
    for node in G:
        for move in adj:
            if node + move in G:
                ptype = G.nodes[node]["type"]
                ntype = G.nodes[node + move]["type"]
                # Doesn't look like any double slopes, report if not
                if ptype == "." and ntype == ".":
                    G.add_edge(node, node + move)
                    G.add_edge(node + move, node)
                elif ptype == "^" and ntype == ".":
                    if move == -1j:
                        G.add_edge(node, node + move)
                elif ptype == ">" and ntype == ".":
                    if move == 1:
                        G.add_edge(node, node + move)
                elif ptype == "v" and ntype == ".":
                    if move == 1j:
                        G.add_edge(node, node + move)
                elif ptype == ">" and ntype == ".":
                    if move == -1:
                        G.add_edge(node, node + move)
                elif ptype == "." and ntype == "^":
                    if move == -1j:
                        G.add_edge(node, node + move)
                elif ptype == "." and ntype == ">":
                    if move == 1:
                        G.add_edge(node, node + move)
                elif ptype == "." and ntype == "v":
                    if move == 1j:
                        G.add_edge(node, node + move)
                elif ptype == "." and ntype == "<":
                    if move == -1:
                        G.add_edge(node, node + move)

    return [start for start in G.nodes() if start.imag == 0][0], [end for end in G.nodes() if end.imag == y - 1][0]


# Find a unique route through the maze
def getRoutes(start, finish, route, routes):
    for x in nx.neighbors(G, start):
        if x not in route:
            localroute = route.copy()
            localroute.append(x)
            if x == finish:
                routes.append(localroute)
            else:
                getRoutes(x, finish, localroute, routes)


# Find most scenic route that doesn't repeat a node
def processData(start, finish):
    routes = []
    route = []
    getRoutes(start, finish, route, routes)
    longest = max([len(x) for x in routes])
    '''
    for i in range(longest):
        print(f"{i+1}:", end="")
        for r in routes:
            if i < len(r):
                print(f"\t{r[i]}".expandtabs(10), end="")
            else:
                print("\t".expandtabs(10), end="")
        print()
    '''

    return longest


# Process harder
def processMore():
    return False


def main():
    start, finish = parseInput(args.input)

    # Part 1
    print(f"Part 1: {processData(start, finish)}")

    # Part 2
    print(f"Part 2: {processMore()}")


if __name__ == "__main__":
    main()
