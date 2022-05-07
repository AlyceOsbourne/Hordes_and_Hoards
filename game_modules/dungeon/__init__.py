import game_modules.dungeon.wfc as wfc
import game_modules.dungeon.tiledata as td

VERBOSE = False
def test():
    wfc.VERBOSE = VERBOSE
    td.VERBOSE = VERBOSE
    grid = wfc.NodeGrid.generate_grid(16, 16)
    print("\n".join(["".join(["{:1}".format(x) for x in row]) for row in grid]))

