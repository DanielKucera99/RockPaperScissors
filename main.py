import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from network import NetworkGame
import tkinter as tk
from tkinter import messagebox
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



def visualize_results(player_wins, playersList):


    # Construct players and wins lists for all players
    players = list(player_wins.keys())
    wins = list(player_wins.values())

    # Print player wins
    for player, win in zip(players, wins):
        print(f"Player {player}: {win} wins")

    # Plot the bar graph
    plt.bar(players, wins)
    plt.xlabel('Players')
    plt.ylabel('Number of Wins')
    plt.title('Number of Wins for Each Player')

    # Set the x-axis ticks to cover all players
    plt.xticks(players)

    # Display the plot
    strategy_thread = threading.Thread(target=show_player_strategies, args=(playersList,))

    strategy_thread.start()
    plt.show()


def main():
    num_players = 10
    game = NetworkGame(num_players)
    player_wins = game.run_simulation()
    players = game.players
    visualize_results (player_wins,players)


if __name__ == "__main__":
    main()
