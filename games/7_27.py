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
from typing import Dict, List, Optional, Sequence
from cardcounter.engine import card
from cardc ounter.engine.counting_engine import odds_of

def play(playerlist: Sequence[str], thisname: str) -> None:
    """
    Main gameplay loop for 7-27. Call this to start play.
    """

    tablestate = get_deal()

    # Keep going around the table
    # Until nobody takes a card
    done = False
    while not done:
        done = True  # assume done each round unless someone does take
        for player in playerlist:
            if player == thisname:
                pass  # TODO determine whether or not to draw
            else:
                playerdraw = get_single_draw(
                    'What card did {} draw? "-" for no draw.'.format(player), True)

            # Whoever it was, if they drew, update tablestate and this isn't the end.
            if playerdraw is not None:
                tablestate[player].append(playerdraw)
                done = False

        # Everyone's done, tally the hands and display the winners
        pass  # TODO

def get_deal(playerlist: Sequence[str], thisname: str) -> Dict[str, List[card.Card]]:
    """
    Get what card everyone has showing after the initial deal.
    """

    tablestate = {}
    for player in playerlist:
        if player == thisname:
            message = "What card do I have? "
        else:
            message = "What card does {} have? ".format(player)
        tablestate[player] = get_single_draw(message)
    return tablestate

def get_single_draw(message: str, can_pass=False : bool) -> Optional[card.Card]:
    """
    Get one draw from user; keep trying until user inputs something valid
    """

    prompt = 'Enter card as rank followed by suit, e.g. "AS", "7D", "QH", "10C".\n'
    while True:
        entry = input(message)
        if can_pass and (entry == '-'):
            return  # No card
        else:
            try:  # Until they put in something valid
                return [card.parse_card(input(message))]
            except ValueError:
                print("Invalid card.", prompt)
