from __future__ import annotations

import os
import random
from enum import Enum
import json

from pygame_core import get_handles

event_handler, asset_manager, state_manager = get_handles()

class Direction(Enum):
    # relative x, y
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)


class Tiles(Enum):
    VOID = (0, "░")

    WALL_HORIZONTAL = (1, "═")
    WALL_VERTICAL = (2, "║")

    WALL_T_UP = (3, "╩")
    WALL_T_DOWN = (4, "╦")
    WALL_T_LEFT = (5, "╠")
    WALL_T_RIGHT = (6, "╣")

    WALL_X = (7, "╬")

    WALL_TR_CORNER = (7, "╗")
    WALL_TL_CORNER = (8, "╔")
    WALL_BR_CORNER = (9, "╝")
    WALL_BL_CORNER = (10, "╚")

    FLOOR = (11, "▓")

    HOARD = (12, "⚑")

    ENTRANCE_VERTICAL = (13, "│")
    ENTRANCE_HORIZONTAL = (14, "─")

    BIG_BOSS_SPAWN = (15, "Ω")

    def __new__(cls, value, char):
        obj = object.__new__(cls)
        obj._value_ = value
        obj.char = char
        return obj

    @classmethod
    def from_char(cls, char):
        for tile in cls:
            if tile.char == char:
                return tile
        return None

    @classmethod
    def potential_tiles(cls):
        return {tile.name: True for tile in cls}


# input sample class for the Wave Function Collapse algorithm
class Sample:
    def __init__(self, sample_str):
        self.sample_str = sample_str
        self.tiles = self.parse_sample()
        self.rules = self.calculate_adjacency_rules(self.tiles)

    def parse_sample(self):
        tiles = []
        for line in self.sample_str.split("\n"):
            tiles.append([])
            for char in line:
                tiles[-1].append(Tiles.from_char(char))
        return tiles

    def calculate_adjacency_rules(self, tiles):
        width = len(self.tiles[-1])
        height = len(self.tiles)
        adjacency_rules = {}
        for y in range(height):
            for x in range(width):
                # wraps around the x and y axis to get the adjacent tiles
                # needs to store direction data too
                for direction in [direction for direction in Direction]:
                    adjacent_x = x + direction.value[0]
                    adjacent_y = y + direction.value[1]
                    if adjacent_x < 0:
                        adjacent_x = width - 1
                    elif adjacent_x >= width:
                        adjacent_x = 0
                    if adjacent_y < 0:
                        adjacent_y = height - 1
                    elif adjacent_y >= height:
                        adjacent_y = 0
                    if tiles[y][x] != tiles[adjacent_y][adjacent_x]:
                        if tiles[y][x] not in adjacency_rules:
                            adjacency_rules[tiles[y][x]] = []
                        adjacency_rules[tiles[y][x]].append(
                            (direction, tiles[adjacent_y][adjacent_x])
                        )
        return adjacency_rules





sample = "\n".join(
    [
        "░░░░░░░░░░░░░",
        "░╔═╦═══╦═─═╗░",
        "░║▓║▓▓▓║▓▓▓║░",
        "░║▓║▓⚑▓║▓▓▓║░",
        "░║▓║▓▓▓║▓▓▓║░",
        "░╠═╬═══╬═══╣░",
        "░║▓║▓▓▓║▓▓▓║░",
        "░│▓║▓Ω▓║▓▓▓│░",
        "░║▓║▓▓▓║▓▓▓║░",
        "░╚═╩═══╩═─═╝░",
        "░░░░░░░░░░░░░"]
)
# create test sample

sample = Sample(sample)
print(sample.tiles)
print(*list(sample.rules.items()), sep="\n")
