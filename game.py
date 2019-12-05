"""
Potential first iteration of the GUI?
Created mostly for purposes of learning pygame
"""

import pygame
pygame.init()
from collections import namedtuple

# card dimensions
CARD_WIDTH = 123
CARD_HEIGHT = 175
CARD_SPACE = 35
# window dimensions
SCREEN_WIDTH = CARD_WIDTH * 7 + CARD_SPACE * 3 + 100
SCREEN_HEIGHT = CARD_HEIGHT * 3 + CARD_SPACE * 5
SCREEN_NAME = "DC Game"
# background color for the whole screen
GAME_BKG_COLOR = (112, 208, 127)

"""
card class
__init__(image_name, name, type, cost, power, draw, vp, text): loads card face image and info namedtuple
get_width(), get_height(): get width and height of card face image
move(dx, dy): move the card by that distance
inform(): returns a text pygame.surface that shows the info namedtuple in text form
"""
class Card:
    font = pygame.font.SysFont("ubuntucondensed", 24) # the font to be used to write all things card-related

    def __init__(self, image_name, type, cost, vp=0, text="", name="", custom=0, power=(0,0), draw=(0,0), destroy_top=(False,0), destroy_hand=0, destroy_discard=0, destroy_hand_or_discard=0, puts_on_top=False, discard=0, op_discard=0, weakness=(False,0), defense=(False, 0), first_appearance=0):
        """
        takes a file path for an image that will be the face of the card
        and a pre-populated card_info namedtuple
        """
        self.img = pygame.image.load(image_name) # the image corresponding to the face of the card
        self.name = name # will be read from DCCardsList below
        self.type = type # will be read from DCCardsList below
        self.cost = cost # will be read from DCCardsList below
        self.vp = vp # will be read from DCCardsList below
        self.text = text # will be read from DCCardsList below
        self.pos = (0, 0) # the coordinates of the top left corner of the card

    def get_width(self):
        return self.img.get_width()

    def get_height(self):
        return self.img.get_height()

    def move(self, dx, dy):
        """move the card to new coordinates on the screen"""
        self.pos = (self.pos[0] + dx, self.pos[1] + dy)

    #TODO figure out of this is actually needed anymore (probably outdated because of resizing the cards)

    # def inform(self):
    #     """return a text surface containing the information about the card (name, type, cost, power, draw, VPs, text)"""
    #     # the aforementioned text surface
    #     text = pygame.Surface((SCREEN_WIDTH, Card.font.get_linesize() * 7)) # as wide as the screen for 7 lines: name, type, cost, power, draw, VPs, text
    #     text.fill(GAME_BKG_COLOR) # get rid of text background
    #     linenum = 0
    #     for field in self.info.fields:
    #         # make a surface containing the text of this line ("Name: Aquaman's Trident" or "Type: Supervillain" or whatever)
    #         line = Card.font.render(" " + field + ": " + getattr(self.info, field), False, (255, 255, 255))
    #         text.blit(line, (0, Card.font.get_linesize() * linenum)) # draw the line onto the text at the appropriate line height
    #         linenum += 1
    #     return text
    
    def get_name(self):
        return self.info[0]

    def get_type(self):
        return self.info[1]

    def get_cost(self):
        return self.info[2]

    def get_power(self):
        return self.info[3]

    def get_draw(self):
        return self.info[4]

    def get_vp(self):
        return self.info[5]

    def get_text(self):
        return self.info[6]


# list containing all the images to be used
cards = []

"""
DC Card List
A namedtuple to hold the card's information
ORDER: Name, Type, Cost, Power, Draw, VP, Text
TO COPY:  = Card("cardimgs/imagename", card_info("N", "T", "C", "P", "D", "V", ""))
"""

# the namedtuple that holds all the information about the card
card_info = namedtuple("card_info", ["Name", "Type", "Cost", "Power", "Draw", "VP", "Text"])

# STARTERS, WEAKNESSES, KICKS (oh my)
#Punch = Card("cardimgs/imagename", card_info("Punch", "Starter", "0", "1", "0", "0", ""))
#Vulnerability = Card("cardimgs/imagename", card_info("Vulnerability", "Starter", "0", "0", "0", "0", ""))
#Weakness  = Card("cardimgs/imagename", card_info("Weakness", "Weakness", "0", "0", "0", "-1", ""))
#Kick = Card("cardimgs/imagename", card_info("Kick", "Super", "3", "2", "0", "1", ""))

"""  DEFAULT CARD
 = Card("cardimgs/imagename.jpg", cost=, power=(,), name="", vp=, type="SuperVillain", text="") #
"""

# EQUIPMENT
EquipmentList = []

Aquamans_Trident = Card("cardimgs/aquamanstrident.jpg", cost=3, power=(2,0), puts_on_top=True, name="Aquaman's Trident", type="Equipment", vp=1, text="You may put any one card you buy or gain this turn on top of your deck.") #3
Batarang = Card("cardimgs/aquamanstrident.jpg", cost=2, power=(2,0), name="Batarang", vp=1, type="Equipment", text="") #2
Soultaker_Sword = Card("cardimgs/imagename.jpg", cost=4, power=(2,0), name="Soultaker Sword", vp=1, type="Equipment", text="You may destroy a card in your hand.", destroy_hand=1) #3
Legion_Flight_Ring = Card("cardimgs/imagename.jpg", cost=2, name="Legion Flight Ring", vp=1, type="Equipment", text="", draw=(1,0)) #2
Lasso_of_Truth = Card("cardimgs/imagename.jpg", cost=2, power=(1,0), name="Lasso of Truth", vp=1, type="Equipment", defense=(True,1), text="Defense: You may discard this card to avoid an Attack. If you do, draw a card.") #2
Power_Ring = Card("cardimgs/imagename.jpg", cost=3, power=(2,1), name="Power Ring", vp=1, type="Equipment", text="Reveal the top card of your deck. If its cost is 1 or greater, additional +1 Power.") #3
Nth_Metal = Card("cardimgs/imagename.jpg", cost=3, power=(1,0), name="Nth Metal", vp=1, type="Equipment", text="Look at the top card of your deck. You may destroy it.", destroy_top=(True,1)) #3
White_Lantern_Power_Battery = Card("cardimgs/imagename.jpg", cost=7, name="White Lantern Power Battery", vp=2, type="Equipment", text="Gain any card from the Line-Up and put it on top of your deck.") #1

EquipmentList.append(Aquamans_Trident)
EquipmentList.append(Batarang)
EquipmentList.append(Lasso_of_Truth)
EquipmentList.append(Legion_Flight_Ring)
EquipmentList.append(Nth_Metal)
EquipmentList.append(Power_Ring)
EquipmentList.append(Soultaker_Sword)
EquipmentList.append(White_Lantern_Power_Battery)

# SUPER POWERS
PowerList = []

Shazam = Card("cardimgs/imagename.jpg", cost=7, name="Shazam!", type="Power", text="Reveal and play the top card of the main deck, then return it to the top of the main deck.", custom=2) #1
Super_Strength = Card("cardimgs/imagename.jpg", cost=7, power=(5,0), name="Super Strength", vp=2, type="Power", text="") #2
Starbolt  = Card("cardimgs/imagename.jpg", cost=5, power=(2,2), name="Starbolt", vp=1, type="Power", text="+1 additional Power for each Super Power in your discard pile.") #3
Bulletproof = Card("cardimgs/imagename.jpg", cost=4, power=(2,0), name="Bulletproof", vp=1, type="Power", defense=(True,2), text="Defense: You may discard this card to avoid an Attack. If you do, draw a card and you may destroy a card in your discard pile.") #2
Giant_Growth = Card("cardimgs/imagename.jpg", cost=2, power=(2,0), name="Giant Growth", vp=1, type="Power", text="") #2
X_Ray_Vision = Card("cardimgs/imagename.jpg", cost=4, name="X-Ray Vision", vp=1, type="Power", custom=4, text="Each foe reveals the top card of their deck. Choose a non-Location card revealed this way, play it, then return it to the top of its owner's deck.") #1
Ultra_Strength = Card("cardimgs/imagename.jpg", cost=9, power=(3,0), name="Ultra Strength", vp=3, draw=(2,0), type="Power", text="") #1
Heat_Vision = Card("cardimgs/imagename.jpg", cost=6, power=(3,0), name="Heat Vision", vp=2, type="Power", destroy_hand_or_discard=1, text="") #3

PowerList.append(Bulletproof)
PowerList.append(Giant_Growth)
PowerList.append(Heat_Vision)
PowerList.append(Shazam)
PowerList.append(Starbolt)
PowerList.append(Super_Strength)
PowerList.append(Ultra_Strength)
PowerList.append(X_Ray_Vision)


# HEROES
HeroList = []

Raven = Card("cardimgs/imagename.jpg", cost=3, power=(1,0), name="Raven", draw=(1,0), vp=1, type="Hero", text="") #3
Catwoman = Card("cardimgs/imagename.jpg", cost=2, power=(2,0), name="Catwoman", vp=1, type="Hero", text="") #2
Katana = Card("cardimgs/imagename.jpg", cost=2, power=(1,0), name="Katana", vp=1, type="Hero", defense=(True,1), text="") #2
Winged_Warrior = Card("cardimgs/imagename.jpg", cost=6, power=(2,3), name="Winged Warrior", vp=2, type="Hero", text="If you play or have played another Hero this turn, additional +3 Power.") #1
Power_Girl = Card("cardimgs/imagename.jpg", cost=5, power=(3,0), name="Power Girl", vp=2, type="Hero", text="") #3
Hawkgirl = Card("cardimgs/imagename.jpg", cost=2, power=(1,4), name="Hawkgirl", vp=1, type="Hero", text="+1 additional Power for each Hero in your discard pile.") #2
Kid_Flash = Card("cardimgs/imagename.jpg", cost=2, name="Kid Flash", vp=1, draw=(1,0), type="Hero", text="") #2
Supergirl = Card("cardimgs/imagename.jpg", cost=4, name="Supergirl", vp=1, type="Hero", custom=5, text="") #2
Jonn_Jonnz = Card("cardimgs/imagename.jpg", cost=6, name="J'onn J'onnz", vp=2, custom=1, type="Hero", text="Play the top card of the Super-Villain stack, then return it to the top of the stack.") #1
The_Fastest_Man_Alive = Card("cardimgs/imagename.jpg", cost=5, name="The Fastest Man Alive", vp=1, draw=(2,0), type="Hero", text="") #1
King_of_Atlantis = Card("cardimgs/imagename.jpg", cost=5, power=(1,5), name="King of Atlantis", vp=1, destroy_discard=1, type="Hero", text="You may destroy a card in your discard pile. If you do, gain +2 additional Power.") #1

HeroList.append(Catwoman)
HeroList.append(Hawkgirl)
HeroList.append(Jonn_Jonnz)
HeroList.append(Katana)
HeroList.append(Kid_Flash)
HeroList.append(King_of_Atlantis)
HeroList.append(Power_Girl)
HeroList.append(Raven)
HeroList.append(Supergirl)
HeroList.append(The_Fastest_Man_Alive)
HeroList.append(Winged_Warrior)


# VILLAINS
VillainList = []

Johnny_Quick = Card("cardimgs/imagename.jpg", cost=2, draw=(1,0), name="Johnny Quick", vp=1, type="Villain", text="") #2
Bane = Card("cardimgs/imagename.jpg", cost=4, power=(2,0), name="Bane", vp=1, op_discard=1, type="Villain", text="Attack: Each foe chooses and discards a card.") #UNDECIDED NUMBER
Mr_Zsasz = Card("cardimgs/imagename.jpg", cost=3, power=(2,0), name="Mr. Zsasz", vp=1, weakness=(True,1), type="Villain", text="Attack: Each foe reveals the top card of his deck. If its cost is odd, that player gains a Weakness.") #UNDECIDED NUMBER
Scarecrow = Card("cardimgs/imagename.jpg", cost=5, power=(2,0), name="Scarecrow", vp=1, weakness=(True,2), type="Villain", text="Attack: Each foe gains a Weakness.") #UNDECIDED NUMBER
Doomsday = Card("cardimgs/imagename.jpg", cost=6, power=(4,0), name="Doomsday", vp=2, type="Villain", text="") #2
Red_Lantern_Corps = Card("cardimgs/imagename.jpg", cost=5, power=(1,6), name="Red Lantern Corps", vp=1, type="Villain", destroy_hand=1, text="You may destroy a card in your hand. If you do, additional +2 Power.") #2
Lobo = Card("cardimgs/imagename.jpg", cost=7, power=(3,0), name="Lobo", vp=2, type="Villain", destroy_hand_or_discard=2, text="You may destroy up to two cards in your hand and/or discard pile.") #1
Gorilla_Grod = Card("cardimgs/imagename.jpg", cost=5, power=(3,0), name="Gorilla Grod", vp=2, type="Villain", text="") #2
<<<<<<< HEAD
Jervis_Tetch = Card("cardimgs/imagename.jpg", cost=3, power=(1,0), name="Jervis Tetch", vp=1, type="Villain", destroy_top=(True,2), text="") #2
=======
Jervis_Tetch = Card("cardimgs/imagename.jpg", cost=3, power=(1,0), name="Jervis Tetch", vp=1, type="Villain", destroy_top=(True, 2), text="") #2
>>>>>>> 5aeb82b567e999587ecde6e3647a3862db02c9c3
Killer_Croc = Card("cardimgs/imagename.jpg", cost=4, power=(2,7), name="Killer Croc", vp=1, type="Villain", text="If you play or have played another Villain this turn, additional +1 Power.") #2
Two_Face = Card("cardimgs/imagename.jpg", cost=2, power=(1,0), name="Two-Face", vp=1, type="Villain", draw=(0,1), text="Choose even or odd, then reveal the top card of your deck. If its cost matches your choice, draw it. If not, discard it.") #2

VillainList.append(Bane)  # NUMBER UNDECIDED
VillainList.append(Doomsday)
VillainList.append(Gorilla_Grod)
VillainList.append(Jervis_Tetch)
VillainList.append(Johnny_Quick)
VillainList.append(Killer_Croc)
VillainList.append(Lobo)
VillainList.append(Mr_Zsasz)  #NUMBER UNDECIDED
VillainList.append(Red_Lantern_Corps)
VillainList.append(Scarecrow)  #NUMBER UNDECIDED
VillainList.append(Two_Face)

# SUPER VILLAINS
SuperVillainList = []

Lex_Luthor = Card("cardimgs/imagename.jpg", cost=10, draw=(3,0), first_appearance=1, name="Lex Luthor", vp=5, type="SuperVillain", text="Draw three cards.\nFirst Appearance--Attack: Each player gains a Weakness for each villain in the Line-Up.")
Black_Manta = Card("cardimgs/imagename.jpg", cost=8, power=(3,0), draw=(1,0), first_appearance=2, name="Black Manta", vp=4, type="SuperVillain", text="+3 Power and draw a card.\nFirst Appearance--Attack: Each player discards the top card of their deck. If you discarded a card with cost 1 or more, choose one: Destroy it; or discard your hand.")
The_Flash = Card("cardimgs/imagename.jpg", cost=8, draw=(3,0), discard=1, name="The Flash", vp=4, type="SuperVillain", text="Draw three cards, and then discard a card.")
Mongol = Card("cardimgs/imagename.jpg", cost=11, power=(2,0), draw=(2,0), destroy_hand=1, first_appearance=3, name="Mongol", vp=6, type="SuperVillain", text="+2 Power and draw two cards. Then destroy a card in your hand.\nFirst Appearance--Attack: Each player discards two random cards from their hand.")
Parallax = Card("cardimgs/imagename.jpg", cost=12, first_appearance=6, name="Parallax", vp=6, custom=6, type="SuperVillain", text="Double your current Power this turn.\nFirst Appearance--Attack: Each player reveals their hand and discards all cards with cost 2 or less.")
Trigon = Card("cardimgs/imagename.jpg", cost=12, first_appearance=7, name="Trigon", vp=6, custom=7, type="SuperVillain", text="Look at the top two cards of the main deck. Put one into your hand and the other on the bottom of the main deck.\nFirst Appearance--Attack: Each player destroys a card with cost 1 or greater in their hand.")
Graves = Card("cardimgs/imagename.jpg", cost=9, first_appearance=8, name="Graves", vp=5, custom=8, type="SuperVillain", text="+4 Power and you may put a card from your discard pile on top of your deck.\nFirst Appearance--Attack: Each player puts a card from their hand face down. Destroy those cards. If one player destroyed a card with cost higher than each other player, they draw two cards.")
Nekron = Card("cardimgs/imagename.jpg", cost=12, first_appearance=9, name="Nekron", vp=6, custom=9, type="SuperVillain", text="Destroy up to three cards in your hand and/or discard pile. For each you destroy, draw a card.\nFirst Appearance--Attack: Each player totals the cost of the cards in their hand. The player(s) with the highest total destroys a random card in their hand. Each other player chooses and destroys a card in their hand.")
Bart_Allen = Card("cardimgs/imagename.jpg", cost=14, first_appearance=10, name="Bart Allen", vp=7, custom=10, type="SuperVillain", text="Gain two cards from the Line-Up and put them into your hand. Then refill the Line-Up.\nFirst Appearance--Attack: Each player reveals their hand and gains a Weakness for each different card with VP value 1 or greater revealed this way.")
Black_Adam = Card("cardimgs/imagename.jpg", cost=11, first_appearance=11, name="Black Adam", vp=6, custom=11, type="SuperVillain", text="+2 Power for each different card type you play or have played this turn.\nFirst Appearance--Attack: Each player destroys a Hero in their hand or discard pile.")
Hel = Card("cardimgs/imagename.jpg", cost=9, first_appearance=12, name="H'el", vp=5, custom=12, type="SuperVillain", text="Reveal and draw cards from the top of your deck until you have drawn 7 or greater cost worth of cards.\nFirst Appearance--Attack: Each player reveals the top three cards of their deck. Choose one of them with cost 1 or greater, then destroy it. Discard the rest.")
Arkillo = Card("cardimgs/imagename.jpg", cost=10, first_appearance=13, name="Arkillo", vp=5, custom=13, type="SuperVillain", text="+2 Power and put all Equipment from your discard pile into your hand.\nFirst Appearance--Attack: Each player totals the cost of cards in their hand. The player(s) with the highest total gains three Weakness cards.")





cards.append(Aquamans_Trident)

# make the game window
screen = pygame.display.set_mode(size=[SCREEN_WIDTH, SCREEN_HEIGHT])
pygame.display.set_caption(SCREEN_NAME)
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
bkg.blit(card_outline, (CARD_SPACE * 3 + CARD_WIDTH * 2 - 5, CARD_HEIGHT + CARD_SPACE + 5))
bkg.blit(card_outline, (CARD_SPACE * 3 + CARD_WIDTH * 3 + 15, CARD_HEIGHT + CARD_SPACE + 5))
bkg.blit(card_outline, (CARD_SPACE * 3 + CARD_WIDTH * 4 + 35, CARD_HEIGHT + CARD_SPACE + 5))
bkg.blit(card_outline, (CARD_SPACE * 3 + CARD_WIDTH * 5 + 55, CARD_HEIGHT + CARD_SPACE + 5))
bkg.blit(card_outline, (CARD_SPACE * 3 + CARD_WIDTH * 6 + 75, CARD_HEIGHT + CARD_SPACE + 5))
# outline the player's hand
hand_outline = pygame.Surface((SCREEN_WIDTH, 10))
hand_outline.fill((127, 127, 127))
bkg.blit(hand_outline, (0, CARD_HEIGHT * 2 + CARD_SPACE * 5 - 5))

# initialize all the variables needed for the game loop
click = False # is the mouse button down
pos = (0, 0) # position of the mouse
dx, dy = 0, 0 # the change in the mouse coordinates between frames
i = 1
done = False
# game loop
while not done:
    mouse_pos = pygame.mouse.get_pos() # assume we will always need to know the position of the mouse

    for event in pygame.event.get(): # evaluate all the current events
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            click = True
        elif event.type == pygame.MOUSEBUTTONUP:
            click = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q: # have a quit key
                done = True

    # do this before you draw anything on the screen so you don't cover anything up
    screen.blit(bkg, (0, 0))
    for card in cards:
        # if the mouse is on this card
        if mouse_pos[0] > card.pos[0] and mouse_pos[1] > card.pos[1] and mouse_pos[0] < card.pos[0] + card.get_width() and mouse_pos[1] < card.pos[1] + card.get_height():
            pass
            #TODO get the card to increase in size when moused over (or something like that)
            #info = card.inform()
            #screen.blit(info, (0, SCREEN_HEIGHT - info.get_height()))
        if click:
            dx, dy = pygame.mouse.get_pos()[0] - mouse_pos[0], pygame.mouse.get_pos()[1] - mouse_pos[1] # get the change in mouse position between frames
            # if the mouse is on this card
            if mouse_pos[0] > card.pos[0] and mouse_pos[1] > card.pos[1] and mouse_pos[0] < card.pos[0] + card.get_width() and mouse_pos[1] < card.pos[1] + card.get_height():
                card.move(dx, dy)
            mouse_pos = (mouse_pos[0] + dx, mouse_pos[1] + dy)
        screen.blit(card.img, card.pos)

    # last thing done in the loop: update the display to reflect everything you just drew
    pygame.display.flip()

pygame.quit()

