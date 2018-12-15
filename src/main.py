import pygame
from pygame.locals import *
import os
import sys
import math
import random

pygame.init()

W, H = 800, 600
# width and height of the screen because background image is 800 by 750
win = pygame.display.set_mode((W, H))
pygame.display.set_caption('Side Scroller')

bg = pygame.image.load(os.path.join('./../images/', 'bg.png')).convert()
# background image
bgX = 0
bgX2 = bg.get_width()

clock = pygame.time.Clock()
# used to change the FPS as we move


class player(object):
    run = [pygame.image.load(os.path.join('./../images/', str(x) +
           '.png')) for x in range(8, 16)]
    jump = [pygame.image.load(os.path.join('./../images/', str(x) +
            '.png')) for x in range(1, 8)]
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
    fall = pygame.image.load(os.path.join('./../images/', '0.png'))
    jumpList = [1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3,
                3, 3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, -1, -1, -1, -1, -1, -1, -2, -2, -2, -2, -2, -2, -2,
                -2, -2, -2, -2, -2, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3,
                -3, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4]

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

    def draw(self, win):
        # animation for the character running, jumping, and sliding
        if self.falling:
            win.blit(self.fall, (self.x, self.y + 30))
        elif self.jumping:
            self.y -= self.jumpList[self.jumpCount] * 1.2
            win.blit(self.jump[self.jumpCount // 18], (self.x, self.y))
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
            win.blit(self.slide[self.slideCount // 10], (self.x, self.y))
            self.slideCount += 1

        else:
            if self.runCount > 42:
                self.runCount = 0
            win.blit(self.run[self.runCount // 6], (self.x, self.y))
            self.runCount += 1
            self.hitbox = (self.x + 4, self.y, self.width - 24,
                           self.height - 13)
        pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)


class box(object):
    img = pygame.image.load(os.path.join('./../images/', 'Box.png'))

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.hitbox = (x, y, width, height)
        self.count = 0

    def draw(self, win):
        self.hitbox = (self.x + 5, self.y + 5, self.width - 10, self.height)
        if self.count >= 8:
            self.count = 0
        win.blit(pygame.transform.scale(self.img, (64, 64)), (self.x, self.y))
        self.count += 1
        pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)

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
    img = [pygame.image.load(os.path.join('./../images/','BAT0.png')),pygame.image.load(os.path.join('./../images/','BAT1.png')),pygame.image.load(os.path.join('./../images/','BAT2.png')),pygame.image.load(os.path.join('./../images/','BAT3.png'))]

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.hitbox = (x, y, width, height)
        self.count = 0

    def draw(self, win):
        self.hitbox = (self.x + 5, self.y + 5, self.width - 10, self.height)
        if self.count >= 8:
            self.count = 0
        win.blit(self.img[self.count//2], (self.x,self.y))
        self.count += 1
        pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)

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


def redrawWindow():
    win.blit(bg, (bgX, 0))
    win.blit(bg, (bgX2, 0))
    runner.draw(win)
    for x in objects:
        x.draw(win)
    font = pygame.font.SysFont('comicsans', 30)
    text = font.render('Score: ' + str(score), 1, (0, 0, 0))
    win.blit(text, (700, 10))
    pygame.display.update()


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
        win.blit(bg, (0, 0))
        largeFont = pygame.font.SysFont('comicsans', 70)
        previousScore = largeFont.render('Previous Score: ' +
            str(updateFile()), 1, (0, 0, 0))
        win.blit(previousScore, (W / 2 - previousScore.get_width() / 2, 200))
        newScore = largeFont.render('Score: ' + str(score), 1, (0, 0, 0))
        win.blit(newScore, (W / 2 - newScore.get_width() / 2, 320))
        play = largeFont.render('Click the screen to Play Again!', 1, (0, 0, 0))
        win.blit(play, (1, 440))

        pygame.display.update()

    score = 0
    runner.falling = False

runner = player(200, 470, 64, 64)
# location of the character on the background
pygame.time.set_timer(USEREVENT + 1, 500)
# in milliseconds so every half second increase speed by calling this event
pygame.time.set_timer(USEREVENT + 2, random.randrange(2000, 5000))
# between 2 seconds and 5
speed = 30
run = True
pause = 0
fallSpeed = 0
objects = []

while run:
    score = speed // 2 - 15
    if pause > 0:
        pause += 1
        if pause > fallSpeed * 2:
            endScreen()

    for objectt in objects:
        if objectt.collide(runner.hitbox):
            # runner is variable for player
            # executes what happens when he gets hit
            runner.falling = True
            if pause == 0:
                fallSpeed = speed
                pause = 1
        objectt.x -= 1.4
        # moves x value of object to create appearance of sliding
        if objectt.x < -objectt.width * -1:
            objects.pop(objects.index(objectt))
            # if off the screen pop removes object at the index

    bgX -= 1.4
    # larger number makes background go faster
    bgX2 -= 1.4
    # number must match number above
    if bgX < bg.get_width() * -1:
        # first background image starting at 0,0 starts moving until it gets to
        # the Negative width of the background
        bgX = bg.get_width()
        # after width is at ie -900 then we can no longer see it so we reset
        # the image to see background as continous
    if bgX2 < bg.get_width() * -1:
        # 2nd background object on the screen to give the appearance of
        # continous running background
        bgX2 = bg.get_width()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
            quit()
        if event.type == USEREVENT + 1:
            speed += 1
        if event.type == USEREVENT + 2:
            r = random.randrange(0, 2)
            if r == 0:
                objects.append(box(810, 470, 64, 64))
            else:
                objects.append(bat(810, 400, 64, 64))

    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
        if not(runner.jumping):
            # stops runner from jumping while already jumping
            runner.jumping = True

    if keys[pygame.K_DOWN]:
        if not(runner.sliding):
            # if runner is sliding when we hit down arrow again
            # prevents from sliding again
            runner.sliding = True

    clock.tick(speed)
    redrawWindow()
