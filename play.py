#! /usr/bin/python3

import cardcounter

GAMESET = {'7-27': cardcounter.games.seven_twentyseven}

if __name__ == '__main__':
    playargs = cardcounter.engine.getplayers.get_player_info()

    should_play = True
    while should_play:
        print("Which game would you like me to play?")
        for game in GAMESET:
            print(game)
        to_play = GAMESET[input("Choose one: ")]
        # TODO validate input
        same_game = True
        while same_game:
            same_game = to_play.play(*playargs)
        should_play = input("Ah, done, are we? Do you want to play something else?\n(y/n): ") == 'y'
        # TODO validate input
    print("All right, then. Goodbye!")
