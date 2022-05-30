import random
from collections import deque
from functools import reduce, cache
import numpy as np
from utils.testing_tools import time_it_min


@time_it_min(30)
def voronoi(sites: list[tuple[int, int]], width: int, height: int):
    # filter sites and assign index
    sites = {
        site: i
        for i, site
        in enumerate(
            [
                site
                for site in set(sites)
                if 0 <= site[0] < width
                and 0 <= site[1] < height
            ],
            1
        )
    }
    # create map_grid
    voronoi_array = np.zeros((width, height), dtype=int)

    def subdivide_quad(x1, y1, x2, y2):
        mx = x1 + (x2 - x1) // 2
        my = y1 + (y2 - y1) // 2
        return [
            # top left          top right
            (x1, y1, mx, my), (mx, y1, x2, my),
            # bottom left       bottom right
            (x1, my, mx, y2), (mx, my, x2, y2),
        ]

    quad_queue = deque([quad for quad in subdivide_quad(0, 0, width, height)])

    @cache
    def distance(a, b):
        return np.linalg.norm(np.array(a) - np.array(b))

    # this can actually be done asynchronously? as no quads will touch other quads
    def process_quad(x1, y1, x2, y2):
        # quad isn't the size of 1x1
        if x2 - x1 > 1 and y2 - y1 > 1:
            corner_sites = [set() for _ in range(4)]
            for i, corner in enumerate([(x1, y1), (x2, y1), (x1, y2), (x2, y2)]):
                corner_sites[i].add(
                    sites[min(sites, key=lambda site: distance(site, corner))]
                )
            # intersection of the corners
            intersection = reduce(set.intersection, corner_sites)
            if len(intersection) != 1:
                quad_queue.extend(subdivide_quad(x1, y1, x2, y2))
            else:
                found = next(iter(intersection))
                voronoi_array[x1:x2, y1:y2] = found
        else:
            found = sites[min(sites, key=lambda site: distance(site, (x1, y1)))]
            voronoi_array[x1:x2, y1:y2] = found

    while quad_queue:
        x1, y1, x2, y2 = quad_queue.popleft()
        process_quad(x1, y1, x2, y2)
    return voronoi_array, sites


def draw_voronoi(voronoi_diagram: np.ndarray, sites: dict):
    colour_map = {
        site: (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        for site
        in sites.values()
    }
    # add black for 0
    colour_map[0] = (0, 0, 0)
    for row in voronoi_diagram:
        for node in row:
            r, g, b = colour_map[node]
            print(f"\033[48;2;{r};{g};{b}m   \033[0m", end="")
        print()


def print_voronoi(voronoi_diagram: np.ndarray):
    for row in voronoi_diagram:
        for node in row:
            print(f"{node:2} ", end="")
        print()


if __name__ == "__main__":
    width, height = 720 // 10, 1080 // 10
    mod = 10
    jitter = 3
    # place sites in to create a hexagonal pattern
    sites_in = [
        (i + random.randint(-jitter, jitter), j + random.randint(-jitter, jitter))
        for i in range(0, width, width // mod)
        for j in range(0, height, height // mod)
    ]
    print(f"{len(sites_in)} sites")
    voronoi_diagram, sites_out = voronoi(sites_in, width, height)
    draw_voronoi(voronoi_diagram, sites_out)
