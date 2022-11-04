from Game import Game
from Board import Board
from Player import MinMaxComputerPlayer

game = Game()
winner = game.start()

# win1 = win2 = draw = 0
# for i in range(100):
#     game = Game()
#     winner = game.start("3")
#     if winner == 1:
#         win1 += 1
#     elif winner == 2:
#         win2 += 1
#     else:
#         draw += 1
# print(win1, win2, draw)


# board = Board(3)
# player = MinMaxComputerPlayer(1)
# board.write((0, 0), 1)
# board.write((0, 2), 1)
# board.write((2, 2), 1)
#
# board.write((0, 1), 2)
# board.write((1, 0), 2)
# board.write((1, 2), 2)
# board.draw()
# minmax_res = player.get_positions(board)
# print("result", minmax_res)








