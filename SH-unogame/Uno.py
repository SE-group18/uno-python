"""
UNO - CARD GAME

Allowing 2-4 people to play. Each player gets 7 cards each. The game follows basic Uno rules.
UNO RULES HERE: https://www.unorules.com/

-> Type Of Cards
Normal Card - Must match the top of the Discard Pile by number or colour
Swap Card - Will reverse the playing order. Must match the top of the Discard Pile by sign or colour.
Skip Card - Will skip the next person's turn. Must match the top of the Discard Pile by sign or colour.
2+ Card - The next player will pick up 2 cards. Must match the top of the Discard Pile by number or colour.
          If the previous one was also a 2+ card, the score will add up for the next player.
Wild Card - Allows the player to choose the next colour. Can be played on any type or colour.
4+ Wild Card - The next player picks up 4 cards and allows the current player to choose the next colour.
               If the previous one was also a 4+ card, the score will add up for the next player.
"""

import UnoGame as uno
from time import sleep

options = ['PLAY', 'EXIT']

while True:
    print(uno.thick_borders+"""\n\n|| ||   ||\ ||    // \\\\\n|| ||   ||\\\||   ((   ))\n\\\ //   || \||    \\\ //\n\n"""+uno.thin_borders+"\n")
    for i, option in enumerate(options):
        print(("{}| {}\n").format(i+1, option))
    print(uno.thick_borders)

    menu_choice = input("Select option: ").upper()
    if menu_choice == options[0] or menu_choice == '1':
        sleep(1)
        print("\n"+uno.thin_borders+"STARTING GAME"+uno.thin_borders)
        sleep(1)
        uno.Game().start_game()
    elif menu_choice == options[1] or menu_choice == '2':
        raise SystemExit