import random

class AlwaysRockStrategy:
    def __init__(self):
        self.name = "Always Rock"

    def move(self):
        return 'rock'


class AlwaysScissorsStrategy:
    def __init__(self):
        self.name = "Always Scissors"

    def move(self):
        return 'scissors'


class AlwaysPaperStrategy:
    def __init__(self):
        self.name = "Always Paper"

    def move(self):
        return 'paper'


class RandomStrategy:
    def __init__(self):
        self.name = "Random"

    def move(self):
        return random.choice(['rock', 'paper', 'scissors'])


class RockScissorsPaperStrategy:
    def __init__(self):
        self.name = "Rock-Scissors-Paper"
        self.moves = ['rock', 'scissors', 'paper']
        self.current_move_index = 0

    def move(self):
        move = self.moves[self.current_move_index]
        self.current_move_index = (self.current_move_index + 1) % len(self.moves)
        return move


class WinRepeatLoseChangeStrategy:
    def __init__(self):
        self.name = "Win-Repeat/Lose-Change"
        self.last_move = None
        self.last_outcome = None
        self.moves = ['rock', 'paper', 'scissors']

    def move(self):
        if self.last_outcome == 'win':
            # Repeat the last move if the player won
            return self.last_move
        elif self.last_outcome == 'lose':
            # Change the move to something else if the player lost
            # Choose a move different from the last one
            new_move = self.last_move
            while new_move == self.last_move:
                new_move = random.choice(self.moves)
            return new_move
        else:
            # Choose a random move for the first round
            return random.choice(self.moves)

    def update_last_outcome(self, outcome, move, opponent_move):
        self.last_outcome = outcome
        self.last_move = move


class WinRepeatLoseCopyStrategy:
    def __init__(self):
        self.last_opponent_move = None
        self.name = "Win-Repeat/Lose-Copy"
        self.last_move = None
        self.last_outcome = None
        self.moves = ['rock', 'paper', 'scissors']

    def move(self, outcome=None):
        if outcome is not None:
            self.last_outcome = outcome

        if self.last_outcome == 'win':
            # Repeat the last move if the player won
            return self.last_move
        elif self.last_outcome == 'lose':
            # Copy the opponent's move if the player lost
            return self.last_opponent_move
        else:
            # Choose a random move for the first round
            return random.choice(self.moves)

    def update_last_outcome_to_copy(self, outcome, move, opponent_move):
        self.last_outcome = outcome
        self.last_move = move
        self.last_opponent_move = opponent_move
