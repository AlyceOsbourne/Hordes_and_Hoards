"""
Dungeon generator for my game, using the WFC algorithm.
Note, there are still artifacts at this time, I will refine the ruleset over time.
"""
from __future__ import annotations
import random
from collections import Counter, deque
from functools import cache

from game_modules.dungeon.tiledata import Tiles, Direction
from test_functions import time_it
VERBOSE = False

sample = "\n".join([
    "░░░░░░░░░░░░░░░░╔══════════════╗",
    "░╔╗╔╗░╔══╗░╔══╗░║▓▓▓▓▓▓▓▓▓▓▓▓▓▓║",
    "░╚╝╚╝░║░░║░║▓▓║░║▓╔╗╔╗▓▓▓▓╔╗╔╗▓║",
    "░╔╗╔╗░║░░║░║▓▓║░║▓╚╬╬╝▓▓▓▓╚╩╩╝▓║",
    "░╚╝╚╝░╚══╝░╚══╝░║▓╔╬╬╗▓▓▓▓╔╦╦╗▓║",
    "░░░░░░░░░░░░░░░░║▓╚╝╚╝▓▓▓▓╚╝╚╝▓║",
    "░╔═╦═╗░░░╔═╦═╗░░║▓▓▓▓▓▓▓▓▓▓▓▓▓▓║",
    "░║░║░║╔╦╗║▓║▓║░░║▓║▓═▓╗▓╔▓╝▓╚▓▓║",
    "░╠═╬═╣╠╬╣╠═╬═╣░░║▓▓▓▓▓▓▓▓▓▓▓▓▓▓║",
    "░║░║░║╚╩╝║▓║▓║░░║▓▓╦▓╩▓╣▓╠▓╬▓▓▓║",
    "░╚═╩═╝░░░╚═╩═╝░░║▓▓▓▓▓▓▓▓▓▓▓▓▓▓║",
    "░╔══╦══╗╔══╦══╗░║▓╔╗╔╗▓▓▓▓╔╗╔╗▓║",
    "░║╔═╩═╗║║╔═╬═╗║░║▓╚╝╚╝▓▓▓▓╚╣╠╝▓║",
    "░║║▓▓▓║║║║╔╩╗║║░║▓╔╗╔╗▓▓▓▓╔╣╠╗▓║",
    "░╠╣▓▓▓╠╣╠╬╣▓╠╬╣░║▓╚╝╚╝▓▓▓▓╚╝╚╝▓║",
    "░║║▓▓▓║║║║╚╦╝║║░║▓▓▓▓▓▓▓▓▓▓▓▓▓▓║",
    "░║╚═╦═╝║║╚═╬═╝║░║╔═╦═╗▓▓▓╔═╦═╗▓║",
    "░╚══╩══╝╚══╩══╝░║║░║░║╔╦╗║▓║▓║▓║",
    "░░░╔╗╔╗░░╔╗╔╗░░░║╠═╬═╣╠╬╣╠═╬═╣▓║",
    "░░░╚╩╩╝░░╚╣╠╝░░░║║░║░║╚╩╝║▓║▓║▓║",
    "░░░╔╦╦╗░░╔╣╠╗░░░║╚═╩═╝▓▓▓╚═╩═╝▓║",
    "░░░╚╝╚╝░░╚╝╚╝░░░║▓▓▓▓▓▓▓▓▓▓▓▓▓▓║",
    "░░░╔═╗░░░░╔╗╔╗░░║▓╔╗╔╗▓▓▓▓▓╔═╗▓║",
    "░░░╚╦╝░░░░║╠╣║░░║▓║╠╣║▓▓▓▓▓╚╦╝▓║",
    "░░░╔╩╗░░░░╚╝╚╝░░║▓╚╝╚╝▓▓▓▓▓╔╩╗▓║",
    "░░░╚═╝░░░░░░░░░░║▓▓▓▓▓▓▓▓▓▓╚═╝▓║",
    "░░╔╗░░░░░░░╔╗░░░║▓╔╦╦╗▓▓▓▓▓▓▓▓▓║",
    "░░╠╝░░░░░░░╚╣░░░║▓║╠╣║▓▓▓▓▓▓▓▓▓║",
    "░╔╣░░╔═══╗░░╠╗░░║▓╚╩╩╝▓▓▓▓▓▓▓▓▓║",
    "░╚╝╔╗╚═══╝╔╗╚╝░░║▓▓▓▓▓▓▓▓▓▓▓▓▓▓║",
    "░░░╚╩╦╗░╔╦╩╝░░░░║▓▓▓▓▓▓▓▓▓▓▓▓▓▓║",
    "╔═══╗╚╝░╚╝╔═══╗░║▓▓▓▓▓▓▓▓▓▓▓▓▓▓║",
    "╚═══╝░░░░░╚═══╝░║▓▓▓◙▓▓▓▓▓▓⌂▓▓▓║",
    "░░╔╦╦╗░░░╔╗╔╗░░░║▓▓▓▓▓▓▓▓▓▓▓▓▓▓║",
    "░░║╠╣║░░░╚╬╬╝░░░║▓▓▓▓▓▓▓▓▓▓▓▓▓▓║",
    "░░╚╩╩╝░░░╔╬╬╗░░░╚══════════════╝",
    "░░░░░░╔╗░╚╝╚╝░░░░░░░░░░░░░░░░░░░",
    "░░░░░╔╝╚╗░░░░░░░░░░░░░░░░░░░░░░░",
    "░░░░░╚╗╔╝░░░░░░░░░░░░░░░░░░░░░░░",
    "░╔═╗░░╚╝░░╔═╗░░░░░░░░░░░░░░░░░░░",
    "╔╝░╚╗░░░░╔╝▓╚╗░░░░╔═══╗░░░░░░░░░",
    "║░░░║░░░░║▓▓▓║░░░░║░░░║░╔═╗░░░░░",
    "╚╗░╔╝░░░░╚╗▓╔╝░░░░║░∩░║░║∩║░░░░░",
    "░╚═╝░░░░░░╚═╝░░░░░║░║░║░║║║░░░░░",
    "░░░░░░░░░░░░░░░░░░╚═╩═╝░╚╩╝░░░░░",
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
                    if wrap_around:
                        if adj_x < 0:
                            if VERBOSE:
                                print(f"Adjacent tile at {adj_x}, {adj_y} is out of bounds, wrapping")
                            difference = abs(adj_x - len(tiles))
                            adj_x = -difference
                            # adj_x = len(tiles) - 1
                        if adj_y < 0:
                            if VERBOSE:
                                print(f"Adjacent tile at {adj_x}, {adj_y} is out of bounds, wrapping")
                            difference = abs(adj_y - len(tiles[x]))
                            adj_y = -difference
                            # adj_y = len(tiles[x]) - 1
                        if adj_x >= len(tiles):
                            if VERBOSE:
                                print(f"Adjacent tile at {adj_x}, {adj_y} is out of bounds, wrapping")
                            difference = abs(adj_x - len(tiles))
                            adj_x = difference
                            # adj_x = 0
                        if adj_y >= len(tiles[x]):
                            if VERBOSE:
                                print(f"Adjacent tile at {adj_x}, {adj_y} is out of bounds, wrapping")
                            difference = abs(adj_y - len(tiles[x]))
                            adj_y = difference
                            # adj_y = 0
                    else:
                        if adj_x < 0 or adj_y < 0 or adj_x >= len(tiles) or adj_y >= len(tiles[x]):
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
    def start_generation(self, pregen=True, max_iterations=50):
        grid = None
        iteration = 0
        if VERBOSE:
            print("Starting Generation.")
        while grid is None and iteration < max_iterations:
            iteration += 1
            if VERBOSE:
                print(f"Current Iteration: {iteration}")
            grid = self.generate(pregen)
        if VERBOSE:
            print()
        if grid is None:
            if VERBOSE:
                print(f"Failed to generate grid after {iteration} iterations")
        else:
            if VERBOSE:
                print(f"Generation took {iteration} iterations")
            self.grid = grid

    def generate(self, pregen=True):
        grid = [[Node((x, y), self.ruleset) for y in range(self.height)] for x in range(self.width)]
        ################################################################################################################
        if pregen:
            for x in range(self.width):
                grid[x][0].potential = {Tiles.VOID}
                self.propagate_node(grid[x][0], grid)
                grid[x][-1].potential = {Tiles.VOID}
                self.propagate_node(grid[x][-1], grid)
            for y in range(self.height):
                grid[0][y].potential = {Tiles.VOID}
                self.propagate_node(grid[0][y], grid)
                grid[-1][y].potential = {Tiles.VOID}
                self.propagate_node(grid[-1][y], grid)
            door_node = None
            while door_node is None or door_node.is_collapsed():
                door_node = grid[random.randint(0, self.width - 1)][random.randint(0, self.height - 1)]
            door_node.potential = {Tiles.ENTRANCE}
            self.propagate_node(door_node, grid)
            boss_node = None
            while boss_node is None or boss_node.is_collapsed():
                boss_node = grid[random.randint(0, self.width - 1)][random.randint(0, self.height - 1)]
            boss_node.potential = {Tiles.BOSS}
            self.propagate_node(boss_node, grid)
            hoard_node = None
            while hoard_node is None or hoard_node.is_collapsed():
                hoard_node = grid[random.randint(0, self.width - 1)][random.randint(0, self.height - 1)]
            hoard_node.potential = {Tiles.HOARD}
            self.propagate_node(hoard_node, grid)
            for _ in range(2 + ((self.width + self.height) // 8)):
                node = grid[random.randint(0, self.width - 1)][random.randint(0, self.height - 1)]
                while Tiles.FLOOR not in node.potential or len(node.potential) < 2:
                    node = grid[random.randint(0, self.width - 1)][random.randint(0, self.height - 1)]
                node.potential = {Tiles.FLOOR}
                self.propagate_node(node, grid)
                for adj, _ in self.get_adjacents(node, grid):
                    if Tiles.FLOOR in adj.potential and random.randint(0, 10):
                        adj.potential = {Tiles.FLOOR}
                        self.propagate_node(adj, grid)

        ################################################################################################################
        while (node := self.get_lowest_entropy(grid)) is not None:
            if VERBOSE:
                self.print_grid(grid)
            if node.collapse():
                self.propagate_node(node, grid)
            else:
                if VERBOSE:
                    print("\nFailed to collapse node, please try and create valid rule")
                    self.print_grid(grid)
                return None
        return grid

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

    @staticmethod
    def print_grid(grid):
        colours = {
            "red": '\033[91m',
            "green": '\033[92m',
            "blue": '\033[94m',
            "end": '\033[0m'
        }
        print()
        for x in range(len(grid)):
            for y in range(len(grid[x])):
                if grid[x][y].is_collapsed():
                    tile = next(iter(grid[x][y].potential))
                    print(f"{colours['green']}{tile:^2}{colours['end']}", end="")
                elif len(grid[x][y].potential) > 1:
                    print(f"{colours['blue']}{int(grid[x][y].entropy()):^2}{colours['end']}", end="")
                else:
                    print(f"{colours['red']}{'█':^2}{colours['end']}", end="")
            print()

    @staticmethod
    def pretty_print_grid(grid):
        if grid is not None:
            for x in range(len(grid)):
                for y in range(len(grid[x])):
                    tile = next(iter(grid[x][y].potential))
                    print(f"{tile}", end="")
                print()

    def propagate_node(self, node, grid):
        queue = deque(((self.get_adjacents(node, grid), node.potential),))
        seen = {node}
        while len(queue) > 0:
            adjacents, potentials = queue.pop()
            for adjacent, direction in adjacents:
                if adjacent not in seen:
                    seen.add(adjacent)
                    for potential in potentials:
                        adjacent.constrain_potential(potential, direction)
                    if adjacent.is_collapsed():
                        queue.appendleft((self.get_adjacents(adjacent, grid), adjacent.potential))

    def get_adjacents(self, node, grid):
        for direction in [Direction.North, Direction.East, Direction.South, Direction.West]:
            adj_x, adj_y = node.x + direction.x, node.y + direction.y
            if not (adj_x < 0 or adj_x >= self.width or adj_y < 0 or adj_y >= self.height):
                yield grid[adj_x][adj_y], direction

    def collapse_to_char_grid(self):
        collapsed_grid = [[None for _ in range(self.width)] for _ in range(self.height)]
        for x in range(len(self.grid)):
            for y in range(len(self.grid[x])):
                node = self.grid[x][y]
                if node.is_collapsed():
                    collapsed_grid[x][y] = next(iter(node.potential)).char
        return collapsed_grid

    @classmethod
    def generate_grid(cls, param, param1):
        wfc = cls((param, param1))
        wfc.start_generation()
        return Tiles.convert_to_tiles(wfc.collapse_to_char_grid())



