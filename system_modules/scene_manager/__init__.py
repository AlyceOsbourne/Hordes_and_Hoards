from __future__ import annotations

from abc import ABC, abstractmethod

from pygame_core import *

game = get_game()
event_handler, asset_handler, state_handler = game.handles

scene_manager = None


class SceneManager:
    def __init__(self):
        self.scenes = {}
        self.current_scene = None
        state_handler.set_state('loaded_scenes', len(self.scenes))

    def add_scene(self, scene):
        self.scenes[scene.name] = scene
        state_handler.set_state('loaded_scenes', len(self.scenes))

    def set_scene(self, scene_name):
        self.current_scene = self.scenes[scene_name]
        self.current_scene.start()
        state_handler.set_state('current_scene', self.current_scene.name)

    def update(self):
        self.current_scene.update()

    def render(self, screen):
        self.current_scene.render(screen)


class Scene(ABC):
    def __init__(self, name):
        self.name = name
        self.handles = (event_handler, asset_handler, state_handler)
        self.objects = []
        self.sprites = []
        self.groups = []
        self.scene_surface = None
        self.scene_rect = None
        self.camera = None
        self.camera_rect = None
        self.camera_offset = (0, 0)

    @abstractmethod
    def init(self):
        pass

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def render(self, screen):
        pass

    @abstractmethod
    def end(self):
        pass

    @abstractmethod
    def cleanup(self):
        pass


def init():
    state_handler.add_states(
        loaded_scenes=-1,
        current_scene=None,
    )
    global scene_manager
    scene_manager = SceneManager()
