import os
import logging
from random import randint
from Board import Board
from Player import Player


result_logger = logging.getLogger(__name__)
file_handler = logging.FileHandler('result.log')
result_logger.setLevel(logging.INFO)
file_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(file_format)
result_logger.addHandler(file_handler)


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
        print("\n")
        self.board.draw()
        while (not self.board.win) and len(self.board.free_fields) > 0:
            for player in self.players:
                player.play(self.board)
                self.board.draw()
                self.board.check_win()
                if len(self.board.free_fields) == 0 or self.board.win:
                    break
        if self.board.win:
            print(f"Player {self.board.winner} won!")
            result_logger.info(f"Games result is : {self.board.winner}")
            return self.board.winner
        else:
            print("The game has ended in a draw.")
            result_logger.info("Games result is : 3")
            return 3
