###
# Brian Legarth
# Final Project
# enemy.py
#
# This class controls about enemies. Each enemy will start at the same
# position and will progress on the same path that is discovered with
# dijkstras algorithm in the grid class.
###

import pygame
import random
from .drawable import Drawable
from .vector2D import Vector2


SPRITE_SIZE = 32
ENEMY_VELOCITY = Vector2(175, 175)


class Enemy(Drawable):
    def __init__(self, position, health, level, path, flying=False):
        rect = pygame.Rect(level * SPRITE_SIZE, 0, SPRITE_SIZE, SPRITE_SIZE)
        self._velocity = ENEMY_VELOCITY
        self._health = health
        self._path = path
        self._pathIndex = 0
        self.updatePath(self._path)
        self._reward = self._health * 10

        self._flying = flying
        self._dead = False
        super().__init__('images/orbs.png', position, rect)
        self._centerPosition = Vector2(
            self._position.x + 20, self._position.y + 20)
        self._hitBox = pygame.Rect(
            self._position.x + 5, self._position.y + 5, SPRITE_SIZE - 10, SPRITE_SIZE - 10)

    def update(self, worldInfo, ticks):
        '''Updates the objects's position based on its current velocity and path'''
        # Checks to see which way the path goes on the x axis
        if self._position.x > self._path[self._pathIndex][1] + 4:
            self._position.x -= self._velocity.x * ticks
        elif self._position.x < self._path[self._pathIndex][1] - 4:
            self._position.x += self._velocity.x * ticks

        # Checks to see which way the path goes on the y axis
        if self._position.y > self._path[self._pathIndex][0] + 4:
            self._position.y -= self._velocity.y * ticks
        elif self._position.y < self._path[self._pathIndex][0] - 4:
            self._position.y += self._velocity.y * ticks

        # Checks to make sure it isnt at the end of the size of the path
        if (self._position.x <= self._path[self._pathIndex][1] + 4) and \
            (self._position.x >= self._path[self._pathIndex][1] - 4) and \
            (self._position.y <= self._path[self._pathIndex][0] + 4) and \
                (self._position.y >= self._path[self._pathIndex][0] - 4):
            if self._pathIndex < len(self._path) - 1:
                self._pathIndex += 1

        # Updates the center position so that the bullets can track it
        self._centerPosition = Vector2(
            self._position.x + 20, self._position.y + 20)

        # Updates the hit box for the enemy
        self._hitBox = pygame.Rect(
            self._position.x + 5, self._position.y + 5, SPRITE_SIZE - 10, SPRITE_SIZE - 10)

    def isDead(self):
        '''Returns the _dead variable'''
        return self._dead

    def kill(self):
        '''Kills the enemy'''
        self._dead = True

    def getHit(self):
        '''This happens when the enemy gets hit by a particle'''
        self._health -= 1
        if self._health <= 0:
            self._dead = True

    def getHealth(self):
        '''Returns the health'''
        return self._health

    def getReward(self):
        '''Returns the reward for killing it'''
        return self._reward

    def updatePath(self, path):
        '''Updates the path'''
        tempPath = []

        for x in range(len(path)):
            # This normalizes it to pixels rather than grid locations
            # and positions it to be the middle of the square so that
            # these path points will now serve as waypoints
            tempPath.append((path[x][0] * 40 + 4, path[x][1] * 40 + 4))
        self._path = tempPath
        if self._pathIndex > 0:
            self._pathIndex += 1

    def getCollideRect(self):
        '''Returns a Rect variable representing the collision area of the current object'''
        return self._hitBox
