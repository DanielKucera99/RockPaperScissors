from game import RockPaperScissors
from strategies import (AlwaysRockStrategy, AlwaysScissorsStrategy, AlwaysPaperStrategy, RandomStrategy,
                        RockScissorsPaperStrategy, WinRepeatLoseChangeStrategy, WinRepeatLoseCopyStrategy,
                        MostWinsStrategy, CounterStrategy)
import networkx as nx


class Player:
    def __init__(self, name, strategy, most_used_move, number_of_times_most_used_move_was_used,
                 number_of_times_rock_was_used, number_of_times_paper_was_used, number_of_times_scissors_were_used):
        self.name = name
        self.strategy = strategy
        self.most_used_move = most_used_move
        self.number_of_times_most_used_move_was_used = number_of_times_most_used_move_was_used
        self.number_of_times_rock_was_used = number_of_times_rock_was_used
        self.number_of_times_paper_was_used = number_of_times_paper_was_used
        self.number_of_times_scissors_were_used = number_of_times_scissors_were_used

    def get_player_strategy(self):
        return self.strategy

    def get_most_used_move(self):
        return self.most_used_move

    def increase_rock_use(self):
        self.number_of_times_rock_was_used = self.number_of_times_rock_was_used + 1

    def increase_paper_use(self):
        self.number_of_times_paper_was_used = self.number_of_times_paper_was_used + 1

    def increase_scissors_use(self):
        self.number_of_times_scissors_were_used = self.number_of_times_scissors_were_used + 1

    def get_number_of_times_most_used_move_was_used(self):
        return self.number_of_times_most_used_move_was_used

    def set_most_used_move(self, move):
        self.most_used_move = move

    def get_number_of_times_rock_was_used(self):
        return self.number_of_times_rock_was_used

    def get_number_of_times_paper_was_used(self):
        return self.number_of_times_paper_was_used

    def get_number_of_times_scissors_were_used(self):
        return self.number_of_times_scissors_were_used

    def set_number_of_times_most_used_move_was_used(self, number):
        self.number_of_times_most_used_move_was_used = number


class NetworkGame:
    def __init__(self, num_players):
        self.num_players = num_players
        self.network = self.create_complete_graph(num_players)
        self.players = self.assign_players()

    @staticmethod
    def create_complete_graph(num_players):
        return nx.complete_graph(num_players)

    def assign_players(self):
        players = []

        strategies = [
            AlwaysRockStrategy(),
            AlwaysScissorsStrategy(),
            AlwaysPaperStrategy(),
            RockScissorsPaperStrategy(),
            WinRepeatLoseChangeStrategy(),
            WinRepeatLoseCopyStrategy(),
            MostWinsStrategy(),
            CounterStrategy()
        ]

        strategies.extend(RandomStrategy() for _ in range(8, self.num_players))
        for i, strategy in enumerate(strategies, start=1):
            player_name = f'Player {i}'
            players.append(Player(player_name, strategy, "", 0, 0, 0, 0))

        return players

    @staticmethod
    def play_round(player1, player2, move1, move2, rock_wins, paper_wins, scissors_wins):

        player1win = False
        player2win = False

        if move2 == RockPaperScissors().winning_moves[move1]:
            result = f"{player1.name} wins"
            player1win = True
        elif move1 == RockPaperScissors().winning_moves[move2]:
            result = f"{player2.name} wins"
            player1win = True
        else:
            result = "Draw"


        if hasattr(player1.strategy, 'update_last_outcome'):
            player1.strategy.update_last_outcome(move1, move2, player1win)
        if hasattr(player2.strategy, 'update_last_outcome'):
            player2.strategy.update_last_outcome(move2, move1, player2win)

        if hasattr(player1.strategy, 'update_last_outcome_most_wins'):
            player1.strategy.update_last_outcome_most_wins(rock_wins, paper_wins, scissors_wins)
        if hasattr(player2.strategy, 'update_last_outcome_most_wins'):
            player2.strategy.update_last_outcome_most_wins(rock_wins, paper_wins, scissors_wins)

        if hasattr(player1.strategy, 'update_opponent_move'):
            player1.strategy.update_opponent_move(player2)
        if hasattr(player2.strategy, 'update_opponent_move'):
            player2.strategy.update_opponent_move(player1)

        if hasattr(player1.strategy, 'update_last_outcome_most_wins'):
            player1.strategy.update_last_outcome_most_wins(rock_wins, paper_wins, scissors_wins)
        if hasattr(player2.strategy, 'update_last_outcome_most_wins'):
            player2.strategy.update_last_outcome_most_wins(rock_wins, paper_wins, scissors_wins)
        return result

    def run_simulation(self):
        results = []
        rock_wins = 0
        paper_wins = 0
        scissors_wins = 0

        player_wins = {player.name: 0 for player in self.players}

        for i, player1 in enumerate(self.players):
            for j, player2 in enumerate(self.players):
                if i < j:
                    move1 = player1.strategy.move()
                    move2 = player2.strategy.move()
                    result = self.play_round(player1, player2, move1, move2, rock_wins, paper_wins, scissors_wins)
                    results.append((player1.name, player2.name, result))

                    self.count_the_most_used_move(player1, move1)
                    self.count_the_most_used_move(player2, move2)

                    if "wins" in result:
                        if player1.name in result:
                            player_wins[player1.name] += 1
                            winning_move = move1
                        else:
                            winning_move = move2
                            player_wins[player2.name] += 1

                        if winning_move == 'rock':
                            rock_wins += 1
                        elif winning_move == 'paper':
                            paper_wins += 1
                        elif winning_move == 'scissors':
                            scissors_wins += 1

        return player_wins, rock_wins, paper_wins, scissors_wins

    @staticmethod
    def count_the_most_used_move(player, move):
        if player.get_most_used_move() != move:
            if move == 'rock':
                player.increase_rock_use()
                number_of_rock_used = player.get_number_of_times_rock_was_used()
                if number_of_rock_used > player.get_number_of_times_most_used_move_was_used():
                    player.set_most_used_move(move)
                    player.set_number_of_times_most_used_move_was_used(number_of_rock_used)
            elif move == 'paper':
                player.increase_paper_use()
                number_of_paper_used = player.get_number_of_times_paper_was_used()
                if number_of_paper_used > player.get_number_of_times_most_used_move_was_used():
                    player.set_most_used_move(move)
                    player.set_number_of_times_most_used_move_was_used(number_of_paper_used)
            elif move == 'scissors':
                player.increase_scissors_use()
                number_of_scissors_used = player.get_number_of_times_scissors_were_used()
                if number_of_scissors_used > player.get_number_of_times_most_used_move_was_used():
                    player.set_most_used_move(move)
                    player.set_number_of_times_most_used_move_was_used(number_of_scissors_used)
