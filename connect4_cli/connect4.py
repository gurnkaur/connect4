EMPTY_CELL = "_"
COIN_RED = "R"
COIN_BLUE = "B"
GRID_HEIGHT = 6
GRID_WIDTH = 7

class Game:
    def __init__(self, p_red, p_blue):
        print("Starting a game of Connect4 between {0} and {1}.".format(p_red, p_blue))
        self.p_red = p_red
        self.p_blue = p_blue
        print("{0} gets first turn.".format(p_red))
        self.current_turn = p_red
        self.winner = ""
        self.state = "ONGOING"
        self.game_grid = Grid()
        self.w = GRID_WIDTH
        self.h = GRID_HEIGHT

    def get_state(self):
        return self.state

    def play_turn(self):
        print("\n{}'s turn".format(self.current_turn))
        col = int(input("Enter a column (1-{}): ".format(self.w)))
        if self.current_turn == self.p_blue:
            i, j = self.game_grid.put_coin(col-1, COIN_BLUE)
        else:
            i, j = self.game_grid.put_coin(col-1, COIN_RED)
        self.game_grid.print_grid()
        victory = self.game_grid.check_victory(i, j)
        if victory:
            self.state = "COMPLETED"
            self.winner = self.current_turn
            print("\n{} has won!! Congratulations! :D".format(self.winner))
        else:
            self.rotate_turn()

    def rotate_turn(self):
        if self.current_turn == self.p_blue:
            self.current_turn = self.p_red
        else:
            self.current_turn = self.p_blue

class Grid:
    def __init__(self):
        self.w = GRID_WIDTH
        self.h = GRID_HEIGHT
        self.grid = [[EMPTY_CELL] * self.w for i in range(self.h)]

    def print_grid(self):
        print("-----" * self.w)
        for row in self.grid:
            print(row)
        print("-----" * self.w)

    def put_coin(self, col_num, coin_type):
        if coin_type not in [COIN_BLUE, COIN_RED]:
            raise NotImplementedError("Invalid Coin Type")

        def find_empty_row():
            for i in range(self.h - 1, -1, -1):
                current_row = self.grid[i]
                if current_row[col_num] == EMPTY_CELL:
                    return i
            return -1

        empty_row = find_empty_row()
        if empty_row > -1:
            self.grid[empty_row][col_num] = coin_type
            print(empty_row, col_num)
            return empty_row, col_num
        else:
            return False

    def check_victory(self, x, y):
        def check_horizontal(i, j, dir):
            if j + 1 + dir * 4 > self.w or j + 1 + dir * 4 < 0:
                return False
            else:
                val = self.grid[i][j]
                if val == EMPTY_CELL:
                    return False
                val_1 = self.grid[i][j + dir * 1]
                if val_1 == val:
                    val_2 = self.grid[i][j + dir * 2]
                    if val_2 == val_1:
                        val_3 = self.grid[i][j + dir * 3]
                        if val_3 == val_2:
                            return True

        def check_vertical(i, j, dir):
            if i + dir * 4 > self.h or i + dir * 4 < 0:
                return False
            else:
                val = self.grid[i][j]
                if val == EMPTY_CELL:
                    return False
                val_1 = self.grid[i + dir * 1][j]
                if val_1 == val:
                    val_2 = self.grid[i + dir * 2][j]
                    if val_2 == val_1:
                        val_3 = self.grid[i + dir * 3][j]
                        if val_3 == val_2:
                            return True

        def check_diag(i, j, dir):
            if i - dir * 4 < 0 or i - dir * 4 > self.h or j + 1 + dir * 4 > self.w or j + 1 + dir * 4 < 0:
                return False
            else:
                val = self.grid[i][j]
                if val == EMPTY_CELL:
                    return False
                val_1 = self.grid[i - dir * 1][j + dir * 1]
                if val_1 == val:
                    val_2 = self.grid[i - dir * 2][j + dir * 2]
                    if val_2 == val_1:
                        val_3 = self.grid[i - dir * 3][j + dir * 3]
                        if val_3 == val_2:
                            return True

        def check_right(i, j):
            return check_horizontal(i, j, 1)

        def check_left(i, j):
            return check_horizontal(i, j, -1)

        def check_bottom(i, j):
            return check_vertical(i, j, 1)

        if check_bottom(x, y):
            return x, y, "Top"
        if check_right(x, y):
            return x, y, "Right"
        if check_left(x, y):
            return x, y, "Left"
        if check_diag(x, y, 1):
            return x, y, "DiagRight"
        if check_diag(x, y, -1):
            return x, y, "DiagLeft"
        return False

if __name__ == "__main__":
    player1 = input("Enter Player 1 : ")
    player2 = input("Enter Player 2 : ")
    game = Game(player1, player2)
    while game.get_state() != "COMPLETED":
        game.play_turn()
