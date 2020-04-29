###
# Brian Legarth
# Maze Wars
# grid.py
#
# This class controls the entire game board and whether
# and if anything can be placed on it to build more towers
# this class will include the findPath function that will
# create a path for enemies to get through the most
# efficiently. It will change everytime a new tower is placed
# on the board. The starting points on the board are (0,0) end
# is (19,14). The key for the different places are 0 is free,
# 1 is unbuildable (start and end location), 2 is a tower,
# 3 is out of bounds, and 4 is the goal.
###

import pygame
import collections

SCREEN_SIZE = (800, 800)
SPRITE_SIZE = 40


class Grid(object):
    def __init__(self, size):
        # creates the grid of the passed size
        self._grid = []
        for row in range(size[1]):
            self._grid.append([])
            for col in range(size[0]):
                # out of bounds
                if col >= 15:
                    self._grid[row].append(3)
                # Everything else is buildable
                else:
                    self._grid[row].append(0)
        # Sets the enemy starting location to be unbuildable
        self._grid[0][0] = 1
        self._grid[19][14] = 4

        self._path = self.findPath()

    def getStatus(self, loc):
        '''Returns the status of the grid space that 
        someone is trying to see if anything is in it'''
        return self._grid[loc[0]][loc[1]]

    def build(self, loc):
        '''Makes the grid space unavailable'''
        self._grid[loc[0]][loc[1]] = 2
        self._path = self.findPath()
        if self._path is None:
            self._grid[loc[0]][loc[1]] = 0
            self._path = self.findPath()
            return False
        return True

    def getGrid(self):
        '''Returns the grid'''
        return self._grid

    def getSquare(self, loc):
        '''Returns the index of the grid piece that was touched'''
        return (loc[0]//SPRITE_SIZE, loc[1]//SPRITE_SIZE)

    def getPath(self):
        '''Returns the path to get through'''
        return self._path

# https://stackoverflow.com/questions/47896461/get-shortest-path-to-a-cell-in-a-2d-array-python
# I decided to stick with this instead of going dijkstra's because of multiple reasons. The
# first being that I don't have to use dijkstra's because a path doesn't have to be updated
# super often only once in a while when a tower is added. The second being that there are
# no easy dijkstra's algorithm for the type of grid I am using. The third being this one
# works well so why fix it if it ain't broke :)
    def findPath(self):
        '''BFS to find the right path A* will be implemented soon'''
        queue = collections.deque([[(0, 0)]])
        seen = set([(0, 0)])
        while queue:
            path = queue.popleft()
            x, y = path[-1]
            if self._grid[y][x] == 4:
                return path
            for x2, y2 in ((x+1, y), (x-1, y), (x, y+1), (x, y-1)):
                if 0 <= x2 < 15 and 0 <= y2 < 20 and self._grid[y2][x2] != 2 and self._grid[y2][x2] != 3 and (x2, y2) not in seen:
                    queue.append(path + [(x2, y2)])
                    seen.add((x2, y2))
        return None
#################################
