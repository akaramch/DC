"""Everything to do with the DC player's cards: the class, the info namedtuple, and all the lists of specific cards"""

import pygame
pygame.init() # I don't know why I have to do this but StackOverflow told me to

"""
card class
__init__(image_name, name, type, cost, power, draw, vp, text): loads card face image and info namedtuple
get_width(), get_height(): get width and height of card face image
move(dx, dy): move the card by that distance
inform(): returns a text pygame.surface that shows the info namedtuple in text form
"""
class Card:
    font = pygame.font.SysFont("jamrul", 24) # the font to be used to write all things card-related

    def __init__(self, image_name, info):
        """
        takes a file path for an image that will be the face of the card
        and a pre-populated card_info namedtuple
        """
        self.img = pygame.image.load(image_name) # the image corresponding to the face of the card
        self.info = info # will be read from DCCardsList below
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

# EQUIPMENT
Aquamans_Trident = Card("cardimgs/aquamanstrident.jpg", card_info("Aquaman's Trident", "Equipment", "3", "2", "0", "1", "You may put any one card you buy or gain this turn on top of your deck.")) #3
#Batarang = Card("cardimgs/imagename", card_info("Batarang", "Equipment", "2", "2", "0", "1", "")) #2
#Soultaker_Sword = Card("cardimgs/imagename", card_info("Soultaker Sword", "Equipment", "4", "2", "0", "1", "You may destroy a card in your hand.")) #3
#Legion_Flight_Ring = Card("cardimgs/imagename", card_info("Legion Flight Ring", "Equipment", "2", "0", "1", "1", "")) #2
#Lasso_of_Truth = Card("cardimgs/imagename", card_info("Lasso of Truth", "Equipment", "2", "1", "0", "1", "Defense: You may discard this card to avoid an Attack. If you do, draw a card.")) #2    Defense
#Power_Ring = Card("cardimgs/imagename", card_info("Power Ring", "Equipment", "3", "2", "0", "1", "Reveal the top card of your deck. If its cost is 1 or greater, additional +1 Power.")) #3
#Nth_Metal = Card("cardimgs/imagename", card_info("Nth Metal", "Equipment", "3", "1", "0", "1", "Look at the top card of your deck. You may destroy it.")) #3
#White_Lantern_Power_Battery = Card("cardimgs/imagename", card_info("White Lantern Power Battery", "Equipment", "7", "0", "0", "2", "Gain all Power Rings from the Line-Up and put them into your hand. Then gain any card from the Line-Up and put it on top of your deck.")) #1

#EquipmentList = [Aquamans_Trident, Batarang, Soultaker_Sword, Legion_Flight_Ring, Lasso_of_Truth, Power_Ring, Nth_Metal, White_Lantern_Power_Battery]

# SUPER POWERS
#Shazam = Card("cardimgs/imagename", card_info("Shazam!", "Power", "7", "2", "0", "2", "Reveal and play the top card of the main deck, then return it to the top of the main deck.")) #1
#Super_Strength = Card("cardimgs/imagename", card_info("Super Strength", "Power", "7", "5", "0", "2", "")) #2
#Starbolt = Card("cardimgs/imagename", card_info("Starbolt", "Power", "5", "2", "0", "1", "+1 additional Power for each Super Power in your discard pile.")) #3
#Force_Field = Card("cardimgs/imagename", card_info("Force Field", "Power", "3", "0", "1", "1", "Ongoing: Do not discard this card at the end of your turn. Defense: While this card is in play, you may put it into your discard pile to avoid an Attack.")) #2     Defense  Ongoing
#Giant_Growth = Card("cardimgs/imagename", card_info("Giant Growth", "Power", "2", "2", "0", "1", "")) #2
#X_Ray_Vision = Card("cardimgs/imagename", card_info("X-Ray Vision", "Power", "3", "0", "0", "1", "Each foe reveals the top card of their deck. Choose a non-Location card revealed this way, play it, then return it to the top of its owner's deck.")) #1
#Ultra_Strength = Card("cardimgs/imagename", card_info("Ultra Strength", "Power", "9", "3", "2", "3", "")) #1
#Heat_Vision = Card("cardimgs/imagename", card_info("Heat Vision", "Power", "6", "3", "0", "2", "You may destroy a card in your hand or discard pile.")) #3

#PowerList = [Shazam, Super_Strength, Starbolt, Force_Field, Giant_Growth, X_Ray_Vision, Ultra_Strength, Heat_Vision]

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
#Harley_Quinn = Card("cardimgs/imagename", card_info("Harley Quinn", "Villain", "2", "1", "0", "1", "Attack: Each foe puts a Punch or Vulnerability from their discard pile on top of their deck.")) #2
#Cheetah = Card("cardimgs/imagename", card_info("Cheetah", "Villain", "2", "0", "0", "1", "Gain any card with cost 4 or less from the Line-Up.")) #2
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

