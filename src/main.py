import pygame
from pygame.locals import *
import os
import sys
import math
import random
# imports to be used

pygame.init()

W, H = 800, 600
# width and height of the screen
# background image is 800 by 600
window = pygame.display.set_mode((W, H))
pygame.display.set_caption('Side Scroller Game')
# creates caption at the top of pygame window

bg = pygame.image.load(os.path.join('./../images/', 'bg.png')).convert()
# background image which is in the images folder
bgX = 0
# used to keep track of x position of two different images
bgX2 = bg.get_width()

clock = pygame.time.Clock()
# used to change the FPS as the player moves


class player(object):
    # player class
    run = [pygame.image.load(os.path.join('./../images/', str(x) +
           '.png')) for x in range(8, 16)]
    # loading in the images for run animation from the images folder
    jump = [pygame.image.load(os.path.join('./../images/', str(x) +
            '.png')) for x in range(1, 8)]
    # loading in the images for jump animation from the images folder
    slide = [pygame.image.load(os.path.join('./../images/', 'S1.png')),
             pygame.image.load(os.path.join('./../images/', 'S2.png')),
             pygame.image.load(os.path.join('./../images/', 'S2.png')),
             pygame.image.load(os.path.join('./../images/', 'S2.png')),
             pygame.image.load(os.path.join('./../images/', 'S2.png')),
             pygame.image.load(os.path.join('./../images/', 'S2.png')),
             pygame.image.load(os.path.join('./../images/', 'S2.png')),
             pygame.image.load(os.path.join('./../images/', 'S2.png')),
             pygame.image.load(os.path.join('./../images/', 'S3.png')),
             pygame.image.load(os.path.join('./../images/', 'S4.png')),
             pygame.image.load(os.path.join('./../images/', 'S5.png'))]
    # loading in the images for slide animation from the images folder
    fall = pygame.image.load(os.path.join('./../images/', '0.png'))
    # loading in the images for the fall animation from the images folder
    jumpList = [1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3,
                3, 3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, -1, -1, -1, -1, -1, -1, -2, -2, -2, -2, -2, -2, -2,
                -2, -2, -2, -2, -2, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3,
                -3, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4]
    # jumplist used for character jumping so he jumps at the correct speed

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.jumping = False
        self.sliding = False
        self.slideCount = 0
        self.jumpCount = 0
        self.runCount = 0
        self.slideUp = False
        self.falling = False

    # animation for character running, jumping, sliding, and falling
    # source: https://github.com/techwithtim/side_scroller
    def draw(self, window):
        # animation for the character running, jumping, and sliding
        if self.falling:
            window.blit(self.fall, (self.x, self.y + 30))
        elif self.jumping:
            self.y -= self.jumpList[self.jumpCount] * 1.2
            window.blit(self.jump[self.jumpCount // 18], (self.x, self.y))
            # blit(image, (left, top))
            # Draw the image to the screen at the given position
            # blit() accepts either Surface or string as its image parameter
            self.jumpCount += 1
            if self.jumpCount > 108:
                self.jumpCount = 0
                self.jumping = False
                self.runCount = 0
                # hitbox for character while jumping
            self.hitbox = (self.x + 4, self.y, self.width - 24,
                           self.height - 10)
        elif self.sliding or self.slideUp:
            if self.slideCount < 20:
                self.y += 1
            elif self.slideCount == 80:
                self.y -= 19
                self.sliding = False
            elif self.slideCount > 20 and self.slideCount < 80:
                self.hitbox = (self.x, self.y + 3, self.width - 8,
                               self.height - 35)
                self.slideUp = True
            if self.slideCount >= 110:
                self.slideCount = 0
                self.slideUp = False
                self.runCount = 0
                self.hitbox = (self.x + 4, self.y, self.width - 24,
                               self.height - 10)
            window.blit(self.slide[self.slideCount // 10], (self.x, self.y))
            self.slideCount += 1

        else:
            if self.runCount > 42:
                self.runCount = 0
            window.blit(self.run[self.runCount // 6], (self.x, self.y))
            self.runCount += 1
            self.hitbox = (self.x + 4, self.y, self.width - 24,
                           self.height - 13)
        pygame.draw.rect(window, (255, 0, 0), self.hitbox, 2)


class box(object):
    img = pygame.image.load(os.path.join('./../images/', 'Box.png'))

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.hitbox = (x, y, width, height)
        self.count = 0

    def draw(self, window):
        self.hitbox = (self.x + 5, self.y + 5, 30, 30)
        if self.count >= 8:
            self.count = 0
        window.blit(pygame.transform.scale(self.img, (64, 64)),
                   (self.x, self.y))
        self.count += 1
        pygame.draw.rect(window, (255, 0, 0), self.hitbox, 2)

    def collide(self, rect):
        # rect takes hitbox of the player
        if (rect[0] + rect[2] > self.hitbox[0] and
                rect[0] < self.hitbox[0] + self.hitbox[2]):
                # rect [0] is the x position of the player
                # rect[2] is the width
                # checks if the x coordinates are within each other
            if rect[1] + rect[3] > self.hitbox[1]:
                # checks the y coordinates are within each other
                return True
            return False


class bat(object):
    img = [pygame.image.load(os.path.join('./../images/', 'BAT0.png')),
           pygame.image.load(os.path.join('./../images/', 'BAT1.png')),
           pygame.image.load(os.path.join('./../images/', 'BAT2.png')),
           pygame.image.load(os.path.join('./../images/', 'BAT3.png'))]

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.hitbox = (x, y, width, height)
        self.count = 0

    def draw(self, window):
        self.hitbox = (self.x, self.y, 35, 35)
        if self.count >= 8:
            self.count = 0
        window.blit(self.img[self.count // 2], (self.x, self.y))
        self.count += 1
        pygame.draw.rect(window, (255, 0, 0), self.hitbox, 2)

    def collide(self, rect):
        # rect takes hitbox of the player
        if (rect[0] + rect[2] > self.hitbox[0] and
                rect[0] < self.hitbox[0] + self.hitbox[2]):
                # rect [0] is the x position of the player
                # rect[2] is the width
                # checks if the x coordinates are within each other
            if rect[1] + rect[3] > self.hitbox[1]:
                # checks the y coordinates are within each other
                return True
            return False


def drawWindow():
    # function used to draw background and all objects on the screen
    window.blit(bg, (bgX, 0))
    # draws background at the background x position
    window.blit(bg, (bgX2, 0))
    # draws 2nd background at the background x position
    character.draw(window)
    for x in objects:
        x.draw(window)
    font = pygame.font.SysFont('comicsans', 30)
    text = font.render('Score: ' + str(score), 1, (0, 0, 0))
    window.blit(text, (700, 10))
    instructions = font.render('Use UP and DOWN Keys to jump and slide!',
                               1, (0, 0, 0))
    window.blit(instructions, (100, 10))
    pygame.display.update()
    # updates to add all the objects


def updateFile():
    f = open('scores.txt', 'r')
    file = f.readlines()
    last = int(file[0])

    if last < int(score):
        f.close()
        file = open('scores.txt', 'w')
        file.write(str(score))
        file.close()

        return score

    return last


def endScreen():
    global pause, objects, speed, score
    # name of all the variables we want to change and access
    pause = 0
    objects = []
    speed = 30

    run = True
    while run:
        pygame.time.delay(100)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False
        window.blit(bg, (0, 0))
        largeFont = pygame.font.SysFont('comicsans', 70)
        previousScore = largeFont.render('Previous Score: ' +
                                         str(updateFile()), 1, (0, 0, 0))
        window.blit(previousScore, (W / 2 - previousScore.get_width() /
                                    2, 200))
        newScore = largeFont.render('Score: ' + str(score), 1, (0, 0, 0))
        window.blit(newScore, (W / 2 - newScore.get_width() / 2, 320))
        play = largeFont.render('Click the screen to Play Again!', 1,
                                (0, 0, 0))
        window.blit(play, (1, 440))

        pygame.display.update()

    score = 0
    character.falling = False

character = player(200, 470, 64, 64)
# location of the character on the background
pygame.time.set_timer(USEREVENT + 1, 500)
# timer event used to make screen go faster
# in milliseconds so every half second increase speed by calling USEREVENT
pygame.time.set_timer(USEREVENT + 2, random.randrange(2000, 5000))
# between 2 seconds and 5
speed = 30
run = True
pause = 0
fallSpeed = 0
objects = []

while run:
    # main loop for Game

    score = speed // 2 - 15
    if pause > 0:
        pause += 1
        if pause > fallSpeed * 2:
            endScreen()

    for objectt in objects:
        if objectt.collide(character.hitbox):
            # character is variable for player
            # executes what happens when he gets hit
            character.falling = True
            if pause == 0:
                fallSpeed = speed
                pause = 1
        objectt.x -= 1.5
        # moves x value of object to create appearance of sliding
        if objectt.x < -objectt.width * -1:
            objects.pop(objects.index(objectt))
            # if off the screen pop removes object at the index

    bgX -= 1.5
    # Speed at which background is moving
    bgX2 -= 1.5
    # speed at which background is moving
    # should match speed above to give appearance of continous background
    if bgX < bg.get_width() * -1:
        # first background image starting at 0,0 starts moving until it gets to
        # the negative width of the background
        bgX = bg.get_width()
        # after it is at its negative width it is no longer on screen
    if bgX2 < bg.get_width() * -1:
        # 2nd background object that comes onto screen after first image is off
        # screen to give the appearance of continous running background
        bgX2 = bg.get_width()
    # Event loop
    for event in pygame.event.get():
        # if event is type quit than we want to quit the game
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
            quit()
        if event.type == USEREVENT + 1:
            speed += 1
            # increasing speed for every time USEREVENT is called
        if event.type == USEREVENT + 2:
            r = random.randrange(0, 3)
            if r == 0:
                objects.append(box(810, 470, 64, 64))
            else:
                # if r == 1:
                    objects.append(bat(810, 400, 64, 64))
                # if r == 2:
                #     objects.append(bat(810, 470, 64, 64))

    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
        if not(character.jumping):
            # stops character from jumping while already jumping
            character.jumping = True

    if keys[pygame.K_DOWN]:
        if not(character.sliding):
            # if character is sliding when we hit down arrow again
            # prevents from sliding again
            character.sliding = True

    clock.tick(speed)
    # sets FPS for speed
    drawWindow()
