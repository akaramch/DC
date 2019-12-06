#various individual functions for card effects

"""
Takes a player that played the card and the card and executes the effects of the card
Parameter list:
    player: the player who played the card
    card: the card to be played
Return:
    list of cards to buy
"""
def card_effect(player, card):
    #add the base, unconditional power to the player's power
    player.power += card.power[0]

    #check the conditional bonus power
    power_bonus = 0
    power_bonus_type = card.power[1] #sig
    if power_bonus_type != 0: #has a bonus power chance
        if power_bonus_type == 1: #power ring
            #if the top of the undrawn deck has cost > 0, +1 power
            if player.own_deck.peek.get_cost() > 0:
                power_bonus += 1

        elif power_bonus_type == 2: #starbolt
            #for each super power in discard, +1
            for card in player.own_deck.discard:
                if card.get_type() == "Power":
                    power_bonus += 1

        elif power_bonus_type == 3: #winged warrior
            #if hero played before or after in turn, +3
            #TODO how to check if a hero is played after it
            pass
        elif power_bonus_type == 4: #hawkgirl
            # for each hero in discard, +1
            for card in player.own_deck.discard:
                if card.get_type() == "Hero":
                    power_bonus += 1

        elif power_bonus_type == 5: #king of atlantis
            #+2 Power if you destroy a card in discard pile
            #TODO how to prompt players about destroy
            pass
        elif power_bonus_type == 6: #red lantern corps
            #+2 additional power if you destroy a card in hand
            #TODO how to prompt players about destroy
            pass
        elif power_bonus_type == 7: #killer croc
            #+1 if play/have played another Villain this turn
            #TODO how to check if a villain is played after it
            pass
    #add calculated bonus power to player power
    player.power += power_bonus

    #do any drawing for the card
    draw = card.draw[0]

    draw_bonus = 0
    draw_bonus_type = card.draw[1]
    if draw_bonus_type != 0:
        if draw_bonus_type == 1: #two face
            #guess top cost even/odd, if right, draw it, else discard
            #TODO how to prompt player for their guess
            pass

    #add draw bonus
    draw += draw_bonus
    #draw the correct number of cards
    for i in range(0, draw):
        player.own_deck.draw()

    #TODO any type of destruction (can't do this at all without prompting users