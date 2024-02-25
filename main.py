import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from network import NetworkGame
import tkinter as tk
import threading


def show_player_strategies(players):
    root = tk.Tk()
    root.title("Player Strategies")
    root.geometry("300x200")

    label = tk.Label(root, text="Player Strategies")
    label.pack()

    for player in players:
        label = tk.Label(root, text=f"{player.name}: {player.strategy.name}")
        label.pack()

    root.mainloop()


def visualize_move_wins(rock_wins, paper_wins, scissors_wins):
    moves = ['Rock', 'Paper', 'Scissors']
    wins = [rock_wins, paper_wins, scissors_wins]

    root = tk.Tk()
    root.title("Winning moves")
    root.geometry("300x200")

    label = tk.Label(root, text="Winning moves")
    label.pack()

    for i in range(3):
        label = tk.Label(root, text=f"{moves[i]}: {wins[i]}")
        label.pack()

    root.mainloop()


def visualize_results(player_wins, players_list, rock_wins, paper_wins, scissors_wins):
    players = list(player_wins.keys())
    wins = list(player_wins.values())

    for player, win in zip(players, wins):
        print(f"Player {player}: {win} wins")

    plt.bar(players, wins)
    plt.xlabel('Players')
    plt.ylabel('Number of Wins')
    plt.title('Number of Wins for Each Player')

    plt.xticks(players)

    results_thread = threading.Thread(target=visualize_move_wins, args=(rock_wins, paper_wins, scissors_wins,))
    results_thread.start()

    strategy_thread = threading.Thread(target=show_player_strategies, args=(players_list,))
    strategy_thread.start()

    plt.show()


def main():
    num_players = 9
    game = NetworkGame(num_players)
    player_wins, rock_wins, paper_wins, scissors_wins = game.run_simulation()
    players = game.players
    visualize_results(player_wins, players, rock_wins, paper_wins, scissors_wins)


if __name__ == "__main__":
    main()
