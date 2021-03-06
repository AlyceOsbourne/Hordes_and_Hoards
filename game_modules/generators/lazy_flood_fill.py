# inspired by: https://www.youtube.com/watch?v=YS0MTrjxGbM
# with some modifications, namely -
#   Using a 3x3 neighbourhood instead of using adjacents
#   Using a method to increase the rate of decay, this is so there is a larger drop off at the edges,
#       this gives us a larger walkable surface in the center, and creates more "wispy" edges
#   I have also excluded the 'visited' list, instead just checking for void spaces, this way it can go back and fill
#       spaces in that had previously not been filled, this just helps to create a less fragmented space which is better
#       suited to cave generation rather than biome placement.
import math
import random
from collections import deque
from itertools import count

import numpy as np


def lazy_flood_fill(grid: np.ndarray,
                    start_point: tuple[int, int],
                    fill_value: int,
                    decay_rate: float,
                    use_cardinal_directions: bool = False,
                    increase_entropy_over_time: bool = True
                    ):
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
            if grid[neighbour] == 0 and chance >= random.randint(0, 100):
                queue.append(neighbour)
                chance -= decay_rate
        if increase_entropy_over_time:
            decay_rate -= 0.00001
            decay_rate = max(min(decay_rate, 99.99999), 0.00001)
            print(f"decay rate: {decay_rate}")
    return grid


def draw_flood(array: np.ndarray, show_values: bool = False):
    palette = {
        -2: (255, 255, 255),
        -1: (50, 50, 50),
        0: (0, 0, 0)
    }
    for row in array:
        for value in row:
            if value not in palette:
                palette[value] = (random.randint(100, 200), random.randint(100, 200), random.randint(100, 200))
            print(
                f"\033[48;2;{palette[value][0]};{palette[value][1]};{palette[value][2]}m{int(value):^4}\033[0m"
                if show_values else f"\033[48;2;{palette[value][0]};{palette[value][1]};{palette[value][2]}m   \033[0m",
                end="")
        print()


if __name__ == "__main__":
    # tart filling map_grid at regular intervals
    width, height = 60, 60
    step_width = width // 3
    step_height = height // 3
    grid = np.zeros((width, height), dtype=int)
    c = count(1)
    for x in range(step_width//2, width-step_width//2, step_height):
        for y in range(step_height//2, height-step_height//2, step_height):
            grid = lazy_flood_fill(grid, (x, y), next(c), decay_rate=.03, use_cardinal_directions=True)
    draw_flood(grid)
