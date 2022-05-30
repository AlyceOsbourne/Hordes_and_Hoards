import random

import numpy as np
from numpy.random import shuffle

from utils.testing_tools import time_it_min

# TODO: make these imports relative for plugin loader
from game_modules.generators.a_star import a_star, distance
from game_modules.generators.lazy_flood_fill import lazy_flood_fill, draw_flood



def generate_sites(size: tuple[int, int], num_rooms: int, margin: int, padding: int, euclidian: bool):
    """
    generates a list of site to propagate as rooms, also used to generate_dungeon corridors
    :param size: size of the map
    :param num_rooms: the number of sites to be generated
    :param margin: distance from border
    :param padding: distance from other rooms
    :param euclidian: whether to use euclidian distance or manhattan
    :return: a list of sites
    """
    sites = {}
    x_len, y_len = (list(range(margin, size[0] - margin))), (list(range(margin, size[1] - margin)))

    for i in range(1, num_rooms + 1):
        # if sites len is 0, pick and add any point
        if len(sites) == 0:
            site = np.random.randint(margin, size[0] - margin), np.random.randint(margin, size[1] - margin)
            sites[i] = site
        else:
            # now find sites that are a minimum of size divided by the num of rooms away from all other sites
            # we do this by finding using ranges
            site = None
            for x in sorted(x_len, key=lambda _: np.random.random()):
                for y in sorted(y_len, key=lambda _: np.random.random()):
                    if (x, y) not in sites.values():
                        dist = min([distance(s, (x, y), euclidian) for s in sites.values()])
                        if dist >= padding:
                            site = x, y
                            break
                if site is not None:
                    break
            if site is None:
                break
            sites[i] = site
    return sites


def generate_entrance_path(size, sites, grid, euclidian):
    """
    generates a path from a cell to the border of the map
    :param size:  size of the map
    :param sites: the points the entrance con be connected too
    :param grid: the map
    :param euclidian: whether to use euclidian distance or manhattan
    :return: a path
    """
    entrance = None
    while entrance is None:
        # select a coordinate that is on one of the edges and is not already assigned
        # can be anything on the first row or column
        x = np.random.randint(0, size[0] - 1)
        y = np.random.randint(0, size[1] - 1) if x == 0 or x == size[0] - 1 else np.random.choice([0, size[1] - 1])
        if (x, y) not in sites.values():
            entrance = x, y
    # find closes toom to entrance
    closest_dist = size[0] * size[1]
    closest_room = 1
    for i in sites.keys():
        dist = distance(entrance, sites[i], False)
        if dist < closest_dist:
            closest_room = i
            closest_dist = dist
    path = a_star(sites[closest_room], entrance, grid, [0, closest_room], euclidian)
    return path


def generate_site_pairs(sites):
    """
    generates a list of site pairs to generate_dungeon corridors between them. tries to ensure everything is connected
    :param sites:
    :return:
    """
    site_pairs = []
    for key in sites.keys():
        for i in range(np.random.randint(2, 3)):
            candidates = [i for i in sites.keys() if i != key]
            # weights is 1 / distances from key
            weights = [1 / distance(sites[key], sites[i], False) for i in candidates]
            pair = None
            while pair is None or pair in site_pairs:
                pair = key, random.choices(candidates, weights=weights, k=1)[0]
            site_pairs.append(pair)
    return set(site_pairs)


def check_map_validity(grid, sites, entrance_path):
    node_vals = set()
    valid = [-2, -1, *sites.keys()]
    for site in sites.values():
        if a_star(entrance_path[0], site, grid, valid, False) is None:
            return False
        else:
            node_vals.add(grid[site[0]][site[1]])
    for key in sites.keys():
        if key not in node_vals:
            return False
    return True


@time_it_min(5)
def generate_dungeon(size, /, num_rooms=10, margin=10, padding=30, room_decay=1000., corridor_decay=0.01,
                     allow_crossing_corridors=True, euclidian_paths=True, cardinal_fill=True, increase_entropy=False):
    """
    Generates a dungeon of the specified size.
    :param size: size of the dungeon
    :param num_rooms: number of rooms to generate_dungeon
    :param margin: margin to add around the dungeon
    :param padding: minimum distance between rooms
    :param room_decay: decay rate for room generation
    :param corridor_decay: decay rate for corridor generation
    :param allow_crossing_corridors: whether to allow corridors to cross each other, allows crossroads in corridors,
    but can lead to corridor bunching
    :param euclidian_paths: whether to use euclidian paths or not, this means paths will follow diagonals too
    :param cardinal_fill: whether to fill in cardinal directions
    :param increase_entropy: whether to increase the entropy of the fill algorithm, over time the decay rate decreases
    in small random increments, gives a more branching appearance
    :return: a dungeon of the specified size
    """
    grid = np.zeros(size, dtype=int)
    sites = generate_sites(size, num_rooms, margin=margin, padding=padding, euclidian=euclidian_paths)
    entrance_path = generate_entrance_path(size, sites, grid, euclidian_paths)
    site_pairs = generate_site_pairs(sites)

    for index, site in sites.items():
        lazy_flood_fill(grid, site, index, (1 / np.random.random()) * room_decay, cardinal_fill, increase_entropy)

    for (x, y) in entrance_path:
        if grid[x, y] == 0:
            lazy_flood_fill(grid, (x, y), -2, (1 / np.random.random()) * corridor_decay, cardinal_fill,
                            increase_entropy)

    for site_index_a, site_index_b in site_pairs:
        pathable = [0, site_index_a, site_index_b]
        if allow_crossing_corridors and np.random.random() < 0.1:
            pathable.append(-1)
        path = a_star(sites[site_index_a], sites[site_index_b], grid, pathable, euclidian_paths)
        if path is None and not allow_crossing_corridors:  # cause sometimes the rule has to be bent
            path = a_star(sites[site_index_b], sites[site_index_a], grid, pathable + [-1], euclidian_paths)
        if path is None:
            continue
        for x, y in path:
            if grid[x, y] == site_index_a or grid[x, y] == site_index_b:
                continue
            if grid[x, y] == -1:
                if np.random.random() < 0.1:
                    continue  # just so paths don't get so thicc
            lazy_flood_fill(grid, (x, y), -1, (1 / np.random.random()) * corridor_decay, cardinal_fill,
                            increase_entropy)
    # TODO!!!! this is a hack, fix it, make this an iterative process rather than a recursive one
    if not check_map_validity(grid, sites, entrance_path):
        # recurse and regenerate
        return generate_dungeon(size, num_rooms=num_rooms, margin=margin, padding=padding, room_decay=room_decay,
                                corridor_decay=corridor_decay, allow_crossing_corridors=allow_crossing_corridors,
                                euclidian_paths=euclidian_paths, cardinal_fill=cardinal_fill,
                                increase_entropy=increase_entropy)
    return grid


if __name__ == "__main__":
    for _ in range(1):
        map_grid = generate_dungeon((200, 200), num_rooms=30, margin=15, padding=35, room_decay=0.003, corridor_decay=5,
                                    allow_crossing_corridors=True, euclidian_paths=True, cardinal_fill=False,
                                    increase_entropy=False)
        for x in range(map_grid.shape[0]):
            for y in range(map_grid.shape[1]):
                print(f"{map_grid[x, y]:^3}" if map_grid[x, y] != 0 else "   ", end="")
            print()
        print()

        draw_flood(map_grid)
