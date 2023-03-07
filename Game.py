import os
import logging
import random
from Board import Board
from Player import HumanPlayer, ComputerPlayer, MiniMaxComputerPlayer

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
        # Constants Game types
        self.GAME_TYPE_H_VS_H = "1"  # Human vs Human
        self.GAME_TYPE_H_VS_C = "2"  # Human vs Computer
        self.GAME_TYPE_C_VS_MM = "3"  # Computer vs MiniMax Computer
        self.GAME_TYPE_H_VS_MM = "4"  # Human vs MiniMax Computer
        self.GAME_TYPES = [self.GAME_TYPE_H_VS_H, self.GAME_TYPE_H_VS_C, self.GAME_TYPE_C_VS_MM, self.GAME_TYPE_H_VS_MM]

    def start(self, display_game=True, game_type_in=" ") -> int:
        # main game function, default - choose game type from cli, if game type is not empty - choice will be skipped
        # returns number of player who has won the game or 0 if it ended in a draw
        # display game -if true game is displayed in cli with wait times
        # get game type
        type_ok, game_type = self.get_game_type(game_type_in)
        if not type_ok:
            raise Exception("Wrong game type passed as argument")
        # all games involving human player are displayed
        if game_type != self.GAME_TYPE_C_VS_MM:
            display_game = True
        # correct game type - create players
        self.get_players(game_type, display_game)
        os.system('cls')
        if display_game:
            print("\n")
            # draw empty board
            print(self.board)
        # play until somebody wins or board is full
        self.play(display_game)
        # Game is finished
        # Someone Won
        if self.board.win and display_game:
            print(f"Player {self.board.winner} won!")
        # Draw
        elif display_game:
            print("The game has ended in a draw.")
        # Log result with drawing of the board
        result_logger.info(f"Games result is: {self.board.winner}\n"
                           f" Players:{self.players[0].mark}:{self.players[0].player_type}"
                           f" {self.players[1].mark}:{self.players[1].player_type}\n"
                           + str(self.board))
        # return winner
        return self.board.winner

    def get_game_type(self, game_type_in) -> (bool, str):
        # get game type as function argument or inserted by user
        # return True if game type is ok + game type as str
        type_ok = False
        game_type = ""
        # game type inserted as argument
        if game_type_in != " ":
            if game_type_in in self.GAME_TYPES:
                game_type = game_type_in
                type_ok = True
            return type_ok, game_type
        # no game type as argument - ask user to insert game type from command line
        # repeat until correct type is inserted
        while not type_ok:
            os.system('cls')
            print("Choose game type:\n \
                   1 - Player vs Player\n \
                   2 - Player vs Computer\n \
                   3 - Computer vs MinMaxComputer\n \
                   4 - Player vs MinMaxComputer\n")
            game_type = input()
            os.system('cls')
            if game_type in self.GAME_TYPES:
                type_ok = True
            else:
                print("Wrong game type.")
        return type_ok, game_type

    def get_players(self, game_type, display_game):
        # Create list of player objects based on game type
        # randomize player marks "X" and "O"
        player_marks = random.sample([self.X_PLAYER, self.O_PLAYER], 2)
        # Game type 1: Human vs Human
        if game_type == self.GAME_TYPE_H_VS_H:
            # game is always displayed
            # Create players with random marks
            self.players.append(HumanPlayer(player_marks[0]))
            self.players.append(HumanPlayer(player_marks[1]))
        # Game type 2: Human vs Regular Computer
        elif game_type == self.GAME_TYPE_H_VS_C:
            # game is always displayed
            # Create players with random marks
            self.players.append(ComputerPlayer(player_marks[0]))
            self.players.append(HumanPlayer(player_marks[1]))
        # Game type 3: Regular Computer vs MinMax Computer
        elif game_type == self.GAME_TYPE_C_VS_MM:
            # Create players with random marks
            self.players.append(MiniMaxComputerPlayer(player_marks[0], display_game))
            self.players.append(ComputerPlayer(player_marks[1], display_game))
        # Game type 4: Human vs MinMax Computer
        elif game_type == self.GAME_TYPE_H_VS_MM:
            # game is always displayed
            # Create players with random marks
            self.players.append(MiniMaxComputerPlayer(player_marks[0]))
            self.players.append(HumanPlayer(player_marks[1]))
        # randomize which player starts
        random.shuffle(self.players)

    def play(self, display_game):
        # call play functions of each player in a loop until game is finished
        while True:
            # play each of two players
            for player in self.players:
                played_positions = player.play(self.board)
                # draw the board
                if display_game:
                    print(self.board)
                # check for possible winner
                self.board.check_win(played_positions)
                # end inner loop if there are no more fields or victory was achieved - no turn for the second player
                if len(self.board.free_fields) == 0 or self.board.win:
                    return
