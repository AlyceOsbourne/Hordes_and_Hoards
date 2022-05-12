from __future__ import annotations

from pygame_core import *

event_handler, asset_handler, state_handler = get_game().handles


def init():
    state_handler.add_states(
        dungeon_size=(32, 32),
        tile_size=(16, 16),
        dungeon_loaded=False
    )


def render(screen):
    pass


def update():
    pass
