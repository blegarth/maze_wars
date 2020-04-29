
from ..drawable import Drawable
from ..vector2D import Vector2
import pygame
import os
import random

# When the pauser is enable it doesn't stop the time for the enemies to
# to spawn so they may spawn so they may spawn close to each other


class Pauser(Drawable):
    def __init__(self, screenSize):
        self._active = False
        super().__init__(os.path.join('images', 'paused.png'),
                         (screenSize[0] // 2, screenSize[1] // 2))
        self._position -= Vector2(*self.getSize()) // 2
        self._font = pygame.font.SysFont('Arial', 50)
        self._file = open(os.path.join('resources', 'tips.txt'), 'r')
        self._text = self._file.readlines()
        self._size = len(self._text) - 1
        self._currentTip = None

    def handleEvent(self, event):
        '''Pauses the game and gets a new tip'''
        if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
            if not self._active:
                self._currentTip = self.getTip()
            self._active = not self._active

    def draw(self, surface):
        if self._active:
            surface.blit(self._font.render(
                self._currentTip, False, (0, 0, 0)), (125, 350))
            super().draw(surface)

    def isActive(self):
        '''Checks to see if the pauser is active'''
        return self._active

    def getTip(self):
        '''Returns a random tip from the tip file'''
        return self._text[random.randint(0, self._size)].rstrip()
