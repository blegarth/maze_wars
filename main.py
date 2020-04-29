##
# Brian Legarth
# Project 2
# main.py
#
# In this project a creator makes a path of towers to defeat the
# awful shapes.
###

import pygame
import sys
import os
from modules.vector2D import Vector2
from modules.drawable import Drawable
from modules.utils.gameManager import GameManager

# Set the constants
SCREEN_SIZE = (800, 800)


def main():
    # Initialize everything needed
    pygame.init()
    pygame.font.init()

    pygame.display.set_caption('Maze Wars')

    screen = pygame.display.set_mode(SCREEN_SIZE)

    # Background loading
    background = pygame.image.load('images/background.png').convert()

    clock = pygame.time.Clock()
    game = GameManager(SCREEN_SIZE)

    RUNNING = True

    while RUNNING:

        # Flip the display to monitor
        pygame.display.flip()

        # Tick the clock
        clock.tick(60)
        ticks = min(0.04, clock.get_time() / 1000)

        # Draw background for the grid and the choosing area
        screen.blit(background, (0, 0))

        # Draw the game
        game.draw(screen)

        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            # exit case
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and
                                             event.key == pygame.K_ESCAPE):
                RUNNING = False
            else:
                game.handleEvent(event)

        # update
        game.update(clock, ticks, SCREEN_SIZE)


if __name__ == "__main__":
    main()
