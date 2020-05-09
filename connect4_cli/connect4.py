import numpy as np

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
        self.current_coin = COIN_RED
        self.winner = ""
        self.state = "ONGOING"
        self.game_grid = Grid()
        self.w = GRID_WIDTH
        self.h = GRID_HEIGHT

    def get_state(self):
        return self.state

    def play_turn(self):
        print("\n{}'s turn".format(self.current_turn))
        retry = True
        while retry:
            try:
                retry = False
                col = int(input("Enter a column (1-{}): ".format(self.w)))
                if not 1 <= col <= 7:
                    raise Exception
            except Exception:
                print("You entered an invalid input! Please re-enter!")
                retry = True
        i, j = self.game_grid.put_coin(col-1, self.current_coin)
        self.game_grid.print_grid()
        victory = self.game_grid.check_victory(i, j, self.current_coin)
        if victory:
            self.state = "COMPLETED"
            self.winner = self.current_turn
            print("\n{} has won!! Congratulations! :D".format(self.winner))
        else:
            self.rotate_turn()

    def rotate_turn(self):
        if self.current_turn == self.p_blue:
            self.current_turn = self.p_red
            self.current_coin = COIN_RED
        else:
            self.current_turn = self.p_blue
            self.current_coin = COIN_BLUE

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
            return empty_row, col_num
        else:
            return False

    def check_victory(self, x, y, current_coin):
        sub_seq_len = np.zeros((3, 3), dtype=np.uint)
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if i == j == 0:
                    continue
                for step_size in range(1, 4):
                    x_new = x + step_size * i
                    y_new = y + step_size * j
                    if x_new in range(0, GRID_HEIGHT) and y_new in range(0, GRID_WIDTH) \
                            and self.grid[x_new][y_new] == current_coin:
                        sub_seq_len[i][j] += 1
                    else:
                        break
        if np.sum(sub_seq_len, axis=0)[1] == 3 or np.sum(sub_seq_len, axis=1)[1] == 3 \
                or np.trace(sub_seq_len) == 3 or np.trace(np.fliplr(sub_seq_len)) == 3:
            return True
        return False

if __name__ == "__main__":
    player1 = input("Enter Player 1 : ")
    player2 = input("Enter Player 2 : ")
    game = Game(player1, player2)
    while game.get_state() != "COMPLETED":
        game.play_turn()
