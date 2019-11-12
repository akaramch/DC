"""
Potential first iteration of the GUI?
Created mostly for purposes of learning pygame
"""

import pygame
pygame.init()
from collections import namedtuple
from cards import *

# window dimensions
SCREEN_WIDTH = 1500
SCREEN_HEIGHT = 1020
# background color for the whole screen
GAME_BKG_COLOR = (127, 127, 127)

# make the game window
screen = pygame.display.set_mode(size=[SCREEN_WIDTH, SCREEN_HEIGHT])

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

