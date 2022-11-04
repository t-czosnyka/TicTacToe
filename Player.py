import random
from Board import Board
import os
import time


class Player:
    # parent class for both types of players
    def __init__(self, number: int):
        self.number = number
        self.player_type = " "

    def get_positions(self, board):
        pass

    def play(self, board: Board):
        # get positions for both type of players
        played = False
        while not played:
            print(f"Player {self.number} {self.player_type} turn: ")
            positions = self.get_positions(board)
            if board.write(positions, self.number):
                played = True
        if played:
            os.system('cls')
            print(f"Player {self.number} played [{positions[1] + 1},{positions[0] + 1}].")


class ComputerPlayer(Player):

    def __init__(self, number: int):
        super().__init__(number)
        self.player_type = "Computer"

    def get_positions(self, board):
        # function to choose where to play based on current situation on board
        choices = list()
        prio = 100  # action priority - smaller -> more important
        corners = [(0, 0), (0, board.size - 1), (board.size - 1, 0), (board.size - 1, board.size - 1)]
        if len(board.free_fields) >= 8:  # first move - center or corners
            prio = 50
            if all([item in board.free_fields for item in corners]):  # all corners free
                choices = corners + [(1, 1)]
            elif board.check_empty((1, 1)):  # opponent took corner play center
                choices = [(1, 1)]
            else:                           # opponent took corner play center
                choices = corners
        elif len(board.free_fields) < 8:
            possible_choices = list()  # Evaluate situation on board
            for i in range(1, 9):
                line = board.check_line(i)
                if len(line[2]) != 0:
                    possible_choices.append(board.check_line(i))
            for line_1 in possible_choices:
                if line_1[self.number - 1] == 2 and line_1[2 - self.number] == 0:  # Victory possible prio = 1
                    if prio > 10:
                        choices.clear()
                        prio = 10
                    if prio == 10:
                        choices = choices + line_1[2]
                elif line_1[self.number - 1] == 0 and line_1[2 - self.number] == 2 and prio >= 2:  # Block defeat prio=2
                    if prio > 20:
                        choices.clear()
                        prio = 20
                    if prio == 20:
                        choices = choices + line_1[2]
                elif line_1[self.number - 1] == 1 and line_1[2 - self.number] == 0 and line_1[3] <= 6 \
                        and len(board.free_fields) == 6 and not board.check_empty((1, 1)):  # special case
                    if prio > 25:
                        choices.clear()
                        prio = 25
                    if prio == 25:
                        choices = choices + line_1[2]

                elif line_1[self.number - 1] == 1 and line_1[2 - self.number] == 0:  # Play in a most promising line
                    if prio > 30:
                        line_corners = [value for value in line_1[2] if value in corners]  # find free corner to play
                        if len(line_corners) > 0:
                            prio = 30
                            choices.clear()
                        if prio == 30:
                            choices = choices + line_corners
                    if prio > 40:
                        prio = 40
                        choices.clear()
                    if prio == 40:
                        choices = choices + line_1[2]
                # print("Prio: ", prio, choices)
        # print(choices)
        if prio < 100:
            choices = [value for value in board.free_fields if value in choices]
            positions = random.choice(choices)
        elif prio == 100:
            positions = random.choice(board.free_fields)
        time.sleep(3)
        return positions


class HumanPlayer(Player):

    def __init__(self, number: int):
        super().__init__(number)
        self.player_type = "Human"

    def get_positions(self, board):
        # Get position input from human player
        played = False
        while not played:  # Repeat until correct value received
            pos = input("Input position, format: \"x,y\", range 1-3: ")
            if ',' in pos:
                positions = pos.split(',')
                if positions[0].isdecimal() and positions[1].isdecimal():
                    positions = [int(value) - 1 for value in positions]
                    if positions[0] in range(0, 3) and positions[1] in range(0, 3):
                        positions.reverse()
                        if board.check_empty(positions):
                            played = True
                            return positions[0], positions[1]
                        else:
                            print("Field already taken.")
                    else:
                        print("Position value out of range.")
                else:
                    print("Wrong format.")
            else:
                print("Wrong format.")


class MinMaxComputerPlayer(Player):

    def __init__(self, number: int):
        super().__init__(number)
        self.player_type = "MinMax Computer"

    def get_positions(self, board):
        # function to choose where to play based on current situation on board
        choices = list()
        corners = [(0, 0), (0, board.size - 1), (board.size - 1, 0), (board.size - 1, board.size - 1)]
        if len(board.free_fields) == 9:  # first move - center or corners
            choices = corners + [(1, 1)]
        elif len(board.free_fields) == 8:    # second move
            if not board.check_empty((1, 1)):   # if center taken play corner
                choices = corners
            elif not all([item in board.free_fields for item in corners]):  # if corner taken play center
                choices = [(1, 1)]
            else:                                                           # else play corner or center
                choices = corners + [(1, 1)]
        else:     # next moves use MinMax algorithm
            evaluation, choices = self.min_max(board, self.number)
        choices = [value for value in board.free_fields if value in choices] # take choices only if they are free field
        positions = random.choice(choices)
        time.sleep(3)
        return positions

    def min_max(self, board, player):
        free_fields = board.free_fields.copy()
        max_eval = -100
        min_eval = 100
        max_move = list()
        if player == self.number:
            for move in free_fields:
                board.write(move, self.number)
                board.check_win()
                if board.win or len(board.free_fields) == 0:
                    evaluation = self.eval(board)
                else:
                    evaluation, temp_move = self.min_max(board, 3 - self.number)
                #print(evaluation)
                if evaluation > max_eval:
                    max_eval = evaluation
                    max_move.clear()
                    max_move.append(move)
                elif evaluation == max_eval:
                    max_move.append(move)
                max_eval = max(evaluation, max_eval)
                board.write(move, 0)
                board.check_win()
            return max_eval, max_move
        else:
            for move in free_fields:
                board.write(move, 3 - self.number)
                board.check_win()
                if board.win or len(board.free_fields) == 0:
                    evaluation = self.eval(board)
                else:
                    evaluation, temp_move = self.min_max(board, self.number)
                # print(evaluation)
                if evaluation <= min_eval:
                    min_eval = evaluation
                    min_move = move
                #min_eval = min(evaluation, min_eval)
                board.write(move, 0)
                board.check_win()
            return min_eval, min_move

    def eval(self, board):
        if board.win and board.winner == self.number:
            return len(board.free_fields)+1
        elif board.win and board.winner != self.number:
            return (len(board.free_fields)+1)*-1
        else:
            return 0
