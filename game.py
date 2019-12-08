"""
Holds the working version of the GUI including the game loop
and also the Card class and all the instantiantions and lists of cards
"""

import pygame
pygame.init()
import dc_player
import deck
import card_effect
import buy_cards
import random

# card dimensions
CARD_WIDTH = 123
CARD_HEIGHT = 175
CARD_SPACE = 35
CARD_ZOOM_WIDTH = 316
CARD_ZOOM_HEIGHT = 450
# window dimensions
SCREEN_WIDTH = CARD_WIDTH * 7 + CARD_SPACE * 3 + 100
SCREEN_HEIGHT = CARD_HEIGHT * 3 + CARD_SPACE * 5
SCREEN_NAME = "DC Game"
# background color for the whole screen
GAME_BKG_COLOR = (112, 208, 127)
GAME_FONT = pygame.font.SysFont("ubuntucondensed", 14) # the font to be used to write all things card-related
# clock in the game to time framerate
GAME_CLOCK = pygame.time.Clock()

"""
Card class
__init__(image_name, name, type, cost, power, draw, vp, text): loads card face image and info namedtuple
get_width(), get_height(): get width and height of card face image
move(dx, dy): move the card by that distance
inform(): returns a text pygame.surface that shows the info namedtuple in text form
"""
class Card:

    def __init__(self, image_name, type, cost, vp=0, text="", name="", custom=0, power=(0,0), draw=(0,0), destroy_top=(False,0), destroy_hand=0, destroy_discard=0, destroy_hand_or_discard=0, puts_on_top=False, discard=0, op_discard=0, weakness=(False,0), defense=(False, 0), first_appearance=0):
        """
        takes a file path for an image that will be the face of the card
        and all of the fields that the card needs to know about
        Required fields are image_name, type, cost
        """
        self.img_name = image_name
        self.img = pygame.image.load(image_name[:-4] + "small.jpg") # the image corresponding to the small card
        self.name = name # the card's name
        self.type = type # the type of the card, e.g. "starter" or "superpower"
        self.cost = cost # cost to buy the card
        self.vp = vp # victory point value of the card
        self.text = text # text of the card
        self.custom = custom # custom "value" of the card
        self.power = power # tuple of (unconditional power generated, total power according to the algorithm)
        self.draw = draw # tuple of (unconditional cards drawn, int corresponding to type of conditional draw)
        self.destroy_top = destroy_top # tuple of (T/F this card destroys the top card of the library, where the card goes if it isn't destroyed (1 for discard, 2 for back on top))
        self.destroy_hand = destroy_hand # number of cards this card can destroy from your hand
        self.destroy_discard = destroy_discard # number of cards this card can destroy from your discard
        self.destroy_hand_or_discard = destroy_hand_or_discard # number of cards this card can destroy from either your hand or your discard
        self.puts_on_top = puts_on_top # T/F whether this card lets you put a card you buy on top of your deck
        self.discard = discard # number of cards this card makes you discard
        self.op_discard = op_discard # number of cards this card makes each opponent discard
        self.weakness = weakness # tuple of (T/F this card gives an opponent a weakness, code number for when that happens)
        self.defense = defense # tuple of (T/F this card is a defense, code number for what it does)
        self.first_appearance = first_appearance # an index into a hardcoded list of supervillain first-appearance attacks
        self.pos = (0, 0) # the coordinates of the top left corner of the card
    
    def __str__(self):
        return self.name

    def get_width(self):
        return self.img.get_width()

    def get_height(self):
        return self.img.get_height()

    def move(self, dx, dy):
        """move the card to new coordinates on the screen"""
        self.pos = (self.pos[0] + dx, self.pos[1] + dy)

    def zoom(self):
        # load the big image and return it to blit to the screen where big images go
        return pygame.image.load(self.img_name)
    
    def get_name(self):
        return self.name

    def get_type(self):
        return self.type

    def get_cost(self):
        return self.cost

    def get_power(self):
        return self.power

    def get_draw(self):
        return self.draw

    def get_vp(self):
        return self.vp

    def get_text(self):
        return self.text


"""
DC Card List
A namedtuple to hold the card's information
ORDER: Name, Type, Cost, Power, Draw, VP, Text
TO COPY:  = Card("cardimgs/imagename.jpg", card_info("N", "T", "C", "P", "D", "V", ""))
"""

# STARTERS, WEAKNESSES, KICKS (oh my)
Punch = Card("cardimgs/punch.jpg", type="Starter", cost=0, power=(1,0), name="Punch", text="+1 Power.")
Vulnerability = Card("cardimgs/vulnerability.jpg", type="Starter", cost=0, name="Vulnerability")
Weakness = Card("cardimgs/weakness.jpg", cost=0, vp=-1, name="Weakness", type="Weakness", text="Weakness cards reduce your score at the end of the game.") # HOWEVER MANY

StartingPlayerDeck = [Vulnerability] * 3 + [Punch] * 7

StartingMainDeck = [] # will be used to build the card list for the main deck

"""  DEFAULT CARD
 = Card("cardimgs/imagename.jpg", cost=, power=(,), name="", vp=, type="SuperVillain", text="") # 
"""

# EQUIPMENT
EquipmentList = []

Aquamans_Trident = Card("cardimgs/aquamanstrident.jpg", cost=3, power=(2,0), puts_on_top=True, name="Aquaman's Trident", type="Equipment", vp=1, text="+2 Power. You may put any one card you buy or gain this turn on top of your deck.") # 3
Batarang = Card("cardimgs/batarang.jpg", cost=2, power=(2,0), name="Batarang", vp=1, type="Equipment", text="+2 Power.") # 2
Soultaker_Sword = Card("cardimgs/soultakersword.jpg", cost=4, power=(2,0), name="Soultaker Sword", vp=1, type="Equipment", text="+2 Power. You may destroy a card in your hand.", destroy_hand=1) # 3
Legion_Flight_Ring = Card("cardimgs/legionflightring.jpg", cost=2, name="Legion Flight Ring", vp=1, type="Equipment", text="Draw a card.", draw=(1,0)) # 2
Lasso_of_Truth = Card("cardimgs/lassooftruth.jpg", cost=2, power=(1,0), name="Lasso of Truth", vp=1, type="Equipment", defense=(True,1), text="+1 Power. Defense: You may discard this card to avoid an Attack. If you do, draw a card.") # 2
Power_Ring = Card("cardimgs/powerring.jpg", cost=3, power=(2,1), name="Power Ring", vp=1, type="Equipment", text="+2 Power. Reveal the top card of your deck. If its cost is 1 or greater, additional +1 Power.") # 3
Nth_Metal = Card("cardimgs/nthmetal.jpg", cost=3, power=(1,0), name="Nth Metal", vp=1, type="Equipment", text="+1 Power. Look at the top card of your deck. You may destroy it.", destroy_top=(True,1)) # 3
White_Lantern_Power_Battery = Card("cardimgs/whitelanternpowerbattery.jpg", cost=7, name="White Lantern Power Battery", vp=2, type="Equipment", text="Gain any card from the Line-Up and put it on top of your deck.") # 1

EquipmentList.append(Aquamans_Trident)
EquipmentList.append(Batarang)
EquipmentList.append(Lasso_of_Truth)
EquipmentList.append(Legion_Flight_Ring)
EquipmentList.append(Nth_Metal)
EquipmentList.append(Power_Ring)
EquipmentList.append(Soultaker_Sword)
EquipmentList.append(White_Lantern_Power_Battery)

# add equipment to main deck
StartingMainDeck += [Aquamans_Trident] * 3
StartingMainDeck += [Batarang] * 2
StartingMainDeck += [Lasso_of_Truth] * 2
StartingMainDeck += [Legion_Flight_Ring] * 2
StartingMainDeck += [Nth_Metal] * 3
StartingMainDeck += [Power_Ring] * 3
StartingMainDeck += [Soultaker_Sword] * 3
StartingMainDeck += [White_Lantern_Power_Battery] * 1

# SUPER POWERS
PowerList = []

Kick = Card("cardimgs/kick.jpg", cost=3, power=(2,0), name="Kick", vp=1, type="Power", text="+2 Power.") #HOWEVER MANY
Shazam = Card("cardimgs/shazam.jpg", cost=7, name="Shazam!", type="Power", text="Reveal and play the top card of the main deck, then return it to the top of the main deck.", custom=2) #1
Super_Strength = Card("cardimgs/superstrength.jpg", cost=7, power=(5,0), name="Super Strength", vp=2, type="Power", text="+5 Power.") #2
Starbolt  = Card("cardimgs/starbolt.jpg", cost=5, power=(2,2), name="Starbolt", vp=1, type="Power", text="+1 additional Power for each Super Power in your discard pile.") #3
Bulletproof = Card("cardimgs/bulletproof.jpg", cost=4, power=(2,0), name="Bulletproof", vp=1, type="Power", defense=(True,2), text="+1 Power\nDefense: You may discard this card to avoid an Attack. If you do, draw a card and you may destroy a card in your discard pile.") #2
Giant_Growth = Card("cardimgs/giantgrowth.jpg", cost=2, power=(2,0), name="Giant Growth", vp=1, type="Power", text="+2 Power.") #2
X_Ray_Vision = Card("cardimgs/xrayvision.jpg", cost=3, name="X-Ray Vision", vp=1, type="Power", custom=4, text="Each foe reveals the top card of their deck. Choose a non-Location card revealed this way, play it, then return it to the top of its owner's deck.") #1
Ultra_Strength = Card("cardimgs/ultrastrength.jpg", cost=9, power=(3,0), name="Ultra Strength", vp=3, draw=(2,0), type="Power", text="+3 Power and draw 2 cards.") #1
Heat_Vision = Card("cardimgs/heatvision.jpg", cost=6, power=(3,0), name="Heat Vision", vp=2, type="Power", destroy_hand_or_discard=1, text="+3 Power and you may destroy a card in your hand or discard pile.") #3

PowerList.append(Bulletproof)
PowerList.append(Giant_Growth)
PowerList.append(Heat_Vision)
PowerList.append(Kick)
PowerList.append(Shazam)
PowerList.append(Starbolt)
PowerList.append(Super_Strength)
PowerList.append(Ultra_Strength)
PowerList.append(X_Ray_Vision)

# add non-kick powers to main deck list
StartingMainDeck += [Bulletproof] * 2
StartingMainDeck += [Giant_Growth] * 2
StartingMainDeck += [Heat_Vision] * 2 # changed
StartingMainDeck += [Shazam] * 1
StartingMainDeck += [Starbolt] * 3
StartingMainDeck += [Super_Strength] * 2
StartingMainDeck += [Ultra_Strength] * 1
StartingMainDeck += [X_Ray_Vision] * 3

# HEROES
HeroList = []

Raven = Card("cardimgs/raven.jpg", cost=3, power=(1,0), name="Raven", draw=(1,0), vp=1, type="Hero", text="+1 Power and draw a card.") # 3
Catwoman = Card("cardimgs/catwoman.jpg", cost=2, power=(2,0), name="Catwoman", vp=1, type="Hero", text="+2 Power.") # 2
Katana = Card("cardimgs/katana.jpg", cost=2, power=(1,0), name="Katana", vp=1, type="Hero", defense=(True,1), text="+1 Power.\nDefense: You may discard this card to avoid an Attack. If you do, draw a card.") # 2
Winged_Warrior = Card("cardimgs/wingedwarrior.jpg", cost=6, power=(2,3), name="Winged Warrior", vp=2, type="Hero", text="+2 Power.\nIf you play or have played another Hero this turn, additional +3 Power.") # 1
Power_Girl = Card("cardimgs/powergirl.jpg", cost=5, power=(3,0), name="Power Girl", vp=2, type="Hero", text="+3 Power.") # 3
Hawkgirl = Card("cardimgs/hawkgirl.jpg", cost=2, power=(1,4), name="Hawkgirl", vp=1, type="Hero", text="+1 Power and and additional +1 Power for each Hero in your discard pile.") # 2
Kid_Flash = Card("cardimgs/kidflash.jpg", cost=2, name="Kid Flash", vp=1, draw=(1,0), type="Hero", text="Draw a card.") # 2
Supergirl = Card("cardimgs/supergirl.jpg", cost=4, name="Supergirl", vp=1, type="Hero", custom=5, text="You may put a Kick from the Kick stack into your hand.") # 2
Jonn_Jonzz = Card("cardimgs/jonnjonzz.jpg", cost=6, name="J'onn J'onzz", vp=2, custom=1, type="Hero", text="Play the top card of the Super-Villain stack, then return it to the top of the stack.") # 1
The_Fastest_Man_Alive = Card("cardimgs/thefastestmanalive.jpg", cost=5, name="The Fastest Man Alive", vp=1, draw=(2,0), type="Hero", text="Draw two cards.") # 1
King_of_Atlantis = Card("cardimgs/kingofatlantis.jpg", cost=5, power=(1,5), name="King of Atlantis", vp=1, destroy_discard=1, type="Hero", text="You may destroy a card in your discard pile. If you do, +3 Power. Otherwise, +1 Power.") # 1

HeroList.append(Catwoman)
HeroList.append(Hawkgirl)
HeroList.append(Jonn_Jonzz)
HeroList.append(Katana)
HeroList.append(Kid_Flash)
HeroList.append(King_of_Atlantis)
HeroList.append(Power_Girl)
HeroList.append(Raven)
HeroList.append(Supergirl)
HeroList.append(The_Fastest_Man_Alive)
HeroList.append(Winged_Warrior)

# add heroes to main deck list
StartingMainDeck += [Catwoman] * 2
StartingMainDeck += [Hawkgirl] * 2
StartingMainDeck += [Jonn_Jonzz] * 1
StartingMainDeck += [Katana] * 2
StartingMainDeck += [Kid_Flash] * 2
StartingMainDeck += [King_of_Atlantis] * 1
StartingMainDeck += [Power_Girl] * 3
StartingMainDeck += [Raven] * 3
StartingMainDeck += [Supergirl] * 2
StartingMainDeck += [The_Fastest_Man_Alive] * 1
StartingMainDeck += [Winged_Warrior] * 1

# VILLAINS
VillainList = []

Johnny_Quick = Card("cardimgs/johnnyquick.jpg", cost=2, draw=(1,0), name="Johnny Quick", vp=1, type="Villain", text="Draw a card.") # 2
Bane = Card("cardimgs/bane.jpg", cost=4, power=(2,0), name="Bane", vp=1, op_discard=1, type="Villain", text="+2 Power.\nAttack: Each foe chooses and discards a card.") # UNDECIDED NUMBER
Mr_Zsasz = Card("cardimgs/mrzsasz.jpg", cost=3, power=(2,0), name="Mr. Zsasz", vp=1, weakness=(True,1), type="Villain", text="+2 Power.\nAttack: Each foe reveals the top card of his deck. If its cost is odd, that player gains a Weakness.") # UNDECIDED NUMBER
Scarecrow = Card("cardimgs/scarecrow.jpg", cost=5, power=(2,0), name="Scarecrow", vp=1, weakness=(True,2), type="Villain", text="+2 Power.\nAttack: Each foe gains a Weakness.") # UNDECIDED NUMBER
Doomsday = Card("cardimgs/doomsday.jpg", cost=6, power=(4,0), name="Doomsday", vp=2, type="Villain", text="+4 Power.") # 2
Red_Lantern_Corps = Card("cardimgs/redlanterncorps.jpg", cost=5, power=(1,6), name="Red Lantern Corps", vp=1, type="Villain", destroy_hand=1, text="+1 Power. You may destroy a card in your hand. If you do, additional +2 Power.") # 2
Lobo = Card("cardimgs/lobo.jpg", cost=7, power=(3,0), name="Lobo", vp=2, type="Villain", destroy_hand_or_discard=2, text="+3 Power. You may destroy up to two cards in your hand and/or discard pile.") # 1
Gorilla_Grodd = Card("cardimgs/gorillagrodd.jpg", cost=5, power=(3,0), name="Gorilla Grodd", vp=2, type="Villain", text="+3 Power.") # 2
Jervis_Tetch = Card("cardimgs/jervistetch.jpg", cost=3, power=(1,0), name="Jervis Tetch", vp=1, type="Villain", destroy_top=(True,2), text="+1 Power. Look at the top card of your deck. Destroy it or discard it.") # 2
Killer_Croc = Card("cardimgs/killercroc.jpg", cost=4, power=(2,7), name="Killer Croc", vp=1, type="Villain", text="+2 Power. If you play or have played another Villain this turn, additional +1 Power.") # 2
Two_Face = Card("cardimgs/twoface.jpg", cost=2, power=(1,0), name="Two-Face", vp=1, type="Villain", draw=(0,1), text="+1 Power. Choose even or odd, then reveal the top card of your deck. If its cost matches your choice, draw it. If not, discard it.") # 2

VillainList.append(Bane)
VillainList.append(Doomsday)
VillainList.append(Gorilla_Grodd)
VillainList.append(Jervis_Tetch)
VillainList.append(Johnny_Quick)
VillainList.append(Killer_Croc)
VillainList.append(Lobo)
VillainList.append(Mr_Zsasz)
VillainList.append(Red_Lantern_Corps)
VillainList.append(Scarecrow)
VillainList.append(Two_Face)

# add villains to main deck list
StartingMainDeck += [Bane] * 2
StartingMainDeck += [Doomsday] * 2
StartingMainDeck += [Gorilla_Grodd] * 2
StartingMainDeck += [Jervis_Tetch] * 2
StartingMainDeck += [Johnny_Quick] * 2
StartingMainDeck += [Killer_Croc] * 2
StartingMainDeck += [Lobo] * 1
StartingMainDeck += [Mr_Zsasz] * 2
StartingMainDeck += [Red_Lantern_Corps] * 2
StartingMainDeck += [Scarecrow] * 2
StartingMainDeck += [Two_Face] * 3

# SUPER VILLAINS
SuperVillainList = []

Lex_Luthor = Card("cardimgs/lexluthor.jpg", cost=10, draw=(3,0), first_appearance=1, name="Lex Luthor", vp=5, type="Villain", text="Draw three cards.\nFirst Appearance--Attack: Each player gains a Weakness for each villain in the Line-Up.")
Black_Manta = Card("cardimgs/blackmanta.jpg", cost=8, power=(3,0), draw=(1,0), first_appearance=2, name="Black Manta", vp=4, type="Villain", text="+3 Power and draw a card.\nFirst Appearance--Attack: Each player discards the top card of their deck. If you discarded a card with cost 1 or more, choose one: Destroy it; or discard your hand.")
The_Flash = Card("cardimgs/theflash.jpg", cost=8, draw=(3,0), discard=1, name="The Flash", vp=4, type="Hero", text="Draw three cards, and then discard a card.")
Mongul = Card("cardimgs/mongul.jpg", cost=11, power=(2,0), draw=(2,0), destroy_hand=1, first_appearance=3, name="Mongul", vp=6, type="Villain", text="+2 Power and draw two cards. Then destroy a card in your hand.\nFirst Appearance--Attack: Each player discards two random cards from their hand.")
Parallax = Card("cardimgs/parallax.jpg", cost=12, first_appearance=4, name="Parallax", vp=6, custom=6, type="Villain", text="Double your current Power this turn.\nFirst Appearance--Attack: Each player reveals their hand and discards all cards with cost 2 or less.")
Trigon = Card("cardimgs/trigon.jpg", cost=12, first_appearance=5, name="Trigon", vp=6, custom=7, type="Villain", text="Look at the top two cards of the main deck. Put one into your hand and the other on the bottom of the main deck.\nFirst Appearance--Attack: Each player destroys a card with cost 1 or greater in their hand.")
Graves = Card("cardimgs/graves.jpg", cost=9, first_appearance=6, name="Graves", vp=5, custom=8, type="Villain", text="+4 Power and you may put a card from your discard pile on top of your deck.\nFirst Appearance--Attack: Each player puts a card from their hand face down. Destroy those cards. If one player destroyed a card with cost higher than each other player, they draw two cards.")
Nekron = Card("cardimgs/nekron.jpg", cost=12, first_appearance=7, name="Nekron", vp=6, custom=9, type="Villain", text="Destroy up to three cards in your hand and/or discard pile. For each you destroy, draw a card.\nFirst Appearance--Attack: Each player totals the cost of the cards in their hand. The player(s) with the highest total destroys a random card in their hand. Each other player chooses and destroys a card in their hand.")
Bart_Allen = Card("cardimgs/bartallen.jpg", cost=14, first_appearance=8, name="Bart Allen", vp=7, custom=10, type="Hero", text="Gain two cards from the Line-Up and put them into your hand. Then refill the Line-Up.\nFirst Appearance--Attack: Each player reveals their hand and gains a Weakness for each different card with VP value 1 or greater revealed this way.")
Black_Adam = Card("cardimgs/blackadam.jpg", cost=11, first_appearance=9, name="Black Adam", vp=6, custom=11, type="Villain", text="+2 Power for each different card type you play or have played this turn.\nFirst Appearance--Attack: Each player destroys a Hero in their hand or discard pile.")
Hel = Card("cardimgs/hel.jpg", cost=9, first_appearance=10, name="H'el", vp=5, custom=12, type="Villain", text="Reveal and draw cards from the top of your deck until you have drawn 7 or greater cost worth of cards.\nFirst Appearance--Attack: Each player reveals the top three cards of their deck. Choose one of them with cost 1 or greater, then destroy it. Discard the rest.")
Arkillo = Card("cardimgs/arkillo.jpg", cost=10, first_appearance=11, name="Arkillo", vp=5, custom=13, type="Villain", text="+2 Power and put all Equipment from your discard pile into your hand.\nFirst Appearance--Attack: Each player totals the cost of cards in their hand. The player(s) with the highest total gains three Weakness cards.")

# list of villains not including the Flash who goes on top
SuperVillainDeckList = []
SuperVillainDeckList.append(Lex_Luthor)
SuperVillainDeckList.append(Black_Manta)
SuperVillainDeckList.append(Mongul)
SuperVillainDeckList.append(Parallax)
SuperVillainDeckList.append(Trigon)
SuperVillainDeckList.append(Graves)
SuperVillainDeckList.append(Nekron)
SuperVillainDeckList.append(Bart_Allen)
SuperVillainDeckList.append(Black_Adam)
SuperVillainDeckList.append(Hel)
SuperVillainDeckList.append(Arkillo)

# player buys card
# if the card is in the lineup, need an index in case there's more than one of the same card in the lineup
# checks how much power the player has and whether that's enough to buy the card
# puts the card where it needs to go (depending on what cards you've played this turn)
# decreases player.power by the cost of the card
# returns boolean whether the buy was successful
def buy(player, card, i=0):
    if player.power < card.cost:
        return False
    # player spends power
    player.power -= card.cost
    if card.name == "Kick":
        kick_deck.draw() # don't need to catch it because it's already card
    elif card in SuperVillainDeckList or card == The_Flash:
        super_villain_deck.draw() # same
    else: # everything else comes from the lineup
        lineup[i] = None # remove it and keep its spot
    player.gain_card_discard(card)
    return True

# #Normal card attacks:
# #Bane's attack
# def bane_attack(player):
#     #prompt for choice
#     if len(player.hand) > 0: #if the player has a hand
#         selection = card_effect.prompt_player("You've been attacked by Bane. Choose a card to discard from your hand. ", player.own_deck.hand, False)
#         #discard the card
#         player.own_deck.hand.remove(selection) #get card out of hand
#         player.own_deck.add_to_discard(selection) #put it in the discard
#
# #Super villain first appearance attacks
# #lex luthor's first appearance
# def lex_luthor_fa(player):
#     #for each villain in lineup, gain weakness
#     for card in lineup:
#         if card.get_type() == "Villain":
#             if not weakness_deck.isEmpty(): #if we still have weaknesses
#                 weakness_deck.draw() #take weakness from weakness deck
#                 player.gain_card_discard(Weakness) #give player the weakness
#
#
# """
# Takes the card that's attacking and a list of targets being attacked and runs the attack
# Will eventually ask players if they wish to defend
# """
# def attack(card, targets):
#     #TODO implement all these attacks
#     if card.name = "Bane":
#         for target in targets:
#             bane_attack(target)
#     #TODO check if players defended and only call attack effects if not
#
#

#executes a computer turn based on our algorithms
def computer_turn(player, opponent):
    #asdf
    while len(player.own_deck.hand) != 0: #while there are cards to play, play them
        #TODO integrate the algorithm for playing cards
        card = player.own_deck.hand[0]
        player.own_deck.hand_to_played(0)

        #coded in game.py
        if card.custom == 1:
            jonn_jonzz(player)
        elif card.custom == 2:
            shazam(player)
        elif card.custom == 3:
            white_lantern_power_battery(player)
        elif card.custom == 4:
            xray_vision(player, opponent)
        elif card.custom == 5:
            super_girl(player)
        elif card.custom == 7:
            trigon(player)
        elif card.custom == 10:
            bart_allen(player)
        else:  # if not here, then handled by card_effect
            card_effect.card_effect(player, card)

    #get which cards the computer wants to buy
    cards_to_buy = buy_cards.buy_cards(player.power, super_villain_deck, main_deck, kick_deck, player.own_deck, lineup, opponent.own_deck, None)
    for card in cards_to_buy: #buy cards in card to buy
        index = 0
        if card.name != "Kick" and not (card in SuperVillainDeckList or card == The_Flash): #if card is in lineup
            index = lineup.index(card)
        buy(player, card, index)

    end_turn(player)

#ends the turn for the player whose turn it was
def end_turn(player):
    # move cards to discard
    player.end_turn()
    # refill lineup
    for i in range(0,5):
        if not lineup[i]:
            lineup[i] = main_deck.draw()
    hand_scroll = 0
    # TODO super villain flip and attacks

def jonn_jonzz(player): #1
    villain = super_villain_deck.peek()
    print("J'onn J'onnz played:", villain)
    #get the top super villain
    # all of the cards that needed to be implemented in game.py
    if villain.custom == 1:
        jonn_jonzz(player)
    elif villain.custom == 2:
        shazam(player)
    elif villain.custom == 3:
        white_lantern_power_battery(player)
    elif villain.custom == 4:
        xray_vision(player, opponent)
    elif villain.custom == 5:
        super_girl(player)
    elif villain.custom == 7:
        trigon(player)
    elif villain.custom == 10:
        bart_allen(player)
    else:  # if not here, then handled by card_effect
        card_effect.card_effect(human_player, villain)

def shazam(player): #2
    player.power += 2
    top = main_deck.peek() #get top card of main deck
    print("Shazam! played:", top)
    # all of the cards that needed to be implemented in game.py
    if top.custom == 1:
        jonn_jonzz(player)
    elif top.custom == 2:
        shazam(player)
    elif top.custom == 3:
        white_lantern_power_battery(player)
    elif top.custom == 4:
        xray_vision(player, opponent)
    elif top.custom == 5:
        super_girl(player)
    elif top.custom == 7:
        trigon(player)
    elif top.custom == 10:
        bart_allen(player)
    else:  # if not here, then handled by card_effect
        card_effect.card_effect(human_player, top)


def white_lantern_power_battery(player): #3
    #ask which to take
    gained = card_effect.prompt_player("Pick a card from the lineup to gain to the top of your deck.", lineup, False)
    index = lineup.index(gained) #get the card index in lineup
    lineup[index] = None #remove the card from lineup
    player.gain_card_top(gained) #add card to top of undrawn

def xray_vision(player, opponent): #4
    #get the top card of opponent
    top = opponent.own_deck.peek()
    # all of the cards that needed to be implemented in game.py
    if top.custom == 1:
        jonn_jonzz(player, opponent)
    elif top.custom == 2:
        shazam(player, opponent)
    elif top.custom == 3:
        white_lantern_power_battery(player)
    elif top.custom == 4:
        xray_vision(player, opponent)
    elif top.custom == 5:
        super_girl(player)
    elif top.custom == 7:
        trigon(player)
    elif top.custom == 10:
        bart_allen(player)
    else:  # if not here, then handled by card_effect
        card_effect.card_effect(player, top)

def super_girl(player): #5
    kick_deck.draw()#remove the kick from the kick deck
    player.gain_card_hand(Kick) #add kick to hand

def trigon(player): #7
    top_two = [main_deck.draw(), main_deck.draw()] #get top two cards
    selection = card_effect.prompt_player("Pick which card to add to your hand. The other will go to the bottom of the main deck.", top_two, False)
    player.gain_card_hand(selection) #add selected card to hand
    top_two.remove(selection) #only card left here is the not selected one
    main_deck.add_to_bottom(top_two[0])

def bart_allen(player):
    #get first choice
    selection1 = card_effect.prompt_player("Pick the first card to gain from the lineup.", lineup, False)
    index1 = lineup.index(selection1) #find an index of the first card
    lineup[index1] = None #remove from lineup
    player.gain_card_hand(selection1) #player gets the card to hand
    selection2 = card_effect.prompt_player("Pick the second card to gain from the lineup.", lineup, False)
    index2 = lineup.index(selection2) #find index of the second card
    lineup[index2] = None
    player.gain_card_hand(selection2) #gain other card
    #refill the lineup
    lineup[index1] = main_deck.draw()
    lineup[index2] = main_deck.draw()



# make the game window
screen = pygame.display.set_mode(size=(SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(SCREEN_NAME)

# draw a background to put on the screen every frame
bkg = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
bkg.fill(GAME_BKG_COLOR)
card_outline = pygame.Surface((CARD_WIDTH + 10, CARD_HEIGHT + 10))
card_outline.fill((127, 127, 127))
card_interior = pygame.Surface((CARD_WIDTH - 10, CARD_HEIGHT - 10))
card_interior.fill(GAME_BKG_COLOR)
card_outline.blit(card_interior, (10, 10))
# outline the weakness, kick, supervillain, and main decks
bkg.blit(card_outline, (CARD_SPACE - 5, CARD_SPACE - 5))
bkg.blit(card_outline, (CARD_WIDTH + CARD_SPACE * 2 - 5, CARD_SPACE - 5))
bkg.blit(card_outline, (CARD_SPACE - 5, CARD_HEIGHT + CARD_SPACE * 2 - 5))
bkg.blit(card_outline, (CARD_WIDTH + CARD_SPACE * 2 - 5, CARD_HEIGHT + CARD_SPACE * 2 - 5))
# outline the lineup
bkg.blit(card_outline, (CARD_SPACE * 4 + CARD_WIDTH * 2 - 5, CARD_SPACE - 5))
bkg.blit(card_outline, (CARD_SPACE * 4 + CARD_WIDTH * 2 - 5, CARD_HEIGHT // 4 + CARD_SPACE - 5))
bkg.blit(card_outline, (CARD_SPACE * 4 + CARD_WIDTH * 2 - 5, CARD_HEIGHT // 4 * 2 + CARD_SPACE - 5))
bkg.blit(card_outline, (CARD_SPACE * 4 + CARD_WIDTH * 2 - 5, CARD_HEIGHT // 4 * 3 + CARD_SPACE - 5))
bkg.blit(card_outline, (CARD_SPACE * 4 + CARD_WIDTH * 2 - 5, CARD_HEIGHT // 4 * 4 + CARD_SPACE - 5))
# outline the player's deck and discard pile
bkg.blit(card_outline, (SCREEN_WIDTH - CARD_WIDTH - CARD_SPACE - 5, CARD_SPACE + GAME_FONT.get_height() * 2 - 4))
bkg.blit(card_outline, (SCREEN_WIDTH - CARD_WIDTH - CARD_SPACE - 5, CARD_SPACE * 3 + CARD_HEIGHT + GAME_FONT.get_height() + 1))
# outline the player's hand
hand_outline = pygame.Surface((CARD_WIDTH * ((SCREEN_WIDTH - CARD_SPACE * 2) // CARD_WIDTH) + 10, CARD_HEIGHT + 10))
hand_outline.fill((127, 127, 127))
hand_interior = pygame.Surface((CARD_WIDTH * ((SCREEN_WIDTH - CARD_SPACE * 2) // CARD_WIDTH) - 10, CARD_HEIGHT - 10))
hand_interior.fill(GAME_BKG_COLOR)
hand_outline.blit(hand_interior, (10, 10))
bkg.blit(hand_outline, (CARD_SPACE - 5, SCREEN_HEIGHT - CARD_HEIGHT - 10))
# draw an alternate background for showing the player's discard pile
discard_bkg = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
discard_bkg.fill(GAME_BKG_COLOR)
discard_bkg.blit(GAME_FONT.render("Your discard pile", True, (0, 0, 0), GAME_BKG_COLOR), (CARD_SPACE, CARD_SPACE))
pile_outline = pygame.Surface((CARD_WIDTH + 10, CARD_HEIGHT // 6 * ((SCREEN_HEIGHT - CARD_SPACE * 2) // (CARD_HEIGHT // 6)) + 10))
pile_interior = pygame.Surface((CARD_WIDTH - 10, CARD_HEIGHT // 6 * ((SCREEN_HEIGHT - CARD_SPACE * 2) // (CARD_HEIGHT // 6)) - 10))
pile_outline.fill((127, 127, 127))
pile_interior.fill(GAME_BKG_COLOR)
pile_outline.blit(pile_interior, (10, 10))
discard_bkg.blit(pile_outline, (SCREEN_WIDTH - CARD_WIDTH - CARD_SPACE - 5, CARD_SPACE - 5))
# scroll buttons for scrolling through the discard pile or a too-large hand
scroll_button_u = pygame.Surface((CARD_WIDTH, CARD_SPACE - 5))
scroll_button_u_dark = scroll_button_u.copy()
scroll_button_u.fill(GAME_BKG_COLOR)
scroll_button_u_dark.fill((GAME_BKG_COLOR[0] // 1.5, GAME_BKG_COLOR[1] // 1.5, GAME_BKG_COLOR[2] // 1.5))
scroll_button_d = scroll_button_u.copy()
scroll_button_d_dark = scroll_button_u_dark.copy()
pygame.draw.polygon(scroll_button_u, (127, 127, 127), [(CARD_WIDTH // 2 - CARD_SPACE // 4, int(CARD_SPACE * (3/4))), (CARD_WIDTH // 2, CARD_SPACE // 4), (CARD_WIDTH // 2 + CARD_SPACE // 4, int(CARD_SPACE * (3/4)))])
pygame.draw.polygon(scroll_button_u_dark, (95, 95, 95), [(CARD_WIDTH // 2 - CARD_SPACE // 4, int(CARD_SPACE * (3/4))), (CARD_WIDTH // 2, CARD_SPACE // 4), (CARD_WIDTH // 2 + CARD_SPACE // 4, int(CARD_SPACE * (3/4)))])
pygame.draw.polygon(scroll_button_d, (127, 127, 127), [(CARD_WIDTH // 2 - CARD_SPACE // 4, CARD_SPACE // 4), (CARD_WIDTH // 2, int(CARD_SPACE * (3/4))), (CARD_WIDTH // 2 + CARD_SPACE // 4, CARD_SPACE // 4)])
pygame.draw.polygon(scroll_button_d_dark, (95, 95, 95), [(CARD_WIDTH // 2 - CARD_SPACE // 4, CARD_SPACE // 4), (CARD_WIDTH // 2, int(CARD_SPACE * (3/4))), (CARD_WIDTH // 2 + CARD_SPACE // 4, CARD_SPACE // 4)])
scroll_button_l = pygame.Surface((CARD_SPACE - 5, CARD_HEIGHT))
scroll_button_l_dark = scroll_button_l.copy()
scroll_button_l.fill(GAME_BKG_COLOR)
scroll_button_l_dark.fill((GAME_BKG_COLOR[0] // 1.5, GAME_BKG_COLOR[1] // 1.5, GAME_BKG_COLOR[2] // 1.5))
scroll_button_r = scroll_button_l.copy()
scroll_button_r_dark = scroll_button_l_dark.copy()
pygame.draw.polygon(scroll_button_l, (127, 127, 127), [(int(CARD_SPACE * (3/4)) - 5, int(CARD_HEIGHT / 2 - CARD_SPACE / 4)), (CARD_SPACE // 4 - 5, CARD_HEIGHT // 2), (int(CARD_SPACE * (3/4)) - 5, int(CARD_HEIGHT / 2 + CARD_SPACE / 4))])
pygame.draw.polygon(scroll_button_l_dark, (95, 95, 95), [(int(CARD_SPACE * (3/4)) - 5, int(CARD_HEIGHT / 2 - CARD_SPACE / 4)), (CARD_SPACE // 4 - 5, CARD_HEIGHT // 2), (int(CARD_SPACE * (3/4)) - 5, int(CARD_HEIGHT / 2 + CARD_SPACE / 4))])
pygame.draw.polygon(scroll_button_r, (127, 127, 127), [(CARD_SPACE // 4, int(CARD_HEIGHT / 2 - CARD_SPACE / 4)), (int(CARD_SPACE * (3/4)), CARD_HEIGHT // 2), (CARD_SPACE // 4, int(CARD_HEIGHT / 2 + CARD_SPACE / 4))])
pygame.draw.polygon(scroll_button_r_dark, (95, 95, 95), [(CARD_SPACE // 4, int(CARD_HEIGHT / 2 - CARD_SPACE / 4)), (int(CARD_SPACE * (3/4)), CARD_HEIGHT // 2), (CARD_SPACE // 4, int(CARD_HEIGHT / 2 + CARD_SPACE / 4))])
# a piece to cover up the overflowing cards
cover = pygame.Surface((CARD_WIDTH, CARD_HEIGHT))
cover.fill(GAME_BKG_COLOR)
cover_line = pygame.Surface((CARD_WIDTH, 5))
cover_line.fill((127, 127, 127))
cover.blit(cover_line, (0, 0))

# initialize all the variables needed for the game loop
click = False # is the mouse button down
super_villain_bought = False # if the supervillain was bought this turn, don't flip the next one until next turn
enough_power_num = 0 # number of frames remaining to tick through to stop displaying "not enough power" if the player tries to buy a card that they can't afford
hand_scroll = 0 # how far left the player's hand is scrolled (in cards)
discard_pile = False # show a blown-up view of the player's discard pile
discard_scroll = 0 # how far the discard pile is scrolled if the player is looking at the discard pile screen
card_selection = None # user's choice of card when they're being prompted to pick a card
done = False # game loop exit variable

# initialize game variables (decks and players)
human_player = dc_player.Player(StartingPlayerDeck, False) # makes the human player
computer_player = dc_player.Player(StartingPlayerDeck, True) # makes computer player
players = [human_player, computer_player] # list of players (there are only 2 for now)
main_deck = deck.Deck(StartingMainDeck)
super_villain_deck = deck.Deck(SuperVillainDeckList)
kick_deck = deck.Deck([Kick] * 16) #Should be 16
weakness_deck = deck.Deck([Weakness] * 20)
# the lineup, which will 5 cards drawn sequentially from the main deck after it is shuffled
lineup = [None, None, None, None, None]

# shuffle the deck
super_villain_deck.shuffle()
super_villain_deck.add_to_front(The_Flash) # put the flash on top
main_deck.shuffle()
human_player.own_deck.shuffle()
computer_player.own_deck.shuffle()
# fill the lineup
for i in range(5):
    lineup[i] = main_deck.draw()
# fill the player's hand
for i in range(5):
    human_player.own_deck.draw()

while not done:
    mouse_pos = pygame.mouse.get_pos() # assume we will always need to know the position of the mouse

    # click should only be true on the frame when the button is pressed
    if click:
        click = False
    for event in pygame.event.get(): # evaluate all the current events
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            click = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q: # have a quit key
                done = True
    
    # if the player has clicked on the discard pile, everything looks and behaves differently
    if discard_pile:
        # draw the background for the discard pile before anything else so you don't cover anything up
        screen.blit(discard_bkg, (0, 0))
        # make an exit button and allow the user to use it
        GAME_FONT.set_underline(True)
        screen.blit(GAME_FONT.render("DONE", True, (0, 0, 0), GAME_BKG_COLOR), (SCREEN_WIDTH - CARD_SPACE * 2 - CARD_WIDTH - 30, CARD_SPACE + CARD_ZOOM_HEIGHT))
        GAME_FONT.set_underline(False)
        if click and SCREEN_WIDTH - CARD_SPACE * 2 - CARD_WIDTH - 30 < mouse_pos[0] < SCREEN_WIDTH - CARD_SPACE * 2 - CARD_WIDTH and CARD_SPACE + CARD_ZOOM_HEIGHT < mouse_pos[1] < CARD_SPACE + CARD_ZOOM_HEIGHT + GAME_FONT.get_height():
            discard_pile = False
            discard_scroll = 0
        # draw the discard pile all lined up nice and neat
        for i in range(discard_scroll, len(human_player.own_deck.discard)):
            screen.blit(human_player.own_playingdeck.discard[i].img, (SCREEN_WIDTH - CARD_WIDTH - CARD_SPACE, CARD_SPACE + CARD_HEIGHT // 6 * (i - discard_scroll)))
        # cover up the cards that overflow over the discard pile boundary
        screen.blit(cover, (SCREEN_WIDTH - CARD_SPACE - CARD_WIDTH, CARD_SPACE + pile_outline.get_height() - 10))
        # draw the scroll buttons light or dark depending on whether the mouse is over them and do their things if the user clicks on them
        # mouse is over the scroll up button (and there's more up to scroll)
        if discard_scroll > 0 and SCREEN_WIDTH - CARD_WIDTH - CARD_SPACE < mouse_pos[0] < SCREEN_WIDTH - CARD_SPACE and 0 < mouse_pos[1] < CARD_SPACE - 5:
            screen.blit(scroll_button_u_dark, (SCREEN_WIDTH - CARD_WIDTH - CARD_SPACE, 0))
            screen.blit(scroll_button_d, (SCREEN_WIDTH - CARD_WIDTH - CARD_SPACE, CARD_SPACE - 5 + pile_outline.get_height()))
            if click:
                discard_scroll -= 1
        # mouse is over the scroll down button (and there's more down to scroll)
        elif discard_scroll < len(human_player.own_deck.discard) - (pile_outline.get_height() // (CARD_HEIGHT // 6)) + 5 and SCREEN_WIDTH - CARD_WIDTH - CARD_SPACE < mouse_pos[0] < SCREEN_WIDTH - CARD_SPACE and CARD_SPACE - 5 + pile_outline.get_height() < mouse_pos[1] < CARD_SPACE * 2 - 10 + pile_outline.get_height():
            screen.blit(scroll_button_u, (SCREEN_WIDTH - CARD_WIDTH - CARD_SPACE, 0))
            screen.blit(scroll_button_d_dark, (SCREEN_WIDTH - CARD_WIDTH - CARD_SPACE, CARD_SPACE - 5 + pile_outline.get_height()))
            if click:
                discard_scroll += 1
        # mouse is elsewhere
        else:
            screen.blit(scroll_button_u, (SCREEN_WIDTH - CARD_WIDTH - CARD_SPACE, 0))
            screen.blit(scroll_button_d, (SCREEN_WIDTH - CARD_WIDTH - CARD_SPACE, CARD_SPACE - 5 + pile_outline.get_height()))
        # is the mouse on a card in the discard pile
        if SCREEN_WIDTH - CARD_WIDTH - CARD_SPACE < mouse_pos[0] < SCREEN_WIDTH - CARD_SPACE and CARD_SPACE < mouse_pos[1] < CARD_SPACE + min((len(human_player.own_deck.discard) - 1) * (CARD_HEIGHT // 6) + CARD_HEIGHT, pile_outline.get_height() - 10):
            i = min(discard_scroll + (mouse_pos[1] - CARD_SPACE) // (CARD_HEIGHT // 6), len(human_player.own_deck.discard) - 1)
            screen.blit(human_player.own_deck.discard[i].zoom(), (SCREEN_WIDTH - CARD_WIDTH - CARD_ZOOM_WIDTH - CARD_SPACE * 2, CARD_SPACE - 5))

    # the normal version of the GUI
    else:
        # draw the background before you draw anything on the screen so you don't cover anything up
        screen.blit(bkg, (0, 0))
        screen.blit(pygame.image.load("cardimgs/cardback.jpg") if super_villain_bought else super_villain_deck.peek().img, (CARD_SPACE, CARD_SPACE)) # the supervillain deck (represented by the small image of the top card of the deck)
        screen.blit(GAME_FONT.render("Cards remaining: " + str(super_villain_deck.num_cards), True, (0, 0, 0), GAME_BKG_COLOR), (CARD_SPACE, CARD_SPACE + CARD_HEIGHT + 5))
        screen.blit(pygame.image.load("cardimgs/cardback.jpg"), (CARD_WIDTH + CARD_SPACE * 2, CARD_SPACE)) # the main deck (represented by a small card back)
        screen.blit(GAME_FONT.render("Cards remaining: " + str(main_deck.num_cards), True, (0, 0, 0), GAME_BKG_COLOR), (CARD_SPACE * 2 + CARD_WIDTH, CARD_SPACE + CARD_HEIGHT + 5))

        if kick_deck.isEmpty():
            screen.blit(pygame.Surface((0, 0)), (0,0))
        else:
            screen.blit(kick_deck.peek().img,(CARD_SPACE * 2 + CARD_WIDTH, CARD_SPACE * 2 + CARD_HEIGHT))
        if weakness_deck.isEmpty():
            screen.blit(pygame.Surface((0, 0)), (0, 0))
        else:
            screen.blit(weakness_deck.peek().img, (CARD_SPACE, CARD_SPACE * 2 + CARD_HEIGHT))
        screen.blit(GAME_FONT.render("Kicks remaining: " + str(kick_deck.num_cards), True, (0, 0, 0), GAME_BKG_COLOR), (CARD_SPACE * 2 + CARD_WIDTH, CARD_SPACE * 2 + CARD_HEIGHT * 2 + 5))
        screen.blit(GAME_FONT.render("Weaknesses remaining: " + str(weakness_deck.num_cards), True, (0, 0, 0), GAME_BKG_COLOR), (CARD_SPACE, CARD_SPACE * 2 + CARD_HEIGHT * 2 + 5))
        
        # the player's deck, represented either by a card back or nothing (if the deck is empty)
        if human_player.own_deck.undrawn != []:
            screen.blit(pygame.image.load("cardimgs/cardback.jpg"), (SCREEN_WIDTH - CARD_WIDTH - CARD_SPACE, CARD_SPACE + GAME_FONT.get_height() * 2 + 1))
        screen.blit(GAME_FONT.render("Your deck", True, (0, 0, 0), GAME_BKG_COLOR), (SCREEN_WIDTH - CARD_WIDTH - CARD_SPACE, CARD_SPACE - 5))
        screen.blit(GAME_FONT.render("Cards remaining: " + str(len(human_player.own_deck.undrawn)), True, (0, 0, 0), GAME_BKG_COLOR), (SCREEN_WIDTH - CARD_WIDTH - CARD_SPACE, CARD_SPACE + GAME_FONT.get_height() - 5))
        # the player's discard pile, represented by the top card or nothing (if the discard is empty)
        if len(human_player.own_deck.discard) != 0:
            screen.blit(human_player.own_deck.discard[-1].img, (SCREEN_WIDTH - CARD_WIDTH - CARD_SPACE, CARD_SPACE * 3 + CARD_HEIGHT + GAME_FONT.get_height() + 6))
        screen.blit(GAME_FONT.render("Your discard pile", True, (0, 0, 0), GAME_BKG_COLOR), (SCREEN_WIDTH - CARD_WIDTH - CARD_SPACE, CARD_SPACE * 3 + CARD_HEIGHT - GAME_FONT.get_height()))
        screen.blit(GAME_FONT.render("Click to expand", True, (0, 0, 0), GAME_BKG_COLOR), (SCREEN_WIDTH - CARD_WIDTH - CARD_SPACE, CARD_SPACE * 3 + CARD_HEIGHT))
        # end turn button
        END_TURN_BUTTON_LEFT = 420
        END_TURN_BUTTON_TOP = 400
        END_TURN_BUTTON_WIDTH = 53
        END_TURN_BUTTON_HEIGHT = 18
        GAME_FONT.set_underline(True) # underline the text
        screen.blit(GAME_FONT.render("END TURN", True, (0, 0, 0), GAME_BKG_COLOR), (END_TURN_BUTTON_LEFT, END_TURN_BUTTON_TOP))
        GAME_FONT.set_underline(False)
        # all the cards the player has played this turn
        for i in range(len(human_player.own_deck.played)):
            screen.blit(human_player.own_deck.played[i].img, (CARD_WIDTH * (3 + i % 2) + CARD_SPACE * 5, CARD_SPACE + GAME_FONT.get_height() + (CARD_HEIGHT // 6) * (i // 2)))
        screen.blit(GAME_FONT.render("Played cards (" + str(human_player.power) + " power)", True, (0, 0, 0), GAME_BKG_COLOR), (CARD_SPACE * 5 + CARD_WIDTH * 3, CARD_SPACE - 5))
        # the player's hand (scrollable)
        screen.blit(GAME_FONT.render("Your hand", True, (0, 0, 0), GAME_BKG_COLOR), (CARD_SPACE, CARD_SPACE * 5 + CARD_HEIGHT * 2 - GAME_FONT.get_height() - 10))
        for i in range(hand_scroll, min(len(human_player.own_deck.hand), hand_scroll + (hand_outline.get_width() + 10) // CARD_WIDTH)):
            screen.blit(human_player.own_deck.hand[i].img, (CARD_SPACE + CARD_WIDTH * (i - hand_scroll), SCREEN_HEIGHT - CARD_HEIGHT - 5))
        # draw the hand scroll buttons light or dark depending on whether the mouse is over them and do their things if the user clicks on them
        # mouse over left button (and there's more left to scroll)
        if hand_scroll > 0 and 0 < mouse_pos[0] < CARD_SPACE - 5 and SCREEN_HEIGHT - CARD_HEIGHT - 5 < mouse_pos[1] < SCREEN_HEIGHT - 5 and hand_scroll > 0:
            screen.blit(scroll_button_l_dark, (0, SCREEN_HEIGHT - CARD_HEIGHT - 5))
            screen.blit(scroll_button_r, (CARD_SPACE + hand_outline.get_width() - 5, SCREEN_HEIGHT - CARD_HEIGHT - 5))
            if click:
                hand_scroll -= 1
        # mouse over right button (and there's more right to scroll)
        elif hand_scroll < len(human_player.own_deck.hand) - hand_outline.get_width() // CARD_WIDTH and CARD_SPACE + hand_outline.get_width() - 5 < mouse_pos[0] < CARD_SPACE * 2 + hand_outline.get_width() and SCREEN_HEIGHT - CARD_HEIGHT - 5 < mouse_pos[1] < SCREEN_HEIGHT - 5 and hand_scroll < len(human_player.own_deck.hand):
            screen.blit(scroll_button_l, (0, SCREEN_HEIGHT - CARD_HEIGHT - 5))
            screen.blit(scroll_button_r_dark, (CARD_SPACE + hand_outline.get_width() - 5, SCREEN_HEIGHT - CARD_HEIGHT - 5))
            if click:
                hand_scroll += 1
        # mouse elsewhere
        else:
            screen.blit(scroll_button_l, (0, SCREEN_HEIGHT - CARD_HEIGHT - 5))
            screen.blit(scroll_button_r, (CARD_SPACE + hand_outline.get_width() - 5, SCREEN_HEIGHT - CARD_HEIGHT - 5))
        # the lineup
        for i in range(5):
            if lineup[i] is not None:
                screen.blit(lineup[i].img, (CARD_WIDTH * 2 + CARD_SPACE * 4, CARD_HEIGHT // 4 * i + CARD_SPACE))
        if enough_power_num:
            enough_power_num -= 1
            screen.blit(GAME_FONT.render("Not enough power.", True, (0, 0, 0), GAME_BKG_COLOR), (5, 5))
            
        # is the mouse on the supervillain deck
        if mouse_pos[0] > CARD_SPACE and mouse_pos[0] < CARD_SPACE + CARD_WIDTH and mouse_pos[1] > CARD_SPACE and mouse_pos[1] < CARD_SPACE + CARD_HEIGHT:
            # can only interact with the supervillain deck once per turn
            if not super_villain_bought:
                screen.blit(super_villain_deck.peek().zoom(), (CARD_WIDTH * 3 + CARD_SPACE * 5 - 5, CARD_SPACE - 5))
                if click:
                    if not buy(human_player, super_villain_deck.peek()):
                        enough_power_num = 20
                    else:
                        super_villain_bought = True
                        
        # is the mouse over the weakness deck
        elif (not weakness_deck.isEmpty()) and CARD_SPACE < mouse_pos[0] < CARD_SPACE + CARD_WIDTH and CARD_SPACE * 2 + CARD_HEIGHT < mouse_pos[1] < CARD_SPACE * 2 + CARD_HEIGHT * 2:
            screen.blit(weakness_deck.peek().zoom(), (CARD_WIDTH * 3 + CARD_SPACE * 5 - 5, CARD_SPACE - 5))
            
        # is the mouse over the kick deck
        elif (not kick_deck.isEmpty()) and CARD_SPACE * 2 + CARD_WIDTH < mouse_pos[0] < CARD_SPACE * 2 + CARD_WIDTH * 2 and CARD_SPACE * 2 + CARD_HEIGHT < mouse_pos[1] < CARD_SPACE * 2 + CARD_HEIGHT * 2:
            screen.blit(kick_deck.peek().zoom(), (CARD_WIDTH * 3 + CARD_SPACE * 5 - 5, CARD_SPACE - 5))
            # click to buy a kick
            if click:
                if not buy(human_player, kick_deck.peek()):
                    enough_power_num = 20
                    
        # is the mouse over end turn
        elif mouse_pos[0] > END_TURN_BUTTON_LEFT and mouse_pos[0] < (END_TURN_BUTTON_LEFT + END_TURN_BUTTON_WIDTH) and mouse_pos[1] > END_TURN_BUTTON_TOP and mouse_pos[1] < END_TURN_BUTTON_TOP + END_TURN_BUTTON_HEIGHT:
            if click:
                end_turn(human_player)
                computer_turn(computer_player, human_player)
                
        # is the mouse on a card in the hand
        elif CARD_SPACE < mouse_pos[0] < CARD_SPACE + min(hand_outline.get_width() - 10, CARD_WIDTH * (len(human_player.own_deck.hand) - hand_scroll)) and SCREEN_HEIGHT - CARD_HEIGHT - 5 < mouse_pos[1] < SCREEN_HEIGHT - 5:
            i = hand_scroll + (mouse_pos[0] - CARD_SPACE) // CARD_WIDTH
            screen.blit(human_player.own_deck.hand[i].zoom(), (CARD_SPACE - 5, CARD_SPACE - 5))
            if click: # click on a card to play it
                card = human_player.own_deck.hand[i] #because if we destroy from hand, indices get messed up
                human_player.own_deck.hand_to_played(i)
                # if the hand is scrolled all the way to the right and the player plays a card, scroll the hand left to fill the space
                if hand_scroll > 0 and len(human_player.own_deck.hand) - hand_scroll < (hand_outline.get_width() - 10) // CARD_WIDTH:
                    hand_scroll -= 1
                handlen = len(human_player.own_deck.hand)
                #all of the cards that needed to be implemented in game.py
                #asdf
                if card.custom == 1:
                    jonn_jonzz(human_player)
                elif card.custom == 2:
                    shazam(human_player)
                elif card.custom == 3:
                    white_lantern_power_battery(human_player)
                elif card.custom == 4:
                    xray_vision(human_player, computer_player)
                elif card.custom == 5:
                    super_girl(human_player)
                elif card.custom == 7:
                    trigon(human_player)
                elif card.custom == 10:
                    bart_allen(human_player)
                else: #if not here, then handled by card_effect
                    card_effect.card_effect(human_player, card)
                if handlen > len(human_player.own_deck.hand): # if the card effect discarded a card from the hand
                    if hand_scroll > 0 and len(human_player.own_deck.hand) - hand_scroll < (hand_outline.get_width() - 10) // CARD_WIDTH:
                        hand_scroll -= 1
                
        # is the mouse on any of the played cards
        for i in range(len(human_player.own_deck.played)):
            if mouse_pos[0] > CARD_WIDTH * (3 + i % 2) + CARD_SPACE * 5 and mouse_pos[0] < CARD_WIDTH * (4 + i % 2) + CARD_SPACE * 5 and mouse_pos[1] > CARD_SPACE + GAME_FONT.get_height() + (CARD_HEIGHT // 6) * (i // 2):
                # treat the last two played cards differently because they're shown in full and are thus much taller
                if i + 2 >= len(human_player.own_deck.played):
                    if mouse_pos[1] < CARD_SPACE + GAME_FONT.get_height() + CARD_HEIGHT + (CARD_HEIGHT // 6) * (i // 2):
                        screen.blit(human_player.own_deck.played[i].zoom(), (CARD_SPACE - 5, CARD_SPACE - 5))
                else:
                    if mouse_pos[1] < CARD_SPACE + GAME_FONT.get_height() + (CARD_HEIGHT // 6) * (i // 2 + 1):
                        screen.blit(human_player.own_deck.played[i].zoom(), (CARD_SPACE - 5, CARD_SPACE - 5))
                        
        # is the mouse on any of the lineup cards
        if CARD_SPACE * 4 + CARD_WIDTH * 2 < mouse_pos[0] < CARD_SPACE * 4 + CARD_WIDTH * 3 and CARD_SPACE < mouse_pos[1] < CARD_SPACE + CARD_HEIGHT // 4 * 4 + CARD_HEIGHT:
            i = min((mouse_pos[1] - CARD_SPACE) // (CARD_HEIGHT // 4), 4)
            # if you mouse over an empty spot in the lineup, show the next card down instead
            while i >= 0:
                if lineup[i] is None:
                    i -= 1
                else:
                    break
            if i >= 0:
                screen.blit(lineup[i].zoom(), (CARD_SPACE - 5, CARD_SPACE - 5))
                if click:
                    if not buy(human_player, lineup[i], i):
                        enough_power_num = 20
        
        # is the mouse on the discard pile
        if SCREEN_WIDTH - CARD_WIDTH - CARD_SPACE < mouse_pos[0] < SCREEN_WIDTH - CARD_SPACE and CARD_SPACE * 3 + CARD_HEIGHT + GAME_FONT.get_height() + 6 < mouse_pos[1] < CARD_SPACE * 3 + CARD_HEIGHT * 2 + GAME_FONT.get_height() + 6:
            if len(human_player.own_deck.discard) > 0:
                screen.blit(human_player.own_deck.discard[-1].zoom(), (CARD_SPACE - 5, CARD_SPACE - 5))
            # click on the discard pile to expand it
            if click:
                discard_pile = True

    # last thing done in the loop: update the display to reflect everything you just drew
    pygame.display.flip()
    # makes the game run no faster than 20 fps (for timing)
    GAME_CLOCK.tick(20)

pygame.quit()

