class Board:
    # class representing 3x3 TicTacToe board as 2d list of strings 'fields' [y,x]

    def __init__(self):
        self.size = 3
        self.fields = list()
        self.free_fields = list()
        # populating fields list with empty fields
        for i in range(self.size):
            self.fields.append(list())
            for j in range(self.size):
                self.fields[i].append(" ")
                # free fields - list of tuple with positions in of unmarked fields (y,x)
                self.free_fields.append((i, j))
        self.win = False
        self.winner = 0
        # Constants "X" player is 1, "O" player is 2
        self.X_PLAYER = 1
        self.O_PLAYER = 2
        self.VERTICAL_LINES = [1, 2, 3]
        self.HORIZONTAL_LINES = [4, 5, 6]
        self.FIRST_DIAGONAL_LINE = [7]
        self.SECOND_DIAGONAL_LINE = [8]


    def read_field(self, pos: tuple[int, int]) -> str:
        # read field value
        return self.fields[pos[0]][pos[1]]

    def check_empty(self, pos: tuple[int, int]) -> bool:
        # check if field is empty
        return self.read_field(pos) == " "

    def mark_field(self, pos: tuple[int, int], player: int) -> bool:
        # mark field pos if its empty, return True if successfully marked
        if self.check_empty(pos):
            if player == self.X_PLAYER:
                self.fields[pos[0]][pos[1]] = "X"
                self.free_fields.remove(pos)
                return True
            elif player == self.O_PLAYER:
                self.fields[pos[0]][pos[1]] = "O"
                self.free_fields.remove(pos)
                return True
        return False

    def clear_field(self, pos: tuple[int, int]) -> None:
        # remove mark form the field indicated by pos, return field to free fields list
        self.fields[pos[0]][pos[1]] = " "
        self.free_fields.append(pos)

    def check_line(self, line_id: int) -> (int, int, list, int):
        # check situation in given line, return amount of field belonging to each player and empty fields in each line
        # line_id == 1, 2, 3: vertical lines, line_id == 4, 5, 6 horizontal, line_id == 7, 8 diagonal
        x_player = 0
        o_player = 0
        empty_fields_in_line = list()
        field_position = (0, 0)
        # check every field in line
        for i in range(self.size):
            # calculate field to read based on line_id
            # vertical lines
            if line_id in self.VERTICAL_LINES:
                field_position = (i, line_id - 1)
            # horizontal lines
            elif line_id in self.HORIZONTAL_LINES:
                field_position = (line_id - 4, i)
            # first diagonal
            elif line_id in self.FIRST_DIAGONAL_LINE:
                field_position = (i, i)
            # second diagonal
            elif line_id in self.SECOND_DIAGONAL_LINE:
                field_position = (2 - i, i)
            # check value of given field
            value = self.read_field(field_position)
            # add to player value if it is taken or save its position if it is empty
            if value == 'X':
                x_player += 1
            elif value == 'O':
                o_player += 1
            else:
                empty_fields_in_line.append(field_position)
        # after finished loop return result
        return x_player, o_player, empty_fields_in_line, line_id

    def draw(self):
        # draw current situation on board
        for y in range(len(self.fields)):
            for x in range(len(self.fields[y])):
                print(self.read_field((y, x)), end="")
                if x != 2:
                    print("|", end="")
            if y != 2:
                print("\n-----")
        print("\n")

    def get_line_ids_from_field(self, pos: tuple[int, int]):
        # based on fields position return list of line_ids it belongs to
        # line_id == 1, 2, 3: vertical lines, line_id == 4, 5, 6 horizontal, line_id == 7, 8 diagonal
        # vertical and horizontal line
        line_ids = [pos[1] + 1, pos[0] + 4]
        # check if field is on the first diagonal
        if pos[0] == pos[1]:
            line_ids.append(self.FIRST_DIAGONAL_LINE[0])
        # check if field is on the second diagonal
        if pos[0] + pos[1] == 2:
            line_ids.append(self.SECOND_DIAGONAL_LINE[0])
        return line_ids

    def reset_winner(self):
        # reset board winner - used for reversing test moves for Minmax
        self.win = False
        self.winner = 0

    def check_win(self, pos: tuple[int, int]) -> bool:
        # check if any player won after marking field indicated by pos
        # if there are more than 4 free fields victory is impossible
        if len(self.free_fields) > 4:
            return self.win
        # if there are less free fields evaluate lines
        # get list of line_ids that field pos belongs to
        line_ids = self.get_line_ids_from_field(pos)
        # check lines
        for line_id in line_ids:
            result = self.check_line(line_id)
            # if line is fully marked by player than player won
            if result[0] == self.size:
                self.win = True
                self.winner = self.X_PLAYER
                break
            elif result[1] == self.size:
                self.win = True
                self.winner = self.O_PLAYER
                break
        # return result after loop is ended
        return self.win
