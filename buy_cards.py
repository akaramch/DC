from copy import deepcopy


#import cards -- commented out because throwing an error, assuming no longer needed.

import deck


"""
Finds cards in the lineup to buy with given power that maximizes VP gain
*ONLY CALL WHEN A SOLUTION EXISTS*
Parameter list:
    power: buying power
    lineup: lineup (sorted by descending vp value)
    lineup1: lineup (sorted by decreasing vp to cost ratio)

Return:
    list of cards to buy
"""
def max_vp_lineup(power, lineup, lineup1):
    """
    lineup is sorted by vp value, highest to lowest, with the tiebreaker for cards with
    equal value being cards with lowest cost first
    lineup1 is sorted by vp value/cost ratio, highest to lowest, with the tiebreaker for
    cards with equal ratio being cards with highest cost first
    Both need to be sorted before entered for the function
    """
    cards_to_buy_val = [] #cards bought by sorting by val
    cards_to_buy_ratio = [] #cards bought by sorting by ratio
    val_buy_total = 0 #value of cards bought by sorting by val
    ratio_buy_total = 0 #value of cards bought by sorting by ratio
    leftovers = []
    #Buy in order as we can the highest values
    while len(lineup) > 0:
        if power > lineup[0].get_cost(): #if we can buy the most vp
            card = lineup.remove[0] #most vp left on lineup
            power -= card.get_cost()
            val_buy_total += card.get_vp
            cards_to_buy_val.append(card) #add most vp to cards to buy
        else: #if we can't buy it, add it to leftovers
            leftovers.append(lineup.remove[0])
    #bought the entire lineup so can just return
    if len(leftovers) < 1:
        return cards_to_buy_val

    while len(lineup1) > 0:
        if power > lineup1[0].get_cost(): #if we can buy the most vp
            card = lineup1.remove[0] #most vp left on lineup
            power -= card.get_cost()
            ratio_buy_total += card.get_vp
            cards_to_buy_ratio.append(card) #add most vp to cards to buy
        else: #if we can't buy it, add it to leftovers
            leftovers.append(lineup1.remove[0])
    if val_buy_total > ratio_buy_total: #if we get higher victory points sorting by val, return that
        return cards_to_buy_val
    else:
        return cards_to_buy_ratio #otherwise return the cards bought by sorting by ratio



"""
Wrapper for various functions for the sort function
"""
def cost(card):
    return card.cost #returns cost

def vp(card):
    return (card.get_vp() - (0.01*card.cost)) #Returns vp, breaks ties towards cards with lower cost

def vp_ratio(card):
    return ((card.get_vp()/card.get_cost()) + (0.01*card.cost)) #Returns vp to cost ratio, breaks ties towards cards with higher cost

def deck_power(card): #Returns the difference between the card's power and the average power in the deck
    return card.indeck_power #"But Kabir, this doesn't exist!" you say. Don't even worry about it...

def dp_ratio(card): #like above, but a ratio
    return (card.indeck_power/card.get_cost)
"""
Now for the fun stuff- getting the power a card generates. This looks explicitly at power for cards in your deck, so drawing not considered
"""
def get_power(card, own_deck, kick_deck, main_deck_size, opponent_deck, player_power, super_deck_size, from_deck):
    power = 0 #The power the card generates, both directly and through other means
    if (card.custom != 0): #customs are various cards with precalculated power generation, mostly supervillains
        if (card.custom == 1):
            return 6
        if (card.custom == 2):
            return 5
        if (card.custom == 3):
            return 6
        """
        X-ray vision
        """
        if (card.custom == 4):

            power_in_deck = 0 #going to look at the total power in the opponent's deck to calculate average
            for tempcard in opponent_deck.contents:
                power_in_deck += get_power(tempcard, own_deck, kick_deck, main_deck_size, opponent_deck, player_power, super_deck_size, False)
            average_power = power_in_deck/(opponent_deck.size)
            return average_power
        if (card.custom == 5): #Supergirl is worth different things depending on how many kicks are left

            if (kick_deck.size >= 12):
                return 4
            if (kick_deck.size >= 9):
                return 3
            if (kick_deck.size >= 5):
                return 2
            else:
                return 0
        if (card.custom == 6):
            power_in_deck = 0 #going to look at the total power in the deck to calculate average
            for tempcard in own_deck.contents:
                if(tempcard.custom != 6): #don't want to look at Parallax itself when calculating average power
                    power_in_deck += get_power(tempcard, own_deck, kick_deck, main_deck_size, opponent_deck, player_power, super_deck_size, True)
            average_power = power_in_deck/(own_deck.size-1)
            average_power = 4*average_power
            return average_power
        if (card.custom == 7):
            return 8
        if (card.custom == 8):
            return 6
        if (card.custom == 9):
            return 9
        if (card.custom == 10):
            return 15
        if (card.custom == 11):
            return 7
        if (card.custom == 12):
            return 6
        if (card.custom == 13):
            power += 2
            for tempcard in own_deck.contents:
                if (tempcard.type == "Equipment"):
                    power += 1
            return power
    power += card.power[0]
    """
    If it's a power ring, checks percent of deck that has above zero cost, 
    then adds that fraction to power.
    """
    if (card.power[1]==1):
        non_zero_count = 0
        for tempcard in own_deck.contents:
            if (tempcard.cost >= 1):
                non_zero_count += 1
        power += (non_zero_count/own_deck.size)
    """
    If it's starbolt, does the thing mentioned in our alg doc
    """
    if (card.power[1]==2):
        power_count = 0
        for tempcard in own_deck.contents:
            if(tempcard.type == "Power"):
                power_count += 1
        power += (0.5*power_count)
        if (player_power == "Superman" or player_power == "Cyborg"):
            power += (0.05*main_deck_size)
        elif(player_power == "Wonderwoman" or player_power == "Black Canary" or player_power == "The Sphinx" or player_power == "Hawkman" or player_power == "Batman" ):
            power += (0.01*main_deck_size)
        else:
            power += (0.02*main_deck_size)
    """
    Winged warrior does the thing the alg says it does
    """
    if (card.power[1]==3):
        if (player_power == "The Sphinx" or player_power == "Hawkman"):
            power += 3
        elif(player_power == "Wonderwoman" or player_power == "Black Canary" or player_power == "Cyborg" or player_power == "Superman" or player_power == "Batman" ):
            power += 0
        else:
            hero_count = 0
            for tempcard in own_deck.contents:
                if(tempcard.type == "Hero"):
                    hero_count += 1
            power += 3*(hero_count/own_deck.size)
    """
    Hawkgirl does the thing mentioned in our alg doc
    """
    if (card.power[1]==4):
        hero_count = 0
        for tempcard in own_deck.contents:
            if(tempcard.type == "Hero"):
                hero_count += 1
        power += (0.5*hero_count)
        if (player_power == "The Sphinx" or player_power == "Hawkman"):
            power += (0.05*main_deck_size)
        elif(player_power == "Wonderwoman" or player_power == "Black Canary" or player_power == "Cyborg" or player_power == "Superman" or player_power == "Batman" ):
            power += (0.01*main_deck_size)
        else:
            power += (0.02*main_deck_size)
    """
    King of Atlantis heuristicified to always +2
    """
    if (card.power[1]==5):
        power += 2
    """
    RLC heuristicized to +1.5
    """
    if (card.power[1]==6):
        power += 1.5
    """
    Killer croc does the thing our alg says it does
    """
    if (card.power[1]==7):
        if (player_power == "Wonderwoman" or player_power == "Black Canary"):
            power += 1
        elif(player_power == "The Sphinx" or player_power == "Hawkman" or player_power == "Cyborg" or player_power == "Superman" or player_power == "Batman" ):
            power += 0
        else:
            vill_count = 0
            for tempcard in own_deck.contents:
                if(tempcard.type == "Villain"):
                    vill_count += 1
            power += (vill_count/own_deck.size)
    """
    If it's from deck, the card draw is treated as +2, if not then it's calculated as
    an average of cards in deck, and the max of that and 1.99 is taken, as per the alg
    """
    if (from_deck):
        power += (2*card.draw[0])
    else:
        power_in_deck = 0 #going to look at the total power in the deck to calculate average
        for tempcard in own_deck.contents:
            power_in_deck += get_power(tempcard, own_deck, kick_deck, main_deck_size, opponent_deck, player_power, super_deck_size, True)
        average_power = power_in_deck/(own_deck.size)
        power += card.draw*max(1.99, average_power)
        
    """
    Two-face draws half a card on average, which is not quite true but a good heuristic
    """
    if (card.draw[1]==1):
        power += 1
    """
    Destroying from top of deck value calculated as by alg
    """
    if (card.destroy_top[0]):
        wk_count = 0
        punch_count = 0
        vul_count = 0
        for tempcard in own_deck.contents:
            if (tempcard.name == "Weakness"):
                wk_count +=1
            elif (tempcard.name == "Punch"):
                punch_count += 1
            elif (tempcard.name == "Vulnerability"):
                vul_count += 1
        power += (0.05*punch_count + 0.1*vul_count + 0.15*wk_count)
    """
    Destroying from hand value calculated as by alg, nothing in this set destroys more
    than one card from hand
    """
    if (card.destroy_hand > 0):
        wk_count = 0
        punch_count = 0
        vul_count = 0
        for tempcard in own_deck.contents:
            if (tempcard.name == "Weakness"):
                wk_count +=1
            elif (tempcard.name == "Punch"):
                punch_count += 1
            elif (tempcard.name == "Vulnerability"):
                vul_count += 1
        power += (0.01*punch_count + 0.15*vul_count + 0.2*wk_count)
    """
    Destroying from hand or discard value as calculated by alg
    """
    if (card.destroy_hand_or_discard > 0):
        wk_count = 0
        punch_count = 0
        vul_count = 0
        for tempcard in own_deck.contents:
            if (tempcard.name == "Weakness"):
                wk_count +=1
            elif (tempcard.name == "Punch"):
                punch_count += 1
            elif (tempcard.name == "Vulnerability"):
                vul_count += 1
        power += card.destroy_hand_or_discard*(0.1*punch_count + 0.2*vul_count + 0.25*wk_count)
    """
    If the card puts a card you buy on top, it's worth 0.5 more, as per the alg
    """
    if (card.puts_on_top):
        power += 0.5
    """
    If something makes you discard a card, it's -0.5 power
    """
    if (card.discard > 0):
        power -= (card.discard*0.5)
    """
    Making your opponents discard is worth +0.5 power, as per the alg. 
    They never have to discard more than 1 in this set.
    """
    if (card.op_discard):
        power += 0.5
    """
    Weaknesses value calculated as per alg and probability of giving them a weakness
    """
    if (card.weakness[0]):
        if (card.weakness[1] == 1):
            num_odds = 0
            for tempcard in opponent_deck.contents:
                if(tempcard.cost%2 == 1):
                    num_odds += 1
            mult = (num_odds/opponent_deck.size)
        elif (card.weakness[1] == 2):
            mult =1
        if (super_deck_size > 8 and main_deck_size > 51):
            power += 2*mult
        elif (super_deck_size > 4 and main_deck_size > 25):
            power += mult
        else:
            power += 0.25*mult
    """
    Defenses are worth +0.75, regardless of defensive effect, as per the alg
    """
    if (card.defense[0]):
        power += 0.75
    """
    We're finally done calculating the card's power!
    """
    return power


"""
Sorts the lineup by vp values (method doesn't really matter, the list will only be at most 8 or 9 cards)
Parameter list:
    lineup: lineup to sort
Return:
    lineup: lineup sorted by vp values
"""
def sort_by_cost(lineup):
    lineup.sort(key=cost) #sorts lineup in ascending order of cost
    return lineup

def sort_by_vp(lineup):
    lineup.sort(key=vp, reverse=True) #sorts lineup in place based on result of vp called on its elements
    return lineup

def sort_by_ratio(lineup):
    lineup.sort(key=vp_ratio, reverse=True) #sorts lineup in place based on result of vp ratio called on its elements
    return lineup

def sort_by_deck_power(lineup):
    lineup.sort(key=deck_power, reverse=True) #sorts lineup in place based on highest value added to deck
    return lineup

def sort_by_dp_ratio(lineup):
    lineup.sort(key=dp_ratio, reverse=True) #sorts lineup in place based on highest value added to deck
    return lineup

    
"""
Checks if it can end the game and returns whether it can and the cards to buy.
Doesn't need kick deck because kicks are worth at most 1 vp
Parameter list:
    power: buying power
    super_villain: super villain card
    super_deck_size: cards left in super deck
    main_deck_size: cards left in main deck
    lineup:cards in lineup sorted by price
Return:
    boolean, cards_to_buy, remaining_power
"""
def check_end_game(power, super_villain_deck, main_deck_size, lineup, kick_deck):
    needed_to_end = main_deck_size + 1  # number of cards to buy from the lineup to end the game
    if needed_to_end > 5: #can't buy enough cards to end game
        return False, []
    power_needed = 0
    lineup = sort_by_cost(lineup)
    for i in range(0, needed_to_end-1):
        power_needed += lineup[i] #minimum power needed to end game
    if power_needed < power: #not enough power
        return False, []
    #calculate max vp by backtracking we know there is at least one solution
    else:
        cost_lineup = sort_by_cost(lineup)
        tobuy = [] #keep track of what you're buying to trigger end of game        
        while (len(tobuy)<needed_to_end): #keeps buying the cheapest card till we have enough to end game
            power -= cost_lineup[0]
            tobuy.append(cost_lineup.pop(0)) #remove card from the lineup and add it to tobuy -- does this work?
        if super_villain_deck.peek().get_cost() <= power: #if we can buy the supervillain, buy it
            power -= super_villain_deck.peek().get_cost()
            tobuy.append(super_villain_deck.peek()) #add the super villain to the cards to buy
            if power <= 1: #buying super spent all power so no need to check other stuff
                return True, tobuy
        lineup.append(kick_deck) #adds the kick deck to stuff we can buy, because we want to optimize buying, kick deck included
        vp_sorted = lineup.copy()
        vp_sorted = sort_by_vp(vp_sorted)
        ratio_sorted = lineup.copy()
        ratio_sorted = sort_by_ratio(ratio_sorted)
        max_vp = max_vp_lineup(power, vp_sorted, ratio_sorted) #set of cards that can be bought that maximize vp
        tobuy.extend(max_vp) #adds the cards found above to the cards to buy. This and the above 4 lines are the same as in buy_cards during almost end game
        return True, tobuy
"""
The big one- buying cards from lineup based on power
"""
def max_power_lineup(power, lineup, lineup1):
    """
    lineup is sorted by power value minus average deck power, highest to lowest
    lineup1 is sorted by power value minus average deck power/cost ratio, highest to lowest
    Both need to be sorted before entered for the function
    """
    cards_to_buy_val = [] #cards bought by sorting by val
    cards_to_buy_ratio = [] #cards bought by sorting by ratio
    val_buy_total = 0 #value of cards bought by sorting by val
    ratio_buy_total = 0 #value of cards bought by sorting by ratio
    leftovers = []
    #Buy in order as we can the highest values
    while len(lineup) > 0:
        if power > lineup[0].get_cost(): #if we can buy the most power
            card = lineup.remove[0] #most power left on lineup
            power -= card.get_cost()
            val_buy_total += card.indeck_power
            cards_to_buy_val.append(card) #add most power to cards to buy
        else: #if we can't buy it, add it to leftovers
            leftovers.append(lineup.remove[0])
    #bought the entire lineup so can just return
    if len(leftovers) < 1:
        return cards_to_buy_val

    while len(lineup1) > 0:
        if power > lineup1[0].get_cost(): #if we can buy the best
            card = lineup1.remove[0] #best ratio left on lineup
            power -= card.get_cost()
            ratio_buy_total += card.indeck_power
            cards_to_buy_ratio.append(card) #add best ratio to cards to buy
        else: #if we can't buy it, add it to leftovers
            leftovers.append(lineup1.remove[0])
    if val_buy_total >= ratio_buy_total: #if we improve the deck average more sorting by val, return that
        return cards_to_buy_val
    else:
        return cards_to_buy_ratio #otherwise return the cards bought by sorting by ratio

"""
Takes the amount of buying power along with the super villain, and the lineup in order by cost
and returns a list of cards to buy based on our algorithm for buying cards.
Parameter list:
    power: buying power from playing cards
    super_villain_deck: current super villain deck
    main_deck: current main deck
    kick_deck: current kick deck
    own_deck: current own deck
    lineup: list of cards available to buy
    opponent_deck: Opponent's deck (for x-ray vision)
    player_power: The superhero/villain the player has
"""
def buy_cards(power, super_villain_deck, main_deck, kick_deck, own_deck, lineup, opponent_deck, player_power):
    #first, we'll play to try to end the game when possible
    cards_to_buy = []
    #(bool can_end_game, cards_to_buy, remaining_power)
    end_game = check_end_game(power, super_villain_deck, main_deck.size, lineup, kick_deck)
    if end_game[0]:
        cards_to_buy.append(end_game[1]) #end_game[1] should be a list
        return cards_to_buy

    #can buy super_villain
    if super_villain_deck.peek().get_cost() <= power:
        power -= super_villain_deck.peek().get_cost()
        cards_to_buy.append(super_villain_deck.peek()) #add the super villain to the cards to buy
        if power <= 1: #buying super spent all power so no need to check other stuff
            return cards_to_buy
    lineup.extend(kick_deck) #from here on in, we need to add kicks to the lineup to consider optimal buy
    #end game coming soon, but cannot end it on our turn
    if super_villain_deck.num_cards <= 3 or main_deck.num_cards <= 15:
        vp_sorted = lineup.copy()
        vp_sorted = sort_by_vp(vp_sorted)
        ratio_sorted = lineup.copy()
        ratio_sorted = sort_by_ratio(ratio_sorted)
        max_vp = max_vp_lineup(power, vp_sorted, ratio_sorted) #set of cards that can be bought that maximize vp
        cards_to_buy.extend(max_vp) #adds the cards found above to the cards to buy
        return cards_to_buy

    power_in_deck = 0 #next few lines calculate average power in deck
    for tempcard in own_deck.contents:
        power_in_deck += get_power(tempcard, own_deck, kick_deck, main_deck.size, opponent_deck, player_power, supervillain_deck.size, True)
    average_power = power_in_deck/(own_deck.size)
    for lineup_card in lineup: #assigns indeck_power for sorting
        lineup_card.indeck_power = get_power(lineup_card, own_deck, kick_deck, main_deck.size, opponent_deck, player_power, supervillain_deck.size, False) - average_power
    power_sorted = lineup.copy()
    power_sorted = sort_by_deck_power(power_sorted)
    dp_ratio_sorted = lineup.copy()
    dp_ratio_sorted = sort_by_dp_ratio(dp_ratio_sorted)
    max_pow = max_power_lineup(power, power_sorted, dp_ratio_sorted)
    cards_to_buy.extend(max_pow)
    return cards_to_buy

