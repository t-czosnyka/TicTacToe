from Field import Field

class Board:

    def __init__(self, size):
        self.size = size

        self.fields = list()
        for i in range(self.size):
            self.fields.append(list())
            for j in range(self.size):
                self.fields[i].append(Field())
        self.win = False
        self.winner = 0
        self.taken = 0

    def check_empty(self, y, x):
        if self.read(y, x) == " ":
            return True
        else:
            return False

    def check_field(self, y: int, x: int, empty: list):
        pl1 = pl2 = 0
        value = self.read(y, x)
        if value == "X":
            pl1 = 1
        elif value == "O":
            pl2 = 1
        else:
            empty.append(tuple((y, x)))
        return pl1, pl2

    def check_line(self, line: int):
        # line=1,2,3 vertical lines, line= 4,5,6 horizontal, line= 8,9 diagonal
        player1 = 0
        player2 = 0
        empty = list()

        for i in range(len(self.fields)):
            if 0 < line < 4:  # vertical lines
                result = self.check_field(i, line - 1, empty)
            elif 4 <= line < 8:  # horizontal lines
                result = self.check_field(line - 4, i, empty)
            elif line == 8:  # first diagonal
                result = self.check_field(i, i, empty)
            elif line == 9:  # second diagonal
                result = self.check_field(2 - i, i, empty)
            else:
                print("Wrong parameter: ", line)
                result = (0, 0)

            player1 += result[0]
            player2 += result[1]
        return player1, player2, empty

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

    def check_win(self):  # Possible improvement
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
                print("win diagonal")  # check win diagonal 1
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