from Game import Game


def test_game():
    # test computer vs MinMax Computer game without display, return winner number
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
    # for _ in range(100):
    #     if test_game() == 0:
    #         draws += 1
    # print(draws)
