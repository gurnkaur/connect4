from django.db import models


class Player(models.Model):
    name = models.CharField(max_length=40)
    games_won = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Game(models.Model):
    player_1 = models.ForeignKey(Player, related_name="player_1", on_delete=models.CASCADE)
    player_2 = models.ForeignKey(Player, related_name="player_2", on_delete=models.CASCADE)
    current_player = models.ForeignKey(Player, related_name="current_player", on_delete=models.CASCADE)
    winner = models.ForeignKey(Player, related_name="winner", on_delete=models.CASCADE, null=True)
    # Declaring possible states for a game
    GAME_STATE_CHOICES = [
        ("READY", "READY"),
        ("IN PROGRESS", "IN PROGRESS"),
        ("COMPLETE", "COMPLETE")
    ]
    game_state = models.CharField(choices=GAME_STATE_CHOICES, default="READY", max_length=20)

    def __str__(self):
        return "Connect4 Game between {0} and {1}".format(self.player_1, self.player_2)


class Grid(models.Model):
    height = models.IntegerField()
    width = models.IntegerField()
    game = models.ForeignKey(Game, on_delete=models.CASCADE)

    def __str__(self):
        return "Game Grid of {0}".format(self.game)


class Cell(models.Model):
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
    owner = models.ForeignKey(Player, null=True, on_delete=models.CASCADE)
    # Adding game grid to which this cell belongs
    grid = models.ForeignKey(Grid, on_delete=models.CASCADE)

    def __str__(self):
        return "Cell at position ({0}, {1}) on {2}".format(self.x_pos, self.y_pos, self.grid)
