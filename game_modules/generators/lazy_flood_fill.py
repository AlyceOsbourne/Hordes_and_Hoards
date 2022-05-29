# inspired by: https://www.youtube.com/watch?v=YS0MTrjxGbM
# with some modifications, namely -
#   Using a 3x3 neighbourhood instead of using adjacents
#   Using a method to increase the rate of decay, this is so there is a larger drop off at the edges,
#       this gives us a larger walkable surface in the center, and creates more "wispy" edges
#   I have also excluded the 'visited' list, instead just checking for void spaces, this way it can go back and fill
#       spaces in that had previously not been filled, this just helps to create a less fragmented space which is better
#       suited to cave generation rather than biome placement.

import random
from collections import deque
from itertools import count

import numpy as np


def lazy_flood_fill(grid: np.ndarray,
                    start_point: tuple[int, int],
                    fill_value: int,
                    decay_rate: float,
                    use_cardinal_directions: bool = False):
    def get_neighbours(point, cardinal_directions=False):
        x, y = point
        radial = [
            (x - 1, y - 1),
            (x, y - 1),
            (x + 1, y - 1),
            (x - 1, y),
            (x + 1, y),
            (x - 1, y + 1),
            (x, y + 1),
            (x + 1, y + 1)
        ]
        cardinal = [
            # n
            (x, y - 1),
            # s
            (x, y + 1),
            # e
            (x + 1, y),
            # w
            (x - 1, y)
        ]
        neighbours = [n for n in
                      (cardinal
                       if cardinal_directions
                       else radial)
                      if 0 <= n[0] < grid.shape[0]
                      and 0 <= n[1] < grid.shape[1]]
        return neighbours

    chance = 100
    grid[start_point] = fill_value
    queue = deque([start_point])
    while queue:
        point = queue.popleft()
        grid[point] = fill_value
        for neighbour in get_neighbours(point, use_cardinal_directions):
            if grid[neighbour] == 0 \
                    and chance >= random.randint(0, 100) \
                    and chance >= random.randint(0, 100):
                queue.append(neighbour)
                chance -= decay_rate
    return grid


def draw_flood(array: np.ndarray):
    palette = {
        -1: (50, 50, 50),
        0: (0, 0, 0)
    }
    for row in array:
        for value in row:
            if value not in palette:
                palette[value] = (random.randint(50, 250), random.randint(50, 250), random.randint(50, 250))
            print(f"\033[48;2;{palette[value][0]};{palette[value][1]};{palette[value][2]}m   \033[0m", end="")
        print()


if __name__ == "__main__":
    # tart filling grid at regular intervals
    width, height = 60, 60
    step_width = width // 3
    step_height = height // 3
    grid = np.zeros((width, height), dtype=int)
    c = count(1)
    for x in range(step_width//2, width-step_width//2, step_height):
        for y in range(step_height//2, height-step_height//2, step_height):
            grid = lazy_flood_fill(grid, (x, y), next(c), decay_rate=.03, use_cardinal_directions=True)
    draw_flood(grid)
