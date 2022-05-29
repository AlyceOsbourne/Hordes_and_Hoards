import random

import numpy as np

from game_modules.generators.lazy_flood_fill import lazy_flood_fill, draw_flood
from game_modules.generators.voronoi import voronoi, draw_voronoi


# generate a voronoi diagram
def generate_voronoi(map_size, seed, jitter=3, mod=10):
    random.seed(seed)
    width, height = map_size
    # generate random sites on the map_template
    sites = [
        (i + random.randint(-jitter, jitter), j + random.randint(-jitter, jitter))
        for i in range(0, width, width // mod)
        for j in range(0, height, height // mod)
    ]
    # generate the voronoi diagram
    return voronoi(sites, *map_size)


# create flood fill map_template from selected sites
def generate_flood_fill(map_size, sites, decay):
    map = np.zeros(map_size, dtype=int)
    for (i, j), index in sites.items():
        lazy_flood_fill(map, (i, j), index, decay)
    return map


if __name__ == "__main__":
    size = (30, 30)
    v, s = generate_voronoi(size, 2, 3, 5)
    draw_voronoi(v, s)
    print()
    f = generate_flood_fill(size, s, .13)
    draw_flood(f)
