import random
from Board import Board
import os
import time


class Player:
    # parent class for both types of players
    def __init__(self, mark: int):
        self.mark = mark
        self.player_type = " "

    def get_positions(self, board) -> tuple[int, int]:
        pass

    def play(self, board: Board):
        # general function to make a move by every type of player
        positions = list()
        played = False
        # repeat loop until correct positions are inserted
        while not played:
            print(f"Player {self.mark} {self.player_type} turn: ")
            # get positions
            positions = self.get_positions(board)
            # write field
            if board.write_field((positions[0], positions[1]), self.mark):
                # exit loop if player successfully marked a field
                played = True
        # write information after player makes a move
        os.system('cls')
        print(f"Player {self.mark} played [{positions[1] + 1},{positions[0] + 1}].")


class ComputerPlayer(Player):

    def __init__(self, mark: int):
        super().__init__(mark)
        self.player_type = "Computer"

    def get_positions(self, board):
        # function to choose where to play based on current situation on board
        choices = list()
        positions = list()
        prio = 100  # action priority - smaller -> more important
        corners = [(0, 0), (0, board.size - 1), (board.size - 1, 0), (board.size - 1, board.size - 1)]
        # first move - center or corners
        if len(board.free_fields) >= 8:
            prio = 50
            # all corners free
            if all([item in board.free_fields for item in corners]):
                choices = corners + [(1, 1)]
            # opponent took corner play center
            elif board.check_empty((1, 1)):
                choices = [(1, 1)]
            # play corners
            else:
                choices = corners
        # Next moves
        elif len(board.free_fields) < 8:
            # Evaluate situation on board
            not_full_lines = list()
            # get information from every line on board
            for i in range(1, 9):
                line = board.check_line(i)
                # save line if it is not full
                if len(line[2]) != 0:
                    not_full_lines.append(line)
            # evaluate not full lines
            for line_1 in not_full_lines:
                if line_1[self.mark - 1] == 2 and line_1[2 - self.mark] == 0:  # Victory possible prio = 1
                    if prio > 10:
                        choices.clear()
                        prio = 10
                    if prio == 10:
                        choices = choices + line_1[2]
                elif line_1[self.mark - 1] == 0 and line_1[2 - self.mark] == 2 and prio >= 2:  # Block defeat prio=2
                    if prio > 20:
                        choices.clear()
                        prio = 20
                    if prio == 20:
                        choices = choices + line_1[2]
                elif line_1[self.mark - 1] == 1 and line_1[2 - self.mark] == 0 and line_1[3] <= 6 \
                        and len(board.free_fields) == 6 and not board.check_empty((1, 1)):  # special case
                    if prio > 25:
                        choices.clear()
                        prio = 25
                    if prio == 25:
                        choices = choices + line_1[2]

                elif line_1[self.mark - 1] == 1 and line_1[2 - self.mark] == 0:  # Play in a most promising line
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

    def __init__(self, mark: int):
        super().__init__(mark)
        self.player_type = "Human"

    def get_positions(self, board):
        # Get position input from human player
        while True:  # Repeat until correct value received
            user_input = input("Input position, format: \"x,y\", range 1-3: ")
            if ',' not in user_input:
                print("Wrong format.")
                continue
            positions = user_input.split(',')
            if not positions[0].isdecimal() or not positions[1].isdecimal():
                print("Wrong format.")
                continue
            positions = [int(value) - 1 for value in positions]
            if positions[0] not in range(0, 3) or positions[1] not in range(0, 3):
                print("Position value out of range.")
                continue
            positions.reverse()
            if not board.check_empty(positions):
                print("Field already taken.")
                continue
            return positions[0], positions[1]

class MinMaxComputerPlayer(Player):

    def __init__(self, mark: int):
        super().__init__(mark)
        self.player_type = "MinMax Computer"
        self.evaluations = 0

    def get_positions(self, board):
        # function to choose where to play based on current situation on board
        self.evaluations = 0
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
            evaluation, choices = self.min_max(board, self.mark, -100, 100)
        choices = [value for value in board.free_fields if value in choices]  # take choices only if they are free field
        positions = random.choice(choices)
        time.sleep(3)
        return positions

    def min_max(self, board, player, best_max, best_min):
        # minmax algorithm with alpha beta returning evaluation and best move
        free_fields = board.free_fields.copy()
        max_eval = -100
        min_eval = 100
        max_move = min_move = list()
        if player == self.mark:  # maximizing player
            for move in free_fields:
                board.write_field(move, self.mark)                # make a test move
                board.check_win()
                if board.win or len(board.free_fields) == 0:  # evaluate result if game is finished
                    evaluation = self.eval(board)
                    self.evaluations += 1
                else:                                          # if game is not finish recursive call for min player
                    evaluation, temp_move = self.min_max(board, 3 - self.mark, best_max, best_min)
                if evaluation > max_eval:                     # if evaluation is better than current max save as max
                    max_eval = evaluation                     # clear current best move, add move to best moves
                    max_move.clear()
                    max_move.append(move)
                elif evaluation == max_eval:
                    max_move.append(move)                    # if evaluation is the same as best add move to best moves
                best_max = max(best_max, evaluation)         # save current best evaluation as best_max
                board.clear_field(move)                         # undo the test move
                board.check_win()
                if evaluation > best_min:                   # if evaluation is better than other option for calling
                    break                                   # minimizing player - break the loop - beta
            return max_eval, max_move
        else:  # minimizing player
            for move in free_fields:
                board.write_field(move, 3 - self.mark)        # make a test move
                board.check_win()
                if board.win or len(board.free_fields) == 0:  # evaluate result if game is finished
                    evaluation = self.eval(board)
                    self.evaluations += 1
                else:                                       # if game is not finish recursive call for max player
                    evaluation, temp_move = self.min_max(board, self.mark, best_max, best_min)
                min_eval = min(evaluation, min_eval)      # find the lowest evaluation
                min_move = move                           # save min move - doesn't matter
                best_min = min(best_min, evaluation)      # save current best evaluation for minimizer as best_min
                board.clear_field(move)                      # undo the test move
                board.check_win()
                if evaluation < best_max:
                    break
            return min_eval, min_move

    def eval(self, board):
        # evaluation of state on board if calling player is winner - positive if opponent - negative
        # no winner = 0, each free field + 1 point
        if board.win and board.winner == self.mark:
            return len(board.free_fields)+1
        elif board.win and board.winner != self.mark:
            return (len(board.free_fields)+1)*-1
        else:
            return 0
