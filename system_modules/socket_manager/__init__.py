from pygame_interface import *
from .connection import *

game = get_game()
event_handler, asset_handler, state_handler = game.handles

def init():
    state_handler.add_state("connection_state", ConnectionStatus.OFFLINE)
