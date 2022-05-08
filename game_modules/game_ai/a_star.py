from functools import cache
from math import sqrt
from queue import PriorityQueue

import numpy as np

from test_functions import time_it, time_it_min

VERBOSE = False


@time_it_min(0.003)
def a_star(start: tuple[int, int], goal: tuple[int, int], input_map: list[list[bool]]):
    input_map = np.array(input_map, dtype=bool)
    open_list = PriorityQueue()
    open_list.put((0, start))
    closed = set()
    came_from = {}
    g_score = {start: 0}
    f_score = {start: g_cost(start, goal)}
    path = []
    if VERBOSE:
        print("Starting A* search...")
    while not open_list.empty():
        current = open_list.get()[1]
        if VERBOSE:
            print("Current node:", current)
        if current == goal:
            if VERBOSE:
                print("Goal found!")
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(current)
            path.reverse()
            if VERBOSE:
                print("Path:", path)
            return path
        closed.add(current)
        for neighbor in neighbors(current, input_map):
            if VERBOSE:
                print("Neighbor:", neighbor)
            if neighbor in closed:
                if VERBOSE:
                    print("Neighbor already visited")
                continue
            g_score_step = g_score[current] + 1
            if neighbor not in g_score or g_score_step < g_score[neighbor]:
                if VERBOSE:
                    print("Neighbor is new or better")
                came_from[neighbor] = current
                g_score[neighbor] = g_score_step
                f_score[neighbor] = g_cost(neighbor, goal)
                open_list.put((f_score[neighbor], neighbor))
    return None

@cache
def distance(a: tuple[int, int], b: tuple[int, int], euclidian=False):
    if euclidian:
        return np.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)
    return np.abs(a[0] - b[0]) + np.abs(a[1] - b[1])


def g_cost(node, start):
    return distance(start, node)


def h_cost(node, end):
    return distance(end, node)


def f_cost(start, node, end):
    return g_cost(node, start) + h_cost(node, end)


def passable(node, input_map):
    return input_map[node[0]][node[1]] is True


def neighbors(node, input_map):
    for direction in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        adj_x, adj_y = node[0] + direction[0], node[1] + direction[1]
        if 0 <= adj_x < len(input_map) and 0 <= adj_y < len(input_map[0]) and passable((adj_x, adj_y), input_map):
            yield adj_x, adj_y
