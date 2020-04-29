###
# Brian Legarth
# Maze Wars
# particles.py
#
# These particles will be used to create the different
# types of attacks. Currently just going to work on the
# tracking type of attack. May choose to expand on this
# later.
###


from .drawable import Drawable
from .vector2D import Vector2
import random
import math
import pygame

"""A basic particle class from which all particles inherit. Applys linear movement."""


class Particle(Drawable):
    """Initializes a particle at the startPosition, making a copy of the startPosition
        to prevent cloning of the Vector2. Creates the pygame surface for drawing."""

    def __init__(self, startPosition, particleSize=(10, 10)):
        super().__init__("", Vector2(*startPosition))

        self._startPosition = Vector2(*startPosition)
        self._image = pygame.Surface(particleSize, pygame.SRCALPHA)

        self.timer = 0
        self.speed = Vector2(0, 0)

    def update(self, ticks, velX, velY):
        '''Updates the particle based on the given velocity and ticks'''
        self.timer += ticks

        self._position.x += velX * ticks
        self._position.y += velY * ticks

    def restart(self):
        '''Reuse the particle by returning to the start position'''
        self._position.x = self._startPosition.x
        self._position.y = self._startPosition.y

    def setVelocity(self, velocity, jitter=0.1):
        '''General setVelocity to force a small amount of jitter to any values.
        Less jitter means that the particles may "line up" eventually.'''
        self.speed.x = velocity.x * \
            ((random.random() * jitter * 2 - jitter) + 1 - jitter)
        self.speed.y = velocity.y * \
            ((random.random() * jitter * 2 - jitter) + 1 - jitter)


class TrackingParticle(Particle):
    '''This class uses the particle as a tracker to hit the nearest unit'''

    def __init__(self, startPosition, color, trackingObject, initialVelocity):
        super().__init__(startPosition)
        self._initialVelocity = initialVelocity
        self.restart()
        self._trackingObject = trackingObject
        pygame.draw.circle(self._image, color, (2, 2), 2)

    def restart(self, newPosition=None):
        '''Restarts the particle to set the velocity'''
        if newPosition != None:
            self._position = Vector2(*newPosition)
        self.setVelocity(
            Vector2(self._initialVelocity.x, self._initialVelocity.y))
        super().restart()

    def update(self, ticks, velX, velY):
        '''Updates the objects's position based on its current velocity and tracking point'''
        trackingLoc = self._trackingObject._centerPosition

        # Moves it closer to the target
        if self._position.x > trackingLoc.x:
            self._position.x -= self.speed.x * ticks
        elif self._position.x < trackingLoc.x:
            self._position.x += self.speed.x * ticks

        # Moves it closer to the target
        if self._position.y > trackingLoc.y:
            self._position.y -= self.speed.y * ticks
        elif self._position.y < trackingLoc.y:
            self._position.y += self.speed.y * ticks
