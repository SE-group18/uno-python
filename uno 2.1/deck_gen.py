import game_classes
from random import shuffle


col=0
flag = True
def generate_cards():
    """
    Generate one set of all uno cards by iterating through all the possible
    subtrings that relate to the filepath of the cards image in small_cards.
    This method thus limits to only having the PY-UNO game run within its own
    containing folder.

    Returns: An "ordered" list of all cards that are possible to create with
    the images within small_cards. Cards are defined by the Card class in
    game_classes.

    O(m*n) runtime where n is the number of colors and m is the number of types.
    However, if the card game requires a small vairance of cards the impact of
    function is greatly reduced
    """
    cards = []
    # predefined cards substrings 4/18일 수정 새로운 덱 구현
    colors = ["blue_", "red_", "green_", "yellow_"]
    colors_name = ["b", "r", "g", "y"]
    card_type = ["picker", "skip", "reverse","king","draw1","0",
                 "1", "2", "3", "4", "5", "6", "7", "8", "9"]

    # make predefined cards
    for i in range(len(colors)):  # O(m*n)
        for ct in card_type:
            if col == 0:
                filename_str = "small_cards/" + colors[i] + ct + ".png"
            elif col == 1:
                filename_str = "small_cards_color/" + colors[i] + ct + ".png"
            name_str = colors_name[i] + "_" + ct
            cards.append(game_classes.Card(name_str, filename_str, None))

    # make four wild pick 4
    if col == 1:
        cards.append(game_classes.Card(
            "w_d1", "small_cards_color/wild_pick_four.png", None))
        cards.append(game_classes.Card(
            "w_d2", "small_cards_color/wild_pick_four.png", None))
        cards.append(game_classes.Card(
            "w_d3", "small_cards_color/wild_pick_four.png", None))
        cards.append(game_classes.Card(
            "w_d4", "small_cards_color/wild_pick_four.png", None))

        # make four wild color
        cards.append(game_classes.Card(
            "w_c1", "small_cards_color/wild_color_changer.png", None))
        cards.append(game_classes.Card(
            "w_c2", "small_cards_color/wild_color_changer.png", None))
        cards.append(game_classes.Card(
            "w_c3", "small_cards_color/wild_color_changer.png", None))
        cards.append(game_classes.Card(
            "w_c4", "small_cards_color/wild_color_changer.png", None))
        
        # make all_draw1 와일드 카드 모두 한장씩 4/18일 수정
        cards.append(game_classes.Card(
            "w_a1", "small_cards_color/all_draw1.png", None))
        cards.append(game_classes.Card(
            "w_a2", "small_cards_color/all_draw1.png", None))
        cards.append(game_classes.Card(
            "w_a3", "small_cards_color/all_draw1.png", None))
        cards.append(game_classes.Card(
            "w_a4", "small_cards_color/all_draw1.png", None))

        return cards
    else:
        cards.append(game_classes.Card(
            "w_d1", "small_cards/wild_pick_four.png", None))
        cards.append(game_classes.Card(
            "w_d2", "small_cards/wild_pick_four.png", None))
        cards.append(game_classes.Card(
            "w_d3", "small_cards/wild_pick_four.png", None))
        cards.append(game_classes.Card(
            "w_d4", "small_cards/wild_pick_four.png", None))

        # make four wild color
        cards.append(game_classes.Card(
            "w_c1", "small_cards/wild_color_changer.png", None))
        cards.append(game_classes.Card(
            "w_c2", "small_cards/wild_color_changer.png", None))
        cards.append(game_classes.Card(
            "w_c3", "small_cards/wild_color_changer.png", None))
        cards.append(game_classes.Card(
            "w_c4", "small_cards/wild_color_changer.png", None))
        
        # make all_draw1 와일드 카드 모두 한장씩 4/18일 수정
        cards.append(game_classes.Card(
            "w_a1", "small_cards/all_draw1.png", None))
        cards.append(game_classes.Card(
            "w_a2", "small_cards/all_draw1.png", None))
        cards.append(game_classes.Card(
            "w_a3", "small_cards/all_draw1.png", None))
        cards.append(game_classes.Card(
            "w_a4", "small_cards/all_draw1.png", None))

        return cards

def generate_cards_d():
    """
    Generate one set of all uno cards by iterating through all the possible
    subtrings that relate to the filepath of the cards image in small_cards.
    This method thus limits to only having the PY-UNO game run within its own
    containing folder.
    Returns: An "ordered" list of all cards that are possible to create with
    the images within small_cards. Cards are defined by the Card class in
    game_classes.
    O(m*n) runtime where n is the number of colors and m is the number of types.
    However, if the card game requires a small vairance of cards the impact of
    function is greatly reduced
    """
    cards = []
    # predefined cards substrings
    colors = ["blue_", "red_", "green_", "yellow_"]
    colors_name = ["b", "r", "g", "y"]
    card_type = [ "0","1", "2", "3", "4", "5", "6", "7", "8", "9"]

    # make predefined cards
    for i in range(len(colors)):  # O(m*n)
        for ct in card_type:
            if col == 1:
                filename_str = "small_cards_color/" + colors[i] + ct + ".png"
            else:
                filename_str = "small_cards/" + colors[i] + ct + ".png"
            name_str = colors_name[i] + "_" + ct
            cards.append(game_classes.Card(name_str, filename_str, None))
    return cards



def card_shuffler(cards):
    """
    Shufles a list of cards "randomly".

    Note: that shuffle is sudorandom thus behavour is not perfect, but is
    acceptable for game use.

    Returns:  A randomly shuffed list of cards. Output list contains the same
    elements as the input list.

    O(n) runtime
    """
    print("\n\nSHUFFLING CARDLIST...", end="   ")
    shuffle(cards)  # O(n)
    print("DONE\n\n")
    print("SHUFFLED CARDLIST:\n")
    return cards


def build_deck(deckname, card_list):
    """
    Function call that builds an uno game class deck from a list of uno game
    cards.

    Note: the output of build_deck is not shuffled, gen_rand_deck handels
    random card list generation.

    Returns: a Deck class using the cards defined in card_list

    O(1) runtime
    """
    deckout = game_classes.Deck(deckname, card_list)
    print("deck generated named: ", end="")
    print(deckname)
    return deckout


def gen_rand_deck(deckname, size):
    """
    Function that Generates random uno deck with assigned size (how many copies
    of one deck is included) and with name specified as input deckname.

    O(s*(m*n)^2) runtime where n is the number of colors and m is the number of types
    and s is the size of the dek to be generated.
    """
    cards = []
    for i in range(size):
        if deckname == "deck_d": # deck_d는 스테이지4
            cards = card_shuffler(generate_cards_d()) + cards
        else:
            cards = card_shuffler(generate_cards()) + cards
            cards = card_shuffler(cards)

    return build_deck(deckname, cards)

def generate_test_A(deckname):
    cards=[]
    wild = game_classes.Card("w_d1", "small_cards/wild_pick_four.png", None)
    normal = game_classes.Card("b_0", "small_cards/blue_0.png", None)
    for i in range (0,1000):
        cards.append(wild)
        cards.append(normal)
    return build_deck(deckname, cards)