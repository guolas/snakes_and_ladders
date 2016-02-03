#!/bin/python3

import sys

"""
Build the graph including the information of the snakes and the ladders.
The numbering of the positions is 1-based, so first id is 1, and not 0,
careful about this.
The possible positions that can be reached from a given square are given by the
roll of a die, so they could be 1-6 squares away from the starting position.
"""
def build_graph(snakes, ladders):
    G = {}
    for ii in range(100):
        """
        Index starting in 1
        """
        start = ii + 1
        """
        If the node is the beginning of a ladder or a snake, ignore it
        """
        if start in snakes:
            continue
        if start in ladders:
            continue
        G[start] = []
        """
        If this is the last position, finish
        """
        if start == 100:
            break
        """
        For all possible values of the die
        """
        for jj in range(1, 7):
            end = start + jj
            if end > 100:
                break
            """
            The end square is different if `end` is a ladder or a snake
            """
            if end in snakes:
                end = snakes[end]
            if end in ladders:
                end = ladders[end]
            G[start].append(end)
    return G

"""
Get the node with the minimum distance in a list of nodes
"""
def get_node_with_minimum_distance(queue, distances):
    sorted_queue = sorted(queue, key=lambda x:distances[x])
    return sorted_queue[0]

"""
Find the shortest path using Dijkstra's algorithm, as I remember it...
I know that the graph is going to have the nodes labeled with numbers from 1 to
the total number of nodes in the graph.
It is also asumed that the shortest path is alwas calculated from node labeled
as 1.
The distance metric used will be the number of die rolls.
"""
def find_min_number_of_rolls(G):
    """
    Initialize the auxiliary variables used to calculate the shortest path
    """
    distance_to = {}
    whence_to = {}
    unused_nodes = []
    for node in G:
        distance_to[node] = 1e4
        whence_to[node] = -1
        unused_nodes.append(node)

    """
    The first position is the square labeled as 1
    """
    distance_to[1] = 0

    while len(unused_nodes) > 0:
        origin = get_node_with_minimum_distance(unused_nodes, distance_to)
        unused_nodes.remove(origin)
        for destination in G[origin]:
            temp_distance = distance_to[origin] + 1
            if temp_distance < distance_to[destination]:
                distance_to[destination] = temp_distance
                whence_to[destination] = origin

    """
    If the end square was not reached the return value should be -1
    """
    if distance_to[100] == 1e4:
        distance_to[100] = -1
    return distance_to[100]

"""
Get the number of cases
"""
T = int(input().strip())

"""
Go through all the cases
"""
for case in range(T):
    """
    Number of ladders
    """
    L = int(input().strip())
    """
    Read the ladders
    """
    ladders = {}
    for ii in range(L):
        start, end = [int(x) for x in input().strip().split(" ")]
        ladders[start] = end
    """
    Number of snakes
    """
    S = int(input().strip())
    """
    Read the snakes
    """
    snakes = {}
    for ii in range(S):
        start, end = [int(x) for x in input().strip().split(" ")]
        snakes[start] = end
    """
    Form the graph considering the snakes and the ladders
    """
    G = build_graph(snakes, ladders)
    print(str(find_min_number_of_rolls(G)))

