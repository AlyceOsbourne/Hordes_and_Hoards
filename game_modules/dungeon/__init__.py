from __future__ import annotations

from pygame_core import *

eh, am, sm = get_game().handles


def init():
    sm.add_states(
        dungeon_size=(32, 32),
        tile_size=(16, 16),
        dungeon_loaded=False
    )

def render(screen):
    pass


def update():
    pass
