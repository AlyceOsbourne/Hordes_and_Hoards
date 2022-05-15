from __future__ import annotations

from abc import ABC, abstractmethod, ABCMeta

from pygame_interface import *

game = get_game()
event_handler, asset_handler, state_handler = game.handles


class Scene(metaclass=ABCMeta):
    def __init__(self):
        pass

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def render(self, screen):
        pass
