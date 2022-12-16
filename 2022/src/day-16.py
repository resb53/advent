#!/usr/bin/env python3

import argparse
import sys
import networkx as nx
import re
import copy
from itertools import combinations

# Check correct usage
parser = argparse.ArgumentParser(description="Parse some data.")
parser.add_argument('input', metavar='input', type=str,
                    help='Input data file.')
args = parser.parse_args()

data = []


# Parse the input file
def parseInput(inp):
    try:
        input_fh = open(inp, 'r')
    except IOError:
        sys.exit("Unable to open input file: " + inp)

    for line in input_fh:
        match = re.match(r"^Valve ([A-Z]{2}) has flow rate=(\d+); tunnels? leads? to valves? (.+)\n$", line)

        if match is not None:
            data.append([match[1], int(match[2]), match[3].split(", ")])


# Build cave map - it's never worth stopping at or turning on a valve when the valve = 0
def caveMap():
    G = nx.Graph()
    zeroes = []

    for paths in data:
        G.add_node(paths[0], flow=paths[1])
        G.add_edges_from([(paths[0], x, {"weight": 1}) for x in paths[2]])

    for node in G.nodes():
        if node != "AA" and G.nodes[node]["flow"] == 0:
            zeroes.append(node)

    for node in zeroes:
        for connect in combinations(G.neighbors(node), 2):
            if connect not in G.edges():
                G.add_edge(connect[0], connect[1], weight=nx.shortest_path_length(G, connect[0], connect[1], "weight"))
            G.remove_node(node)

    for connect in combinations(G.neighbors("AA"), 2):
        if connect not in G.edges():
            G.add_edge(connect[0], connect[1], weight=nx.shortest_path_length(G, connect[0], connect[1], "weight"))

    return G


def getNextNode(G: nx.Graph, pos: str, todo: set):
    nodes = set()
    for node in G.neighbors(pos):
        if node in todo:
            nodes.add(node)
    if len(nodes) == 0:
        for node in todo:
            nodes.add(node)
    return nodes


# Find route that releases the most pressure in 30 minutes
def processData(caves: nx.Graph):
    routes = [[["AA", 0], 0, 0, 0, set(caves.nodes())]]
    routes[0][4].remove("AA")
    results = []
    maxtime = 30

    for _ in range(len(caves.nodes())):
        if len(routes) == 0:
            break
        previous = routes
        routes = []
        for route in previous:
            # Advance time till next valve opened
            pos = route[0][0]
            time = route[1] + route[0][1]
            released = route[2] + (route[0][1] * route[3])
            flow = route[3] + caves.nodes[pos]["flow"]
            # Check time
            if time >= maxtime:
                results.append(route[2] + ((maxtime - route[1]) * route[3]))
            else:
                if len(route[4]) > 0:
                    for node in getNextNode(caves, pos, route[4]):
                        path = [node, nx.shortest_path_length(caves, pos, node, "weight") + 1]
                        notopen = set(route[4] - {node})
                        routes.append([path, time, released, flow, notopen])
                else:
                    results.append(released + ((maxtime - time) * flow))

    print(f"Part 1: {max(results)}")


# Work with an elephant for 26 minutes
def processMore(caves: nx.Graph):
    routes = [[["AA", 0], ["AA", 0], 0, 0, 0, set(caves.nodes())]]
    routes[0][5].remove("AA")
    results = []
    maxtime = 26

    for _ in range(len(caves.nodes())):
        if len(routes) == 0:
            break
        previous = routes
        routes = []
        for route in previous:
            # Advance time till next valve opened
            me = copy.copy(route[0])
            ele = copy.copy(route[1])
            advance = min(me[1], ele[1])
            time = route[2] + advance
            me[1] -= advance
            ele[1] -= advance
            released = route[3] + (advance * route[4])
            flow = route[4]
            if me[1] == 0:
                flow += caves.nodes[me[0]]["flow"]
            if ele[1] == 0:
                flow += caves.nodes[ele[0]]["flow"]
            # Check time
            if time >= maxtime:
                results.append(route[3] + ((maxtime - route[2]) * route[4]))
            else:
                if len(route[5]) > 0:
                    if ele[1] != 0:
                        for node in getNextNode(caves, me[0], route[5]):
                            path = [node, nx.shortest_path_length(caves, me[0], node, "weight") + 1]
                            notopen = set(route[5] - {node})
                            routes.append([path, [ele[0], ele[1]], time, released, flow, notopen])
                    elif me[1] != 0:
                        for node in getNextNode(caves, ele[0], route[5]):
                            path = [node, nx.shortest_path_length(caves, ele[0], node, "weight") + 1]
                            notopen = set(route[5] - {node})
                            routes.append([[me[0], me[1]], path, time, released, flow, notopen])
                    else:
                        for menode in getNextNode(caves, me[0], route[5]):
                            for elenode in getNextNode(caves, ele[0], set(route[5] - {menode})):
                                mepath = [menode, nx.shortest_path_length(caves, me[0], menode, "weight") + 1]
                                elepath = [elenode, nx.shortest_path_length(caves, ele[0], elenode, "weight") + 1]
                                notopen = set(route[5] - {menode} - {elenode})
                                routes.append([mepath, elepath, time, released, flow, notopen])
                else:
                    released += (maxtime - time) * flow
                    if me[1] > 0:
                        released += (maxtime - time - me[1]) * (caves.nodes[me[0]]["flow"])
                        print(flow + caves.nodes[me[0]]["flow"])
                    if ele[1] > 0:
                        released += (maxtime - time - ele[1]) * (caves.nodes[ele[0]]["flow"])
                        print(flow + caves.nodes[ele[0]]["flow"])
                    results.append(released)

    print(f"Part 2: {max(results)}")


def main():
    parseInput(args.input)
    caves = caveMap()

    # Part 1
    processData(caves)

    # Part 2
    processMore(caves)


if __name__ == "__main__":
    main()
