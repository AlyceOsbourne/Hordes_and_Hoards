from functools import cache
from queue import PriorityQueue

import numpy as np

VERBOSE = False


def a_star(start: tuple[int, int], goal: tuple[int, int], input_map: list[list[bool]] or np.ndarray, walkable: list, euclidian=False):
    if not isinstance(input_map, np.ndarray):
        input_map = np.array(input_map)
    open_list = PriorityQueue()
    open_list.put((0, start))
    closed = set()
    came_from = {}
    g_score = {start: 0}
    f_score = {start: distance(start, goal, euclidian)}
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
        for neighbor in neighbors(current, input_map, walkable):
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
                f_score[neighbor] = distance(neighbor, goal, euclidian)
                open_list.put((f_score[neighbor], neighbor))
    return None


@cache
def distance(a: tuple[int, int], b: tuple[int, int], euclidian):
    if euclidian:
        return np.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)
    return np.abs(a[0] - b[0]) + np.abs(a[1] - b[1])


def passable(node, input_map, walkable):
    return input_map[node[0]][node[1]] in walkable


def neighbors(node, input_map, walkable):
    for direction in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        adj_x, adj_y = node[0] + direction[0], node[1] + direction[1]
        if 0 <= adj_x < len(input_map) and 0 <= adj_y < len(input_map[0]) and passable((adj_x, adj_y), input_map,
                                                                                       walkable):
            yield adj_x, adj_y


# tests
def test():
    import copy
    width, height = 10, 10
    template = [
        [1] * width,
        *[[1, *[0] * (width - 2), 1] for _ in range(height - 2)],
        [1] * width,
    ]
    for _ in range(10):
        test_map = copy.deepcopy(template)
        for i in range(len(test_map)):
            for j in range(len(test_map[0])):
                if np.random.rand() < 0.2:
                    test_map[i][j] = 1
        # pick two random points that are walkable
        start = None
        end = None
        while start is None or not passable(start, test_map, [0]):
            start = (np.random.randint(1, width - 1), np.random.randint(1, height - 1))
        while end is None or not passable(end, test_map, [0]) or start == end or distance(start, end) < min(width // 2, height // 2):
            end = (np.random.randint(1, width - 1), np.random.randint(1, height - 1))

        path = a_star(start, end, test_map, [0])
        if path is None:
            print("No path found")
            continue
        # draw map with path with ansi colors
        for i in range(len(test_map)):
            for j in range(len(test_map[0])):
                if (i, j) == start:
                    print("\033[0;41m \033[0m", end="")
                elif (i, j) == end:
                    print("\033[0;43m \033[0m", end="")
                elif (i, j) in path:
                    print("\033[0;42m \033[0m", end="")
                elif test_map[i][j] == 0:
                    print(" ", end="")
                else:
                    print("#", end="")
            print()


if __name__ == "__main__":
    test()
