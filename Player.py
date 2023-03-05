import random
from Board import Board
import os
import time


class Player:
    # Base class for other types of players
    def __init__(self, mark: int, display_game=True):
        self.mark = mark
        self.player_type = " "
        # display game - game to be displayed in console, else only record a result
        self.display_game = display_game

    def get_positions(self, board) -> tuple[int, int]:
        pass

    def play(self, board: Board):
        # general function to make a move by every type of player
        positions = list()
        played = False
        # repeat loop until correct positions are inserted
        while not played:
            if self.display_game:
                print(f"Player {self.mark} {self.player_type} turn: ")
            # get positions
            positions = self.get_positions(board)
            # write field
            if board.mark_field((positions[0], positions[1]), self.mark):
                # exit loop if player successfully marked a field
                played = True
        if self.display_game:
            # write information after player makes a move
            os.system('cls')
            print(f"Player {self.mark} played [{positions[1] + 1},{positions[0] + 1}].")
        return positions


class ComputerPlayer(Player):
    # Regular computer player, playing with simple algorithm

    def __init__(self, mark: int, display_game=True):
        super().__init__(mark, display_game)
        self.player_type = "Computer"
        self.current_priority = 100     # priority of available positions
        self.current_choices = []    # available positions to play


    def get_positions(self, board: Board):
        # function to choose where to play based on current situation on board
        # initialize choices
        self.current_priority = 100  # position priority - smaller -> more important
        self.current_choices = []    # choices for current priority
        # Starting first:
        if len(board.free_fields) == 9:
            # start in the corner
            self.current_priority = 50
            self.current_choices = board.corners
        # Starting second:
        if len(board.free_fields) == 8:
            self.current_priority = 50
            # opponent started in the center - play in the corner
            if not board.check_empty((1, 1)):
                self.current_choices = board.corners
            # in other cases take center
            else:
                self.current_choices = [(1, 1)]
        # Next moves - evaluate situation in each of 8 lines that can lead to victory
        # Each situation has priority - lower = most important,
        # If situation occurs compare its priority with current priority:
        # - If it has lower priority(more important) - overwrite available choices and current priority
        # - If it has the same priority add free fields in this line to current choices
        # - If it has higher priority - do nothing
        elif len(board.free_fields) < 8:
            # Evaluate situation on board
            not_full_lines, not_full_lines_ids = board.check_available_lines()
            # evaluate not full lines
            for line in not_full_lines:
                line_free_fields = line[2]
                # Situation 1: Victory possible in next move - the highest priority 10
                if line[self.mark - 1] == 2 and line[2 - self.mark] == 0:
                    self.compare_priority(10, line_free_fields)
                # Situation 2: Defeat possible in next move - priority 20
                elif line[self.mark - 1] == 0 and line[2 - self.mark] == 2:
                    self.compare_priority(20, line_free_fields)
                # Situation 3: Play in the most promising line - with 1 own mark and no opponent marks
                elif line[self.mark - 1] == 1 and line[2 - self.mark] == 0:
                    self.compare_priority(30, line_free_fields)
            # Special case don't play corners in this situation(own = "O")
            # X |   |
            # ----------
            #   | O |
            # ----------
            #   |   | X
            # check if 6 fields are free and one diagonal is full
            if len(board.free_fields) == 6 and (7 not in not_full_lines_ids or 8 not in not_full_lines_ids):
                # remove corners from choices
                self.current_choices = [choice for choice in self.current_choices if choice not in board.corners]
            if self.current_priority == 30:
                # further evaluate current choices
                self.current_choices = self.evaluate_field(self.current_choices, board, not_full_lines)
        # Priority found - select random field from available choices
        if self.current_priority < 100:
            positions = random.choice(self.current_choices)
        # No priority found - play random free field
        else:
            positions = random.choice(board.free_fields)
        # wait 3s if game is displayed
        if self.display_game:
            time.sleep(3)
        return positions

    def compare_priority(self, situation_priority: int, situation_choices: list):
        # Compare situation priority with current priority:
        # Better situation found overwrite priority and choices
        if self.current_priority > situation_priority:
            self.current_priority = situation_priority
            self.current_choices = situation_choices
        # Equal priority found and situation choices to current choices
        elif self.current_priority == situation_priority:
            self.current_choices = self.current_choices + situation_choices

    def evaluate_field(self, fields, board, line_data):
        # select fields that additionally block opponent lines
        # score is number of opponent lines blocked in this field
        # return fields with max score
        max_score = 0
        best_fields = []
        for field in fields:
            score = 0
            for line_id in board.get_line_ids_from_field(field):
                line = board.check_line(line_id)
                if line[self.mark - 1] == 0 and line[2 - self.mark] == 1:
                    score += 1
            if score > max_score:
                best_fields = [field]
                max_score = score
            elif score == max_score:
                best_fields.append(field)
        return best_fields


class HumanPlayer(Player):
    # Human player - moves inserted from command line
    def __init__(self, mark: int, display_game=True):
        super().__init__(mark, display_game)
        self.player_type = "Human"
        # Human player always displays game
        self.display_game = True

    def get_positions(self, board):
        # Get position input from human player, correct input: x_pos,y_pos
        # Repeat until correct value received
        while True:
            user_input = input("Input position, format: \"x,y\", range 1-3: ")
            if ',' not in user_input:
                print("Wrong format.")
                continue
            positions = user_input.split(',', 1)
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
    # Computer player using MinMax algorithm to play
    def __init__(self, mark: int, display_game=True):
        super().__init__(mark, display_game)
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
        # wait 3s if game is displayed
        if self.display_game:
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
                board.mark_field(move, self.mark)                # make a test move
                board.check_win(move)
                if board.win or len(board.free_fields) == 0:  # evaluate result if game is finished
                    evaluation = self.evaluate_board(board)
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
                board.reset_winner()
                if evaluation > best_min:                   # if evaluation is better than other option for calling
                    break                                   # minimizing player - break the loop - beta
            return max_eval, max_move
        else:  # minimizing player
            for move in free_fields:
                board.mark_field(move, 3 - self.mark)        # make a test move
                board.check_win(move)
                if board.win or len(board.free_fields) == 0:  # evaluate result if game is finished
                    evaluation = self.evaluate_board(board)
                    self.evaluations += 1
                else:                                       # if game is not finish recursive call for max player
                    evaluation, temp_move = self.min_max(board, self.mark, best_max, best_min)
                min_eval = min(evaluation, min_eval)      # find the lowest evaluation
                min_move = move                           # save min move - doesn't matter
                best_min = min(best_min, evaluation)      # save current best evaluation for minimizer as best_min
                board.clear_field(move)                      # undo the test move
                board.reset_winner()
                if evaluation < best_max:
                    break
            return min_eval, min_move

    def evaluate_board(self, board):
        # evaluation of state on board, return score
        # no winner: score = 0
        # self is winner: +1 point + 1 for each free field
        # opponent is winner: -1 point -1 for each free field
        if board.win and board.winner == self.mark:
            return len(board.free_fields)+1
        elif board.win and board.winner != self.mark:
            return (len(board.free_fields)+1)*-1
        else:
            return 0
