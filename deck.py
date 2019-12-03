#Will have the deck class (more or less lists of cards, but with some other implemented fields
import cards

"""
deck class
__init__(card_list): initializes the list with all fields
"""

class Deck:

    def __init__(self, card_list):
        #start with empty deck
        self.num_cards = 0
        self.num_super_powers = 0
        self.num_heroes = 0
        self.num_equipment = 0
        self.num_starters = 0
        self. num_villains = 0
        self.num_weaknesses = 0
        self.contents = []
        #add the cards in card_list to self.contents
        for card in card_list:
            self.add_card(card)

    def add_card(self, card):
        #Add card to deck contents
        self.contents.append(card)
        self.num_cards += 1
        #increment the proper field given card type
        if card.get_type() == "Power":
            self.num_super_powers += 1
        elif card.get_type() == "Hero":
            self.num_heroes += 1
        elif card.get_type() == "Equipment":
            self.num_equipment += 1
        elif card.get_type() == "Starter":
            self.num_starters += 1
        elif card.get_type() == "Villain":
            self.num_villains += 1
        elif card.get_type() == "Weakness":
            self.num_weaknesses += 1

    #Shuffles the deck
    def shuffle(self):
        #TODO
        return 0

    #draws card from deck and returns it
    def draw(self):
        #TODO
        return 0

    #look at the top card of the deck without drawing
    def peek(self):
        #TODO
        return 0
    #TODO implement other useful deck functions (couldn't think of everything, it's 2:15 in the morning)