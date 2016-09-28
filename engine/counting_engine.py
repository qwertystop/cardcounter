"""
Core system for counting cards
"""
from card import full_deck

def odds_of(*, known=None, target=None, joker=False) -> float:
    """
    Calculate odds of a single card not in known (from standard 52- or 54-card deck) being in target
    """
    unknown = [c for c in full_deck(joker) if c not in known]

    return len(c for c in unknown if c in target) / len(unknown)
