from deck_gen import gen_rand_deck
from deck_gen import generate_test_A
import display_funct
import game_AI
import game_classes
import game_logic
import Card_Choose_Tree
import Card_Guess_Tree
import Main_Decision_Tree
import random

def test_setting(deck, player):

    player2AI = game_AI.make_AI_A(deck, "player_2AI", 7)
    AIcard = []
    i=0
    for card in deck.deck:
        if(card.type=="p" or card.type=="s" or card.type=="r" or card.type=="d" or card.type=="c"):
            AIcard.append(i)
            AIcard.append(i)
            AIcard.append(i)
        else:
            AIcard.append(i)
            AIcard.append(i)
        i+=1
    print(i)
    print("Here!!!!!")
    print(len(AIcard))

    test_list = []
    while(len(test_list)<1000):
        temp = random.choice(AIcard)
        test_list.append(temp)
        while temp in AIcard:
            AIcard.remove(temp)
            
    test_list.sort(reverse=True)

    for list in test_list:
        card = deck.deck.pop(list)
        player2AI.hand.append(card)
        card.set_Owner(player2AI.name)

    count = 0
    for card in player2AI.hand:
        if(card.name=="b_0"):
            count+=1
    print("check!")
    print("일반카드 : "+str(count))
    print("특수카드 : "+str(1000-count))
    
    # ai 가 뽑을때 일반2 특수3 배수로 곱한 list를 셔플하고 뽑음
    # 한 장 뽑을때마다 뽑은 카드와 같은 카드를 제거해줌

    Players = [player, player2AI]
    return Players


def setting_A(deck, player):
    # 컴퓨터가 기술카드를 받을 확률 50% 증가
    player2AI = game_AI.make_AI_A(deck, "player_2AI", 7)
    player.grab_cards(deck,7)

    # ai 가 뽑을때 일반2 특수3 배수로 곱한 list를 셔플하고 뽑음
    # 한 장 뽑을때마다 뽑은 카드와 같은 카드를 제거해줌


    Players = [player, player2AI]
    return Players

def setting_B(deck, player):
    player.grab_cards(deck, 18)
    player2AI = game_AI.make_AI_B(deck, "player_2AI", 0)
    player3AI = game_AI.make_AI_B(deck, "player_3AI", 0)
    player4AI = game_AI.make_AI_B(deck, "player_4AI", 0)
    
    Players = [player, player2AI, player3AI, player4AI]
    return Players


def setting_D():
    # 기술카드 없이
    # 상대 카드가 다 보이게
    # 두턴씩
    # 3판 2선
    return 0

