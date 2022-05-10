import pygame
import game_modules.dungeon.wfc as wfc
import game_modules.dungeon.tiledata as td
from pygame_core import get_game

VERBOSE = False
game = get_game()
eh, am, sm = game.handles

sm.register_state("generating", False)
sm.register_state("current_dungeon", None)

dungeon_generation_event = eh.create_event("generate_dungeon")

NUM_TILES_X, NUM_TILES_Y = 32, 32
TILE_SIZE = 16

wfc_node_grid = wfc.NodeGrid((NUM_TILES_X, NUM_TILES_Y))
dungeon_surface = pygame.Surface((NUM_TILES_X * TILE_SIZE, NUM_TILES_Y * TILE_SIZE))


@eh(pygame.KEYDOWN)
def generate_dungeon(event):
    if event.key == pygame.K_F2:
        # todo change the event to be a custom event
        sm.set_state("generating", True)
        dungeon = wfc_node_grid.generate_dungeon()
        sm.set_state("current_dungeon", dungeon)
        sm.set_state("generating", False)
        font = pygame.font.SysFont("monospace", 1)
        font.set_bold(True)
        for y in range(len(dungeon)):
            for x in range(len(dungeon[y])):
                tile = dungeon[y][x].get_tile_image().convert()
                dungeon_surface.blit(tile, (x * TILE_SIZE, y * TILE_SIZE))


def render(screen):
    screen.blit(dungeon_surface, (0, 0))
