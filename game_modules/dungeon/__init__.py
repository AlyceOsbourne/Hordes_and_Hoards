import pygame
import threading
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


def generate():
    sm.set_state("generating", True)
    dungeon = wfc_node_grid.generate_dungeon()
    sm.set_state("current_dungeon", dungeon)
    font = pygame.font.SysFont("monospace", 10)
    font.set_bold(True)
    sm.set_state("generating", False)
    for y in range(len(dungeon)):
        for x in range(len(dungeon[y])):
            tile = dungeon[y][x].get_tile_image().convert()
            dungeon_surface.blit(tile, (x * TILE_SIZE, y * TILE_SIZE))


@eh(pygame.KEYDOWN)
def generate_dungeon(event):
    if event.key == pygame.K_F2:
        # todo change the event to be a custom event
        if not sm.get_state("generating"):
            # create process to generate dungeon
            thread = threading.Thread(target=generate, daemon=False)
            thread.start()


def render(screen):
    font = pygame.font.SysFont("monospace", 10)
    if sm.get_state("generating"):
        # fill dungeon surface with black
        dungeon_surface.fill((0, 0, 0))
        # draw text in center
        text = font.render("Generating...", True, (255, 255, 255))
        text_rect = text.get_rect()
        text_rect.center = (NUM_TILES_X * TILE_SIZE / 2, NUM_TILES_Y * TILE_SIZE / 2)
        dungeon_surface.blit(text, text_rect)
    screen.blit(dungeon_surface, (0, 0))
