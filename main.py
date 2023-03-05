from Game import Game

def test_game():
    game = Game()
    game.start(False, "3")

def main():
    game = Game()
    game.start()


# main game function
if __name__ == '__main__':
    #main()
    for _ in range(101):
        test_game()

