#Contains helper functions for game.py and the Player class
import deck
import buy_cards
import pygame

"""
Class for each player entity
Created by dc_player.player(own_deck, isComputer)
card_list: list of cards in the player's deck to start
isComputer: boolean whether this is a computer or human player 
"""
class Player:

    def __init__(self, card_list, isComputer):
        self.own_deck = deck.PlayerDeck(card_list) #player's deck
        self.isComputer = isComputer #is this the human or computer player
        self.power = 0 #power tracker for turns
        self.prompt = (False, "", [], False) # (is the player being prompted to pick a card, text of prompt, cards to pick from, do they have to pick a card)
        #flags for effects that trigger after the card is played
        self.winged_warrior_effect = False
        self.killer_croc_effect = False
        self.black_adam_effect = (True, True, True, True, True) #(found_hero, found_villain, found_equipment, found_starter, found_power) all true if not in effect
        self.aquamans_trident = False

    # takes card from lineup and adds to discard pile
    def gain_card_discard(self, card):
        self.own_deck.add_card(card)  # adds to deck contents for stats
        self.own_deck.add_to_discard(card) #adds to discard pile

    # takes card from lineup and adds to top of undrawn
    def gain_card_top(self, card):
        self.own_deck.add_card(card) #adds to deck contents for stats
        self.own_deck.add_to_undrawn_top(card)  #adds to the top of the undrawn list

    # takes card from lineup and adds to hand
    def gain_card_hand(self, card):
        self.own_deck.add_card(card)  # adds to deck contents for stats
        self.own_deck.add_to_hand(card) #adds to hand
    

    #ends the turn by discarding all cards from hand and played and draws new hand
    def end_turn(self):
        #move cards from hand to discard
        for i in range(len(self.own_deck.hand)):
            self.own_deck.hand_to_discard(0)
        #move from played to discard
        self.own_deck.played_to_discard()
        #draw new hand
        while len(self.own_deck.hand) < 5:
            self.own_deck.draw()
        #reset power to 0
        self.power = 0
"""
Sets up main deck.
Parameter list: 
    card_list: cards to be added to main deck
Returns: loaded main deck
"""
def load_main_deck(card_list):
    main_deck = deck.Deck(card_list) #create deck
    main_deck.shuffle() #shuffle the deck
    return main_deck

"""
Sets up a player deck.
Parameter list:
    card list: cards that are in the initial player deck
Returns: loaded main deck
"""
def load_player_deck(card_list):
    player_deck = deck.Deck(card_list)
    player_deck.shuffle()
    return player_deck

"""
Set up the super villain deck
Parameter list:
    super_villains: list of super villains (excluding the flash which will be added later)
Returns: loaded villain deck
"""
def load_villain_deck(super_villains):
    villain_deck = deck.Deck(super_villains)
    villain_deck.shuffle()
    return villain_deck

"""
Returns current line-up, for use with WLPB
"""
def current_lineup():
    #return game.lineup
    pass

#run the computer turn
def computer_turn(player, super_villain_deck, main_deck, kick_deck, lineup):
    #TODO figure out power via the playing cards algorithm
    power = 0
    #list of cards to buy
    cards_to_buy = buy_cards.buy_cards(power, super_villain_deck, main_deck, kick_deck, player.own_deck, lineup)
    for card in cards_to_buy:
        pass
        #buy_card(player, card)
    pass


