import os
import logging
import random

from Board import Board
from Player import HumanPlayer
from Player import ComputerPlayer


result_logger = logging.getLogger(__name__)
file_handler = logging.FileHandler('result.log')
result_logger.setLevel(logging.INFO)
file_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(file_format)
result_logger.addHandler(file_handler)


class Game:

    def __init__(self):
        self.players = []
        self.board = Board(3)

    def start(self):
        type_ok = False
        while not type_ok:
            os.system('cls')
            print("Choose game type:\n \
            1 - Player vs Player\n \
            2 - Player vs Computer\n \
            3 - Computer vs Computer\n")
            game_type = input()
            os.system('cls')
            if game_type == "1":
                self.players.append(HumanPlayer(1))
                self.players.append(HumanPlayer(2))
                type_ok = True

            elif game_type == "2":
                plr_num = random.sample([1, 2], 2)
                self.players.append(ComputerPlayer(plr_num[0]))
                self.players.append(HumanPlayer(plr_num[1]))
                type_ok = True

            elif game_type == "3":
                self.players.append(ComputerPlayer(1))
                self.players.append(ComputerPlayer(2))
                type_ok = True
            else:
                print("Wrong game type.")
        random.shuffle(self.players)
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
            result_logger.info(f"Games result is: {self.board.winner}\n"
                               f" Players:{self.players[0].number}:{self.players[0].player_type}"
                               f" {self.players[1].number}:{self.players[1].player_type}")
            return self.board.winner
        else:
            print("The game has ended in a draw.")
            result_logger.info(f"Games result is : 3\n"
                               f" Players:{self.players[0].number}:{self.players[0].player_type}"
                               f" {self.players[1].number}:{self.players[1].player_type}")
            return 3
