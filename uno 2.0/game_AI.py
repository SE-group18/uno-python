import Card_Choose_Tree
import Card_Guess_Tree
import game_classes
import Main_Decision_Tree

#TODO GET RUNTIME
def make_AI_basic(deck, AI_name, mem_depth=0):
    """
    Simple AI creation function that allows for the creation of a simple
    "flash frame decision" low memory style AI.

    Returns: AI_player_gen: a simple generated AI
    """
    AI_player_gen = game_classes.Player(AI_name)
    AI_player_gen.grab_cards(deck, 3)

    AI_player_gen.AI = True
    AI_player_gen.Main_Decision_Tree = Main_Decision_Tree.Main_Decision_Tree(AI_name)
    AI_player_gen.Card_Guess_Tree = Card_Guess_Tree.Card_Guess_Tree(AI_name, mem_depth)
    AI_player_gen.Card_Choose_Tree = Card_Choose_Tree.Card_Choose_Tree(AI_name)

    return AI_player_gen

def make_AI_A(deck, AI_name, mem_depth=0):
    """
    지역 A AI : 초기 7장의 카드를 받을 떄 기술카드를 받을 확률이 50% 더 높다.
    """

    AI_player_gen = game_classes.Player(AI_name)
    #AI_player_gen.grab_cards(deck, 7)

    AI_player_gen.AI = True
    AI_player_gen.Main_Decision_Tree = Main_Decision_Tree.Main_Decision_Tree(AI_name)
    AI_player_gen.Card_Guess_Tree = Card_Guess_Tree.Card_Guess_Tree(AI_name, mem_depth)
    AI_player_gen.Card_Choose_Tree = Card_Choose_Tree.Card_Choose_Tree(AI_name)

    return AI_player_gen


def make_AI_B(deck, AI_name, mem_depth=0):
    """
    지역 B AI : 초기 카드 분배시 모든 덱을 나누어 받음 3명 기준 20장
    """
    mem_depth = 18
    AI_player_gen = game_classes.Player(AI_name)
    #AI_player_gen.grab_cards(deck, 7)
    AI_player_gen.grab_cards(deck, mem_depth)

    AI_player_gen.AI = True
    AI_player_gen.Main_Decision_Tree = Main_Decision_Tree.Main_Decision_Tree(AI_name)
    AI_player_gen.Card_Guess_Tree = Card_Guess_Tree.Card_Guess_Tree(AI_name, mem_depth)
    AI_player_gen.Card_Choose_Tree = Card_Choose_Tree.Card_Choose_Tree(AI_name)

    return AI_player_gen

