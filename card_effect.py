#various individual functions for card effects

"""

Takes a player that played the card and the card and executes the effects of the card
Parameter list:
    player: the player who played the card
    card: the card to be played
Return:
    none
"""

def card_effect(player, card):
    #add the base, unconditional power to the player's power
    player.power += card.power[0]

    #check the conditional bonus power
    power_bonus = 0

    #check previous card bonuses for cards that gain power after
    if player.killer_croc_effect:
        if card.type == "Villain":
            power_bonus += 1 #add killer croc bonus when triggered
            player.killer_croc_effect = False #reset the flag

    if player.winged_warrior_effect:
        if card.type == "Hero":
            power_bonus += 3 #add winged warrior bonus when triggered
            player.winged_warrior_effect = False #reset the flag

    power_bonus_type = card.power[1] #sig
    if power_bonus_type != 0: #has a bonus power chance
        if power_bonus_type == 1: #power ring
            #check if deck is empty
            if len(player.own_deck.undrawn) == 0:
                #if it's empty, refill it from discard
                player.own_deck.refill_deck()
            #if the top of the undrawn deck has cost > 0, +1 power
            if player.own_deck.peek().get_cost() > 0:
                power_bonus += 1

        elif power_bonus_type == 2: #starbolt
            #for each super power in discard, +1
            for card in player.own_deck.discard:
                if card.get_type() == "Power":
                    power_bonus += 1

        elif power_bonus_type == 3: #winged warrior
            #if hero played before or after in turn, +3
            #check if played already
            found_hero = False  # did we find a hero in our played
            for card in player.own_deck.played:
                if card.get_type() == "Hero":
                    power_bonus += 3
                    found_hero = True
                    break
            if not found_hero:
                player.winged_warrior_effect = True

        elif power_bonus_type == 4: #hawkgirl
            # for each hero in discard, +1
            for card in player.own_deck.discard:
                if card.type == "Hero":
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
            # check if played already
            found_villain = False  # did we find a villain in our played
            for card in player.own_deck.played:
                if card.get_type() == "Villain":
                    power_bonus += 1
                    found_villain = True
                    break
            if not found_villain:
                player.killer_croc_effect = True
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