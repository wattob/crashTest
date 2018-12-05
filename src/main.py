import pygame
from pygame.locals import *
import os
import sys
import math

pygame.init()

W, H = 800, 750
# width and height of the screen because background is 447
win = pygame.display.set_mode((W, H))
pygame.display.set_caption('Side Scroller')

bg = pygame.image.load(os.path.join('./../images/', 'bg.png')).convert()
# background image
bgX = 0
bgX2 = bg.get_width()

clock = pygame.time.Clock()
# used to change the FPS as we move


class player(object):
    run = [pygame.image.load(os.path.join('./../images/', str(x) + '.png')) for x in
           range(8, 16)]
    jump = [pygame.image.load(os.path.join('./../images/', str(x) + '.png')) for x in
            range(1, 8)]
    slide = [pygame.image.load(os.path.join('./../images/', 'S1.png')), pygame.image.
             load(os.path.join('./../images/', 'S2.png')), pygame.image.load(
             os.path.join('./../images/', 'S2.png')), pygame.image.load(
             os.path.join('./../images/', 'S2.png')), pygame.image.load(
             os.path.join('./../images/', 'S2.png')), pygame.image.load(
             os.path.join('./../images/', 'S2.png')), pygame.image.load(
             os.path.join('./../images/', 'S2.png')), pygame.image.load(
             os.path.join('./../images/', 'S2.png')), pygame.image.load(
             os.path.join('./../images/', 'S3.png')), pygame.image.load(
             os.path.join('./../images/', 'S4.png')), pygame.image.load(
             os.path.join('./../images/', 'S5.png'))]
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
        if self.jumping:
            self.y -= self.jumpList[self.jumpCount] * 1.2
            win.blit(self.jump[self.jumpCount // 18], (self.x, self.y))
            self.jumpCount += 1
            if self.jumpCount > 108:
                self.jumpCount = 0
                self.jumping = False
                self.runCount = 0
                # hitbox for character while jumping
                self.hitbox = (self.x + 4, self.y, self.width - 24, self.height - 10)
        elif self.sliding or self.slideUp:
            if self.slideCount < 20:
                self.y += 1
            elif self.slideCount == 80:
                self.y -= 19
                self.sliding = False
            elif self.slideCount > 20 and self.slideCount < 80:
                self.hitbox = (self.x, self.y + 3, self.width - 8, self.height - 35)
                self.slideUp = True
            if self.slideCount >= 110:
                self.slideCount = 0
                self.slideUp = False
                self.runCount = 0
                self.hitbox = (self.x + 4, self.y, self.width - 24, self.height - 10)
            win.blit(self.slide[self.slideCount // 10], (self.x, self.y))
            self.slideCount += 1
        elif self.falling:
            win.blit(self.fall, (self.x, self.y + 30))
        else:
            if self.runCount > 42:
                self.runCount = 0
            win.blit(self.run[self.runCount // 6], (self.x, self.y))
            self.runCount += 1
            self.hitbox = (self.x + 4, self.y, self.width - 24, self.height - 13)
        pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)

class saw(object):
    img = [pygame.image.load(os.path.join('./../images/', 'SAW0.png')), pygame.image.
           load(os.path.join('./../images/', 'SAW1.png')), pygame.image.load(
           os.path.join('./../images/', 'SAW2.png')), pygame.image.load(
           os.path.join('./../images/', 'SAW3.png'))]

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
        win.blit(pygame.transform.scale(self.img[self.count // 2], (64, 64)), (
                 self.x, self.y))
        self.count += 1
        pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)


class spike(saw):
    # using saw makes def __init__ reused
    img = pygame.image.load(os.path.join('./../images/', 'spike.png'))

    def draw(self, win):
        self.hitbox = (self.x + 10, self.y, 28, 315)
        win.blit(self.img, (self.x, self.y))
        pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)


def redrawWindow():
    win.blit(bg, (bgX, 0))
    win.blit(bg, (bgX2, 0))
    runner.draw(win)

    pygame.display.update()


runner = player(200, 470, 64, 64)
# location of the character on the background
pygame.time.set_timer(USEREVENT + 1, 500)
# in milliseconds so every half second increase speed by calling this event
speed = 30
run = True
while run:
    redrawWindow()
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
