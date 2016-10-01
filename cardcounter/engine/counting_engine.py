"""
Core system for counting cards
"""
from cardcounter.engine.card import full_deck, Card, Suit
from typing import Iterable, Optional

def odds_of(*, known: Optional[Iterable[Card]]=None, target: Optional[Card]=None,
            joker: bool=False) -> float:
    """
    Calculate odds of a single card not in known (from standard 52- or 54-card deck) being in target
    """
    unknown = [c for c in full_deck(joker) if c not in known]
    return len([c for c in unknown if c[0] == target[0] and c[1] == target[1]]) / len(unknown)

def odds_by_rank(*, known, targetrank, joker):
    """Wrapper to ignore suit in odds calculation"""
    return sum(odds_of(known=known, target=(targetrank, s), joker=joker) for s in Suit)
