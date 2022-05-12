from abc import ABCMeta

from pygame.sprite import Sprite

from pygame_interface import *

game = get_game()
event_handler, asset_handler, state_handler = game.handles

entity_manager = None


class EntityManager:
    def __init__(self):
        self.entities = []
        state_handler.set_state('loaded_entities', 0)

    def add_entity(self, entity):
        self.entities.append(entity)
        state_handler.set_state('loaded_entities', len(self.entities))


class Entity(Sprite, metaclass=ABCMeta):
    pass


def init():
    state_handler.add_states(
        loaded_entities=-1
    )
    global entity_manager
    entity_manager = EntityManager()
