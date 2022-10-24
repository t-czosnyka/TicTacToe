import random

from Board import Board
from random import randint
import os
import time


class Player:

    def __init__(self, control: str, number: int):
        if control == "h" or control == "c":
            self.control = control.lower()
        else:
            print("Wrong player type.")
        self.number = number

    def get_positions(self, board):
        choices = list()
        prio = 100              # action priority - smaller -> more important
        if len(board.free_fields) >= 7:
            prio = 10
            if board.check_empty(1, 1):
                choices = [(1, 1)]
            else:
                choices = [(0, 0), (0, board.size-1), (board.size-1, 0), (board.size-1, board.size-1)]
        elif len(board.free_fields) < 7:
            possible_choices = list()            # Evaluate situation on board
            for i in range(1, 9):
                line = board.check_line(i)
                if len(line[2]) != 0:
                    possible_choices.append(board.check_line(i))
           # print("list of lines created")
            for line_1 in possible_choices:
                #print(line_1[0], line_1[1], line_1[2], self.number)
                if line_1[self.number-1] == 2 and line_1[2 - self.number] == 0:         # Vicotry possible prio = 1
                    if prio > 1:
                        choices.clear()
                    prio = 1
                    choices = choices + line_1[2]
                    #print("Prio 1 found")
                elif line_1[self.number-1] == 0 and line_1[2 - self.number] == 2 and prio >= 2:  # Block defeat prio = 2
                    if prio > 2:
                        choices.clear()
                    prio = 2
                    choices = choices + line_1[2]
                    #print("Prio 2 found")
            print("choices", choices)
        if prio < 100:
            print("Not random played.")
            choices = [value for value in board.free_fields if value in choices]
            print("choices/free fields", choices)
            positions = random.choice(choices)
        elif prio == 100:
            print("Random played.")
            positions = random.choice(board.free_fields)
        return positions


    def play(self, board: Board):
        player_types = {"h": "Human", "c": "Computer"}
        played = False
        while not played:
            positions = [0, 0]
            print(f"Player {self.number}({player_types[self.control]}) turn: ")
            if self.control == "h":
                pos = input("Input position, format \"x,y\", range 1-3: ")
                if ',' in pos:
                    positions = pos.split(',')
                    if positions[0].isdecimal() and positions[1].isdecimal():
                        if int(positions[0]) in range(1, 4) and int(positions[1]) in range(1, 4):
                            if board.write(int(positions[1])-1, int(positions[0])-1, self.number):
                                played = True
                        else:
                            print("Position value out of range.")
                    else:
                        print("Wrong format.")
                else:
                    print("Wrong format.")
            elif self.control == "c":
                while not played:
                    posc = self.get_positions(board)
                    time.sleep(3)
                    if board.write(posc[0], posc[1], self.number):
                        played = True
                        positions = [posc[1]+1, posc[0]+1]

        if played:
            # os.system('cls')
            print(f"Player {self.number} played {positions}.")