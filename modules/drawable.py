###
# Brian Legarth
# Final Project
# drawable.py
#
# This class is the parent class for the tower and enemies. With this one
# the window offset is no longer useful because everything will
# contained on one screen.
###

import pygame
import random
from .vector2D import Vector2

# Set the constants
SCREEN_SIZE = (800, 800)


class Drawable(object):

    def __init__(self, imageName, position, rect=None):
        # Sets up everything with the image whenever a new instance is
        # created
        self._imageName = imageName
        if imageName != '':
            self._load_image = pygame.image.load(imageName).convert()

            if rect is not None:
                self._image = pygame.Surface((rect.width, rect.height))
                self._image.blit(self._load_image, (0, 0), rect)
            else:
                image_size = self._load_image.get_size()
                self._image = pygame.Surface(image_size)
                self._image.blit(self._load_image, (0, 0), pygame.Rect(
                    0, 0, image_size[0], image_size[1]))
            self._image.set_colorkey(self._load_image.get_at((0, 0)))
        self._position = Vector2(position[0], position[1])

    def getPosition(self):
        '''Returns the current position'''
        return self._position

    def setPosition(self, newPosition):
        self._position = newPosition

    def getX(self):
        '''Returns the X coordinate of the current position'''
        return self._position.x

    def getY(self):
        '''Returns the Y coordinate of the current position'''
        return self._position.y

    def getSize(self):
        '''Returns the size of the image surface'''
        return self._image.get_size()

    def getWidth(self):
        '''Returns the width of the image surface'''
        return self._image.get_size()[0]

    def getHeight(self):
        '''Returns the height of the image surface'''
        return self._image.get_size()[1]

    def getCollideRect(self):
        '''Returns a Rect variable representing the collision area of the current object'''
        return self._position + self._image.get_rect()

    def changeImage(self, rect):
        '''Changes the image to an updated one'''
        self._image.blit(self._load_image, (0, 0), rect)

    def draw(self, screen):
        '''Draws its image at the current position on the given surface'''
        screen.blit(self._image, (self.getX(), self.getY()))
