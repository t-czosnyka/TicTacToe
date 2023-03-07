import random
from Board import Board
import os
import time
import copy


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
                self.current_choices = self.evaluate_field(self.current_choices, board)
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

    def evaluate_field(self, fields, board):
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


class MiniMaxComputerPlayer(Player):
    # Computer player using MiniMax algorithm to play
    def __init__(self, mark: int, display_game=True):
        super().__init__(mark, display_game)
        self.player_type = "MiniMax Computer"

    def get_positions(self, board):
        # function to choose where to play based on current situation on board
        # first move - random choice
        if len(board.free_fields) == 9:
            choices = board.free_fields
        # next moves - use MiniMax algorithm
        else:
            evaluation, choices = self.mini_max(board, self.mark, -100, 100, 1)
        positions = random.choice(choices)
        # wait 3s if game is displayed
        if self.display_game:
            time.sleep(3)
        return positions

    def mini_max(self, board, player_mark, alpha, beta, depth):
        # Minimax algorithm function to be called recursively. Returns list of best moves and its evaluation.
        # Minimax algorithm tests every available move in current situation on board by simulating how game would go
        # following that move assuming opposing player chooses the best possible options for him.
        # Calling player is maximizing player, simulated opponent is minimizing player.
        # Maximizing player chooses the highest possible evaluation, while minimizing player chooses lowest.
        ###################################################################################################
        # alpha - evaluation of best already available option for Max player.
        # beta - evaluation of best already available option for Min player.
        # Used for pruning if calling player already has better option than the best possible option on current path -
        # don't evaluate other options on that path.
        ###################################################################################################
        # board - Board class indicates current situation on board
        # player_mark - indicates which player is making a move maximizing/minimizing
        # make a copy of current free fields
        free_fields = copy.copy(board.free_fields)
        # initialize variables
        max_eval = -100
        min_eval = 100
        max_move = list()
        min_move = list()
        # Maximizing player - looking to maximize the evaluation score
        if player_mark == self.mark:
            # Test every possible move
            for move in free_fields:
                # Make a test move
                board.mark_field(move, self.mark)
                board.check_win(move)
                # If the game is finished evaluate result
                if board.win or len(board.free_fields) == 0:
                    evaluation = self.evaluate_board(board)
                # If the game is not finished recursive call for the min player
                else:
                    evaluation, temp_move = self.mini_max(board, 3 - self.mark, alpha, beta, depth+1)
                # Get here after evaluation is available
                # if evaluation is higher than current max - update max and save current move as max move
                if evaluation > max_eval:
                    max_eval = evaluation
                    max_move = [move]
                # if evaluation is equal to current max - add current move to max moves
                elif evaluation == max_eval:
                    max_move.append(move)
                # update alpha
                alpha = max(alpha, evaluation)
                # Backtrack - remove the current move and get to the next one
                board.clear_field(move)
                board.reset_winner()
                # Pruning - current evaluation is already worse(for calling player) than already available option
                # - don't check other options.
                if evaluation > beta:
                    break
            return max_eval, max_move
        # Minimizing player - looking to minimize the evaluation score
        else:
            # Test every possible move
            for move in free_fields:
                # Make a test move
                board.mark_field(move, 3 - self.mark)
                board.check_win(move)
                # If the game is finished evaluate result
                if board.win or len(board.free_fields) == 0:
                    evaluation = self.evaluate_board(board)
                # If the game is not finished recursive call for the maximizing player
                else:
                    evaluation, temp_move = self.mini_max(board, self.mark, alpha, beta, depth+1)
                # Get here after evaluation is available
                # Find the current lowest evaluation
                min_eval = min(evaluation, min_eval)
                min_move = move
                # update beta
                beta = min(beta, evaluation)
                # Backtrack - remove the current move and get to the next one
                board.clear_field(move)
                board.reset_winner()
                # Pruning - current evaluation is already worse(for calling player) than already available option
                # - don't check other options.
                if evaluation < alpha:
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
