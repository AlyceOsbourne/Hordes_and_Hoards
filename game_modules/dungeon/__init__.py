import game_modules.dungeon.wfc as wfc

w = wfc.NodeGrid((50,25))

def test():
    w.start_generation()
    n = w.collapse_to_char_grid(w.grid)
    # pretty print n
    for row in n:
        print("".join(row))
