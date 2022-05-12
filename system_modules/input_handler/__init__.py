# an input handler for pygame
# can take controllers and map them to events
# links to pygame
# can be used as a base class for other input handlers
import pygame
from pygame.locals import *
from pygame.joystick import *
from pygame.event import *
from pygame.key import *
from pygame.mouse import *


class InputHandler:
    def __init__(self):
        self.controllers = []
        self.keys = []
        self.mouse = []
        self.init_controllers()
        self.bindings = {}

    def init_controllers(self):
        for i in range(pygame.joystick.get_count()):
            self.controllers.append(pygame.joystick.Joystick(i))
            self.controllers[-1].init()


