"""
Function to get player information.
"""
from typing import List, Tuple

def get_player_info() -> Tuple[List[str], str]:
    """
    Get the set of players from the user. Returns (playerlist, thisname).
    """
    playerlist = input("Please list the names of all players,"
                      "in the order that they will take their turns.\n"
                      "(space-separated): ").split()
    thisname = input("Which player is this one?\n(by name): ").strip()
    while thisname not in playerlist:
        ans = input('"{}" wasn\'t in your previous list. Add as new player, going last?\n(y/n): '
                    .format(thisname))
        if ans == 'y':
            playerlist.append(thisname)
            print("Player list is {}".format(playerlist))
        elif ans == 'n':
            thisname = input("Which player is this one?\n(by name): ").strip()
        else:
            print("Please input 'y' or 'n'.")

    print("Game is ready to begin.")
    return (playerlist, thisname)
