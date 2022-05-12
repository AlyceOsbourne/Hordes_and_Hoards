import os
from functools import partial

import pygame


# TODO! make the asset manager work on other platforms as files only seem to load on windows
class AssetHandler:
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
