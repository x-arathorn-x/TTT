
from logic import Human, Bot, Game


if __name__ == "__main__":

    print("Play against :")
    print("1}Person ")
    print("2}Bot ")


    choice=int(input("> Pick?: "))
    if choice<=1:

        game=Game(Human(), Human())
    else:
        game=Game(Human(), Bot())



    game.run()