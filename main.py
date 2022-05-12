from pygame_interface import get_game
game = get_game()
game.title = "Hordes and Hoards"
if __name__ == '__main__':
    # game.test(False, True)
    get_game().run()
