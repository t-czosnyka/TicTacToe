from Field import Field


class Board:

    def __init__(self, size):
        self.size = size

        self.fields = list()
        self.free_fields = list()
        for i in range(self.size):
            self.fields.append(list())
            for j in range(self.size):
                self.fields[i].append(Field())
                self.free_fields.append((i, j))
        self.win = False
        self.winner = 0

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
            elif 4 <= line < 7:  # horizontal lines
                result = self.check_field(line - 4, i, empty)
            elif line == 7:  # first diagonal
                result = self.check_field(i, i, empty)
            elif line == 8:  # second diagonal
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
        if self.check_empty(y, x):
            self.free_fields.remove((y, x))
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

    def check_win(self):
        self.win = False
        for i in range(8):
            result = self.check_line(i+1)
            if result[0] == self.size:
                self.win = True
                self.winner = 1
                break
            elif result[1] == self.size:
                self.win = True
                self.winner = 2
                break
        return self.win
