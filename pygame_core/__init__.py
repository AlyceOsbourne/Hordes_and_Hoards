import importlib
import os
from abc import ABC
from functools import partial
from itertools import count

import pygame

pygame.init()


class EventHandler:
    """
    Core event handler, handles pygame and custom events.

    can be called as a function decorator to register a function as an event handler.
    """

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

    def handle(self, event, event_data=None):
        if isinstance(event, str):
            event = self.custom_events[event]
        if isinstance(event, int):
            if event_data is not None:
                event = pygame.event.Event(event, event_data)
            else:
                event = pygame.event.Event(event)
        if event.type in self.handlers:
            for handler in self.handlers[event.type]:
                handler(event)

    def handle_events(self, events):
        for event in events:
            if not isinstance(event, tuple):
                self.handle(event)
            else:
                self.handle(event[0], event[1])

    def create_event_type(self, event_name: str):
        event_id = next(self.custom_event_ids)
        self.custom_events[event_name] = event_id
        self.handlers[event_id] = []
        print(f"Created custom event type {event_name} with id {event_id}")
        return event_name, event_id,

    def delete_custom_event(self, event_name: str):
        del self.custom_events[event_name]
        del self.handlers[self.custom_events[event_name]]

    def get_custom_event_name(self, event_id):
        for event_name, event_id_ in self.custom_events.items():
            if event_id_ == event_id:
                return event_name
        return None

    def get_custom_event_id(self, event_name):
        if event_name in self.custom_events:
            return self.custom_events[event_name]
        else:
            return None

    def __call__(self, event_type):
        def decorator(handler):
            self.register(event_type, handler)
            return handler

        return decorator


class AssetManager:
    """
    Handles the loading of assets from disk and caches them ready for use
    """

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


class GameStateHandler:
    """This is the object we will save and load from disk to act as the save game, maybe?"""

    def __init__(self):
        print("Initializing game state handler...")
        self.states = {}

        print("Game state handler initialized.")

    # we are using raises to make sure all things are being registered and accessed properly,
    # this is an attempt to make sure some types of bugs are mitigated, and not just ignored

    # The following two functions are basically the same, but with intent,
    # this is mostly for readability, and to make sure I am thinking about the flow of code
    def register_state(self, state_name: str, default_state):
        if state_name in self.states:
            raise KeyError(f"State with name {state_name} already exists.")
        self.states[state_name] = default_state

    def change_state(self, state_name: str, state):
        if state_name not in self.states:
            raise KeyError(f"State with name {state_name} does not exist.")
        self.states[state_name] = state

    def unregister_state(self, state_name: str):
        if state_name not in self.states:
            raise KeyError(f"State with name {state_name} does not exist.")
        del self.states[state_name]

    def get_state(self, state_name: str):
        if state_name not in self.states:
            raise KeyError(f"State with name {state_name} does not exist.")
        return self.states[state_name]


class Game:
    """Core game class, has the event handler, the state handler, and asset handler references,
    a built-in plugin system with default function callers (for registering events and states, etc.)
    One of the ideas of this class is its standalone, and one shouldn't need to access anything besides the handles
    to send and receive events and states.
    """

    def __init__(self, *,
                 title="Game",
                 width=800,
                 height=600,
                 fps=60,
                 game_event_handler=None,
                 asset_manager=None,
                 game_state_handler=None
                 ):
        print(f"Initializing {title}...")
        self.game_event_handler = game_event_handler if game_event_handler else EventHandler()
        self.asset_manager = asset_manager if asset_manager else AssetManager()
        self.game_state_handler = game_state_handler if game_state_handler else GameStateHandler()

        self.width = width
        self.height = height
        self.title = title
        self.fps = fps
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()

        self.sprites = pygame.sprite.Group()
        self.register_system_events()
        self.game_modules = []
        self.modules_loaded = False

    def load_game_modules(self):
        # check to see if sub directory game_modules exists, if not create
        if not os.path.exists("game_modules"):
            os.makedirs("game_modules")
        for folder in os.listdir(os.path.join(os.getcwd(), "game_modules")):
            if folder.startswith("."):
                continue
            if not os.path.isdir(os.path.join(os.getcwd(), "game_modules", folder)):
                continue
            if not os.path.exists(os.path.join(os.getcwd(), "game_modules", folder, "__init__.py")):
                continue
            if folder not in [module.__name__ for module in self.game_modules]:
                print(f"Loading game module: {folder}")
                module = importlib.import_module(f"game_modules.{folder}")
                for func_name in [
                    "init",
                    "register_events",
                    "register_states"
                ]:
                    if hasattr(module, func_name):
                        print(f"Calling {func_name} for module {module.__name__}")
                        getattr(module, func_name)()
                self.game_modules.append(module)
        print(f"Loaded {len(self.game_modules)} game modules.")
        self.modules_loaded = True

    def register_system_events(self):
        self.game_event_handler.register(
            pygame.QUIT, lambda event: print(f"Quitting {self.title}") or pygame.quit() or quit(1)
        )

    def set_default_states(self):
        self.game_state_handler.register_state("scene", "menus.SplashScreen")

    def run(self):
        if not self.modules_loaded:
            self.load_game_modules()
        while True:
            try:
                self.game_event_handler.handle_events(pygame.event.get())
                self.update()
                self.render()
                self.clock.tick(self.fps)
            except Exception as e:
                print("(╯°□°）╯︵ ┻━┻")
                print("Something Broke....", e, sep="\n")

    def update(self):
        for game_module in self.game_modules:
            if hasattr(game_module, "update"):
                game_module.update()

    def render(self):
        self.screen.fill((0, 0, 0))
        self.sprites.draw(self.screen)
        for module in self.game_modules:
            if hasattr(module, "render"):
                module.render(self.screen)
        pygame.display.flip()

    def get_event_handler(self):
        return self.game_event_handler.__call__

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self._title = value

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        self._width = value

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        self._height = value

    @property
    def handles(self):
        return self.game_event_handler, self.asset_manager, self.game_state_handler

    # a function to create a markdown file for the docs in each game module, its functions, classes and class
    # functions (done so recursively) function names  and args, kwargs etc are collected and written to the markdown
    # file classes are written to the markdown file with their functions and class functions the markdown file is
    # then added to the docs folder in the game module indents children for readability
    def create_docs(self):
        import inspect
        for game_module in self.game_modules:
            print(f"Creating docs for {game_module.__name__}")
            with open(f"docs/{game_module.__name__}.md", "w") as f:
                f.write(f"# {game_module.__name__}\n\n")
                f.write(f"## Functions\n\n")
                for func_name, func in inspect.getmembers(game_module, inspect.isfunction):
                    f.write(f"### {func_name}\n\n")
                    f.write(f"```python\n{func.__name__}({inspect.signature(func)}\n```\n\n")
                    f.write(f"```{func.__doc__}\n```\n")
                f.write(f"## Classes\n\n")
                for class_name, class_ in inspect.getmembers(game_module, inspect.isclass):
                    f.write(f"### {class_name}\n\n")
                    f.write(f"```python\n{class_.__name__}({inspect.signature(class_.__init__)}\n```\n\n")
                    f.write(f"```{class_.__doc__}\n```\n")
                    f.write(f"## Class Functions\n\n")
                    for func_name, func in inspect.getmembers(class_, inspect.isfunction):
                        f.write(f"### {func_name}\n\n")
                        f.write(f"```python\n{func.__name__}({inspect.signature(func)}\n```\n\n")
                        f.write(f"```{func.__doc__}\n```\n")
            print(f"Finished creating docs for {game_module.__name__}")

    def test(self):
        if not self.modules_loaded:
            self.load_game_modules()
        print(f"Starting tests for {self.title}")
        print(f"{self.title} has {len(self.game_modules)} modules")
        for game_module in self.game_modules:
            if hasattr(game_module, "test"):
                print(f"Testing {game_module.__name__}")
                game_module.test()
        self.game_event_handler.handle(pygame.event.Event(pygame.QUIT))


game = Game()


def get_handles():
    return game.handles
