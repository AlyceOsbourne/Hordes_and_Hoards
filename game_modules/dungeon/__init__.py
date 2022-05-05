import game_modules.dungeon.tileset
from game_modules.dungeon.wfc import NodeGrid


def test():
    grid = NodeGrid.generate_grid(16,16)
    grid = tileset.Tiles.convert_to_tiles(grid)
    print("\n".join(["".join(row) for row in grid]), sep='\n')
