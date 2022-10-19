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
                    positions[0] = randint(0, 2)
                    positions[1] = randint(0, 2)
                    if board.read(positions[0], positions[1]) == " ":
                        time.sleep(1)
                        board.write(positions[0], positions[1], self.number)
                        played = True
        if played:
            os.system('cls')
            print(f"Player {self.number} played {positions}.")