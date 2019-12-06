#Will have the deck class (more or less lists of cards, but with some other implemented fields
import cards
import random
import copy

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
        self.contents = [] #cards left in deck
        #add the cards in card_list to self.contents
        for card in card_list:
            self.add_card(card)

    #adds to bottom of deck
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
        #random's shuffle function does just this (thank you Python)
        random.shuffle(self.contents)

    #draws card from deck and returns it
    def draw(self):
        card = self.contents.pop(0)
        if card.get_type() == "Power":
            self.num_super_powers -= 1
        elif card.get_type() == "Hero":
            self.num_heroes -= 1
        elif card.get_type() == "Equipment":
            self.num_equipment -= 1
        elif card.get_type() == "Starter":
            self.num_starters -= 1
        elif card.get_type() == "Villain":
            self.num_villains -= 1
        elif card.get_type() == "Weakness":
            self.num_weaknesses -= 1
        return card

    #look at the top card of the deck without drawing
    def peek(self):
        return self.contents[0]

    #check if deck is empty
    def isEmpty(self):
        return self.num_cards == 0

    #adds to top of deck
    def add_to_front(self, card):
        self.contents.insert(0, card) #add to front of contents
        self.num_cards += 1
        # increment the proper field given card type
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

    #adds card to bottom of deck
    def add_to_bottom(self, card):
        self.contents.append(card) #add to back of contents
        self.num_cards += 1
        # increment the proper field given card type
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


class PlayerDeck(Deck):
    def __init__(self, card_list):
        super().__init__(card_list)
        self.undrawn = [] #cards in face down deck
        for card in self.contents:
            self.undrawn.append(card) #deep copy cards from initial content to start
        random.shuffle(self.contents) #need to shuffle the starters in undrawn deck
        self.hand = [] #player hand
        self.discard = [] #discard pile
        self.played = [] #cards played this turn

    # Shuffles the undrawn portion of the deck since that's what we care about
    def shuffle(self):
        random.shuffle(self.undrawn)
    
    #destroy a card from the player deck
    def destroy_from_deck(self, card):
        if card.get_type() == "Power":
            self.num_super_powers -= 1
        elif card.get_type() == "Hero":
            self.num_heroes -= 1
        elif card.get_type() == "Equipment":
            self.num_equipment -= 1
        elif card.get_type() == "Starter":
            self.num_starters -= 1
        elif card.get_type() == "Villain":
            self.num_villains -= 1
        elif card.get_type() == "Weakness":
            self.num_weaknesses -= 1
        self.contents.remove(card)
        self.undrawn.remove(card)

    #destroy card from hand
    def destroy_from_hand(self, index):
        if card.get_type() == "Power":
            self.num_super_powers -= 1
        elif card.get_type() == "Hero":
            self.num_heroes -= 1
        elif card.get_type() == "Equipment":
            self.num_equipment -= 1
        elif card.get_type() == "Starter":
            self.num_starters -= 1
        elif card.get_type() == "Villain":
            self.num_villains -= 1
        elif card.get_type() == "Weakness":
            self.num_weaknesses -= 1
        card = self.hand.pop(index)
        self.contents.remove(card)


    #destroy card from played
    def destroy_from_played(self, index):
        if card.get_type() == "Power":
            self.num_super_powers -= 1
        elif card.get_type() == "Hero":
            self.num_heroes -= 1
        elif card.get_type() == "Equipment":
            self.num_equipment -= 1
        elif card.get_type() == "Starter":
            self.num_starters -= 1
        elif card.get_type() == "Villain":
            self.num_villains -= 1
        elif card.get_type() == "Weakness":
            self.num_weaknesses -= 1
        card = self.played.pop(index)
        self.contents.remove(card)


    #destroy card from discard
    def destroy_from_discard(self, card):
        if card.get_type() == "Power":
            self.num_super_powers -= 1
        elif card.get_type() == "Hero":
            self.num_heroes -= 1
        elif card.get_type() == "Equipment":
            self.num_equipment -= 1
        elif card.get_type() == "Starter":
            self.num_starters -= 1
        elif card.get_type() == "Villain":
            self.num_villains -= 1
        elif card.get_type() == "Weakness":
            self.num_weaknesses -= 1
        self.contents.remove(card)
        self.discard.remove(card)

    #moves a card from hand to played
    def hand_to_played(self, index):
        card = self.hand.pop(index)
        self.played.append(card)

    #dumps all played cards into discard at end of turn
    def played_to_discard(self):
        self.discard += self.played
        self.played = []
    
    #draw a card from undrawn to hand
    def draw(self):
        card = self.undrawn.pop(0)
        self.add_to_hand(card)

    #add a card to hand
    def add_to_hand(self, card):
        self.hand.append(card)

    #look at top of undrawn
    def peek(self):
        return self.undrawn[0]

    #add card to discard (must be paired with self.add when new card to deck)
    def add_to_discard(self, card):
        self.discard.append(card)

    #add card to undrawn top (must be paired with self.add when new card to deck)
    def add_to_undrawn_top(self, card):
        self.undrawn.insert(0, card)

    #add card to undrawn bottom (must be paired with self.add when new card to deck)
    def add_to_undrawn_bottom(self, card):
        self.undrawn.append(card)

    #moves cards from discard pile to undrawn and shuffles
    def refill_deck(self):
        for card in self.discard:
            self.add_to_undrawn_bottom(card)
            random.shuffle(self.undrawn)
            self.discard = []
