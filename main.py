import pygame_core

event_handler, asset_manager, gamestate_handler = pygame_core.EventHandler(), pygame_core.AssetManager(), pygame_core.GameStateHandler()
game = pygame_core.Game(event_handler, asset_manager, gamestate_handler)

if __name__ == "__main__":

    game.run()