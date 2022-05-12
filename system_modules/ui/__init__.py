from pygame_interface import *
from .debug import init as debug_init, render_debug_info as debug_render
from .console import init as console_init, render as console_render

game = get_game()
eh, ah, sh = game.handles


def init():
    debug_init()
    print("Debugger Screen Initialized")
    console_init()
    print("Console Screen Initialized")


def update():
    pass


def render(screen):
    debug_render(screen)
    console_render(screen)
