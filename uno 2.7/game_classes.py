import deck_gen
import pygame
import os

class Player:

    def __init__(self, name):
        self.name = name
        self.hand = []
        self.skip = False

        self.Client = False
        # AI vairables only
        self.AI = False
        self.AI_type = None
        self.Main_Decision_Tree = None
        self.Card_Guess_Tree = None
        self.Card_Choose_Tree = None
        self.hatval = dict()

    def grab_card(self, deckname):  # grab a card from the deck
        card = deckname.grab_card()
        if card is None:  # likely the deck is empty
            return None
        card.set_Owner(self.name)
        self.hand.append(card)

    def grab_card_multi(self, deckname, cardname):
        card = deckname.grab_card_multi(cardname)
        card.set_Owner(self.name)
        self.hand.append(card)

    def grab_cards(self, deckname, n):  # grab n number of cards from the deck
        for i in range(n):
            self.grab_card(deckname)

    def play_card(self, boardname, card_ID):
        card = self.hand.pop(card_ID)
        card.set_Owner(None)
        boardname.update_Board(card)

    def push(self, player):
        for a in player:
            print(a)

class Deck:

    def __init__(self, name, input_deck):
        self.name = name
        self.deck_size = len(input_deck)
        self.deck = []

        for card in input_deck:
            card.set_Owner(self.name)
            self.deck.append(card)

    def grab_card(self):
        if self.deck == []:
            print("deck is empty...")
            print("regenerating deck...")
            self.deck = deck_gen.gen_rand_deck(self.name, 1).deck
        
        card = self.deck.pop()
        card.set_Owner(None)
        return card

    def grab_card_multi(self,name):
        for a in self.deck:
            if a.name == name:
                return a

class Board:

    def __init__(self, name):
        self.name = name
        self.card_stack = []
        self.type = None
        self.color = None
        self.turn_iterator = 1

    def update_Board(self, card):  # add a new card onto the board
        card.set_Owner(self.name)
        self.type = card.type
        self.color = card.color
        self.card_stack.append(card)

    def check_Board(self):  # returns the newest card of the board
        if self.card_stack == []:
            print("The board is empty...")
            return None
        return self.card_stack[-1]


class Card:
    def __init__(self, name, filename, owner=None, colormode = False):
        self.name = name
        self.card_data = pygame.image.load(filename)
        self.rect = self.card_data.get_rect()
        self.Owner = owner
        self.color = name[0]
        self.type = name[2]

        self.old_val = 0

    def set_Owner(self, owner):
        self.Owner = owner

    def play_card(self, boardname):
        self.set_Owner(None)
        boardname.update_Board(self)
