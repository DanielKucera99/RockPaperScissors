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
        if self.last_outcome is not None:
            if self.last_outcome:
                return self.last_move
            else:
                new_move = self.last_move
                while new_move == self.last_move:
                    new_move = random.choice(self.moves)
                return new_move
        else:
            return random.choice(self.moves)

    def update_last_outcome(self, move, opponent_move, player_win):
        self.last_outcome = player_win
        self.last_move = move


class WinRepeatLoseCopyStrategy:
    def __init__(self):
        self.last_opponent_move = None
        self.name = "Win-Repeat/Lose-Copy"
        self.last_move = None
        self.last_outcome = None
        self.moves = ['rock', 'paper', 'scissors']

    def move(self):
        if self.last_outcome is not None:
            if self.last_outcome:
                return self.last_move
            else:
                return self.last_opponent_move
        else:
            return random.choice(self.moves)

    def update_last_outcome(self, move, opponent_move, player_win):
        self.last_outcome = player_win
        self.last_move = move
        self.last_opponent_move = opponent_move


class MostWinsStrategy:
    def __init__(self):
        self.name = "Most Wins"
        self.moves = ['rock', 'paper', 'scissors']
        self.win_counts = {'rock': 0, 'paper': 0, 'scissors': 0}

    def move(self):

        most_wins_move = max(self.win_counts, key=self.win_counts.get)
        return most_wins_move

    def update_last_outcome_most_wins(self, rock_wins, paper_wins, scissors_wins):

        self.win_counts = {'rock': rock_wins, 'paper': paper_wins, 'scissors': scissors_wins}


class CounterStrategy:
    def __init__(self):
        self.name = "Counter Strategy"
        self.moves = ['rock', 'paper', 'scissors']
        self.move_to_counter = None

    def move(self):

        if self.move_to_counter is not None:
            most_used_move = self.move_to_counter
        else:
            return random.choice(self.moves)

        winning_move = {'rock': 'paper', 'paper': 'scissors', 'scissors': 'rock'}

        return winning_move[most_used_move]

    def update_opponent_move(self, player):
        self.move_to_counter = player.get_most_used_move()

