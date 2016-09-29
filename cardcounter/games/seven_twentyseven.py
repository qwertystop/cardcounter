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
from collections import defaultdict
from typing import Dict, Iterable, List, Optional, Sequence
from cardcounter.engine import card
from cardcounter.engine.counting_engine import odds_by_rank

POINT_VALUES = {# Ace is a special case, not in this
                card.Rank._2: 2,
                card.Rank._3: 3,
                card.Rank._4: 4,
                card.Rank._5: 5,
                card.Rank._6: 6,
                card.Rank._7: 7,
                card.Rank._8: 8,
                card.Rank._9: 2,
                card.Rank._10: 3,
                card.Rank.Jack: 0.5,
                card.Rank.Queen: 0.5,
                card.Rank.King: 0.5}

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
                # Determine whether or not to draw
                # First, figure the odds of an improved score on a draw.
                hand_value = total_hand(tablestate[thisname])
                (odds, score, direction) = odds_to_beat(hand_value, tablestate)
                # Figure everyone else's likelihood of beating that with their current hand
                # Naive solution, certainly not optimal even if it did predict others' draws
                # Which it doesn't. This is big enough as is, and naive might be good enough
                # to shark the poker group this is intended for.
                other_odds = []
                for other in playerlist:
                    if other != thisname:
                        other_odds.append(odds_to_beat(total_hand(tablestate[other]), tablestate,
                                                       score, direction))
                # Finally, decide whether or not it's worth it
                if max(other_odds) > 0.7 or score == hand_value:
                    # Do not draw if someone else has a better than 70% chance
                    # or if there's no good odds of improvement anyway
                    print("I do not think I will draw a card.")
                    if max(other_odds) > 0.9:
                        print("In fact, I fold.")
                else:
                    playerdraw = get_single_draw("I will draw. What did I get?")
                # TODO Does not account for money involved to determine acceptable odds
            else:
                playerdraw = get_single_draw(
                    'What card did {} draw? "-" for no draw.'.format(player), True)
            # Whoever it was, if they drew, update tablestate and this isn't the end.
            if playerdraw is not None:
                tablestate[player].append(playerdraw)
                done = False

    # Everyone's done
    redo = input("So, we're done now? Or do you want another round?\n ('y' for another round): ")
    return redo == 'y'  # TODO validate input

def get_deal(playerlist: Sequence[str], thisname: str) -> Dict[str, List[card.Card]]:
    """
    Get what cards everyone has after the initial deal.
    """

    tablestate = {}
    for player in playerlist:
        if player == thisname:
            message = "What card do I have showing? "
            tablestate[player] = get_single_draw(message)
            message = "What card do I have hidden? "
        else:
            message = "What card does {} have? ".format(player)
        tablestate[player] = get_single_draw(message)
    return tablestate

def get_single_draw(message: str, can_pass: bool=False) -> Optional[card.Card]:
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

def total_hand(hand):
    """Get the best total of a hand, and whether it's low or high"""
    num_aces = score = 0
    for c in hand:
        if c[0] == card.Rank.Ace:
            num_aces += 1
        else:
            score += POINT_VALUES[c[0]]
    # Now include aces
    return branch_value_by_aces(score, num_aces)

def branch_value_by_aces(base, num_aces):
    """Calculate totals for each possible value of aces, return the best total.
    Naive solution, may not be actual best on multiple aces."""
    if num_aces == 0:
        return base
    elif num_aces < 0:
        raise ValueError("Negative number of aces?!")
    else:
        high = branch_value_by_aces(base + 11, num_aces - 1)
        low = branch_value_by_aces(base + 1, num_aces - 1)
        if rate_score(high)[0] < rate_score(low)[0]:
            return high
        else:
            return low

def rate_score(score, force_direction=0):
    """Scores rated by lower of distance to 7 or 27.
    Can force rating by comparison to 7 (pass negative) or 27 (pass positive)"""
    sevenscore = abs(7 - score)
    twentysevenscore = abs(27 - score)
    if force_direction < 0:
        return sevenscore, -1
    elif force_direction > 0:
        return twentysevenscore, 1
    else:
        return min(sevenscore, twentysevenscore), (sevenscore - twentysevenscore)

def odds_to_beat(hand_total, tablestate, to_beat=None, direction=0):
    """From a hand and the table, determine the odds of beating a given score with one draw.
    Also return the worst score for which the odds of doing at least that well are greater than 60%
    and the direction (- for 7, + for 27) of the score.
    If direction is given as not zero, specifically beat it for a target of (7 or 27, see above)
    With no given score, use the score of the current hand."""

    if to_beat == None:
        to_beat = hand_total

    used_cards = [c for h in tablestate.values for c in h]
    # Get the odds for drawing each rank
    rank_odds = {r: odds_by_rank(known=used_cards, targetrank=r, joker=False)
                for r in card.Rank}
    # Convert that to odds of any given value
    score_odds = defaultdict(int)
    for r in card.Rank:
        if r == card.Rank.Ace:
            score = branch_value_by_aces(hand_total, 1)
        else:
            score = branch_value_by_aces(hand_total + POINT_VALUES[r], 0)
        score_odds[score] += rank_odds[int]
    # Filter out the ones that are too low
    for score, _ in score_odds:
        if rate_score(score, direction)[0] < rate_score(to_beat, direction)[0]:
            del score_odds[score]
    # Sort the rest by how good they are, and sum their odds
    scores = sorted(score_odds.keys, key=lambda x: rate_score(x, direction)[0])
    answer = sum(score_odds.values)
    running_odds = 0.0
    for s in scores:
        running_odds = score_odds[s]
        if running_odds > 0.6:
            sixty_percent = s
            break
    else:  # No break, nothing likely
        sixty_percent = hand_total  # reliable odds are to stay
    return answer, sixty_percent, rate_score(sixty_percent, direction)[1]
