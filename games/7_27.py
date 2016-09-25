"""
System to play the poker game "7-27"

Rules of game:
    Aces are worth either 1 or 11.
    Jacks, Queens, and Kings are worth 0.5
    Each player starts with one card showing and one card facedown.
    Each player has the goal of their hand's total value being closest to either 7 or 27.
    Each player chooses, each turn, whether to draw an additional card from the deck.
    Additional drawn cards are faceup.
    Turns are not simultaneous.
    Turns continue until a turn when all players still in do not take a card.
    Cost of staying in (whether or not you draw on a round):
        Start:       25¢
        Round 1:     25¢
        Round 2:     50¢
        Round 3:     75¢
        Subsequent: $1.00
"""
