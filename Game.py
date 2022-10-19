import os
from random import randint
from Board import Board
from Player import Player

class Game:

    def __init__(self, player1_ctrl, player2_ctrl):
        self.players = []
        self.board = Board(3)
        if randint(0, 1) == 0:
            self.players.append(Player(player1_ctrl, 1))
            self.players.append(Player(player2_ctrl, 2))
        else:
            self.players.append(Player(player2_ctrl, 2))
            self.players.append(Player(player1_ctrl, 1))

    def start(self):
        os.system('cls')
        print("\n1")
        self.board.draw()
        while (not self.board.win) and self.board.taken < 9:
            for player in self.players:
                player.play(self.board)
                self.board.draw()
                self.board.check_win()
                if self.board.taken == 9 or self.board.win:
                    break
        if self.board.win:
            print(f"Player {self.board.winner} won!")
        else:
            print("The game has ended in a draw.")