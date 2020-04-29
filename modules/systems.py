###
# Brian Legarth
# Maze Wars
# systems.py
#
# These systems will be used to create the different
# types of attacks. UPDATE: All of the towers will use
# the tracking system because its the coolest and looks
# the best.
###


from .vector2D import Vector2
from .particles import *
import random
import time

SCREEN_SIZE = Vector2(800, 800)


class TrackingSystem(object):
    '''Shoots a particle at any unit in the nearby area'''

    def __init__(self, position, maxParticles, color, cooldown, trange, initialVelocity, frequency=0.03):
        self._particles = []
        self._position = Vector2(*position)
        self._max = maxParticles
        self._cooldown = cooldown
        self._initialVelocity = initialVelocity
        self._frequency = frequency
        self._particleType = TrackingParticle
        self._color = color
        self._trange = trange
        self._activeArea = self.buildRect()
        self._starttime = time.time()

    def upgrade(self):
        '''Levels up the tower'''
        self._max = int(self._max * 1.25)
        self._cooldown = self._cooldown / 2
        self._particles = []

    def update(self, ticks, objectsNearby):
        '''Updates all existing particles. If one has died add another
        particle if there is space'''
        if self._max > len(self._particles):
            for obj in objectsNearby:
                if time.time() - self._starttime > 0.04:
                    self._starttime = time.time()
                    self._particles.append(self._particleType(
                        self.getPosition(), self._color, obj, self._initialVelocity))

        for particle in self._particles:
            if self._activeArea.collidepoint(*particle._position) and not particle._trackingObject.isDead():
                velX = self._xMove(particle)
                velY = self._yMove(particle)

                particle.update(ticks, velX, velY)
            else:
                self._particles.remove(particle)

    def draw(self, screen):
        '''Invokes Drawable's draw for each particle in the system'''
        for p in self._particles:
            p.draw(screen)

    def _yMove(self, particle):
        '''Returns the particle speed on the y axis'''
        return particle.speed.y

    def _xMove(self, particle):
        '''Returns the particle speed on the x axis'''
        return particle.speed.x

    def getPosition(self):
        '''Returns the position'''
        return self._position

    def getParticles(self):
        '''Returns the locations of all the particles'''
        return self._particles

    def buildRect(self):
        shortx = False
        shorty = False

        # Checks to make sure the x range doesnt go past 0
        if self._position.x - self._trange <= 0:
            xbound = 0
            shortx = True
        else:
            xbound = self._position.x - self._trange

        # Checks to make sure the y range doesnt go past 0
        if self._position.y - self._trange <= 0:
            ybound = 0
            shorty = True
        else:
            ybound = self._position.y - self._trange

        # Checks to make sure the x range doesnt go past the screen size
        if shortx:
            xsize = self._position.x + self._trange
        else:
            if xbound + self._trange * 2 > SCREEN_SIZE.x:
                xsize = SCREEN_SIZE.x
            else:
                xsize = xbound + self._trange * 2

        # Checks to make sure the y range doesnt go past the screen size
        if shorty:
            ysize = self._position.y + self._trange
        else:
            if ybound + self._trange * 2 > SCREEN_SIZE.y:
                ysize = SCREEN_SIZE.y
            else:
                ysize = ybound + self._trange * 2

        return pygame.Rect(xbound, ybound, xsize, ysize)
