from pygame_core import *
from core_modules.ui.debug import init as debug_init, render_debug_info
from core_modules.ui.console import init as console_init, render as console_render

game = get_game()
eh, am, sm = game.handles


def init():
    debug_init()
    print("Debugger Screen Initialized")
    console_init()
    print("Console Screen Initialized")



def update():
    pass

def render(screen):
    render_debug_info(screen)
    console_render(screen)
