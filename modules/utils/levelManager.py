import time
import os


class LevelManager(object):

    def __init__(self):
        '''Defaults to easy'''
        self._file = open(os.path.join('resources', 'easy.txt'), 'r')
        self._text = self._file.readlines()

    def setText(self, difficulty):
        self._file.close()
        self._file = open(os.path.join('resources', difficulty), 'r')
        self._text = self._file.readlines()

    def load(self, level):
        return self._text[level].rstrip()

    def update(self, enemiesText, enemies):
        return enemiesText == '' and enemies == []

    def getNumLevels(self):
        return len(self._text)
