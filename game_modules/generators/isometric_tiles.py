# a file to draw from a numpy array to isometric tiles using pygame
import random
from functools import cache

import pygame as pg
import numpy as np

tile = pg.image.load("tile.png")
wall = pg.image.load("wall.png")
# scale tile to 1/10th of its original size
tile = pg.transform.scale(tile, (tile.get_width() // 5, tile.get_height() // 5))
wall = pg.transform.scale(wall, (wall.get_width() // 5, wall.get_height() // 5))

def cartesian_to_isometric(point):
    x, y = point
    return x - y, (x + y) / 2


def isometric_to_cartesian(point):
    x, y = point
    return x - y, x + y / 2


@cache
def tile_points(tile_size, point, origin):
    """defines the corners of the drawn polygons"""
    x, y = point
    origin_x, origin_y = origin
    tile_width, tile_height = tile_size
    corners = [(0, 0), (0, 1), (1, 1), (1, 0)]
    iso_coords = [
        cartesian_to_isometric((tile_width * (x + x_offset), tile_height * (y + y_offset)))
        for x_offset, y_offset in corners
    ]
    return [(_x + origin_x, _y + origin_y) for (_x, _y) in iso_coords]


def draw_as_grid(screen, grid, origin, tile_size):
    tile_width, tile_height = tile_size
    pallete = {}
    for x in range(len(grid)):
        for y in reversed(range(len(grid[x]))):
            points = tile_points(tile_size, (x, y), origin)
            if grid[x, y] == -10:
                pg.draw.polygon(screen, (255, 255, 255), [(x, y - tile_height) for x, y in points], 0)
                pg.draw.polygon(screen, (50, 50, 50), points, 1)

            elif grid[x, y] != 0:
                if grid[x, y] not in pallete:
                    pallete[grid[x, y]] = random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
                pg.draw.polygon(screen, pallete[grid[x, y]], points, 0)

            else:
                pg.draw.polygon(screen, (50, 50, 50), points, 1)

def draw_as_tiles(screen, grid, origin):
    tile_width, tile_height = tile.get_size()
    for x in range(len(grid)):
        for y in reversed(range(len(grid[x]))):
            # place tiles using iso coordinates
            if grid[x, y] != 0:
                iso_x, iso_y = cartesian_to_isometric((x*tile_width, y*tile_height))
                screen.blit(tile, (iso_x + origin[0], iso_y + origin[1]))
            if grid[x, y] == -10:
                iso_x, iso_y = cartesian_to_isometric((x*tile_width, y*tile_height))
                screen.blit(wall, (iso_x + origin[0], (iso_y + origin[1])-tile_height))


def test(screen_size=(1080, 720), tile_size=tile.get_size()):
    pg.init()
    screen = pg.display.set_mode(screen_size)
    clock = pg.time.Clock()

    from game_modules.generators.dungeon import generate_dungeon, default_dungeon_params

    grid = generate_dungeon(**default_dungeon_params)

    origin = (screen_size[0] // 2, 0)
    draw_as_grid(screen, grid, origin, tile_size)
    #draw_as_tiles(screen, grid, origin)
    pg.display.flip()

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                return
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    return
        clock.tick(60)


if __name__ == "__main__":
    test()
