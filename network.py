from game import RockPaperScissors
from strategies import (AlwaysRockStrategy, AlwaysScissorsStrategy, AlwaysPaperStrategy, RandomStrategy,
                        RockScissorsPaperStrategy, WinRepeatLoseChangeStrategy, WinRepeatLoseCopyStrategy)
import networkx as nx

import random


class Player:
    def __init__(self, name, strategy):
        self.name = name
        self.strategy = strategy

    def get_player_strategy(self):
        return self.strategy



class NetworkGame:
    def __init__(self, num_players):
        self.num_players = num_players
        self.network = self.create_complete_graph(num_players)
        self.players = self.assign_players()

    def create_complete_graph(self, num_players):
        return nx.complete_graph(num_players)

    def assign_players(self):
        players = []

        # Define strategy objects for the first three players along with their names
        strategies = [
            AlwaysRockStrategy(),
            AlwaysScissorsStrategy(),
            AlwaysPaperStrategy(),
            RockScissorsPaperStrategy(),
            WinRepeatLoseChangeStrategy(),
            WinRepeatLoseCopyStrategy()
        ]

        # Assign random strategy names to remaining players
        strategies.extend(RandomStrategy() for _ in range(6, self.num_players))

        # Assign strategies to players
        for i, strategy in enumerate(strategies, start=1):
            player_name = f'Player {i}'
            players.append(Player(player_name, strategy))

        return players

    def play_round(self, player1, player2):
        move1 = player1.strategy.move()
        move2 = player2.strategy.move()

        # Determine the result of the round
        if move2 == RockPaperScissors().winning_moves[move1]:
            result = f"{player1.name} wins"
        elif move1 == RockPaperScissors().winning_moves[move2]:
            result = f"{player2.name} wins"
        else:
            result = "Draw"

        # Update last outcome if the strategy supports it
        if hasattr(player1.strategy, 'update_last_outcome'):
            player1.strategy.update_last_outcome(result, move1, move2)
        if hasattr(player2.strategy, 'update_last_outcome'):
            player2.strategy.update_last_outcome(result, move2, move1)

        return result
    def run_simulation(self):
        results = []
        player_wins = {player.name: 0 for player in self.players}  # Initialize wins for each player

        for i, player1 in enumerate(self.players):
            for j, player2 in enumerate(self.players):
                if i < j:
                    result = self.play_round(player1, player2)
                    results.append((player1.name, player2.name, result))

                    if "wins" in result:
                        if player1.name in result:
                            player_wins[player1.name] += 1
                        else:
                            player_wins[player2.name] += 1

        return player_wins
