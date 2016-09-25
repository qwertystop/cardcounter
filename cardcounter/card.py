"""
Structure for cards:
A card is a tuple(Rank, Suit)
"""
from enum import Enum

class Rank(Enum):
    Ace    = 1
    _2     = 2
    _3     = 3
    _4     = 4
    _5     = 5
    _6     = 6
    _7     = 7
    _8     = 8
    _9     = 9
    _10    = 10
    Jack   = "J"
    Queen  = "Q"
    King   = "K"

class Suit(Enum):
    Heart   = "H"
    Club    = "C"
    Spade   = "S"
    Diamond = "D"
