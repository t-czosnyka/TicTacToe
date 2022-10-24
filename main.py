from Game import Game
import os
from Board import Board

type_ok = False
while not type_ok:
    os.system('cls')
    print("Choose game type:\n \
    1 - Player vs Player\n \
    2 - Player vs Computer\n \
    3 - Computer vs Computer\n")
    game_type = input()
    os.system('cls')
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

# board = Board(3)
# board.write(0, 1, 2)
# board.write(1, 1, 2)
# board.write(2, 1, 2)
#
# board.draw()
# print(board.check_win())








