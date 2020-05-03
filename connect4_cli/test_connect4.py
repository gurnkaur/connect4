from connect4 import Grid, COIN_RED, COIN_BLUE, GRID_WIDTH, GRID_HEIGHT

def drop_alternate(grid, col_num, start_with_red, upto=GRID_HEIGHT):
    for i in range(upto):
        if start_with_red:
            grid.put_coin(col_num, COIN_RED)
            start_with_red = False
        else:
            grid.put_coin(col_num, COIN_BLUE)
            start_with_red = True

class TestDropCoin:
    def test_gravity_alternate(self):
        g = Grid()
        col_num = 2
        coin_red = True
        drop_alternate(g, col_num, coin_red)
        g.print_grid()
        assert g.grid[GRID_HEIGHT - 1][col_num] == COIN_RED
        assert g.grid[GRID_HEIGHT - 2][col_num] == COIN_BLUE
        assert g.grid[GRID_HEIGHT - 3][col_num] == COIN_RED
        assert g.grid[GRID_HEIGHT - 4][col_num] == COIN_BLUE

    def test_gravity_horizontal(self):
        g = Grid()
        coin_red = True
        for i in range(GRID_WIDTH):
            g.put_coin(i, COIN_RED)
        for i in range(GRID_WIDTH):
            g.put_coin(i, COIN_BLUE)
        g.print_grid()

        assert g.grid[GRID_HEIGHT - 1][GRID_WIDTH - 3] == COIN_RED
        assert g.grid[GRID_HEIGHT - 2][GRID_WIDTH - 5] == COIN_BLUE


class TestVictory:
    def test_horizontal(self):
        g = Grid()
        for i in range(4):
            x, y = g.put_coin(i, COIN_RED)
        assert g.check_victory(x, y) == (5, 3, "Left")

    def test_horizontal1(self):
        g = Grid()
        start_with_red = True
        for i in range(3):
            drop_alternate(g, i, start_with_red, GRID_HEIGHT - 2)
        drop_alternate(g, 3, not start_with_red, GRID_HEIGHT - 3)
        x, y = g.put_coin(3, COIN_RED)
        assert g.check_victory(x, y) is False
