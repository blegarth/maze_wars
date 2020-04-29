###
# Brian Legarth
# Final Project
# tower.py
#
# This class controls everything about the towers. This creates towers
# draws them in the correct position and has a specific type cost there
# are three different towers: a short range tower (square), a long range
# tower (triangle), and a special tower (probably a heart). Each one has
# two upgrades that will increase the power and/or range.
###

import pygame
from .drawable import Drawable
from .vector2D import Vector2
from .systems import TrackingSystem


SPRITE_SIZE = 40
SCREEN_SIZE = Vector2(800, 800)
PARTICLE_START_SPEED = Vector2(200, 200)

SHORT_RANGE = 100
SHORT_MAX = 10
SHORT_COST = 10

LONG_RANGE = 150
LONG_MAX = 20
LONG_COST = 50

SPECIAL_RANGE = 200
SPECIAL_MAX = 50
SPECIAL_COST = 100


class Tower(Drawable):
    cost = 0

    def __init__(self, position, rect, psystem):
        # changes location from tuple to Vector2
        position = Vector2(position[0], position[1])
        self._rect = rect
        self._level = 0
        self._gridSpot = (position[0]//SPRITE_SIZE, position[1]//SPRITE_SIZE)
        self._psystem = psystem
        self._canShoot = True
        super().__init__('images/shapes.png', position, self._rect)

    def update(self, worldInfo, ticks, objectsNearby):
        '''Updates the objects's position based on its current velocity'''
        self._psystem.update(ticks, objectsNearby)

    def upgrade(self):
        '''Upgrades you to the next tower and increases level'''
        self._level += 1
        self._rect.top = self._level * SPRITE_SIZE
        self.changeImage(self._rect)
        self._psystem.upgrade()

    def canUpgrade(self):
        '''Checks to see if the tower can be upgraded'''
        return self._level < 2

    def draw(self, screen):
        '''Draws the tower and the particles'''
        self._psystem.draw(screen)
        super().draw(screen)

    def simulate(self):
        self._psystem.simulate()

    def getGridSpot(self):
        '''Returns the grid location of the tower'''
        return self._gridSpot

    def getParticles(self):
        '''Returns all the particles that are attached to this tower'''
        return self._psystem.getParticles()

    def checkEnemy(self, enemy):
        '''Checks to see if the enemy is close enough'''
        return self._psystem._activeArea.collidepoint(*enemy._position)


class ShortTower(Tower):
    '''This is for the short range higher powered tower'''
    cost = SHORT_COST

    def __init__(self, position):
        rect = pygame.Rect(SPRITE_SIZE, 0, SPRITE_SIZE, SPRITE_SIZE)
        sysloc = Vector2(position[0] + 15,
                         position[1] + 15)
        color = pygame.Color(255, 255, 0, 150)

        # Tracking system
        psystem = TrackingSystem(sysloc, SHORT_MAX, color, 2,
                                 SHORT_RANGE, PARTICLE_START_SPEED)
        super().__init__(position, rect, psystem)


class LongTower(Tower):
    '''This is for the long range lower powered tower'''
    cost = LONG_COST

    def __init__(self, position):
        rect = pygame.Rect(SPRITE_SIZE * 2, 0, SPRITE_SIZE, SPRITE_SIZE)
        sysloc = Vector2(position[0] + 15,
                         position[1] + 15)
        color = pygame.Color(255, 0, 0, 150)

        # Tracking system
        psystem = TrackingSystem(sysloc, LONG_MAX, color, 2,
                                 LONG_RANGE, PARTICLE_START_SPEED)
        super().__init__(position, rect, psystem)


class SpecialTower(Tower):
    '''This is for the longer range highest powered tower'''
    cost = SPECIAL_COST

    def __init__(self, position):
        rect = pygame.Rect(SPRITE_SIZE * 3, 0, SPRITE_SIZE, SPRITE_SIZE)
        sysloc = Vector2(position[0] + 15,
                         position[1] + 15)
        color = pygame.Color(0, 255, 0, 150)

        # Tracking system
        psystem = TrackingSystem(sysloc, SPECIAL_MAX, color, 2,
                                 SPECIAL_RANGE, PARTICLE_START_SPEED)
        super().__init__(position, rect, psystem)
