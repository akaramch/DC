from copy import deepcopy

import cards


"""
Finds cards in the lineup to buy with given power that maximizes VP gain
*ONLY CALL WHEN A SOLUTION EXISTS*
Parameter list:
    power: buying power
    lineup: lineup (any sorting)
Return:
    list of cards to buy, power_left
"""
def max_vp_lineup(power, lineup):
    cards_to_buy = []
    leftovers = []
    #Buy in order as we can the highest values
    while len(lineup) > 0:
        if power > lineup[0].get_vp(): #if we can buy the most vp
            card = lineup.remove[0] #most vp left on lineup
            power -= card.get_vp()
            cards_to_buy.append(card) #add most vp to cards to buy
        else: #if we can't buy it, add it to leftovers
            cards_to_buy.append(lineup.remove[0])
    #bought the entire lineup or all but last card which we know isn't worth more
    if len(leftovers) <= 1:
        return cards_to_buy

    index = -1
    #need to check we actually have the top value deepcopy because we'll mess with cards_to_buy
    for card in deepcopy(cards_to_buy):
        index += 1
        leftover_copy = deepcopy(leftovers)
        replacement = []
        new_cost = 0
        new_value = 0
        #add leftovers to replacement as we can
        while new_cost < (power + card.power) and leftover_copy:
            new_card = leftover_copy.remove[0]
            #highest vp we could buy if we got rid of card and bought others
            if power + card.power > new_card.get_vp():
                new_cost += new_card.get_cost()
                new_value += new_card.get_vp()
                replacement.append(new_card)
            else:
                leftover_copy.append(new_card) #put back on end because it's still there
        #switch out to get more vp
        if new_value > card.get_vp:
            cards_to_buy.pop(index)
            leftovers = leftover_copy
            cards_to_buy.extend(replacement)

    return cards_to_buy



"""
Wrapper for card.get_vp for the sort function
"""
def vp(card):
    return card.get_vp()

"""
Sorts the lineup by vp values (method doesn't really matter, the list will only be at most 8 or 9 cards)
Parameter list:
    lineup: lineup to sort
Return:
    lineup: lineup sorted by vp values
"""
def sort_by_vp(lineup):
    lineup.sort(key=vp, reverse=True) #sorts lineup in place based on result of vp called on its elements
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
def check_end_game(power, super_villain, super_deck_size, main_deck_size, lineup):
    cards_to_buy = []
    if super_deck_size == 1 and super_villain.cost < power: #can buy the last super_villain
        cards_to_buy.append(super_villain)
        power -= super_villain.cost #less power to buy other stuff
        max_vp = max_vp_lineup(power, lineup()) #(cards_to_buy, power_left)
        cards_to_buy = cards_to_buy + max_vp[0] #add whatever other cards from lineup maximize power
        power = max_vp[1]
        return True, cards_to_buy, power

    needed_to_end = main_deck_size + 1  # number of cards to buy from the lineup to end the game
    if needed_to_end > 4: #can't buy enough cards to end game
        return False, []
    power_needed = 0
    for i in range(0, needed_to_end-1):
        power_needed += lineup[i] #minimum power needed to end game
    if power_needed < power: #not enough power
        return False, []
    #calculate max vp by backtracking we know there is at least one solution
    else:
        vp_lineup = sort_by_vp(lineup)
        sofar = [] #keep track of current guess
        index = 0
        attempt = 0
        power_left = power #remaining power to buy (can't go below 0 in a solution)
        while True:
            sofar.append(vp_lineup[index])
            power_left -= vp_lineup[index]
            if power_left >= 0:
                if len(sofar) == needed_to_end: #we have our solution
                    return True, sofar, power_left
                else: #we can still potentially build a solution off of this
                    index += 1
                    continue
            else: #current attempt cannot be the solution
                attempt += 1 #track number of attempts
                index = attempt #continue with next attempt ignoring the most costly card
                sofar = [] #reset sofar
                power_left = power #reset power_left
                continue
    return False, [] #should never reach this line, but I'll leave it here just in case

"""
Takes the amount of buying power along with the super villain, and the lineup in order by cost
and returns a list of cards to buy based on our algorithm for buying cards.
Parameter list:
    power: buying power from playing cards
    super_villain: the current card on top of the super villain deck
    super_deck_size: how many cards left in super villain deck
    main_deck_size: how many cards left in main deck
    kick_deck_size: how many kicks left
    lineup: list of cards available to buy
"""
def buy_cards(power, super_villain, super_deck_size, main_deck_size, kick_deck_size, lineup):
    cards_to_buy = []
    #(bool can_end_game, cards_to_buy, remaining_power)
    end_game = check_end_game(power, super_villain, super_deck_size, main_deck_size, lineup)
    if end_game[0]:
        cards_to_buy += end_game[1]
        kicks = end_game[2]//3 #of kicks able to buy with remaining power
        for i in range(1, kicks):
            if kick_deck_size == 0:
                break
            #TODO add kicks to cards to buy (not certain how this will look based on how other stuff is implemented
        return cards_to_buy




    return None