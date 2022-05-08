import game_modules.dungeon.wfc as wfc
import game_modules.dungeon.tiledata as td

VERBOSE = False

def test():
    wfc.VERBOSE = VERBOSE
    td.VERBOSE = VERBOSE
    for _ in range(10):
        grid = wfc.NodeGrid.generate_grid(32, 32)
        if VERBOSE:
            print("\n".join(["".join(["{:1}".format(x) for x in row]) for row in grid]))

