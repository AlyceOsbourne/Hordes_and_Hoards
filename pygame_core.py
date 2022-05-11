import importlib
import os
from functools import partial
from itertools import count

import psutil
import pygame

# TODO! make the asset manager work on other platforms as files only seem to load on windows

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

    def create_event(self, event_name: str):
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

    def __call__(self, *event_types):
        def decorator(handler):
            for event_type in event_types:
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

    def number_of_images(self):
        return len(self.assets["images"])

    def number_of_sounds(self):
        return len(self.assets["sounds"])

    def number_of_fonts(self):
        return len(self.assets["fonts"])


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
    def add_state(self, state_name: str, default_state):
        if state_name in self.states:
            raise KeyError(f"State with name {state_name} already exists.")
        self.states[state_name] = default_state

    def add_states(self, **states):
        for state_name, state in states.items():
            self.add_state(state_name, state)

    def set_state(self, state_name: str, state):
        if state_name not in self.states:
            raise KeyError(f"State with name {state_name} does not exist.")
        self.states[state_name] = state

    def set_states(self, **states):
        for state_name, state in states.items():
            self.set_state(state_name, state)

    def remove_state(self, state_name: str):
        if state_name not in self.states:
            raise KeyError(f"State with name {state_name} does not exist.")
        del self.states[state_name]

    def remove_states(self, *state_names):
        for state_name in state_names:
            self.remove_state(state_name)

    def get_state(self, state_name: str):
        if state_name not in self.states:
            raise KeyError(f"State with name {state_name} does not exist.")
        return self.states[state_name]

    def get_states(self, *state_names):
        return [self.get_state(state_name) for state_name in state_names]

    def get_all_states(self):
        return self.states


class Game:
    """Core game class, has the event handler, the state handler, and asset handler references,
    a built-in plugin system with default function callers (for registering events and states, etc.)
    One of the ideas of this class is its standalone, and one shouldn't need to access anything besides the handles
    to send and receive events and states.
    """

    def __init__(self, *,
                 title="",
                 width=16 * 32,
                 height=16 * 32,
                 fps=60,
                 version="0.0.0",
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
        self.version = version
        self.fps = fps
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(self.title)
        self.clock = pygame.time.Clock()

        self.sprites = pygame.sprite.Group()
        self.register_system_events()
        self.set_default_states()
        self.game_modules = []
        self.modules_loaded = False

    def load_game_modules(self):
        for module_directory in ["core_modules", "game_modules"]:
            if not os.path.exists(module_directory):
                os.makedirs(module_directory)
            for folder in os.listdir(os.path.join(os.getcwd(), module_directory)):
                if folder.startswith("."):
                    continue
                if not os.path.isdir(os.path.join(os.getcwd(), module_directory, folder)):
                    continue
                if not os.path.exists(os.path.join(os.getcwd(), module_directory, folder, "__init__.py")):
                    continue
                if folder not in [module.__name__ for module in self.game_modules]:
                    print(f"Loading {module_directory}: {folder}")
                    module = importlib.import_module(f"{module_directory}.{folder}")
                    for func_name in [
                        "init",
                        "register_events",
                        "register_states"
                    ]:
                        if hasattr(module, func_name):
                            print(f"Calling {func_name} for module {module.__name__}")
                            getattr(module, func_name)()
                    self.game_modules.append(module)
            print(f"Loaded {len(self.game_modules)} {module_directory}.")
            self.modules_loaded = True

    def register_system_events(self):
        self.game_event_handler.register(
            pygame.QUIT, lambda event: print(f"Quitting {self.title}") or pygame.quit() or quit(1)
        )

    def set_default_states(self):
        self.game_state_handler.add_states(
            input_locked=False,
            verbose=True,
            developer_mode=True,
            save_data=None
        )

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
                print("Something Broke....", sep="\n")
                raise e

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
        pygame.display.set_caption(value)
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

    def get_fps(self):
        return self.clock.get_fps()

    @staticmethod
    def get_ram_usage():
        return psutil.Process(os.getpid()).memory_info().rss

    @staticmethod
    def get_cpu_usage():
        return psutil.Process(os.getpid()).cpu_percent()

    @staticmethod
    def get_num_cores():
        return psutil.cpu_count()

    @staticmethod
    def get_disk_usage():
        return psutil.disk_usage(".").percent

    def test(self, verbose=False, raise_exceptions=False):
        if not self.modules_loaded:
            self.load_game_modules()
        print(f"Starting tests for {self.title}")
        print(f"{self.title} has {len(self.game_modules)} modules")
        for game_module in self.game_modules:
            try:
                print(f"Testing {game_module.__name__}")
                if hasattr(game_module, "test"):
                    print(f"{game_module.__name__} has a test function, running...")
                    if verbose and hasattr(game_module, "VERBOSE"):
                        print(f"Making {game_module.__name__} verbose")
                        game_module.VERBOSE = verbose
                    game_module.test()
                else:
                    print(f"{game_module.__name__} has no test function, moving on.")
            except Exception as e:
                print(f"Failed to test {game_module.__name__}")
                if raise_exceptions:
                    raise e
                else:
                    print(f"{e}")
            finally:
                print(f"Finished testing {game_module.__name__}")
        print(f"Finished tests for {self.title}")
        self.game_event_handler.handle(pygame.event.Event(pygame.QUIT))


def get_game(instance=set()):
    if len(instance) == 0:
        instance.add(Game())
    return next(iter(instance))


__all__ = ["get_game", "pygame"]
