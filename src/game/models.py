from django.db import models
from django.contrib.auth.models import User

GAME_GRID_HEIGHT = 6
GAME_GRID_WIDTH = 7


class Player(models.Model):
    """
    Class to represent a Player
    """
    name = models.CharField(max_length=40)
    games_won = models.IntegerField(default=0)


class Game(models.Model):
    """
    Class to represent a game of Connect4 between two players
    """
    player_1 = models.ForeignKey(Player, related_name="player_1", on_delete=models.CASCADE)
    player_2 = models.ForeignKey(Player, related_name="player_2", on_delete=models.CASCADE)
    current_player = models.ForeignKey(Player, related_name="current_player", on_delete=models.CASCADE)
    winner = models.ForeignKey(Player, related_name="winner", on_delete=models.CASCADE)
    # Declaring possible states for a game
    GAME_STATE_TYPES = [
        ("ONGOING", "ONGOING"),
        ("COMPLETE", "COMPLETE")
    ]
    # Field indicating whether a cell is empty or occupied
    game_state = models.CharField(choices=GAME_STATE_TYPES, default="ONGOING", max_length=20)

    def __str__(self):
        return "Game of Connect4 between " + str(self.player_1) + " and " + str(self.player_2)

    def get_state(self):
        """
        Method to fetch state of the game
        """
        return self.game_state

    def get_game_cells(self):
        """
        Method to fetch all game cells belonging to the game
        """
        return GameCell.objects.get(game=self)

    def change_turns(self):
        """
        Method to rotate turns
        """
        self.current_player = self.player_1 if self.current_player != self.player_1 else self.player_2
        self.save()

    def play_turn(self, game_grid_column):
        """
        Method to play a turn in the game
        """
        # Find cell to put coin into
        cell_to_occupy = self.find_empty_cell(game_grid_column)
        if cell_to_occupy == -1:
            return -1
        # Set current player as owner of the empty cell retrieved
        cell_to_occupy.set_state(self.current_player)
        if self.check_victory(cell_to_occupy):
            self.mark_complete()
        else:
            self.change_turns()

    def find_empty_cell(self, game_grid_column):
        """
        Method to find first empty cell in column selected by current player.
        Returns -1 if no empty cell is available.
        """
        for i in range(GAME_GRID_HEIGHT - 1, -1, -1):
            cell = GameCell.objects.get(x_pos=game_grid_column, y_pos=i)
            if cell.get_state()[0] == "EMPTY":
                return cell
        return -1

    def check_victory(self, game_cell):
        """
        Method to check if current player's last move has resulted in victory
        """

        def check_indices(indices):
            cell_states = [GameCell.objects.get_state(x_pos=index[1], y_pos=index[0]) for index in indices]
            is_victory = True
            for cell_state in cell_states:
                if cell_state[0] == "EMPTY" or cell_state[1] != self.current_player:
                    is_victory = False
            return is_victory

        def check_horizontal(i, j, dir):
            if j + 1 + dir * 4 > GAME_GRID_WIDTH or j + 1 + dir * 4 < 0:
                return False
            indices = [(i, j + dir * 1), (i, j + dir * 2), (i, j + dir * 3)]
            return check_indices(indices)

        def check_vertical(i, j, dir):
            if i + dir * 4 > GAME_GRID_HEIGHT or i + dir * 4 < 0:
                return False
            indices = [(i + dir * 1, j), (i + dir * 2, j), (i + dir * 3, j)]
            return check_indices(indices)

        def check_diagonal(i, j, dir):
            if i - dir * 4 < 0 or i - dir * 4 > GAME_GRID_HEIGHT or j + 1 + dir * 4 > GAME_GRID_WIDTH \
                    or j + 1 + dir * 4 < 0:
                return False
            indices = [(i - dir * 1, j + dir * 1), (i - dir * 2, j + dir * 2), (i - dir * 3, j + dir * 3)]
            return check_indices(indices)

        # Get co-ordinates of cell occupied by current player in last move
        # (i, j) indices correspond to (y, x) positions respectively
        # (0,0) at top left corner of the game grid
        j, i = game_cell.get_cell_position()
        if check_vertical(i, j, 1):
            return i, j, "Bottom"
        if check_horizontal(i, j, 1):
            return i, j, "Right"
        if check_horizontal(i, j, -1):
            return i, j, "Left"
        if check_diagonal(i, j, 1):
            return i, j, "Right Diagonal"
        if check_diagonal(i, j, -1):
            return i, j, "Left Diagonal"
        return False

    def mark_complete(self):
        """
        Method to mark a game as complete and record the winner
        """
        self.winner = self.current_player
        self.game_state = "COMPLETE"
        self.save()


class GameCell(models.Model):
    """
    Class to represent a cell in a game of Connect4
    """
    # Co-ordinates to identify a cell's position on the game grid
    x_pos = models.IntegerField()
    y_pos = models.IntegerField()
    # Declaring possible states for a cell
    STATE_TYPES = [
        ("EMPTY", "EMPTY"),
        ("OCCUPIED", "OCCUPIED")
    ]
    # Field indicating whether a cell is empty or occupied
    state = models.CharField(choices=STATE_TYPES, default="EMPTY", max_length=20)
    # Field indicating owner of a cell. Null for 'EMPTY' cells
    owner = models.ForeignKey(Player, null=True, blank=True, on_delete=models.CASCADE)
    # Adding game to which this cell belongs
    game = models.ForeignKey(Game, on_delete=models.CASCADE)

    def set_state(self, player):
        """
        Method to represent occupation of cell by a player
        """
        self.state = "OCCUPIED"
        self.owner = player
        self.save(update_fields=["state", "owner"])

    def get_state(self):
        """
        Method to fetch state of a cell
        """
        return self.state, self.owner

    def get_cell_position(self):
        """
        Method to fetch position of the cell on game grid
        """
        return self.x_pos, self.y_pos
