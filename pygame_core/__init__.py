import importlib
import os

import psutil
import pygame

# TODO! make the asset manager work on other platforms as files only seem to load on windows
from pygame_core.asset_handler import AssetHandler
from pygame_core.event_handler import EventHandler
from pygame_core.state_handler import StateHandler

pygame.init()


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
                 game_asset_manager=None,
                 game_state_handler=None
                 ):
        self.game_event_handler = game_event_handler if game_event_handler else EventHandler()
        self.asset_manager = game_asset_manager if game_asset_manager else AssetHandler()
        self.game_state_handler = game_state_handler if game_state_handler else StateHandler()
        self.register_system_events()
        self.game_state_handler.add_states(
            screen_width=width,
            screen_height=height,
            input_locked=False,
            verbose=True,
            developer_mode=True,
            save_data=None
        )
        self.width = width
        self.height = height
        self.title = title
        self.version = version
        self.fps = fps
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(self.title)
        self.clock = pygame.time.Clock()

        self.sprites = pygame.sprite.Group()

        self.game_modules = []
        self.modules_loaded = False

    def load_game_modules(self):
        for module_directory in ["system_modules", "game_modules"]:
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

    def get_game_module(self, module_name):
        for module in self.game_modules:
            if module.__name__ == module_name:
                return module

    def get_game_modules(self):
        return self.game_modules

    def register_system_events(self):
        self.game_event_handler.register(
            pygame.QUIT, lambda event: print(f"Quitting {self.title}") or pygame.quit() or quit(1)
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


def get_game(instance: set = set()):
    if len(instance) == 0:
        instance.add(Game())
    return next(iter(instance))


__all__ = ["get_game", "pygame", "StateHandler", "EventHandler", "AssetHandler", "Game"]
