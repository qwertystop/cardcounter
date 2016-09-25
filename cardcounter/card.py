"""Structure for cards"""
from enum import Enum
from functools import lru_cache
from itertools import chain

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

@lru_cache(maxsize=2)
def full_deck(jokers):
    """Programmatically assemble an immutable deck, cache as necessary"""
    base_deck = zip((r for r in Rank for n in range(4)),
                    (s for n in range(13) for s in Suit))
    if jokers:
        return tuple(chain((Ellipsis, Ellipsis), base_deck))
    else:
        return tuple(base_deck)
