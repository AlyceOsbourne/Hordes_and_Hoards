import importlib
import os
import sys
from itertools import count
from functools import partial
import pygame

pygame.init()


class EventHandler:

    def __init__(self):
        self.handlers = {}
        self.events = []
        self.custom_event_ids = count(pygame.USEREVENT)
        self.custom_events = {}

    def register(self, event_type, handler):
        if event_type not in self.handlers:
            self.handlers[event_type] = []
        self.handlers[event_type].append(handler)

    def unregister(self, event_type, handler):
        if event_type in self.handlers:
            self.handlers[event_type].remove(handler)

    def handle(self, event):
        if event.type in self.handlers:
            for handler in self.handlers[event.type]:
                handler(event)

    def handle_events(self, events):
        for event in events:
            self.handle(event)

    def create_event_type(self, event_name: str):
        event_id = next(self.custom_event_ids)
        self.custom_events[event_name] = event_id
        self.handlers[event_id] = []

    def delete_custom_event(self, event_name: str):
        del self.custom_events[event_name]
        del self.handlers[self.custom_events[event_name]]

    def get_custom_event_name(self, event_id):
        for event_name, event_id_ in self.custom_events.items():
            if event_id_ == event_id:
                return event_name
        return None

    def get_custom_event_id(self, event_name):
        return self.custom_events[event_name]

    def __call__(self, event_type):
        def decorator(handler):
            self.register(event_type, handler)
            return handler

        return decorator


class AssetManager:

    def __init__(self, root_path: str = "assets"):
        self.assets = {
            "images": {},
            "sounds": {},
            "fonts": {}
        }
        if not os.path.exists(root_path):
            os.mkdir(root_path)
            for folder in ["images", "sounds", "fonts"]:
                os.mkdir(os.path.join(root_path, folder))
        print("Loading assets...")
        self.load_assets(root_path)
        print("Assets loaded.")

    def load_assets(self, root_path: str):
        print(f"Searching for assets in {root_path}")
        for root, dirs, files in os.walk(root_path):
            for dir_name in dirs:
                if dir_name.startswith("."):
                    continue
                self.load_assets(os.path.join(root, dir_name))
            for file_name in files:
                if file_name.startswith("."):
                    continue
                if file_name.endswith(".png") or file_name.endswith(".jpg"):
                    self.load_image(os.path.join(root, file_name))
                elif file_name.endswith(".wav") or file_name.endswith(".ogg"):
                    self.load_sound(os.path.join(root, file_name))
                elif file_name.endswith(".ttf"):
                    self.load_font(os.path.join(root, file_name))
                else:
                    print(f"\rUnrecognized file type for: {file_name}")
                    continue

    def get_image(self, image_name: str):
        return self.assets["images"][image_name]

    def get_sound(self, sound_name: str):
        return self.assets["sounds"][sound_name]

    def get_font(self, font_name: str, font_size: int = 16):
        return self.assets["fonts"][font_name](font_size)

    def load_image(self, path: str):
        self.assets["images"][os.path.basename(path)] = pygame.image.load(path)

    def load_sound(self, path: str):
        self.assets["sounds"][os.path.basename(path)] = pygame.mixer.Sound(path)

    def load_font(self, path: str):
        # these load as partials, so we can still resize the font later
        self.assets["fonts"][os.path.basename(path)] = partial(pygame.font.Font, path)


class Game:

    def __init__(self, width, height, title, fps=60, asset_path=None):
        self.width = width
        self.height = height
        self.title = title
        self.fps = fps
        self.screen = pygame.display.set_mode((self.width, self.height))

        self.clock = pygame.time.Clock()

        self.game_event_handler = EventHandler()
        self.asset_manager = AssetManager(asset_path if asset_path else os.path.join(os.getcwd(), 'assets'))

        self.register_system_events()

        self.game_modules = []
        self.import_game_modules()

    def register_system_events(self):
        print("Registering system events...")
        self.game_event_handler.register(pygame.QUIT, lambda event:
        print(f"Quitting {self.title}") or pygame.quit() or quit(1))
        print("System events registered.")

    def import_game_modules(self):
        print("Importing game modules...")
        module_dir = os.path.join(os.getcwd(), 'game_modules')
        if not os.path.exists(module_dir):
            os.mkdir(module_dir)
        self.game_modules = []
        for module in os.listdir(os.path.join(os.getcwd(), 'game_modules')):
            if module.endswith(".py") and not module.startswith("__"):
                # if module not already imported, import it
                if module not in sys.modules:
                    print(f"Importing {module}...")
                    module = importlib.import_module(f"game_modules.{module[:-3]}")
                    self.game_modules.append(module)
                    print(f"{module.__name__} imported.")
        print(f"Imported {len(self.game_modules)} game modules.")

    def run(self):
        while True:
            self.game_event_handler.handle_events(pygame.event.get())
            self.update()
            self.render()
            self.clock.tick(self.fps)

    def update(self):
        pass

    def render(self):
        pass

    # function to create a decorator for registering functions as event handlers using the event handler class
    def get_event_handler(self):
        return self.game_event_handler.__call__


__all__ = ["Game", "EventHandler", "AssetManager"]
