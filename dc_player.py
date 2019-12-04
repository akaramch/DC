#Contains helper functions for game.py
import deck
import game
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
Returns: loaded main deck
"""
def load_player_deck():
    #TODO make subclass for player decks
    card_list = [game.Punch]*7 + [game.Vulnerability]*3
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
    villain_deck.add_to_front(game.The_Flash) #the Flash starts every game
    return villain_deck
