from lockpattern import Game


def main():
    square_length = 3

    window = Game(square_length)
    window.main_loop()

    print("Hello World!")


if __name__ == '__main__':
    main()
