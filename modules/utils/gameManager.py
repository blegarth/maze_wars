###
# Brian Legarth
# gameManager.py
#
# This class manages the entire game including picking
# the levels and whether or not the game is paused.
###

import pygame
import sys
import time
from modules.grid import Grid
from modules.player import Player
from modules.tower import ShortTower, LongTower, SpecialTower
from modules.vector2D import Vector2
from modules.enemy import Enemy
from .soundManager import SoundManager
from .pauser import Pauser
from .levelManager import LevelManager
from .gameFSM import GameState

SCREEN_SIZE = (800, 800)
SQUARE_SIZE = 40
SPRITE_SIZE = 40
ARROW_SIZE = 32
GRID_SIZE = (20, 20)
SELECTOR_ZONE = (0, 600, 800, 200)
LIVES = 20
ENEMY_HEALTH = [10, 30, 50, 100, 300, 500, 700, 1000, 1400, 2000]
STARTING_MONEY = 1500

# Left to do:
# - Maybe the price underneath too
# - Have a better selection area for difficulty
# - Create the winning screen


class GameManager(object):

    def __init__(self, screenSize):
        self._pauser = Pauser(screenSize)
        self._level = LevelManager()
        self._FSM = GameState()
        self._currentLevel = 0
        self.player = Player(STARTING_MONEY, LIVES)
        self.grid = Grid(GRID_SIZE)
        self.enemies = []
        self.tSelector = False
        self.uSelector = False
        self.prevLocation = None
        self.prevSqloc = None
        self.levelDone = False
        self.totalLevels = None
        self.enemiesText = self._level.load(self._currentLevel)
        self.starttime = time.time()
        self.difficulty = None
        self.font = pygame.font.SysFont('Arial', 25)
        self.startingFont = pygame.font.SysFont('Arial', 120)
        self.bigFont = pygame.font.SysFont('Arial', 300)
        self.text = 'Level ' + str(self._currentLevel) + \
            ' Enemies left to come: ' + str(len(self.enemiesText))

        # made with wordart.com
        # gets all of the title screen pictures
        self.title = pygame.image.load('images/title.png').convert()
        self.title.set_colorkey(self.title.get_at((0, 0)))
        self.title = pygame.transform.scale(self.title, (800, 400))

        # taken from google.com
        self.selectorBackground = pygame.image.load(
            'images/pixel.png').convert()
        self.selectorBackground = pygame.transform.scale(
            self.selectorBackground, (200, 200))

        # setting up all the upgrade tower buttons
        # All art work was taken from Professor Matthews slides
        self.towerPics = pygame.image.load('images/shapes.png').convert()
        self.shortimage = pygame.Surface((SPRITE_SIZE, SPRITE_SIZE))
        self.longimage = pygame.Surface((SPRITE_SIZE, SPRITE_SIZE))
        self.specialimage = pygame.Surface((SPRITE_SIZE, SPRITE_SIZE))

        self.shortimage.blit(self.towerPics, (0, 0), pygame.Rect(
            SPRITE_SIZE, 0, SPRITE_SIZE, SPRITE_SIZE))
        self.longimage.blit(self.towerPics, (0, 0), pygame.Rect(
            SPRITE_SIZE * 2, 0, SPRITE_SIZE, SPRITE_SIZE))
        self.specialimage.blit(self.towerPics, (0, 0), pygame.Rect(
            SPRITE_SIZE * 3, 0, SPRITE_SIZE, SPRITE_SIZE))

        self.shortimage = pygame.transform.scale(
            self.shortimage, (SPRITE_SIZE * 2, SPRITE_SIZE*2))
        self.longimage = pygame.transform.scale(
            self.longimage, (SPRITE_SIZE * 2, SPRITE_SIZE*2))
        self.specialimage = pygame.transform.scale(
            self.specialimage, (SPRITE_SIZE * 2, SPRITE_SIZE*2))

        self.shortimage.set_colorkey(self.towerPics.get_at((0, 0)))
        self.longimage.set_colorkey(self.towerPics.get_at((0, 0)))
        self.specialimage.set_colorkey(self.towerPics.get_at((0, 0)))

        # setting up the upgrade and cancel buttons
        # All art work was taken from Professor Matthews slides
        self.arrows = pygame.image.load('images/arrows.png').convert()
        self.upgradeimage = pygame.Surface((ARROW_SIZE, ARROW_SIZE))
        self.cancelimage = pygame.Surface((ARROW_SIZE, ARROW_SIZE))

        self.upgradeimage.blit(self.arrows, (0, 0), pygame.Rect(
            0, 0, ARROW_SIZE, ARROW_SIZE))
        self.cancelimage.blit(self.arrows, (0, 0), pygame.Rect(
            ARROW_SIZE * 3, 0, ARROW_SIZE, ARROW_SIZE))

        self.upgradeimage = pygame.transform.scale(
            self.upgradeimage, (SPRITE_SIZE * 2, SPRITE_SIZE*2))
        self.cancelimage = pygame.transform.scale(
            self.cancelimage, (SPRITE_SIZE, SPRITE_SIZE))

        self.upgradeimage.set_colorkey(self.arrows.get_at((0, 0)))
        self.cancelimage.set_colorkey(self.arrows.get_at((0, 0)))

        # starts the music
        # this song was taken from YouTube
        SoundManager.getInstance().togglePlayMusic("mega-man-2.mp3", -1)

    def draw(self, screen):
        if self._FSM in ['begin', 'paused', 'running']:
            # Selector zone for making decisions about
            for x in range(4):
                screen.blit(self.selectorBackground, (x * 200, 600))

            # These zones can't be touched. If an enemy reaches the second one a
            # life is decreased
            pygame.draw.rect(screen, (0, 255, 0),
                             (0, 0, SQUARE_SIZE, SQUARE_SIZE), 3)
            pygame.draw.rect(screen, (255, 0, 0), (SQUARE_SIZE * (
                GRID_SIZE[0]-1), SQUARE_SIZE * (GRID_SIZE[1]-6), SQUARE_SIZE, SQUARE_SIZE), 3)

            if self.tSelector:
                # Starts the selection phase
                pygame.draw.rect(
                    screen, (255, 255, 0), (self.prevLocation[0], self.prevLocation[1], SQUARE_SIZE, SQUARE_SIZE), 1)

                # Selector for the short tower
                screen.blit(self.shortimage,
                            (5 * SQUARE_SIZE, 16 * SQUARE_SIZE))
                # Selector for the long tower
                screen.blit(self.longimage,
                            (8 * SQUARE_SIZE, 16 * SQUARE_SIZE))
                # Selector for the special tower
                screen.blit(self.specialimage,
                            (11 * SQUARE_SIZE, 16 * SQUARE_SIZE))
                # Selector for cancel button
                screen.blit(self.cancelimage,
                            (15 * SQUARE_SIZE, 17 * SQUARE_SIZE))

            if self.uSelector:
                # Starts the selection phase
                pygame.draw.rect(
                    screen, (255, 255, 0), (self.prevLocation[0], self.prevLocation[1], SQUARE_SIZE, SQUARE_SIZE), 1)
                # Selector for the upgrade button
                screen.blit(self.upgradeimage,
                            (5 * SQUARE_SIZE, 16 * SQUARE_SIZE))
                # Selector for cancel button
                screen.blit(self.cancelimage,
                            (15 * SQUARE_SIZE, 17 * SQUARE_SIZE))

            # draws the enemies
            if self.enemies:
                for enemy in self.enemies:
                    enemy.draw(screen)

            # draws the towers
            for tower in self.player.getTowers():
                tower.draw(screen)
            self.player.draw(screen)

            screen.blit(self.font.render(
                self.text, False, (0, 0, 0)), (0, 775))

        if self._FSM == 'paused':
            self._pauser.draw(screen)

        if self._FSM == 'title':
            screen.blit(self.title, (0, 0))
            # Selector zone for making decisions about
            for x in range(4):
                screen.blit(self.selectorBackground, (x * 200, 600))

            text = self.startingFont.render(
                'E', False, (0, 0, 0))
            screen.blit(text, (220, 650))
            text = self.startingFont.render(
                'M', False, (0, 0, 0))
            screen.blit(text, (340, 650))
            text = self.startingFont.render(
                'H', False, (0, 0, 0))
            screen.blit(text, (460, 650))

        if self._FSM == 'begin':
            text = self.font.render(
                'Press the space bar to begin level 1', False, (0, 0, 0))
            screen.blit(text, (0, 750))
            if not self.totalLevels:
                self.totalLevels = self._level.getNumLevels()

        if self._FSM == 'end':
            if self.player.isAlive():
                screen.blit(self.bigFont.render(
                    'WIN', False, (0, 255, 0)), (100, 100))
            else:
                screen.blit(self.bigFont.render(
                    'LOSE', False, (255, 0, 0)), (100, 100))
            text = self.font.render(
                'Click escape to exit the game', False, (0, 0, 0))
            screen.blit(text, (0, 775))

    def handleEvent(self, event):
        if self._FSM == 'title':
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if pygame.Rect(220, 650, 80, 80).collidepoint(event.pos):

                    # if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                    # Selecting easy mode
                    self._level.setText('easy.txt')
                    self.difficulty = 'easy'
                    SoundManager.getInstance().stopMusic()
                    # this song was taken from YouTube
                    SoundManager.getInstance().togglePlayMusic("glorious-morning.mp3", -1)
                    self._FSM.manageState('start')

                if pygame.Rect(340, 650, 80, 80).collidepoint(event.pos):
                    # Selecting medium mode
                    self._level.setText('medium.txt')
                    self.difficulty = 'medium'
                    SoundManager.getInstance().stopMusic()
                    # this song was taken from YouTube
                    SoundManager.getInstance().togglePlayMusic("glorious-morning.mp3", -1)
                    self._FSM.manageState('start')

                if pygame.Rect(460, 650, 80, 80).collidepoint(event.pos):
                    # Selecting hard mode
                    self._level.setText('hard.txt')
                    self.difficulty = 'hard'
                    SoundManager.getInstance().stopMusic()
                    # this song was taken from YouTube
                    SoundManager.getInstance().togglePlayMusic("glorious-morning.mp3", -1)
                    self._FSM.manageState('start')

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_d:
                # Selecting demo mode
                self._level.setText('demo.txt')
                self.difficulty = 'demo'
                self.player.updateMoney(10000)
                SoundManager.getInstance().stopMusic()
                # this song was taken from YouTube
                SoundManager.getInstance().togglePlayMusic("glorious-morning.mp3", -1)
                self._FSM.manageState('start')

        if self._FSM == 'begin':
            # This is the build phase before the first level starts
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self._FSM.manageState('start')

        if self._FSM == 'end':
            # This ends the game and exits the program because I havent figured
            # how to restart the GameManager
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                sys.exit()

        if self._FSM == "paused":
            # Pause menu
            self._pauser.handleEvent(event)

            if not self._pauser.isActive():
                self._FSM.manageState("unpause")

        elif self._FSM in ['begin', 'running']:
            self._pauser.handleEvent(event)
            if self._pauser.isActive():
                self._FSM.manageState("pause")
            else:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    sqlocation = self.grid.getSquare(event.pos)
                    location = (sqlocation[0] * SQUARE_SIZE,
                                sqlocation[1] * SQUARE_SIZE)
                    if sqlocation[1] > 14 and (self.tSelector or self.uSelector) and self.prevLocation:
                        # This begins the selector phase which lets you chose a new tower
                        # to put into that location
                        if self.grid.getStatus(self.prevSqloc) == 0:
                            if sqlocation >= (5, 16) and sqlocation < (7, 18) and self.player.getMoney() > 10:
                                # Selection for the short tower
                                if self.grid.build(self.prevSqloc):
                                    # checks to see if the path is blocked if something is built there
                                    self.player.buyTower(
                                        ShortTower, self.prevLocation, self.prevSqloc)
                                    path = self.grid.getPath()
                                    # If a new tower was built the path changes for all enemies
                                    for x in self.enemies:
                                        x.updatePath(path)
                                self.tSelector = False
                                self.prevLocation = None
                                self.prevSqloc = None

                            elif sqlocation >= (8, 16) and sqlocation < (10, 18) and self.player.getMoney() > 20:
                                # Selection for the long tower
                                if self.grid.build(self.prevSqloc):
                                    # checks to see if the path is blocked if something is built there
                                    self.player.buyTower(
                                        LongTower, self.prevLocation, self.prevSqloc)
                                    path = self.grid.getPath()
                                    # If a new tower was built the path changes for all enemies
                                    for x in self.enemies:
                                        x.updatePath(path)
                                self.tSelector = False
                                self.prevLocation = None
                                self.prevSqloc = None

                            elif sqlocation >= (11, 16) and sqlocation < (13, 18) and self.player.getMoney() > 200:
                                # Selection for the special tower
                                if self.grid.build(self.prevSqloc):
                                    # checks to see if the path is blocked if something is built there
                                    self.player.buyTower(
                                        SpecialTower, self.prevLocation, self.prevSqloc)
                                    path = self.grid.getPath()
                                    # If a new tower was built the path changes for all enemies
                                    for x in self.enemies:
                                        x.updatePath(path)
                                self.grid.build(self.prevSqloc)
                                self.tSelector = False
                                self.prevLocation = None
                                self.prevSqloc = None

                            elif sqlocation == (15, 17):
                                # Cancel button
                                self.tSelector = False
                                self.prevLocation = None
                                self.prevSqloc = None

                        elif self.grid.getStatus(self.prevSqloc) == 2 and self.uSelector:
                            # this begins the upgradable phase, if a tower is able to be
                            # upgraded and the player has enough money the tower that is
                            # selected will be upgraded
                            if sqlocation >= (5, 16) and sqlocation < (7, 18) and self.player.getMoney() > 10:
                                # upgrade the tower
                                towerIndex = self.player.selectTower(
                                    self.prevSqloc)
                                towerType = self.player.getTowerType(
                                    towerIndex)
                                self.player.upgradeTower(towerIndex)
                                self.uSelector = False
                                self.prevLocation = None
                                self.prevSqloc = None

                            elif sqlocation == (15, 17):
                                # Cancel button
                                self.uSelector = False
                                self.prevLocation = None
                                self.prevSqloc = None
                        else:
                            # If the grid is already blocked and its not a tower
                            self.tSelector = False
                            self.prevLocation = False
                            self.prevSqloc = False
                    elif self.grid.getStatus(sqlocation) == 0 and sqlocation[1] < 15:
                        # If the player clicks on an empty space
                        self.uSelector = False
                        self.tSelector = True
                        self.prevLocation = location
                        self.prevSqloc = sqlocation

                    elif self.grid.getStatus(sqlocation) == 2 and sqlocation[1] < 15 and self.uSelector == False:
                        # If the player clicks on a built tower is trying to upgrade it
                        self.uSelector = True
                        self.tSelector = False
                        self.prevLocation = location
                        self.prevSqloc = sqlocation

                if self.levelDone and event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                    self._FSM.manageState("nextLevel")

    def update(self, clock, ticks, screenSize):
        if self._FSM == 'running':
            # Checks for how many enemies are left in the level text
            if self.enemiesText != '' and time.time() - self.starttime > 1:
                self.starttime = time.time()
                level = int(self.enemiesText[0])
                # Sets a timer to make sure they are coming at the right time
                # *********** BUG_ALERT ***************
                # If you pause the game it makes it so the next enemy does not
                # spawn at the right time and may spawn in close proximity to
                # the previous enemy
                # *************************************
                self.enemies.append(
                    Enemy((0, 0), ENEMY_HEALTH[level], level, self.grid.getPath()))
                # Moves forward in the level text
                if len(self.enemiesText) > 1:
                    self.enemiesText = self.enemiesText[1:]
                else:
                    self.enemiesText = ''

            # Update the enemies
            if self.enemies:
                self.enemies = [x for x in self.enemies if not x.isDead()]
                for enemy in self.enemies:
                    enemy.update(SCREEN_SIZE, ticks)
                    # Death sequence for when the tower shoots an enemy
                    if enemy.getPosition().x >= SQUARE_SIZE * 19.0 and enemy.getPosition().y >= SQUARE_SIZE * 14.0:
                        self.player.decLives()
                        enemy.kill()
                        if not self.player.isAlive():
                            RUNNING = False
                            break

            # Update the towers
            for tower in self.player.getTowers():
                closeEnemies = []
                for enemy in self.enemies:
                    if tower.checkEnemy(enemy):
                        closeEnemies.append(enemy)
                tower.update(SCREEN_SIZE, ticks, closeEnemies)

                # Checks all the particles to see if any have hit an enemy
                for p in tower.getParticles():
                    if self.enemies:
                        pos = p.getPosition()
                        for enemy in self.enemies:
                            if enemy.getCollideRect().collidepoint(pos[0], pos[1]):
                                enemy.getHit()
                                p.restart()
                                if enemy.isDead():
                                    SoundManager.getInstance().playSound('cha-ching.wav')
                                    self.player.updateMoney(10)

            # Checks to see if all the enemies are dead and no more are being sent out
            self.levelDone = self._level.update(self.enemiesText, self.enemies)

            # Checks to see if you have won the game
            if self.levelDone and self.totalLevels == self._currentLevel + 1:
                self._FSM.manageState('win')

            # Displays the current level and the number of enemies left
            self.text = 'Level ' + str(self._currentLevel + 1) + \
                ' Enemies left to come: ' + str(len(self.enemiesText))

        elif self._FSM == 'startLoading':
            self._currentLevel += 1
            self._level = LevelManager()
            self.enemiesText = self._level.load(self._currentLevel)
            self._FSM.manageState('doneLoading')
            print('Level ', self._currentLevel)
