#Contains helper functions for game.py and the Player class
import deck
import buy_cards
import pygame

"""
Class for each player entity
Created by dc_player.player(own_deck, isComputer)
own_deck: the player's deck to start
isComptuer: whether this is a computer or human player 
"""
class Player:

    def __init__(self, own_deck, isComputer):
        self.own_deck = own_deck
        self.isComputer = isComputer

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
    #TODO make subclass for player decks
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

#remove card from lineup
def remove_from_lineup(card):
    pass

#called when a card is bought
def buy_card(player, card):
    pass


#run the computer turn
def computer_turn(player, super_villain_deck, main_deck, kick_deck, lineup):
    #TODO figure out power via the playing cards algorithm
    power = 0
    #list of cards to buy
    cards_to_buy = buy_cards.buy_cards(power, super_villain_deck, main_deck, kick_deck, player.own_deck, lineup)
    for card in cards_to_buy:
        buy_card(player, card)
    pass

#loop to run while the player is taking their turn
def player_turn():
    pass
