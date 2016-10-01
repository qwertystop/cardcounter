# cardcounter
Extensible functional system for playing card games. Python 3.

`carcounter/engine` contains code to define a card type, determine the odds of drawing a given card, and request a set of players.

`cardcounter/games` contains code to have the computer act as one player, via terminal IO, in a game of 7-27 (similar to blackjack, but with two target numbers).
It's not very smart, but works as a proof-of-concept.

To play, just run `play.py` and follow the prompts.


####To developers:
Feel free to submit pull requests adding more games or more general non-game-specific functionality, if this catches your interest.
Additional games should be single files or submodules in the `cardcounter/games` directory. Type hints are nice, but not required.
