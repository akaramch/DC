#various individual functions for card effects
import pygame
import dc_player
pygame.init()
"""

Takes a player that played the card and the card and executes the effects of the card
Parameter list:
    player: the player who played the card
    card: the card to be played
Return:
    none
"""
# card dimensions
CARD_WIDTH = 123
CARD_HEIGHT = 175
CARD_SPACE = 35
CARD_ZOOM_WIDTH = 316
CARD_ZOOM_HEIGHT = 450
# window dimensions
SCREEN_WIDTH = CARD_WIDTH * 7 + CARD_SPACE * 3 + 100
SCREEN_HEIGHT = CARD_HEIGHT * 3 + CARD_SPACE * 5
SCREEN_NAME = "Prompt"
# background color for the whole screen
GAME_BKG_COLOR = (112, 208, 127)
GAME_FONT = pygame.font.SysFont("ubuntucondensed", 14) # the font to be used to write all things card-related
# clock in the game to time framerate
GAME_CLOCK = pygame.time.Clock()

#draw the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(SCREEN_NAME)


def prompt_player(message, choices, none_choice_possible):
    # draw background for showing the player prompts
    prompt_bkg = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    prompt_bkg.fill(GAME_BKG_COLOR)
    pile_outline = pygame.Surface((CARD_WIDTH + 10, CARD_HEIGHT // 6 * ((SCREEN_HEIGHT - CARD_SPACE * 2) // (CARD_HEIGHT // 6)) + 10))
    pile_interior = pygame.Surface((CARD_WIDTH - 10, CARD_HEIGHT // 6 * ((SCREEN_HEIGHT - CARD_SPACE * 2) // (CARD_HEIGHT // 6)) - 10))
    pile_outline.fill((127, 127, 127))
    pile_interior.fill(GAME_BKG_COLOR)
    pile_outline.blit(pile_interior, (10, 10))
    prompt_bkg.blit(pile_outline, (SCREEN_WIDTH - CARD_WIDTH - CARD_SPACE - 5, CARD_SPACE - 5))
    # scroll buttons for scrolling through the list of choices
    scroll_button_u = pygame.Surface((CARD_WIDTH, CARD_SPACE - 5))
    scroll_button_u_dark = scroll_button_u.copy()
    scroll_button_u.fill(GAME_BKG_COLOR)
    scroll_button_u_dark.fill((GAME_BKG_COLOR[0] // 1.5, GAME_BKG_COLOR[1] // 1.5, GAME_BKG_COLOR[2] // 1.5))
    scroll_button_d = scroll_button_u.copy()
    scroll_button_d_dark = scroll_button_u_dark.copy()
    pygame.draw.polygon(scroll_button_u, (127, 127, 127), [(CARD_WIDTH // 2 - CARD_SPACE // 4, int(CARD_SPACE * (3 / 4))), (CARD_WIDTH // 2, CARD_SPACE // 4), (CARD_WIDTH // 2 + CARD_SPACE // 4, int(CARD_SPACE * (3 / 4)))])
    pygame.draw.polygon(scroll_button_u_dark, (95, 95, 95), [(CARD_WIDTH // 2 - CARD_SPACE // 4, int(CARD_SPACE * (3 / 4))),(CARD_WIDTH // 2, CARD_SPACE // 4), (CARD_WIDTH // 2 + CARD_SPACE // 4, int(CARD_SPACE * (3 / 4)))])
    pygame.draw.polygon(scroll_button_d, (127, 127, 127), [(CARD_WIDTH // 2 - CARD_SPACE // 4, CARD_SPACE // 4), (CARD_WIDTH // 2, int(CARD_SPACE * (3 / 4))), (CARD_WIDTH // 2 + CARD_SPACE // 4, CARD_SPACE // 4)])
    pygame.draw.polygon(scroll_button_d_dark, (95, 95, 95), [(CARD_WIDTH // 2 - CARD_SPACE // 4, CARD_SPACE // 4), (CARD_WIDTH // 2, int(CARD_SPACE * (3 / 4))), (CARD_WIDTH // 2 + CARD_SPACE // 4, CARD_SPACE // 4)])
    GAME_FONT.set_underline(True)
    choose_none = GAME_FONT.render("None", True, (0, 0, 0), GAME_BKG_COLOR), (CARD_SPACE, CARD_SPACE - GAME_FONT.get_height())
    GAME_FONT.set_underline(False)
    # a piece to cover up the overflowing cards
    cover = pygame.Surface((CARD_WIDTH, CARD_HEIGHT))
    cover.fill(GAME_BKG_COLOR)
    cover_line = pygame.Surface((CARD_WIDTH, 5))
    cover_line.fill((127, 127, 127))
    cover.blit(cover_line, (0, 0))
    #print(message)
    click = False
    scroll = 0  # how far the pile is scrolled
    
    #when card is selected, the function returns
    while True:
        mouse_pos = pygame.mouse.get_pos()
        # click should only be true on the frame when the button is pressed
        if click:
            click = False
        for event in pygame.event.get():  # evaluate all the current events
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True
        # draw the background first
        prompt_bkg.blit(GAME_FONT.render(message, True, (0, 0, 0), GAME_BKG_COLOR), (SCREEN_WIDTH // 2 - len(message) * 3, CARD_SPACE - GAME_FONT.get_height() - 6))
        screen.blit(prompt_bkg, (0, 0))
        # draw the choose_none button and make it usable
        if none_choice_possible:
            screen.blit(choose_none[0], (SCREEN_WIDTH - CARD_SPACE * 2 - CARD_WIDTH - choose_none[0].get_width(), CARD_SPACE * 2 + CARD_ZOOM_HEIGHT - GAME_FONT.get_height()))# is the mouse on the None button
            if click and SCREEN_WIDTH - CARD_SPACE * 2 - CARD_WIDTH - choose_none[0].get_width() < mouse_pos[0] < SCREEN_WIDTH - CARD_SPACE * 2 - CARD_WIDTH and CARD_SPACE * 2 + CARD_ZOOM_HEIGHT - GAME_FONT.get_height() < mouse_pos[1] < CARD_SPACE * 2 + CARD_ZOOM_HEIGHT:
                return None
        # draw the list of cards to choose from
        for i in range(scroll, len(choices)):
            screen.blit(choices[i].img, (SCREEN_WIDTH - CARD_WIDTH - CARD_SPACE, CARD_SPACE + CARD_HEIGHT // 6 * (i - scroll)))
        # cover up the cards that overflow over the list boundary
        screen.blit(cover, (SCREEN_WIDTH - CARD_SPACE - CARD_WIDTH, CARD_SPACE + pile_outline.get_height() - 10))
        # draw the scroll buttons light or dark depending on whether the mouse is over them and allow the user to use them
        # mouse is over the scroll up button (and there's more up to scroll)
        if scroll > 0 and SCREEN_WIDTH - CARD_WIDTH - CARD_SPACE < mouse_pos[0] < SCREEN_WIDTH - CARD_SPACE and 0 < mouse_pos[1] < CARD_SPACE - 5:
            screen.blit(scroll_button_u_dark, (SCREEN_WIDTH - CARD_WIDTH - CARD_SPACE, 0))
            screen.blit(scroll_button_d, (SCREEN_WIDTH - CARD_WIDTH - CARD_SPACE, CARD_SPACE - 5 + pile_outline.get_height()))
            if click:
                scroll -= 1
        # mouse is over the scroll down button (and there's more down to scroll)
        elif scroll < len(choices) - (pile_outline.get_height() // (CARD_HEIGHT // 6)) + 5 and SCREEN_WIDTH - CARD_WIDTH - CARD_SPACE < mouse_pos[0] < SCREEN_WIDTH - CARD_SPACE and CARD_SPACE - 5 + pile_outline.get_height() < mouse_pos[1] < CARD_SPACE * 2 - 10 + pile_outline.get_height():
            screen.blit(scroll_button_u, (SCREEN_WIDTH - CARD_WIDTH - CARD_SPACE, 0))
            screen.blit(scroll_button_d_dark, (SCREEN_WIDTH - CARD_WIDTH - CARD_SPACE, CARD_SPACE - 5 + pile_outline.get_height()))
            if click:
                scroll += 1
        # mouse is elsewhere
        else:
            screen.blit(scroll_button_u, (SCREEN_WIDTH - CARD_WIDTH - CARD_SPACE, 0))
            screen.blit(scroll_button_d, (SCREEN_WIDTH - CARD_WIDTH - CARD_SPACE, CARD_SPACE - 5 + pile_outline.get_height()))
        # is the mouse on a card in the list of choices
        if SCREEN_WIDTH - CARD_WIDTH - CARD_SPACE < mouse_pos[0] < SCREEN_WIDTH - CARD_SPACE and CARD_SPACE < mouse_pos[1] < CARD_SPACE + min((len(choices) - 1) * (CARD_HEIGHT // 6) + CARD_HEIGHT, pile_outline.get_height() - 10):
            i = min(scroll + (mouse_pos[1] - CARD_SPACE) // (CARD_HEIGHT // 6), len(choices) - 1)
            screen.blit(choices[i].zoom(), (SCREEN_WIDTH - CARD_WIDTH - CARD_ZOOM_WIDTH - CARD_SPACE * 2, CARD_SPACE - 5))
            if click:
                return choices[i]
        pygame.display.flip()


# the prompt for Two-Face
def prompt_player_even_odd(message):
    prompt_bkg = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    prompt_bkg.fill(GAME_BKG_COLOR)
    pygame.draw.circle(prompt_bkg, (127, 127, 127), (CARD_WIDTH * 3, CARD_HEIGHT + CARD_SPACE * 2), CARD_WIDTH // 2, 5)
    pygame.draw.circle(prompt_bkg, (127, 127, 127), (SCREEN_WIDTH - CARD_WIDTH * 3, CARD_HEIGHT + CARD_SPACE * 2), CARD_WIDTH // 2, 5)
    GAME_FONT.set_underline(True)
    prompt_bkg.blit(GAME_FONT.render("EVEN", True, (0, 0, 0), GAME_BKG_COLOR), (CARD_WIDTH * 3 - 13, CARD_HEIGHT + CARD_SPACE * 2 - GAME_FONT.get_height() // 2))
    prompt_bkg.blit(GAME_FONT.render("ODD", True, (0, 0, 0), GAME_BKG_COLOR), (SCREEN_WIDTH - CARD_WIDTH * 3 - 11, CARD_HEIGHT + CARD_SPACE * 2 - GAME_FONT.get_height() // 2))
    prompt_bkg.blit(GAME_FONT.render(message, True, (0, 0, 0), GAME_BKG_COLOR), (CARD_SPACE, CARD_SPACE))
    GAME_FONT.set_underline(False)
    click = False
    # function returns when the user clicks on one of them
    while True:
        mouse_pos = pygame.mouse.get_pos()
        # click should only be true on the frame when the button is pressed
        if click:
            click = False
        for event in pygame.event.get():  # evaluate all the current events
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True
        
        screen.blit(prompt_bkg, (0, 0))
        # is the mouse on the EVEN button
        if (mouse_pos[0] - (CARD_WIDTH * 3)) ** 2 + (mouse_pos[1] - (CARD_HEIGHT + CARD_SPACE * 2)) ** 2 < (CARD_WIDTH // 2) ** 2:
            if click:
                return 0
        # is the mouse on the ODD button
        elif (mouse_pos[0] - (SCREEN_WIDTH - CARD_WIDTH * 3)) ** 2 + (mouse_pos[1] - (CARD_HEIGHT + CARD_SPACE * 2)) ** 2 < (CARD_WIDTH // 2) ** 2:
            if click:
                return 1
        
        pygame.display.flip()
        


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

    #check black adam effects
    if not player.black_adam_effect[0]:
        if card.type == "Hero":
            power_bonus += 2

    if not player.black_adam_effect[1]:
        if card.type == "Villain":
            power_bonus += 2

    if not player.black_adam_effect[2]:
        if card.type == "Equipment":
            power_bonus += 2

    if not player.black_adam_effect[3]:
        if card.type == "Starter":
            power_bonus += 2

    if not player.black_adam_effect[4]:
        if card.type == "Power":
            power_bonus += 2

    power_bonus_type = card.power[1] # sig
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
            num_heroes = 0  # how may heroes in our played
            for card in player.own_deck.played:
                if card.get_type() == "Hero":
                    num_heroes += 1
            if num_heroes > 1:
                power_bonus += 3
            else:
                player.winged_warrior_effect = True

        elif power_bonus_type == 4: #hawkgirl
            # for each hero in discard, +1
            for card in player.own_deck.discard:
                if card.type == "Hero":
                    power_bonus += 1


        elif power_bonus_type == 5: #king of atlantis
            #+2 Power if you destroy a card in discard pile
            if len(player.own_deck.discard) != 0: #if we have discard cards
                selection = prompt_player("You may pick a card in your discard to destroy for +2 power. Click \"None\" to destroy nothing.", player.own_deck.discard, True)
                if selection: #did the player select something?
                    power_bonus += 2 #give bonus
                    player.own_deck.destroy_from_discard(selection) #destroy the card

        elif power_bonus_type == 6: #red lantern corps
            selection = None
            #+2 additional power if you destroy a card in hand
            if len(player.own_deck.hand) != 0: #if there's a card in hand
                #prompt the player with the choice
                selection = prompt_player("You may pick a card in your hand to destroy for +2 power. Click \"None\" to destroy nothing.", player.own_deck.hand, True)
            if selection:
                power_bonus += 2 #give bonus
                player.own_deck.destroy_from_hand(selection) #destroy the card

        elif power_bonus_type == 7: #killer croc
            #+1 if play/have played another Villain this turn
            # check if played already
            num_villains = 0  # how many villains did we find in our played
            for card in player.own_deck.played:
                if card.get_type() == "Villain":
                    num_villains += 1

            if num_villains > 1:
                power_bonus += 1
            else:
                player.killer_croc_effect = True

    #add calculated bonus power to player power
    player.power += power_bonus

    #do any drawing for the card
    draw = card.draw[0]

    draw_bonus = 0
    draw_bonus_type = card.draw[1]
    if draw_bonus_type != 0:
        if draw_bonus_type == 1: #two face
            evenodd = prompt_player_even_odd("Choose even or odd")
            if player.own_deck.peek().cost % 2 == evenodd:
                player.own_deck.draw()
            else:
                player.own_deck.undrawn_top_to_discard()

    #add draw bonus
    draw += draw_bonus
    #draw the correct number of cards
    for i in range(0, draw):
        player.own_deck.draw()


    #cards that can destroy top of deck
    top_destroy = card.destroy_top[0]
    if top_destroy: #is this a top destroy card?
        top_destroy_option = card.destroy_top[1]
        if top_destroy_option == 1: #nth metal
            if len(player.own_deck.undrawn) == 0: #if undrawn is empty, we need to reshuffle
                player.own_deck.refill_deck()
            selection = prompt_player("This is the top card of your deck. If you wish to destroy it, click the card. Otherwise, click \"None.\"", [player.own_deck.peek()], True) #player.own_deck.peek is the top card of their deck
            if selection: #if they decided to destroy
                player.own_deck.destroy_from_deck(selection) #remove the card from the deck
        if top_destroy_option == 2: #jervis tetch
            if len(player.own_deck.undrawn) == 0: #if undrawn is empty, we need to reshuffle
                player.own_deck.refill_deck()
            selection = prompt_player("This is the top card of your deck. If you wish to destroy it, click the card. Otherwise, click \"None\" and it will be discarded.", [player.own_deck.peek()], True)  # player.own_deck.peek is the top card of their deck
            if selection:  # if they decided to destroy
                player.own_deck.destroy_from_deck(selection)  # remove the card from the deck
            else: #if they didn't destroy
                player.own_deck.undrawn_top_to_discard() #put the card in discard

    if card.name == "Soultaker Sword":
        if not (len(player.own_deck.hand) == 0): #make sure there is a card in the hand
            selection = prompt_player("You may pick a card in your hand to destroy. Click \"None\" to destroy nothing.", player.own_deck.hand, True)
            if selection: #if the player chose one
                player.own_deck.destroy_from_hand(selection) #destroy it

    if card.destroy_hand_or_discard == 1: #heat vision
        selection_discard = prompt_player("Select a card to destroy from your discard pile. If you wish to destroy nothing, or to instead destroy a card from your hand, click \"None.\"", player.own_deck.discard, True)
        if not selection_discard: #if not check if destroy from hand
            selection_hand = prompt_player("You may pick a card in your hand to destroy. Click \"none\" to destroy nothing.", player.own_deck.hand, True)
            if selection_hand: #if destroy from hand
                player.own_deck.destroy_from_hand(selection_hand)
        else: #select destroy from discard
            player.own_deck.destroy_from_discard(selection_discard)

    if card.destroy_hand_or_discard == 2: #lobo
        selection1_discard = prompt_player("Select a card to destroy from your discard pile. If you wish to destroy nothing, or to instead destroy a card from your hand, click \"None.\"", player.own_deck.discard, True) #check if first destroyed from discard
        selection1_hand = None
        if not selection1_discard: #if not check if they want to destroy from hand
            selection1_hand = prompt_player("Select a card to destroy from your hand. If you wish to destroy nothing, click \"None.\"", player.own_deck.hand, True)
            if selection1_hand: #if they selected to destroy from hand
                player.own_deck.destroy_from_hand(selection1_hand)
        else: #selection 1 destroy from discard
            player.own_deck.destroy_from_discard(selection1_discard)

        if not ((selection1_discard is None) and (selection1_hand is None)): #if the player selected one to destroy, ask again
            selection2_discard = prompt_player("Select a card to destroy from your discard pile. If you wish to destroy nothing, or to instead destroy a card from your hand, click \"None.\"", player.own_deck.discard, True)  # check if first destroyed from discard
            if not selection2_discard:  # if not check if they want to destroy from hand
                selection2_hand = prompt_player("Select a card to destroy from your hand. If you wish to destroy nothing, click \"None.\"", player.own_deck.hand, True)
                if selection2_hand:  # if they selected to destroy from hand
                    player.own_deck.destroy_from_hand(selection2_hand)
            else:  # selection 2 destroy from discard
                player.own_deck.destroy_from_discard(selection2_discard)

    if card.discard == 1: #the flash(discard)
        #draw 3, discard 1 (draw is implemented above)
        selection = prompt_player("Select a card in your hand to discard.", player.own_deck.hand, False)
        # can't move over because selection isn't a hand index, so we will destroy it and add a new copy to discard
        player.own_deck.destroy_from_hand(selection)
        player.gain_card_discard(selection)
           
    # custom == 1: jonn jonzz handled in game.py
        
    # custom == 2: shazam! superpower handled in game.py
        
    # custom == 3: white lantern power battery handled in game.py
        
    # custom == 4: xray vision handled in game.py
        
    # custom == 5:  Supergirl handled in game.py
        
    if card.custom == 6: #Parallax
        player.power *= 2
        
    #custom == 7:  Trigon handled in game.py
        
    if card.custom == 8: #Graves
        player.power += 4
        if len(player.own_deck.discard) != 0:
            selection = prompt_player("Pick a card from your discard to put on top of your deck. If you don't want to move a card to the top of your deck, click None", player.own_deck.discard, True)
            if selection: #if the player selected one
                player.own_deck.discard_to_top(selection) #move it to top
            
    if card.custom == 9: #Nekron
        cards_to_draw = 0
        selection1_discard = prompt_player("Select a card to destroy from discard. If you wish to not destroy, or instead destroy a card from your hand, click None.", player.own_deck.discard, True) #check if first destroyed from discard
        selection1_hand = None
        if not selection1_discard: #if not check if they want to destroy from hand
            selection1_hand = prompt_player("Select a card to destroy from hand. If you wish to not destroy, click None.", player.own_deck.hand, True)
            if selection1_hand: #if they selected to destroy from hand
                player.own_deck.destroy_from_hand(selection1_hand)
            if (selection1_discard or selection1_hand):
                cards_to_draw += 1
        else: #selection 1 destroy from discard
            player.own_deck.destroy_from_discard(selection1_discard)
            cards_to_draw += 1

        if not ((selection1_discard is None) and (selection1_hand is None)): #if the player selected one to destroy, ask again
            selection2_hand = None
            selection2_discard = prompt_player("Select a card to destroy from discard. If you wish to not destroy, or instead destroy a card from your hand, click None.", player.own_deck.discard, True)  # check if first destroyed from discard
            if not selection2_discard:  # if not check if they want to destroy from hand
                selection2_hand = prompt_player("Select a card to destroy from hand. If you wish to not destroy, click None.", player.own_deck.hand, True)
                if selection2_hand:  # if they selected to destroy from hand
                    player.own_deck.destroy_from_hand(selection2_hand)
                if (selection2_discard or selection2_hand):
                    cards_to_draw += 1
            else:  # selection 2 destroy from discard
                player.own_deck.destroy_from_discard(selection2_discard)
                cards_to_draw += 1
                
            if not ((selection2_discard is None) and (selection2_hand is None)): #if the player selected one to destroy, ask again
                selection3_hand = None
                selection3_discard = prompt_player("Select a card to destroy from discard. If you wish to not destroy, or instead destroy a card from your hand, click None.", player.own_deck.discard, True)  # check if first destroyed from discard
                if not selection3_discard:  # if not check if they want to destroy from hand
                    selection3_hand = prompt_player("Select a card to destroy from hand. If you wish to not destroy, click None.", player.own_deck.hand, True)
                    if selection3_hand:  # if they selected to destroy from hand
                        player.own_deck.destroy_from_hand(selection3_hand)
                    if (selection1_discard or selection1_hand):
                       cards_to_draw += 1
                else:  # selection 2 destroy from discard
                    player.own_deck.destroy_from_discard(selection3_discard)
                    cards_to_draw += 1
        for i in range(cards_to_draw):
            if len(player.own_deck.undrawn) == 0: #if undrawn is empty, we need to reshuffle
                player.own_deck.refill_deck()
                if len(player.own_deck.undrawn) == 0:
                    break
            player.own_deck.draw()
        
    # custom = 10:  Bart Allen handled in game.py
    
        
    if card.custom == 11: #Black Adam
        found_hero = False
        found_villain = False
        found_equipment = False
        found_starter = False
        found_power = False
        for card in player.own_deck.played:
            card_type = card.get_type()
            if card_type == "Hero" and not found_hero:
                player.power += 2
                found_hero = True
            elif card_type == "Villain" and not found_villain:
                player.power += 2
                found_villain = True
            elif card_type == "Equipment" and not found_equipment:
                player.power += 2
                found_equipment = True
            elif card_type == "Starter" and not found_starter:
                player.power += 2
                found_starter = True
            elif card_type == "Power" and not found_power:
                player.power += 2
                found_power = True
        player.black_adam_effect = (found_hero, found_villain, found_equipment, found_starter, found_power) #set the effect if we didn't find everything
        
    if card.custom == 12: #Hel
        value_drawn = 0
        while value_drawn < 7:
            
            if len(player.own_deck.undrawn) == 0: #if undrawn is empty, we need to reshuffle
                player.own_deck.refill_deck()
                if len(player.own_deck.undrawn) == 0:
                    break
            next_card = player.own_deck.peek()
            next_card_cost = next_card.get_cost()
            player.own_deck.draw()           
            value_drawn += next_card_cost
            
    if card.custom == 13: #Arkillo
        arraySize = len(player.own_deck.discard)
        i = 0
        while i < arraySize:
            if player.own_deck.discard[i].get_type() == "Equipment":
                player.own_deck.discard_to_hand(player.own_deck.discard[i])
                arraySize -= 1
            else:
                i += 1

