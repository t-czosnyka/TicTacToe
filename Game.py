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
        self.board = Board()
        # Constants "X" player is 1, "O" player is 2
        self.X_PLAYER = 1
        self.O_PLAYER = 2

    def start(self, display_game=True, game_type_in=" "):
        # main game function, default - choose game type from cli, if game type is not empty - choice will be skipped
        # display game -if true game is displayed in cli with wait times
        type_ok = False
        # ask user to insert game type from command line
        if game_type_in == " ":
            # repeat until correct type is inserted
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
        # game type inserted as argument
        else:
            # check if correct argument is inserted - if not raise exception
            if game_type_in in ["1", "2", "3", "4"]:
                type_ok = True
                game_type = game_type_in
            else:
                raise Exception("Wrong function argument.")
        # correct game type - start game
        if type_ok:
            # randomize player marks "X" and "O"
            player_marks = random.sample([self.X_PLAYER, self.O_PLAYER], 2)
            # Game type 1: Human vs Human
            if game_type == "1":
                # game is always displayed
                display_game = True
                # Create players with random marks
                self.players.append(HumanPlayer(player_marks[0]))
                self.players.append(HumanPlayer(player_marks[1]))
            # Game type 2: Human vs Regular Computer
            elif game_type == "2":
                # game is always displayed
                display_game = True
                # Create players with random marks
                self.players.append(ComputerPlayer(player_marks[0]))
                self.players.append(HumanPlayer(player_marks[1]))
            # Game type 3: MinMax Computer vs Regular Computer
            elif game_type == "3":
                # Create players with random marks
                self.players.append(MinMaxComputerPlayer(player_marks[0], display_game))
                self.players.append(ComputerPlayer(player_marks[1], display_game))
            # Game type 4: Human vs MinMax Computer
            elif game_type == "4":
                # game is always displayed
                display_game = True
                # Create players with random marks
                self.players.append(MinMaxComputerPlayer(player_marks[0]))
                self.players.append(HumanPlayer(player_marks[1]))
            # randomize which player starts
            random.shuffle(self.players)
            os.system('cls')
            if display_game:
                print("\n")
                # draw empty board
                print(self.board)
            # play until somebody wins or board is full
            while (not self.board.win) and len(self.board.free_fields) > 0:
                for player in self.players:     # play each player
                    played_positions = player.play(self.board)
                    # draw the board
                    if display_game:
                        print(self.board)
                    # check for possible winner
                    self.board.check_win(played_positions)
                    # end inner loop if there are no more fields or victory was achieved - no turn for the second player
                    if len(self.board.free_fields) == 0 or self.board.win:
                        break
            if self.board.win and display_game:
                print(f"Player {self.board.winner} won!")
            elif display_game:
                print("The game has ended in a draw.")
            result_logger.info(f"Games result is: {self.board.winner}\n"
                               f" Players:{self.players[0].mark}:{self.players[0].player_type}"
                               f" {self.players[1].mark}:{self.players[1].player_type}\n"
                               + str(self.board))
            return self.board.winner

