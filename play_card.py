import deck

"""
Assigns priority to cards so that we can decide which to play.
For parameters, takes in the card as well as your deck.
Assigns priority as per the alg
"""
def assign_priority(card, own_deck):
    if card.name == "Weakness":
        return 1000
    if card.name == "Vulnerability":
        return 500
    if card.name == "Punch":
        return 100
    if card.destroy_top[0]:
        return 3
    if card.destroy_hand != 0:
        return 75
    if card.destroy_hand_or_discard != 0 or card.custom == 9:
        if len(own_deck.undrawn) <= 1:
            for tempcard in own_deck.undrawn:
                if (tempcard.name == "Weakness" or tempcard.name == "Vulnerability" or tempcard.name == "Punch"):
                    return 4
        return 8
    if card.destroy_discard != 0:
        for tempcard1 in own_deck.undrawn:
                if (tempcard1.name == "Weakness" or tempcard1.name == "Vulnerability"):
                    return 1
        if len(own_deck.undrawn) <= 1:
            for tempcard in own_deck.undrawn:
                if tempcard.name == "Punch":
                    return 2
        return 10
    if card.discard > 0:
        return 6
    if card.draw[0] > 0 or card.draw[1] > 0:
        return 5
    if card.custom == 4:
        return 7
    if card.power[1] == 2 or card.power[1] == 4 or card.power[1] == 5:
        if len(own_deck.undrawn) <= 1:
            return 1
        else:
            return 60
    

    return 10 #default priority

def to_play(hand, own_deck):
    min = 2000
    index = 11
    i = 0 #iterator thingy
    for card in hand:
        curr_priority = assign_priority(card, own_deck)
        if curr_priority < min:
            index = i
            min = curr_priority
        i += 1
    return hand[index]
"""
Given the top card of your library, will return True if you should destroy it, false otherwise
"""
def top_destroy(card):
    if card.name == "Weakness" or card.name == "Vulnerability" or card.name == "Punch":
        return True
    else:
        return False
"""
Given your hand, will return the card you should destroy
If you don't have a punch weakness, or vulnerability, it will destroy the card with least vp
This for when you have to destroy, there's another for optional destruction.
"""
def must_hand_destroy(hand):
    for card in hand:
        if card.name == "Weakness":
            return card
    for card in hand:
        if card.name == "Vulnerability":
            return card
    for card in hand:
        if card.name == "Punch":
            return card
    min = 0
    index = 11
    i = 0 #iterator
    for card in hand:
        if card.vp > min:
            min = card.vp
            index = i
        i += 1
    return hand[index]
"""
Given your hand, will return the card you should destroy if it's optional 
returns none if you shouldn't destroy any cards
Currently doesn't have code to destroy punches only if it prevents you from buying super
Need to look into whether it's worth passing this function enough things to add that code
"""
def can_hand_destroy(hand):
    to_destroy = must_hand_destroy(hand)
    if to_destroy.name == "Weakness" or to_destroy.name == "Vulnerability" or to_destroy.name == "Punch":
        return to_destroy
    else:
        return None
"""
Given your discard pile, will return which card you should destroy
Returns none if you shouldn's
"""
def discard_destroy(discard):
    for card in discard:
        if card.name == "Weakness":
            return card
    for card in discard:
        if card.name == "Vulnerability":
            return card
    for card in discard:
        if card.name == "Punch":
            return card
    return None
