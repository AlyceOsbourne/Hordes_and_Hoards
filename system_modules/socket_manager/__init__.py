from pygame_core import *
from .client import *
from .server import *
from core_modules.socket_manager.connection import *
from core_modules.socket_manager.server import *
from core_modules.socket_manager.client import *
game = get_game()
event_handler, asset_handler, state_handler = game.handles

def init():
    state_handler.add_state("connection_state", ConnectionStatus.OFFLINE)
