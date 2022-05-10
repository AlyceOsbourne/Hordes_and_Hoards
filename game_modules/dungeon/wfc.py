"""
Dungeon generator for my game, using the WFC algorithm.
Note, there are still artifacts at this time, I will refine the ruleset over time.
"""
from __future__ import annotations

import random
from collections import Counter, deque

from game_modules.dungeon.tiledata import Tiles, Direction
from test_functions import time_it

VERBOSE = False

sample = "\n".join([
    "░░░░░░░░░░░░░░░░╔═════════════════╗░",
    "░╔╗╔╗░╔══╗░╔══╗░║▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓║░",
    "░╚╝╚╝░║░░║░║▓▓║░║▓╔╗╔╗▓▓▓▓╔╗╔╗▓▓▓▓║░",
    "░╔╗╔╗░║░░║░║▓▓║░║▓╚╬╬╝▓▓▓▓╚╩╩╝▓▓▓▓║░",
    "░╚╝╚╝░╚══╝░╚══╝░║▓╔╬╬╗▓▓▓▓╔╦╦╗▓▓▓▓║░",
    "░░░░░░░░░░░░░░░░║▓╚╝╚╝▓▓▓▓╚╝╚╝▓▓▓▓║░",
    "░╔═╦═╗░░░╔═╦═╗░░║▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓║░",
    "░║░║░║╔╦╗║▓║▓║░░║▓║▓═▓╗▓╔▓╝▓╚▓▓▓▓▓║░",
    "░╠═╬═╣╠╬╣╠═╬═╣░░║▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓║░",
    "░║░║░║╚╩╝║▓║▓║░░║▓▓╦▓╩▓╣▓╠▓╬▓▓▓▓▓▓║░",
    "░╚═╩═╝░░░╚═╩═╝░░║▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓║░",
    "░╔══╦══╗╔══╦══╗░║▓╔╗╔╗▓▓▓▓╔╗╔╗▓▓▓▓║░",
    "░║╔═╩═╗║║╔═╬═╗║░║▓╚╝╚╝▓▓▓▓╚╣╠╝▓▓▓▓║░",
    "░║║▓▓▓║║║║╔╩╗║║░║▓╔╗╔╗▓▓▓▓╔╣╠╗▓▓▓▓║░",
    "░╠╣▓▓▓╠╣╠╬╣▓╠╬╣░║▓╚╝╚╝▓▓▓▓╚╝╚╝▓▓▓▓║░",
    "░║║▓▓▓║║║║╚╦╝║║░║▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓║░",
    "░║╚═╦═╝║║╚═╬═╝║░║╔═╦═╗▓▓▓╔═╦═╗▓▓▓▓║░",
    "░╚══╩══╝╚══╩══╝░║║░║░║╔╦╗║▓║▓║▓▓▓▓║░",
    "░░░╔╗╔╗░░╔╗╔╗░░░║╠═╬═╣╠╬╣╠═╬═╣▓▓▓▓║░",
    "░░░╚╩╩╝░░╚╣╠╝░░░║║░║░║╚╩╝║▓║▓║▓▓▓▓║░",
    "░░░╔╦╦╗░░╔╣╠╗░░░║╚═╩═╝▓▓▓╚═╩═╝▓▓▓▓║░",
    "░░░╚╝╚╝░░╚╝╚╝░░░║▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓║░",
    "░░░╔═╗░░░░╔╗╔╗░░║▓╔╗╔╗▓▓▓▓▓╔═╗▓▓▓▓║░",
    "░░░╚╦╝░░░░║╠╣║░░║▓║╠╣║▓▓▓▓▓╚╦╝▓▓▓▓║░",
    "░░░╔╩╗░░░░╚╝╚╝░░║▓╚╝╚╝▓▓▓▓▓╔╩╗▓▓▓▓║░",
    "░░░╚═╝░░░░░░░░░░║▓▓▓▓▓▓▓▓▓▓╚═╝▓▓▓▓║░",
    "░░╔╗░░░░░░░╔╗░░░║▓╔╦╦╗▓▓▓▓▓▓▓▓▓▓▓▓║░",
    "░░╠╝░░░░░░░╚╣░░░║▓║╠╣║▓▓▓▓▓▓▓▓▓▓▓▓║░",
    "░╔╣░░╔═══╗░░╠╗░░║▓╚╩╩╝▓▓▓▓▓▓▓▓▓▓▓▓║░",
    "░╚╝╔╗╚═══╝╔╗╚╝░░║▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓║░",
    "░░░╚╩╦╗░╔╦╩╝░░░░║▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓║░",
    "╔═══╗╚╝░╚╝╔═══╗░║▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓║░",
    "╚═══╝░░░░░╚═══╝░║▓▓▓◙▓▓▓▓▓▓⌂▓▓▓▓▓▓║░",
    "░░╔╦╦╗░░░╔╗╔╗░░░║▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓║░",
    "░░║╠╣║░░░╚╬╬╝░░░║▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓║░",
    "░░╚╩╩╝░░░╔╬╬╗░░░╚═════════════════╝░",
    "░░░░░░╔╗░╚╝╚╝░░░░░░░░░░░░░░░░░░░░░░░",
    "░░░░░╔╝╚╗░░░░░░░░░░░░░░░░░░░░░░░░░░░",
    "░░░░░╚╗╔╝░░░░░░░░░░░░░░░░░░░░░░░░░░░",
    "░╔═╗░░╚╝░░╔═╗░░░░░░░░░░░░░░░░░░░░░░░",
    "╔╝░╚╗░░░░╔╝▓╚╗░░░░╔═══╗░░░░░░░░░░░░░",
    "║░░░║░░░░║▓▓▓║░░░░║░░░║░╔═╗░░░░░░░░░",
    "╚╗░╔╝░░░░╚╗▓╔╝░░░░║░∩░║░║∩║░░░░░░░░░",
    "░╚═╝░░░░░░╚═╝░░░░░║░║░║░║║║░░░░░░░░░",
    "░░░░░░░░░░░░░░░░░░╚═╩═╝░╚╩╝░░░░░░░░░",
])


class RuleSet:
    def __init__(self, sample_str, wrap=False, directions=None):
        self.sample_str = sample_str
        self.tiles = Tiles.parse(self.sample_str)
        # get the weights of each tile tile_type
        self.weights = Counter([t for row in self.tiles for t in row])
        self.rules = self.calculate_adjacency_rules(self.tiles, wrap, directions)

    @staticmethod
    def calculate_adjacency_rules(tiles: list[list[Tiles]], wrap_around=True, directions: list[Direction] = None):
        rules = dict()
        if VERBOSE:
            print(f"Rules: {rules}")
        for x in range(len(tiles)):
            for y in range(len(tiles[x])):
                if VERBOSE:
                    print(f"Tile {tiles[x][y]} at {x}, {y}")
                if tiles[x][y] not in rules:
                    rules[tiles[x][y]] = {}
                for _direction in directions if directions is not None else Direction:
                    if VERBOSE:
                        print(f"Checking direction {_direction}")
                    adj_x, adj_y = (x + _direction.value[0], y + _direction.value[1])
                    if VERBOSE:
                        print(f"Adjacent tile at {adj_x}, {adj_y}")
                    if adj_x < 0 or adj_y < 0 or adj_x >= len(tiles) or adj_y >= len(tiles[x]):
                        if wrap_around:
                            if adj_x < 0:
                                if VERBOSE:
                                    print(f"Adjacent tile at {adj_x}, {adj_y} is out of bounds, wrapping")
                                difference = abs(adj_x - len(tiles))
                                adj_x = -difference
                            if adj_y < 0:
                                if VERBOSE:
                                    print(f"Adjacent tile at {adj_x}, {adj_y} is out of bounds, wrapping")
                                difference = abs(adj_y - len(tiles[x]))
                                adj_y = -difference
                            if adj_x >= len(tiles):
                                if VERBOSE:
                                    print(f"Adjacent tile at {adj_x}, {adj_y} is out of bounds, wrapping")
                                difference = abs(adj_x - len(tiles))
                                adj_x = difference
                            if adj_y >= len(tiles[x]):
                                if VERBOSE:
                                    print(f"Adjacent tile at {adj_x}, {adj_y} is out of bounds, wrapping")
                                difference = abs(adj_y - len(tiles[x]))
                                adj_y = difference
                        else:
                            continue
                    if _direction not in rules[tiles[x][y]]:
                        rules[tiles[x][y]][_direction] = set()
                    adj = tiles[adj_x][adj_y]
                    if VERBOSE:
                        print(f"Adjacent tile is {adj}")
                    rules[tiles[x][y]][_direction].add(adj)
        return rules

    def print_rules(self):
        out = "\n\t" + "\n\t".join(self.sample_str.split("\n"))
        print(f"Ruleset for: \n{out}", end="\n\n")
        for tile in self.rules.keys():
            print(f"\tTile {tile}")
            for direction in self.rules[tile].keys():
                rule = self.rules[tile][direction]
                rule_str = ""
                for r in rule:
                    rule_str += r.char
                print(f"\t\t{direction.char} -> {rule_str}")

    def get_rule(self, tile_type, direction):
        return self.rules[tile_type][direction]


class Node:
    def __init__(self, pos, ruleset: RuleSet):
        self.x, self.y = pos
        self.ruleset = ruleset
        self.potential = set([tile for tile in ruleset.rules.keys() if tile not in Tiles.excluded_from_generation()])

    def constrain_potential(self, tile, direction):
        if direction in self.ruleset.rules[tile]:
            self.potential.intersection_update(self.ruleset.rules[tile][direction])

    def is_collapsed(self):
        return len(self.potential) == 1

    def entropy(self):
        return len(self.potential)

    def collapse(self):
        # shrink set to size 1
        if len(self.potential) > 1:
            weights = {tile: self.ruleset.weights[tile] for tile in self.potential}
            self.potential = {random.choices(list(weights.keys()), list(weights.values()), k=1)[0]}
            return True
        return False


class NodeGrid:
    def __init__(self, size, ruleset: RuleSet = RuleSet(sample), seed=random.randint(0, 100)):
        self.width, self.height = size
        self.ruleset = ruleset
        self.grid = None
        random.seed(seed)

    @time_it
    def generate_dungeon(self, pregen=True, wrap=False, max_iterations=50):
        grid = None
        iteration = 0
        if VERBOSE:
            print("Starting Generation.")
        while (grid is None or not self.verify_and_clean_map(grid, wrap)) and iteration < max_iterations:
            iteration += 1
            if VERBOSE:
                print(f"Current Iteration: {iteration}")
            grid = self.generate(pregen, wrap)
        if VERBOSE:
            print()
        if grid is None:
            if VERBOSE:
                print(f"Failed to generate grid after {iteration} iterations")
        else:
            if VERBOSE:
                print(f"Generation took {iteration} iterations")
            self.grid = grid
            return self.collapse_to_tile()

    def generate(self, pregen, wrap):
        grid = [[Node((x, y), self.ruleset) for y in range(self.height)] for x in range(self.width)]
        if pregen:
            self.pregenerate(grid, wrap)
        while (node := self.get_lowest_entropy(grid)) is not None:
            if node.collapse():
                self.propagate_node(node, grid, wrap)
            else:
                # pretty print grid
                self.pretty_print(grid)
                return None
        return grid if grid is not None else None

    @staticmethod
    def get_lowest_entropy(grid):
        lowest_entropy = None
        by_entropy = {}
        for x in range(len(grid)):
            for y in range(len(grid[x])):
                node = grid[x][y]
                if node.is_collapsed():
                    continue
                e = node.entropy()
                by_entropy.setdefault(e, []).append(node)
                lowest_entropy = e if lowest_entropy is None else min(e, lowest_entropy)
        lowest_node = None
        if lowest_entropy is not None:
            lowest_node = random.choice(by_entropy[lowest_entropy])
        return lowest_node

    def propagate_node(self, node, grid, wrap):
        queue = deque(((self.get_adjacents(node, grid, wrap=wrap), node.potential),))
        seen = {node}
        while len(queue) > 0:
            adjacents, potentials = queue.pop()
            for adjacent, direction in adjacents:
                if adjacent not in seen:
                    seen.add(adjacent)
                    for potential in potentials:
                        adjacent.constrain_potential(potential, direction)
                    if adjacent.is_collapsed():
                        queue.appendleft((self.get_adjacents(adjacent, grid, wrap=wrap), adjacent.potential))

    def get_adjacents(self, node, grid, wrap):
        for direction in [Direction.North, Direction.East, Direction.South, Direction.West]:
            adj_x, adj_y = node.x + direction.x, node.y + direction.y
            if not wrap:
                if not (adj_x < 0 or adj_x >= self.width or adj_y < 0 or adj_y >= self.height):
                    yield grid[adj_x][adj_y], direction
            else:
                if adj_x < 0:
                    adj_x = self.width - 1
                elif adj_x >= self.width:
                    adj_x = 0
                if adj_y < 0:
                    adj_y = self.height - 1
                elif adj_y >= self.height:
                    adj_y = 0
                yield grid[adj_x][adj_y], direction

    def pregenerate(self, grid, wrap=False):
        if not wrap:
            for x in range(self.width):
                grid[x][0].potential = {Tiles.VOID}
                self.propagate_node(grid[x][0], grid, wrap)
                grid[x][-1].potential = {Tiles.VOID}
                self.propagate_node(grid[x][-1], grid, wrap)
            for y in range(self.height):
                grid[0][y].potential = {Tiles.VOID}
                self.propagate_node(grid[0][y], grid, wrap)
                grid[-1][y].potential = {Tiles.VOID}
                self.propagate_node(grid[-1][y], grid, wrap)
        node_types = [Tiles.ENTRANCE, Tiles.BOSS, Tiles.HOARD]
        for node_type in node_types:
            node = None
            while node is None:
                check = grid[random.randint(1, self.width - 2)][random.randint(1, self.height - 2)]
                if not check.is_collapsed():
                    for direction in Direction:
                        for scale in range(1, 10):
                            adj_x, adj_y = check.x + direction.x * scale, check.y + direction.y * scale
                            if wrap:
                                if adj_x < 0:
                                    adj_x = self.width - 1
                                elif adj_x >= self.width:
                                    adj_x = 0
                                if adj_y < 0:
                                    adj_y = self.height - 1
                                elif adj_y >= self.height:
                                    adj_y = 0
                            if not wrap and not (adj_x < 0 or adj_x >= self.width or adj_y < 0 or adj_y >= self.height) \
                                    or grid[adj_x][adj_y].is_collapsed():
                                break
                    else:
                        node = check

            node.potential = {node_type}
            self.propagate_node(node, grid, wrap)

        for _ in range(2 + ((self.width + self.height) // 8)):
            node = None
            while node is None or Tiles.FLOOR not in node.potential or node.is_collapsed():
                node = grid[random.randint(0, self.width - 1)][random.randint(0, self.height - 1)]
            node.potential = {Tiles.FLOOR}
            self.propagate_node(node, grid, wrap)
            for adj, _ in self.get_adjacents(node, grid, wrap):
                if Tiles.FLOOR in adj.potential and random.randint(0, 10):
                    adj.potential = {Tiles.FLOOR}
                    self.propagate_node(adj, grid, wrap)

    def collapse_to_tile(self):
        collapsed = [[next(iter(node.potential)) for node in row] for row in self.grid]
        return collapsed

    @staticmethod
    def pretty_print(grid):
        # if collapsed print char, if potential len > 1 print len, if potential ==0 print ? in red
        for row in grid:
            for node in row:
                if node.is_collapsed():
                    print(f" \033[92m{next(iter(node.potential))}\33[0m", end=" ")
                elif len(node.potential) == 0:
                    print(" \033[91m?\033[0m", end=" ")
                else:
                    print(f"\033[90m{len(node.potential):3}\033[0m", end="")
            print()

    def verify_and_clean_map(self, grid, wrap):
        entrance = None
        hoard = None
        boss = None
        walked = set()
        queue = deque()
        # find entrance, hoard, boss
        for row in grid:
            for node in row:
                if Tiles.ENTRANCE in node.potential:
                    entrance = node
                if Tiles.HOARD in node.potential:
                    hoard = node
                if Tiles.BOSS in node.potential:
                    boss = node
        # find all walkable nodes
        queue.append(entrance)
        while queue:
            node = queue.popleft()
            if node not in walked:
                walked.add(node)
                for adj, _ in self.get_adjacents(node, grid, wrap):
                    if next(iter(adj.potential)) in Tiles.walkable() and adj not in walked:
                        queue.append(adj)

        if entrance not in walked or hoard not in walked or boss not in walked:
            return False

        for row in grid:
            for node in row:
                if node not in walked and next(iter(node.potential)) in Tiles.walkable():
                    node.potential = {Tiles.VOID}
        return True






