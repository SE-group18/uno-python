# Imports - Imports being used in program
from time import sleep
import random

# Base Cards = Cards & Settings that'll be needed throughout the program
colours = ["Red", "Yellow", "Green", "Blue"]
actions = ["Reverse", "Skip", "2+", "Wild 4+", "Wild"]

# Display borders
thin_borders = "-" * 25
thick_borders = "=" * 25


# Each Card contains a value and a type
class Card(object):
    def __init__(self, colour=None, card_type=None, is_starter=False):
        self.colour = colour
        self.type = card_type
        self.starter = is_starter
        self.card = "%s %s" % (self.colour, self.type)

        # Randomly generates a card 
        if not colour:
            chance = random.random()

            if chance >= 0.4 or self.starter:
                self.colour = random.choice(colours)
                self.type = random.randint(1,9)
            else:
                self.colour = random.choice(colours)
                self.type = random.choice(actions[:3])

            self.card = "%s %s" % (self.colour, self.type)

            if chance <= 0.1 and not self.starter:
                self.colour = None
                self.type = random.choice(actions[3:])
                self.card = self.type


class Deck(object):
    def __init__(self):
        self.deck = []

        for i in range(7):
            self.deck.append(Card())
    
    def __str__(self): return self.deck


# Each Table contains a Deck for each player    
class Table(object):
    def __init__(self, number_of_players):
        self.decks = []

        for i in range(number_of_players):
            self.decks.append(Deck())

    @property
    def table(self):
        return self.decks


class PlayerCycle(object):
    def __init__(self, table):
        self.cycle = table.table
        self._current_player = 0
        self.is_reversed = False  
    
    @property
    def current_player(self):
        return self._current_player
    
    @current_player.setter
    def current_player(self, value):
        self._current_player = value % len(self.cycle)

    @property
    def current_deck(self):
        return self.cycle[self.current_player].deck
    
    @property
    def continue_cycle(self):
        if self.current_player is None:
            return -1 if self.is_reversed else 0
        else:
            return self.current_player-1 if self.is_reversed else self.current_player+1
    
    def reverse_cycle(self):
        self.is_reversed = not self.is_reversed


class Settings(object):
    def __init__(self):
        self.options = {"2 Players": '2', "3 Players": '3', "4 Players": '4'}
        
    def display_settings(self):
        print("\n"+thick_borders+"\n\nSelect Number of Players\n\n"+thin_borders+"\n")
        for i, option in enumerate(self.options):
            print('-  '+str(option))
        print("\n"+thick_borders+"\n")
        
    def prompt(self):
        self.display_settings()
        while True:
            prompt_choice = input("Select Option: ")
            if prompt_choice.title() in self.options.keys() or prompt_choice in self.options.values():
                temp = Table(int(prompt_choice[0]))
                return PlayerCycle(temp)
            print(("\nERROR: {} is not an option...").format(prompt_choice.title()))


class Game(object):
    def __init__(self):
        self.table = Settings().prompt()
        self.round = 1
        self.pile_card = Card(None, None, True)

    def __next__(self):
        self.table.current_player = self.table.continue_cycle

    def check_players(self):
        if not self.table.current_deck:
            return True
        if len(self.table.current_deck) == 1:
            sleep(0.5)
            print(("\nUNO: Player {} has ONE card remaining...!").format(self.table.current_player+1))
        
        return False

    def display_hand(self):
        sleep(1)
        if self.check_players():
            return True
        print("\nIt is PLAYER %s's turn!" % str(self.table.current_player+1))
        input("Press ENTER when you're ready!")

        print("\n\n"+thin_borders+"\n-> YOUR HAND\n"+thin_borders+"\n")
        for i, card in enumerate(self.table.current_deck):
            print("%s| %s" % (i+1, card.card))
        print("\n"+thin_borders)

    def prompts(self, choice):
        def player_turn():
            if self.display_hand():
                return

            while True:
                print("LAST CARD: %s" % self.pile_card.card)
                user_choice = input("Select a card or (D)raw: ")
                try:
                    user_choice = int(user_choice) - 1
                    if -1 < user_choice <= len(self.table.current_deck)-1:
                        if not self.vaildate_card(self.table.current_deck[user_choice], user_choice):
                            print(("\nERROR: {} does not match the symbol or colour of {}...")\
                                .format(self.table.current_deck[user_choice].card, self.pile_card.card))
                        else:
                            break
                    else:
                        if len(self.table.current_deck) < 3:
                            print(("\nERROR: You only have {} card/s to select from...").format(len(self.table.current_deck)))
                        else:
                            print(("\nERROR: {} is not within range 1 and {}...").format(user_choice+1, len(self.table.current_deck)))
                except (TypeError, ValueError):
                    if user_choice.lower() == "d" or user_choice.lower() == "draw":
                        self.draw(1)
                        break
                    else:
                        print(("\nERROR: '{}' is not an option. Please select a card or (D)raw...").format(user_choice))

        if choice == 1:
            return player_turn()
    
    def vaildate_card(self, user_card, card_index):
        if user_card.colour:
            if (user_card.colour != self.pile_card.colour) and (user_card.type != self.pile_card.type):
                return False
            else:
                self.pile_card = user_card
                del self.table.current_deck[card_index]
                if user_card.type == "Reverse":
                    self.table.reverse_cycle()
                elif user_card.type == "Skip":
                    self.__next__()
                elif user_card.type == "2+":
                    self.penalty_cards(2)
        else:
            self.pile_card = self.choose_colour(user_card.type)
            del self.table.current_deck[card_index]
            if user_card.type == "Wild 4+":
                self.penalty_cards(4)
        return True

    def choose_colour(self, type):
        sleep(1)
        print("\n"+thick_borders)
        for colour in colours:
            print(("• {}").format(colour))
        print(thick_borders)

        while True:
            new_colour = input("Select new colour: ").title()
            if new_colour in colours:
                new_card = Card(new_colour, type)
                sleep(1)
                print(("Player {} has changed the colour to {}").format(self.table.current_player+1, new_colour))
                return new_card
            print(("\nERROR: {} is not an option...").format(new_colour))
    
    def penalty_cards(self, penalty):
        self.__next__()
        multiplier = 1
        while True:
            if self.penalty(penalty, multiplier):
                break
            multiplier += 1
            self.__next__()
        print(("\nPENALTY: Player {} must draw {} cards...").format(self.table.current_player+1, multiplier*penalty))
        sleep(1)
        self.draw(multiplier*penalty)
        return multiplier

    def penalty(self, penalty_score, multiplier):
        playable_card = False

        for card in self.table.current_deck:
            if card.type == self.pile_card.type:
                playable_card = True
        
        self.display_hand()
        if playable_card:
            print(("PENALTY WARNING: You must either counter with a {} card or (D)raw {} cards from the pile...\n")\
                .format(self.pile_card.type, multiplier*penalty_score))
            while True:
                print("LAST CARD: %s" % self.pile_card.card)
                user_choice = input("Select a card or (D)raw: ")
                try:
                    user_choice = int(user_choice) - 1
                    if -1 < user_choice <= len(self.table.current_deck)-1:
                        if self.table.current_deck[user_choice].type != self.pile_card.type:
                            print(("\nPlease counter with either a {} card or (D)raw {} cards from the pile...")\
                                .format(self.pile_card.type, multiplier*penalty_score))
                        else:
                            if penalty_score is 4:
                                self.pile_card = self.choose_colour("Wild 4+")
                            self.pile_card = self.table.current_deck[user_choice]
                            del self.table.current_deck[user_choice]
                            return False
                    else:
                        print(("\nERROR: {} is not within range").format(user_choice))
                except (TypeError, ValueError):
                    if user_choice.lower() == "d" or user_choice.lower() == "draw":
                        return True
                    else:
                        print(("\nERROR: '{}' is not an option. Please counter with a {} card or (D)raw {} cards from the pile...")\
                            .format(user_choice, self.pile_card.type, multiplier*penalty_score))
        print(("You have no {} cards to counter...").format(self.pile_card.type))
        sleep(1)
        return True


    def draw(self, num_of_cards):
        for i in range(num_of_cards):
            drawn_card = Card()
            sleep(.5)
            print(("\nDRAWN CARD: Player {} draws '{}'!").format(self.table.current_player+1, drawn_card.card))
            self.table.current_deck.append(drawn_card)

    def start_game(self):
        while True:
            self.prompts(1)
            if self.check_players():
                sleep(1)
                print(("\nPLAYER {} HAS WON!!!\n\n").format(self.table.current_player+1))
                sleep(5)
                break
            self.__next__()
