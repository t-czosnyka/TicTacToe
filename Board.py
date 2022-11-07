

class Board:

    def __init__(self, size):
        self.size = size
        self.fields = list()
        self.free_fields = list()
        for i in range(self.size):
            self.fields.append(list())
            for j in range(self.size):
                self.fields[i].append(" ")
                self.free_fields.append((i, j))
        self.win = False
        self.winner = 0

    def read(self, pos):
        # read field value
        try:
            return self.fields[pos[0]][pos[1]]
        except TypeError:
            return None
        except IndexError:
            return None

    def check_empty(self, pos):
        # check if field is empty
        if self.read(pos) == " " and self.read(pos) is not None:
            return True
        else:
            return False

    def write(self, pos, v):
        # write to the field pos if not empty, v - player number 1- X , 2-O
        if self.check_empty(pos):
            if v == 1:
                self.fields[pos[0]][pos[1]] = "X"
                self.free_fields.remove(pos)
                return True
            elif v == 2:
                self.fields[pos[0]][pos[1]] = "O"
                self.free_fields.remove(pos)
                return True
            else:
                return False
        elif not self.check_empty(pos) and v == 0:
            self.fields[pos[0]][pos[1]] = " "
            self.free_fields.append(pos)
            return True
        else:
            return False

    def check_field(self, pos, empty: list):
        # check if field belongs to any player, if empty append to list
        pl1 = pl2 = 0
        value = self.read(pos)
        if value is not None:
            if value == "X":
                pl1 = 1
            elif value == "O":
                pl2 = 1
            else:
                empty.append(pos)
            return pl1, pl2

    def check_line(self, line: int):
        # check situation on board, return amount of field belonging to each player and empty field in each line
        # =1,2,3 vertical lines, line= 4,5,6 horizontal, line= 8,9 diagonal
        player1 = 0
        player2 = 0
        empty = list()

        for i in range(len(self.fields)):
            if 0 < line < 4:  # vertical lines
                result = self.check_field((i, line - 1), empty)
            elif 4 <= line < 7:  # horizontal lines
                result = self.check_field((line - 4, i), empty)
            elif line == 7:  # first diagonal
                result = self.check_field((i, i), empty)
            elif line == 8:  # second diagonal
                result = self.check_field((2 - i, i), empty)
            else:
                print("Wrong parameter: ", line)
                result = (0, 0)

            player1 += result[0]
            player2 += result[1]
        return player1, player2, empty, line

    def draw(self):
        # draw current situation on board
        for y in range(len(self.fields)):
            for x in range(len(self.fields[y])):
                print(self.read((y, x)), end="")
                if x != 2:
                    print("|", end="")
            if y != 2:
                print("\n-----")
        print("\n")

    def check_win(self):
        # check if any of the lines is marked by one player if yes return true
        self.win = False
        self.winner = 0
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
