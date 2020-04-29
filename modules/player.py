###
# Brian Legarth
# Final Project
# player.py
#
# This class controls whether or not the person can
# create different towers throughout the maze. They
# will gain money when they kill different shapes
# and they will lose money when they buy towers.
###

import pygame
from .drawable import Drawable


class Player(Drawable):
    def __init__(self, money, lives):
        self._money = money
        self._lives = lives
        self._living = True
        self._towers = []
        self._font = pygame.font.SysFont('Arial', 50)
        self._text = self._font.render(
            '$' + str(self._money) + ' Lives:' + str(self._lives), False, (0, 0, 0))

    def updateMoney(self, amount):
        '''Increments the money'''
        self._money += amount
        self.updateText()

    def decLives(self):
        '''Decreases lives and kills the person if he is out 
        of lives'''
        self._lives -= 1
        if self._lives == 0:
            self._living = False
        self.updateText()

    def isAlive(self):
        '''Checks to see if the player still has lives'''
        return self._living

    def getMoney(self):
        '''Returns the money'''
        return self._money

    def getLives(self):
        '''Returns the lives'''
        return self._lives

    def updateText(self):
        '''Changes the text'''
        self._text = self._font.render(
            '$' + str(self._money) + ' Lives: ' + str(self._lives), False, (0, 0, 0))

    def draw(self, screen):
        '''Draws the info'''
        screen.blit(self._text, (0, 600))

    def getTowers(self):
        '''Returns the tower'''
        return self._towers

    def getTowerType(self, index):
        '''Returns the tower type'''
        return type(self._towers[index])

    def buyTower(self, towerType, prevLocation, prevSqloc):
        '''Buys and places a new tower in that location'''
        self.updateMoney(-towerType.cost)
        new = towerType(prevLocation)
        self._towers.append(new)

    def selectTower(self, gridSpot):
        '''Returns the index of the tower selected'''
        for x in range(len(self._towers)):
            if self._towers[x].getGridSpot() == gridSpot:
                return x
        return -1

    def upgradeTower(self, index):
        '''Upgrades a tower if possible'''
        if self._towers[index].canUpgrade() and self.getMoney() > type(self._towers[index]).cost:
            self.updateMoney(-type(self._towers[index]).cost)
            self._towers[index].upgrade()
