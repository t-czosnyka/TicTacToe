import os
import logging
import random

from Board import Board
from Player import HumanPlayer, ComputerPlayer, MinMaxComputerPlayer

# logging results
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

    def start(self, game_type_in=" "):
        # main game function
        type_ok = False
        if game_type_in == " ":
            while not type_ok:
                os.system('cls')
                print("Choose game type:\n \
                1 - Player vs Player\n \
                2 - Player vs Computer\n \
                3 - Computer vs Computer\n \
                4 - Player vs MinMaxComputer\n")
                game_type = input()
                os.system('cls')
                if game_type in ["1", "2", "3", "4"]:
                    type_ok = True
                else:
                    print("Wrong game type.")
        else:
            if game_type_in in ["1", "2", "3", "4"]:
                type_ok = True
                game_type = game_type_in
            else:
                raise Exception("Wrong function argument.")
        if type_ok:
            if game_type == "1":
                self.players.append(HumanPlayer(1))
                self.players.append(HumanPlayer(2))

            elif game_type == "2":
                plr_num = random.sample([1, 2], 2)      # randomize player numbers
                self.players.append(ComputerPlayer(plr_num[0]))
                self.players.append(HumanPlayer(plr_num[1]))

            elif game_type == "3":
                self.players.append(MinMaxComputerPlayer(1))
                self.players.append(ComputerPlayer(2))

            elif game_type == "4":
                plr_num = random.sample([1, 2], 2)      # randomize player numbers
                self.players.append(MinMaxComputerPlayer(plr_num[0]))
                self.players.append(HumanPlayer(plr_num[1]))
            random.shuffle(self.players)         # randomize which player starts
            os.system('cls')
            print("\n")
            self.board.draw()
            while (not self.board.win) and len(self.board.free_fields) > 0: # play until somebody wins or board is full
                for player in self.players:     # play each player
                    player.play(self.board)
                    self.board.draw()           # draw the board
                    self.board.check_win()      # check if somebody won
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
