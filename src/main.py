import pygame
from pygame.locals import *
import os
import sys
import math
import random
# imports to be used

pygame.init()
# This will initialize all the pygame modules
clock = pygame.time.Clock()
# used to change the FPS as the player moves

class bat(object):
    # class for bat object that inherits from object
    img = [pygame.image.load(os.path.join('./../images/', 'bat1.png')),
           pygame.image.load(os.path.join('./../images/', 'bat2.png')),
           pygame.image.load(os.path.join('./../images/', 'bat3.png')),
           pygame.image.load(os.path.join('./../images/', 'bat4.png'))]
    # loading images for bat object

    def __init__(self, x, y, width, height):
        # initialization method for variables
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.hitbox = (x, y, width, height)
        self.count = 0

    def draw(self, window):
        # draws the hitbox
        self.hitbox = (self.x, self.y, 40, 40)
        if self.count >= 8:
            self.count = 0
            # resets count variable to 0
        # adds our image to the window
        window.blit(pygame.transform.scale(self.img[self.count // 2],
                    (40, 40)), (self.x, self.y))
        # interger division by 2
        self.count += 1
        # incrementing count
        # pygame.draw.rect(window, (255, 0, 0), self.hitbox, 2)
        # draws hitbox for bat character

    def collide(self, rect):
        # rect takes hitbox of the player
        if (rect[0] + rect[2] > self.hitbox[0] and
                rect[0] < self.hitbox[0] + self.hitbox[2]):
                # rect [0] is the x position of the player
                # rect[2] is the width
                # checks if the x coordinates are within each other
            if (rect[1] + rect[3] > self.hitbox[1] and
                    rect[1] < self.hitbox[1] + self.hitbox[3]):
                # if player goes above bat object than collide will return true
                # checks the y coordinates are within each other
                return True
            return False


class box(object):
    # class for box object that inherits from object
    img = pygame.image.load(os.path.join('./../images/', 'box.png'))
    # loading image for box object

    def __init__(self, x, y, width, height):
        # initialization method for variables
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.hitbox = (x, y, width, height)
        self.count = 0

    def draw(self, window):
        # creates hitbox to be used by the box
        self.hitbox = (self.x, self.y + 5, 55, 55)
        # resets count variable to 0
        # draws image in the screen for box
        # and transforms to fit our screen and style
        window.blit(pygame.transform.scale(self.img, (55, 55)),
                    (self.x, self.y))
        # incrementing count
        self.count += 1
        # pygame.draw.rect(window, (255, 0, 0), self.hitbox, 2)
        # draws a red outline of the boxes hitbox

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


class player(object):
    # player class
    # loading in the images for hurt from the images folder
    hurt = pygame.image.load(os.path.join('./../images/', 'hurt.png'))
    # loading in the images for jump from the images folder
    jump = [pygame.image.load(os.path.join('./../images/', 'jump1.png')),
            pygame.image.load(os.path.join('./../images/', 'jump2.png')),
            pygame.image.load(os.path.join('./../images/', 'jump3.png')),
            pygame.image.load(os.path.join('./../images/', 'jump4.png'))]
    # loading in the images for run from the images folder
    run =  [pygame.image.load(os.path.join('./../images/', 'run1.png')),
            pygame.image.load(os.path.join('./../images/', 'run2.png')),
            pygame.image.load(os.path.join('./../images/', 'run3.png')),
            pygame.image.load(os.path.join('./../images/', 'run4.png')),
            pygame.image.load(os.path.join('./../images/', 'run5.png')),
            pygame.image.load(os.path.join('./../images/', 'run6.png'))]
    # loading in the images for slide from the images folder
    slide = [pygame.image.load(os.path.join('./../images/', 'slide1.png')),
             pygame.image.load(os.path.join('./../images/', 'slide2.png')),
             pygame.image.load(os.path.join('./../images/', 'slide2.png')),
             pygame.image.load(os.path.join('./../images/', 'slide2.png')),
             pygame.image.load(os.path.join('./../images/', 'slide2.png')),
             pygame.image.load(os.path.join('./../images/', 'slide2.png')),
             pygame.image.load(os.path.join('./../images/', 'slide2.png')),
             pygame.image.load(os.path.join('./../images/', 'slide2.png')),
             pygame.image.load(os.path.join('./../images/', 'slide3.png')),
             pygame.image.load(os.path.join('./../images/', 'slide4.png')),
             pygame.image.load(os.path.join('./../images/', 'slide5.png'))]
    # jumplist used for character jumping so he jumps at the correct speed
    jumpList = [1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3,
                3, 3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, -1, -1, -1, -1, -1, -1, -2, -2, -2, -2, -2, -2, -2,
                -2, -2, -2, -2, -2, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3,
                -3, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4]

    def __init__(self, x, y, width, height):
        # initialization method for variables
        self.x = x
        # self keyword points to the instance which x is called
        self.y = y
        # self keyword points to the instance which y is called
        self.width = width
        # self keyword points to the instance which width is called
        self.height = height
        # self keyword points to the instance which height is called
        self.injured = False
        # self keyword points to the instance which injured is called
        # initially set to false to show that the chracter is not currently
        # injured
        self.jumpCount = 0
        # self keyword points to the instance which jumpCount is called
        # initially set to 0
        self.jumping = False
        # self keyword points to the instance which jumping is called
        # set to false to show character is not jumping
        self.runCount = 0
        # self keyword points to the instance which runCount is called
        # initially set to 0
        self.slideCount = 0
        # self keyword points to the instance which slideCount is called
        # initially set to 0
        self.sliding = False
        # self keyword points to the instance which sliding is called
        # set to false to show character is not sliding
        self.slideUp = False
        # self keyword points to the instance which slideUp is called
        # initially set to false to show that the chracter is not currently
        # getting up from sliding


    # animation for character running, jumping, sliding, and injured
    def draw(self, window):
        # speeds up animation while screen background speeds up
        if self.injured:
            window.blit(self.hurt, (self.x, self.y + 30))
            # loction in the window where hurt image is placed
        elif self.jumping:
            self.y -= self.jumpList[self.jumpCount] * 1.5
            # changes jump height and changes how long character spends in jump
            window.blit(self.jump[self.jumpCount // 38], (self.x, self.y))
            # blit(image, (left, top))
            # Draw the image to the screen at the given position
            # blit() accepts either Surface or string as its image parameter
            # location where jump is added to screen
            self.jumpCount += 1
            # increments jumpCount
            if self.jumpCount > 108:
                # if jumpcount is greater than 108 then it is set back to 0
                self.jumpCount = 0
                # then jumpCount is set back to 0
                self.jumping = False
                # jumping is set to false
                self.runCount = 0
                # runcount is set to 0
            # hitbox for character while jumping
            self.hitbox = (self.x + 4, self.y, self.width - 24,
                           self.height - 10)
        elif self.sliding or self.slideUp:
            if self.slideCount < 20:
                self.y += 1
                # increments y variable
            elif self.slideCount == 80:
                self.y -= 19
                # Subtracts a 19 from the variable and assigns the result to
                # the variable y
                self.sliding = False
            elif self.slideCount > 20 and self.slideCount < 80:
                # hitbox while getting up from sliding
                self.hitbox = (self.x, self.y + 3, self.width - 8,
                               self.height - 35)
                self.slideUp = True
            if self.slideCount >= 110:
                # if slide count is greater than or equal to 110 then
                self.slideCount = 0
                # slide count is set to 0
                self.slideUp = False
                # slide up is False
                self.runCount = 0
                # runcount is set to 0
                # hitbox while sliding
                self.hitbox = (self.x + 4, self.y, self.width - 24,
                               self.height - 10)
            window.blit(self.slide[self.slideCount // 10], (self.x, self.y))
            # adds sliding images to window
            self.slideCount += 1
            # increments slideCount

        else:
            if self.runCount > 42:
                self.runCount = 0
            window.blit(self.run[self.runCount // 8], (self.x, self.y))
            # adds run images to the window
            self.runCount += 1
            # increments runCount
            # hitbox for while running
            self.hitbox = (self.x + 2, self.y, self.width - 24,
                           self.height)
        # pygame.draw.rect(window, (255, 0, 0), self.hitbox, 2)
        # draws a red rectangle around character while running, jumping,
        # and sliding


def drawWindow():
    # function used to draw background and all objects on the screen
    window.blit(bg, (bgX, 0))
    # draws background at the background x position
    window.blit(bg, (bgX2, 0))
    # draws 2nd background at the background x position
    character.draw(window)
    # draws character in the window
    for x in objects:
        x.draw(window)
        # draws the objects into the window
    font = pygame.font.SysFont('comicsans', 30)
    # shows the score in black
    text = font.render('Score: ' + str(score), 1, (0, 0, 0))
    window.blit(text, (700, 10))
    # adds to the score to the top right corner of the window
    instructions = font.render('Use UP and DOWN Keys to jump and slide!',
                               1, (0, 0, 0))
    # variable for the instructions in black
    window.blit(instructions, (10, 10))
    # adds the instructions to the left corner
    pygame.display.update()
    # updates to add all the objects


def updateScores():
    # used to maintain score file
    file = open('scores.txt', 'r')
    # opens scores.txt
    openFile = file.readlines()
    # reads the lines of scores.txt
    highScore = int(openFile[0])
    # takes the number in the text file

    if highScore < int(score):
        # if the score in the txt is less than the new score
        file.close()
        openFile = open('scores.txt', 'w')
        # new high score is added in to be used
        openFile.write(str(score))
        openFile.close()
        # file is closed
        return score
    return highScore


def endScreen():
    global pause, objects, speed, score
    # name of all the variables we want to change and access
    pause = 0
    # resets pause to 0 to restart game
    objects = []
    # empty list for objects to be added to
    speed = 30
    # sets speed back to the initial speed

    run = True
    while run:
        pygame.time.delay(100)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # reads input from mouse click to restart run
                run = False
        window.blit(bg, (0, 0))
        # adds background to endScreen
        largeFont = pygame.font.SysFont('comicsans', 70)
        # large font to be used to show High Score and Current Score
        highScore = largeFont.render('High Score: ' +
                                         str(updateScores()), 1, (0, 0, 0))
        # prints High Score and the high score found in the file in black
        window.blit(highScore, (W / 2 - highScore.get_width() /
                                    2, 200))
        # adds high score to the center of the screen
        newScore = largeFont.render('Your Score: ' + str(score), 1, (0, 0, 0))
        # prints the score from the current run in black
        window.blit(newScore, (W / 2 - newScore.get_width() / 2, 320))
        # adds the new score to the center of the screen
        play = largeFont.render('Click the screen to Play Again!', 1,
                                (0, 0, 0))
        # prints the message to restart the game in the window in black
        window.blit(play, (50, 440))
        # adds the message to the window

        pygame.display.update()

    score = 0
    character.injured = False

character = player(200, 470, 64, 64)
# location of the character on the background
pygame.time.set_timer(USEREVENT + 1, 500)
# timer event used to make screen go faster
# in milliseconds so every half second increase speed by calling USEREVENT
pygame.time.set_timer(USEREVENT + 2, random.randrange(2500, 5000))
# timer event that happens between 2.5 seconds and 5 to add objects
speed = 30
# initial speed of the background
run = True
pause = 0
fallSpeed = 0
objects = []
# blank list for objects to be appended to

W, H = 800, 600
# width and height of the screen
# background image is 800 by 600
window = pygame.display.set_mode((W, H))
pygame.display.set_caption('Side Scroller Game')
# creates caption at the top of pygame window
bg = pygame.image.load(os.path.join('./../images/', 'background.png')).convert()
# background image which is in the images folder
bgX = 0
# used to keep track of x position of two different images
bgX2 = bg.get_width()

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
            character.injured = True
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
            # randomly chooses a number to decide what should be appended
            if r == 0:
                objects.append(box(800, 480, 55, 55))
                # appends box object to objects []
            else:
                if r == 1:
                    # else if random number is 1 than bat object is
                    # appended to objects [] at 410 y
                    objects.append(bat(800, 410, 40, 40))
                if r == 2:
                    # if random number == 2 than bat object is appended to
                    # objects [] at 440 y
                    objects.append(bat(810, 440, 40, 40))

    keys = pygame.key.get_pressed()
    # reads keys from user
    if keys[pygame.K_UP]:
        # if the UP key is pressed and the character is not jumping then jump
        # is set to true to start a jump
        if not(character.jumping):
            # if not prevent the user from jumping while already jumping
            character.jumping = True
            # sets the character to jump

    if keys[pygame.K_DOWN]:
        # if the DOWN key is pressed and the character is not already sliding
        # then they will begin to slide
        if not(character.sliding):
            # prevents the user from sliding while already sliding
            character.sliding = True
            # sets the character to begin sliding

    clock.tick(speed)
    # sets FPS for speed
    drawWindow()
    # creates the window where the game takes place
