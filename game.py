"""
Potential first iteration of the GUI?
Created mostly for purposes of learning pygame
"""

import pygame
pygame.init()
from collections import namedtuple

# window dimensions
SCREEN_WIDTH = 1500
SCREEN_HEIGHT = 1020
SCREEN_NAME = "DC Game"
# background color for the whole screen
GAME_BKG_COLOR = (127, 127, 127)

"""
card class
__init__(image_name, name, type, cost, power, draw, vp, text): loads card face image and info namedtuple
get_width(), get_height(): get width and height of card face image
move(dx, dy): move the card by that distance
inform(): returns a text pygame.surface that shows the info namedtuple in text form
"""
class Card:
    font = pygame.font.SysFont("ubuntucondensed", 24) # the font to be used to write all things card-related

    def __init__(self, image_name, type, cost, vp, text, custom=0, power=(0,0), draw=(0,0), destroy_top=(False,0), destroy_hand=0, destroy_discard=0, destroy_hand_or_discard=0, puts_on_top=False, discard=0, op_discard=0, weakness=(False,0), defense=(False, 0), first_appearance=0):
        """
        takes a file path for an image that will be the face of the card
        and a pre-populated card_info namedtuple
        """
        self.img = pygame.image.load(image_name) # the image corresponding to the face of the card
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

    def inform(self):
        """return a text surface containing the information about the card (name, type, cost, power, draw, VPs, text)"""
        # the aforementioned text surface
        text = pygame.Surface((SCREEN_WIDTH, Card.font.get_linesize() * 7)) # as wide as the screen for 7 lines: name, type, cost, power, draw, VPs, text
        text.fill(GAME_BKG_COLOR) # get rid of text background
        linenum = 0
        for field in self.info._fields:
            # make a surface containing the text of this line ("Name: Aquaman's Trident" or "Type: Supervillain" or whatever)
            line = Card.font.render(" " + field + ": " + getattr(self.info, field), False, (255, 255, 255))
            text.blit(line, (0, Card.font.get_linesize() * linenum)) # draw the line onto the text at the appropriate line height
            linenum += 1
        return text
    
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
 = Card("cardimgs/imagename.jpg", cost=, power=(,), name="", vp=, type="Power", text="") #
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
#Raven = Card("cardimgs/imagename", card_info("Raven", "Hero", "3", "1", "1", "1", "")) #3
#Catwoman = Card("cardimgs/imagename", card_info("Catwoman", "Hero", "2", "2", "0", "1", "")) #2
#Katana = Card("cardimgs/imagename", card_info("Katana", "Hero", "2", "1", "D", "1", "")) #2    How to indicate defenses?
#Winged_Warrior = Card("cardimgs/imagename", card_info("Winged Warrior", "Hero", "6", "2", "0", "2", "If you play or have played another Hero this turn, additional +3 Power.")) #1
#Princess_Diana = Card("cardimgs/imagename", card_info("Princess Diana of Themyscira", "Hero", "7", "0", "0", "2", "Gain all Villains with cost 7 or less in the Line-Up.")) #1
#Power_Girl = Card("cardimgs/imagename", card_info("Power Girl", "Hero", "5", "3", "0", "2", "")) #3
#Hawkgirl = Card("cardimgs/imagename", card_info("Hawkgirl", "Hero", "2", "1", "0", "1", "+1 additional Power for each Hero in your discard pile.")) #2
#Kid_Flash = Card("cardimgs/imagename", card_info("Kid Flash", "Hero", "2", "0", "1", "1", "")) #2
#Supergirl = Card("cardimgs/imagename", card_info("Supergirl", "Hero", "4", "0", "0", "1", "You may put a Kick card from the Kick stack into your hand.")) #2
#Jonn_Jonnz = Card("cardimgs/imagename", card_info("J'onn J'onnz", "Hero", "6", "0", "0", "2", "Play the top card of the Super-Villain stack, then return it to the top of the stack.")) #1
#The_Fastest_Man_Alive = Card("cardimgs/imagename", card_info("The Fastest Man Alive", "Hero", "5", "0", "2", "1", "")) #1
#King_Of_Atlantis = Card("cardimgs/imagename", card_info("King of Atlantis", "Hero", "5", "1", "0", "1", "You may destroy a card in your discard pile. If you do, gain +2 additional Power")) #1

#HeroList = [Raven, Catwoman, Katana, Winged_Warrior, Princess_Diana, Power_Girl, Hawkgirl, Kid_Flash, Supergirl, Jonn_Jonnz, The_Fastest_Man_Alive, King_Of_Atlantis]

# VILLAINS
#Johnny_Quick = Card("cardimgs/imagename", card_info("Johnny Quick", "Villain", "2", "0", "1", "1", "")) #2
#Bane = Card("cardimgs/imagename", card_info("Bane", "Villain", "4", "2", "0", "1", "Attack: Each foe chooses and discards a card."))
#Mr_Zsasz = Card("cardimgs/imagename", card_info("Mr. Zsasz", "Villain", "3", "2", "0", "1", "Attack: Each foe reveals the top card of his deck. If its cost is odd, that player gains a Weakness."))
#Scarecrow = Card("cardimgs/imagename", card_info("Bane", "Villain", "5", "2", "0", "1", "Attack: Each foe gains a Weakness"))
#Doomsday = Card("cardimgs/imagename", card_info("Doomsday", "Villain", "6", "4", "0", "2", "")) #2
#Red_Lantern_Corps = Card("cardimgs/imagename", card_info("Red Lantern Corps", "Villain", "5", "1", "0", "1", "You may destroy a card in your hand. If you do, additional +2 Power.")) #2
#Lobo = Card("cardimgs/imagename", card_info("Lobo", "Villain", "7", "3", "0", "2", "You may destroy up to two cards in your hand and/or discard pile.")) #1
#Gorilla_Grod = Card("cardimgs/imagename", card_info("Gorilla Grod", "Villain", "5", "3", "0", "2", "")) #2
#Jervis_Tech = Card("cardimgs/imagename", card_info("Jervis Tech", "Villain", "3", "1", "0", "1", "Look at the top card of your deck. Destroy it or discard it.")) #2
#Killer_Croc = Card("cardimgs/imagename", card_info("Killer Croc", "Villain", "4", "2", "0", "1", "If you play or have played another Villain this turn, additional +1 Power.")) #2
#Two_Face = Card("cardimgs/imagename", card_info("Two-Face", "Villain", "2", "1", "0", "1", "Choose even or odd, then reveal the top card of your deck. If its cost matches your choice, draw it. If not, discard it.")) #2

#VillainList = [Johnny_Quick, Harley_Quinn, Cheetah, Doomsday, Red_Lantern_Corps, Lobo, Gorilla_Grod, Jervis_Tech, Killer_Croc, Two_Face]

# SUPER VILLAINS
#N = Card("cardimgs/imagename", card_info("N", "SVillain", "C", "P", "D", "V", "T"))


cards.append(Aquamans_Trident)

# make the game window
screen = pygame.display.set_mode(size=[SCREEN_WIDTH, SCREEN_HEIGHT])
pygame.display.set_caption(SCREEN_NAME)

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
    screen.fill(GAME_BKG_COLOR)
    for card in cards:
        # if the mouse is on this card
        if mouse_pos[0] > card.pos[0] and mouse_pos[1] > card.pos[1] and mouse_pos[0] < card.pos[0] + card.get_width() and mouse_pos[1] < card.pos[1] + card.get_height():
            info = card.inform()
            screen.blit(info, (0, SCREEN_HEIGHT - info.get_height()))
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

