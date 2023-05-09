from Game import Game
import timeit


def test_game():
    # test computer vs MiniMax Computer game without display, return winner number
    game = Game()
    return game.start(False, "3")


def main():
    # main game function
    game = Game()
    game.start()


if __name__ == '__main__':
    main()
    # testing 100 games
    # draws = 0
    # t1 = timeit.default_timer()
    # for _ in range(100):
    #     if test_game() == 0:
    #         draws += 1
    # t2 = timeit.default_timer()
    # print(f"Draws: {draws}, Time: {t2-t1}")
