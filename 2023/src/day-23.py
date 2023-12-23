#!/usr/bin/env python3

import argparse
import sys
import networkx as nx

# Check correct usage
parser = argparse.ArgumentParser(description="Parse some data.")
parser.add_argument('input', metavar='input', type=str,
                    help='Input data file.')
args = parser.parse_args()

sys.setrecursionlimit(20000)


# Parse the input file
def parseInput(inp):
    try:
        input_fh = open(inp, 'r')
    except IOError:
        sys.exit("Unable to open input file: " + inp)

    # Setup nodes
    G = nx.DiGraph()

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

    return G, [start for start in G.nodes() if start.imag == 0][0], [end for end in G.nodes() if end.imag == y - 1][0]


# Find a unique route through the maze
def getRoutes(G, start, finish, route, routes):
    for x in nx.neighbors(G, start):
        if x not in route:
            localroute = route.copy()
            localroute.append(x)
            if "weight" in G[start][x]:
                localroute[0] += G[start][x]["weight"]
            if x == finish:
                routes.append(localroute)
            else:
                getRoutes(G, x, finish, localroute, routes)


# Find most scenic route that doesn't repeat a node
def processData(G, start, finish):
    routes = []
    route = [0]
    getRoutes(G, start, finish, route, routes)
    longest = max([len(x) for x in routes]) - 1

    return longest


# Collapse edges between "hallway" nodes
def collapse(G):
    criticalNodes = [node for node in G.nodes() if len(list(nx.neighbors(G, node))) != 2]
    for node in criticalNodes:
        destinations = list(G.neighbors(node))
        for dest in destinations:
            while dest not in criticalNodes:
                # Find and collapse path to next critical node
                weight = G[node][dest]["weight"]
                subs = [x for x in G.neighbors(dest) if x != node][0]
                nx.contracted_edge(G, (node, dest), self_loops=False, copy=False)
                G[node][subs]["weight"] += weight
                dest = subs


# With reverse slopes
def processMore(G, start, finish):

    NG = nx.Graph()
    NG.add_nodes_from(G)

    # Setup edges
    adj = [-1j, 1, 1j, -1]
    for node in NG:
        for move in adj:
            if node + move in NG:
                NG.add_edge(node, node + move, weight=1)

    # Collapse Graph
    collapse(NG)

    # Calculate Route
    routes = []
    route = [0]
    getRoutes(NG, start, finish, route, routes)
    longest = max([x[0] for x in routes])

    return longest


def main():
    G, start, finish = parseInput(args.input)

    # Part 1
    print(f"Part 1: {processData(G, start, finish)}")

    # Part 2
    print(f"Part 2: {processMore(G, start, finish)}")


if __name__ == "__main__":
    main()
