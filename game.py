class RockPaperScissors:
    def __init__(self):
        self.moves = ['rock', 'paper', 'scissors']
        self.winning_moves = {
            'rock': 'scissors',
            'paper': 'rock',
            'scissors': 'paper'
        }