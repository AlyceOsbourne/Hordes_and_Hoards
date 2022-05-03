import random
from collections import Counter
from collections import deque
from enum import Enum
from functools import wraps

VERBOSE = False

sample_string = "\n".join([
    "║║║░░║╚╩╝║╚╝║║║",
    "╩╝║╔═╩═╦═╩═╗║╚╩",
    "══╝║╔╗▓║▓╔╗║╚══",
    "╗╔═╝╚╬╗║╔╬╝╚═╗╔",
    "╝║▓╔╗╠╝║╚╣╔╗▓║╚",
    "═╣▓╚╩╝▓║▓╚╩╝▓╠═",
    "╗║▓▓▓▓▓║▓▓▓▓▓║╔",
    "╣╠═════╬═════╣╠",
    "╝║▓▓▓▓▓║▓▓▓▓▓║╚",
    "═╣▓╔╦╗▓║▓╔╦╗▓╠═",
    "░║▓╚╝╠╗║╔╣╚╝▓║░",
    "░╚═╗╔╬╝║╚╬╗╔═╝░",
    "══╗║╚╝▓║▓╚╝║╔══",
    "╦╗║╚═╦═╩═╦═╝║╔╦",
    "║║║░░║╔╦╗║╔╗║║║",
]
)

sample_string_b = "\n".join([
    "╔╝║░░║╚╩╝║╚╝║╚╗",
    "╝░║╔═╩═╦═╩═╗║░╚",
    "══╝║▓▓▓║▓▓▓║╚══",
    "╗╔═╝▓▓▓║▓▓▓╚═╗╔",
    "╝║▓╔╗▓▓║▓▓╔╗▓║╚",
    "═╣▓╚╝▓▓║▓▓╚╝▓╠═",
    "╗║▓▓▓▓▓║▓▓▓▓▓║╔",
    "╣╠═════╬═════╣╠",
    "╝║▓▓▓▓▓║▓▓▓▓▓║╚",
    "═╣▓╔╗▓▓║▓▓╔╗▓╠═",
    "░║▓╚╝▓▓║▓▓╚╝▓║░",
    "░╚═╗▓▓▓║▓▓▓╔═╝░",
    "══╗║▓▓▓║▓▓▓║╔══",
    "╗░║╚═╦═╩═╦═╝║░╔",
    "╚╗║░░║╔╦╗║╔╗║╔╝",
]
)

sample_string_c = "\n".join([
    "░░░░░░░░░░░░░░░░",
    "░╔╗╔╗░╔══╗░╔══╗░",
    "░╚╝╚╝░║░░║░║▓▓║░",
    "░╔╗╔╗░║░░║░║▓▓║░",
    "░╚╝╚╝░╚══╝░╚══╝░",
    "░░░░░░░░░░░░░░░░",
    "░╔═╦═╗░░░╔═╦═╗░░",
    "░║░║░║╔╦╗║▓║▓║░░",
    "░╠═╬═╣╠╬╣╠═╬═╣░░",
    "░║░║░║╚╩╝║▓║▓║░░",
    "░╚═╩═╝░░░╚═╩═╝░░",
    "░╔══╦══╗╔══╦══╗░",
    "░║╔═╩═╗║║╔═╬═╗║░",
    "░║║▓▓▓║║║║╔╩╗║║░",
    "░╠╣▓▓▓╠╣╠╬╣▓╠╬╣░",
    "░║║▓▓▓║║║║╚╦╝║║░",
    "░║╚═╦═╝║║╚═╬═╝║░",
    "░╚══╩══╝╚══╩══╝░",
    "░░░╔╗╔╗░░╔╗╔╗░░░",
    "░░░╚╩╩╝░░╚╣╠╝░░░",
    "░░░╔╦╦╗░░╔╣╠╗░░░",
    "░░░╚╝╚╝░░╚╝╚╝░░░",
    "░░░░░░░░░░░░░░░░",


]
)




# decorator to time functions
def timeit(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        import time
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} took {end - start:2f} seconds")
        return result

    return wrapper


class Direction(Enum):
    North = (-1, 0), "↑"

    South = (1, 0), "↓"

    East = (0, 1), "→"

    West = (0, -1), "←"

    # North_East = (-1, 1), "↗"

    # North_West = (-1, -1), "↖"

    # South_East = (1, 1), "↘"

    # South_West = (1, -1), "↙"

    def __new__(cls, value: tuple[int, int], char):
        obj = object.__new__(cls)
        obj._value_ = value
        obj.char = char
        return obj

    @property
    def opposite(self):
        return Direction.get_from_value((-self.value[0], -self.value[1]))

    @classmethod
    def get_from_value(cls, param):
        for direction in cls:
            if direction.value == param:
                return direction
        return None

    @property
    def x(self):
        return self.value[0]

    @property
    def y(self):
        return self.value[1]


class Tiles(Enum):  # I should remove these hard codings
    VOID = (0, "░")

    WALL_HORIZONTAL = (1, "═")
    WALL_VERTICAL = (2, "║")

    WALL_T_UP = (3, "╩")
    WALL_T_DOWN = (4, "╦")
    WALL_T_LEFT = (5, "╠")
    WALL_T_RIGHT = (6, "╣")

    WALL_X = (7, "╬")

    WALL_TR_CORNER = (8, "╗")
    WALL_TL_CORNER = (9, "╔")
    WALL_BR_CORNER = (10, "╝")
    WALL_BL_CORNER = (11, "╚")

    FLOOR = (12, "▓")

    HOARD = (13, "⚑")

    ENTRANCE_VERTICAL = (14, "│")
    ENTRANCE_HORIZONTAL = (15, "─")

    BIG_BOSS_SPAWN = (16, "Ω")

    def __new__(cls, value, char):
        obj = object.__new__(cls)
        obj._value_ = value
        obj.char = char
        return obj

    @classmethod
    def from_char(cls, char):
        for t in cls:
            if t.char == char:
                return t
        raise ValueError(f"No tile found for char {char}")

    @classmethod
    def from_name(cls, name):
        for t in cls:
            if t.name == name:
                return t

    def __hash__(self):
        return self.value

    def __str__(self):
        return self.char


def parse(string):
    tile_set = []
    if VERBOSE:
        print(f"Parsing \n{string}")
    for line in string.split("\n"):
        if VERBOSE:
            print(f"Parsing line {line}")
        tile_set.append([])
        for char in line:
            if char == " ":
                continue
            if VERBOSE:
                print(f"Parsing char {char}")
            tile = Tiles.from_char(char)
            if VERBOSE:
                print(f"Got tile {tile}")
            if tile is None:
                raise Exception(f"Invalid tile: {char}")
            tile_set[-1].append(tile)
    return tile_set


class RuleSet:
    def __init__(self, sample_str, wrap=False, directions=None):
        self.sample_str = sample_str
        self.tiles = parse(self.sample_str)
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
                        # todo make the wrap take the difference between the two and use that for the offset
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
                # rule as char
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
        self.potential = set([tile for tile in ruleset.rules.keys()])

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
            # get a weighted list from poteintial
            weighted_list = []
            for tile in self.potential:
                weighted_list.append((tile, self.ruleset.sample_str.count(tile.char)))
            #self.potential = {random.choice(list(self.potential))}
            self.potential = {random.choice(weighted_list)[0]}
            return True
        return False


class NodeGrid:
    def __init__(self, size, ruleset: RuleSet = RuleSet(sample_string_b), seed=None):
        self.width, self.height = size
        self.ruleset = ruleset
        self.grid = None
        random.seed(seed if seed is not None else int(random.random()))

    @timeit
    def start_generation(self, force_initial_states=True, max_iterations=100_000):
        grid = None
        iteration = 0
        print("Starting Generation.")
        while grid is None and iteration < max_iterations:
            grid = self.generate(force_initial_states)
            iteration += 1
            if VERBOSE:
                print(f"Current Iteration: {iteration}")
            else:
                print(f"\rCurrent Iteration: {iteration}", end="")
        print()
        if grid is None:
            print(f"Failed to generate grid after {iteration} iterations")
        else:
            print(f"Generation took {iteration} iterations")
            self.grid = grid

    def generate(self, force_initial_states=True):
        num_tiles = self.width * self.height
        grid = [[Node((x, y), self.ruleset) for y in range(self.height)] for x in range(self.width)]

        # this section forces some states to get more desirable results, works without it
        ################################################################################################################
        if force_initial_states:
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
            node = grid[random.randint(0, self.width - 1)][random.randint(0, self.height - 1)]
            for _ in range(min(1, random.randint(num_tiles//5, num_tiles//3))):
                while Tiles.FLOOR not in node.potential:
                    node = grid[random.randint(0, self.width - 1)][random.randint(0, self.height - 1)]
                node.potential = {Tiles.FLOOR}
                self.propagate_node(node, grid)
                for adj, _ in self.get_adjacents(node, grid):
                    if Tiles.FLOOR in adj.potential and random.randint(0, 1):
                        adj.potential = {Tiles.FLOOR}
                        self.propagate_node(adj, grid)


        ################################################################################################################
        while (node := self.get_lowest_entropy(grid)) is not None:
            if VERBOSE:
                self.print_grid(grid)
            if node.collapse():
                self.propagate_node(node, grid)
            else:
                #self.print_grid(grid)
                #quit()
                return None
        return grid

    @staticmethod
    def get_lowest_entropy(grid):
        # find the lowest non collapsed node in the grid
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
        # if collapse print char in green,
        # if len > 1 print len in blue
        # else print exclamation mark in red
        # print row and column indices
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
                    print(f"{colours['blue']}{grid[x][y].entropy():^2}{colours['end']}", end="")
                else:
                    print(f"{colours['red']}{'!':^2}{colours['end']}", end="")
            print()

    def propagate_node(self, node, grid):
        queue = deque(((self.get_adjacents(node, grid), node.potential),))
        seen = set()
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


def test():
    for size in [(5, 5), (5, 10), (10, 10), (10, 15), (15, 15), (15, 20), (20, 20)]:
        print("\n{} x {}".format(*size))
        node_grid = NodeGrid(size)
        node_grid.start_generation(True)
        node_grid.print_grid(node_grid.grid)
