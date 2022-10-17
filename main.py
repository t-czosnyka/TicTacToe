import time
from random import randint
from time import sleep

class Field:

    def __init__(self):
        self.value = " "

    def set(self, player):
        if self.value == " ":
            if player == 1:
                self.value = "X"
                return True
            elif player == 2:
                self.value = "O"
                return True
            else:
                print("Wrong player number.")
                return False
        else:
            print("Field already set.")
            return False

    def get(self):
        return self.value


class Board:

    def __init__(self):
        self.fields = [[Field(), Field(), Field()],
                       [Field(), Field(), Field()],
                       [Field(), Field(), Field()]]
        self.win = False
        self.winner = 0

    def read(self, y, x):
        return self.fields[y][x].get()

    def write(self, y, x, v):
        return self.fields[y][x].set(v)

    def draw(self):
        for y in range(len(self.fields)):
            for x in range(len(self.fields[y])):
                print(self.read(y, x), end="")
                if x != 2:
                    print("|", end="")
            if y != 2:
                print("\n-----")
        print("\n")

    def check_win(self): # Possible improvement
        self.win = False

        for y in range(len(self.fields)):
            if self.read(y, 0) != ' ':  # check win horizontal
                if self.read(y, 0) == self.read(y, 1) == self.read(y, 2):
                    self.win = True
                    winner = self.read(y, 0)
                    print("win horizontal")

            if not self.win and self.read(0, y) != ' ':  # check win vertical
                if self.read(0, y) == self.read(1, y) == self.read(2, y):
                    self.win = True
                    winner = self.read(0, y)
                    print("win vertical")
        if not self.win and self.read(1, 1) != ' ':  # check win diagonal 1
            if self.read(1, 1) == self.read(0, 0) == self.read(2, 2):
                self.win = True
                winner = self.read(1, 1)
                print("win diagonal")                # check win diagonal 1
            elif self.read(1, 1) == self.read(0, 2) == self.read(2, 0):
                self.win = True
                winner = self.read(1, 1)
                print("win diagonal")

        if self.win:
            if winner == 'X':
                self.winner = 1
            elif winner == 'O':
                self.winner = 2
        else:
            print("No win.")
        return self.win


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
                        time.sleep(3)
                        board.write(positions[0], positions[1], self.number)
                        played = True
        if played:
            print(f"Player {self.number} played {positions}.")



class Game:

    def __init__(self, player1_ctrl, player2_ctrl):
        self.players = []
        self.board = Board()
        if randint(0, 1) == 0:
            self.players.append(Player(player1_ctrl, 1))
            self.players.append(Player(player2_ctrl, 2))
        else:
            self.players.append(Player(player2_ctrl, 2))
            self.players.append(Player(player1_ctrl, 1))

    def start(self):
        move_count = 0
        self.board.draw()
        while not self.board.win:
            for player in self.players:
                player.play(self.board)
                self.board.draw()
                self.board.check_win()
                if self.board.win:
                    break
                move_count +=1
                if move_count == 5 and not self.board.win:
                    print("The game has ended in draw.")
        if self.board.win:
            print(f"Player {self.board.winner} won!")



type_ok = False
while not type_ok:
    print("Choose game type:\n \
    1 - Player vs Player\n \
    2 - Player vs Computer\n \
    3 - Computer vs Computer\n")
    game_type = input()
    if game_type == "1":
        game = Game("h", "h")
        type_ok = True
    elif game_type == "2":
        game = Game("h", "c")
        type_ok = True
    elif game_type == "3":
        game = Game("c", "c")
        type_ok = True
    else:
        print("Wrong game type.")

if isinstance(game, Game):
    game.start()









