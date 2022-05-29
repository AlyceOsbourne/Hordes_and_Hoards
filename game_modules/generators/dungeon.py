import random

import numpy as np
from numpy.random import shuffle

from .lazy_flood_fill import lazy_flood_fill, draw_flood
from .a_star import a_star, distance
from itertools import combinations


def generate(size, num_rooms):
    sites = {}
    x_len = (list(range(size[0]//5, size[0] - size[0]//5)))
    y_len = (list(range(size[1]//5, size[1] - size[1]//5)))
    for i in range(1, num_rooms+1):
        # if sites len is 0, pick and add any point
        if len(sites) == 0:
            site = np.random.randint(1, size[0] - 1), np.random.randint(1, size[1] - 1)
            print("adding site:", site)
            sites[i] = site
        else:
            # now find sites that are a minimum of size divided by the num of rooms away from all other sites
            # we do this by finding using ranges
            site = None
            min_dist_x, min_dist_y = (size[0] // num_rooms) * 4, (size[1] // num_rooms) * 4
            for x in sorted(x_len, key=lambda _: random.random()):
                for y in sorted(y_len, key=lambda _: random.random()):
                    if (x, y) not in sites.values():
                        dist = min([distance(s, (x, y), False) for s in sites.values()])
                        if dist >= min_dist_x and dist >= min_dist_y:
                            site = x, y
                            break
                if site is not None:
                    break
            if site is None:
                print("no site found")
                break
            print("adding site:", site)
            sites[i] = site

    print("sites:", sites)
    for x in range(size[0]):
        for y in range(size[1]):
            if (x, y) in sites.values():
                print("X", end="")
            else:
                print(".", end="")
        print()

    grid = np.zeros(size)
    for index, site in sites.items():
        lazy_flood_fill(grid, site, index, 0.01, False)


    entrance = None
    while entrance is None:
        # select a coordinate that is on one of the edges and is not already assigned
        # can be anything on the first row or column
        x = random.randint(0, size[0] - 1)
        y = random.randint(0, size[1] - 1) if x == 0 or x == size[0] - 1 else random.choice([0, size[1] - 1])
        if (x, y) not in sites.values():
            entrance = x, y
    print("entrance:", entrance)
    # find closes toom to entrance
    closest_dist = size[0] * size[1]
    closest_room = 1
    for i in range(num_rooms):
        if i not in sites.keys():
            continue
        dist = distance(entrance, sites[i], False)
        if dist < closest_dist:
            closest_room = i
            closest_dist = dist
    path = a_star(sites[closest_room], entrance,grid, [0, closest_room], True)
    for (x, y) in path:
        if grid[x, y] == 0:
            lazy_flood_fill(grid, (x, y), -1, 7, True)

    # now create random site pairs
    # we need the coordinates of the sites to create paths
    site_pairs = list(combinations(sites.keys(), 2))
    print("site pairs:", site_pairs)
    site_pairs = random.choices(site_pairs, k=min(len(site_pairs), int(num_rooms//2)))
    # check to see if any rooms are not in the pairs, if so create a pair for that room
    for i in range(num_rooms):
        if i not in [p[0] for p in site_pairs] and i not in [p[1] for p in site_pairs]:
            site_pairs.append((i, random.choice(list(sites.keys()))))

    print("site pairs:", site_pairs)
    for site_index_a, site_index_b in site_pairs:
        print("site_index_a:", site_index_a, "site_index_b:", site_index_b)
        if site_index_a not in sites.keys() or site_index_b not in sites.keys():
            print("skipping")
            continue
        path = a_star(sites[site_index_a], sites[site_index_b], grid, [0, site_index_a, site_index_b], True)
        print("path:", path)
        if path is not None:
            for x, y in path:
                if grid[x, y] == site_index_a or grid[x, y] == site_index_b:
                    continue
                if grid[x, y] == -1:
                    if random.random() < 0.3:
                        continue # just so paths don't get so thicc
                lazy_flood_fill(grid, (x, y), -1, 10, True)
    draw_flood(grid)





