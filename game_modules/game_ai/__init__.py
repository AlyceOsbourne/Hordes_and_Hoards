import random

import game_modules.game_ai.a_star as a_s
VERBOSE = False

def test():
    a_s.VERBOSE = VERBOSE
    from game_modules.dungeon.wfc import NodeGrid
    from game_modules.dungeon import tiledata

    grid = NodeGrid.generate_grid(16, 16)
    walkable = tiledata.Tiles.get_walkable_tiles(grid)
    for _ in range(5):
        start = None
        while start is None or not walkable[start[0]][start[1]]:
            start = (random.randint(0, len(walkable)-1), random.randint(0, len(walkable[0]))-1)
        end = None
        while end is None or not walkable[end[0]][end[1]]:
            end = (random.randint(0, len(walkable)-1), random.randint(0, len(walkable[0])-1))
        path = a_s.a_star(start, end, walkable)
        if path is None:
            print("No path found")
        else:
            for x in range(len(grid)):
                for y in range(len(grid[x])):
                    if (x, y) in path:
                        print("\033[91m" + grid[x][y] + "\033[0m", end="")
                    else:
                        print(grid[x][y], end="")
                print()
            print()







