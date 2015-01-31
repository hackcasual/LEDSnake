__author__ = 'charles'

width, height = 64, 64

pixelScale = 20

import pygame, sys
from pygame.locals import *
import numpy as np
import zlib

# set up pygame
pygame.init()

# set up the window
screen = pygame.display.set_mode((width * pixelScale, height * pixelScale), 0, 32)

pygame.joystick.init()
joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
joysticks[0].init()

print (joysticks)

snakeVel = np.array([0,0])


walls = []

for x in range(width):
    walls.append(np.array([x, 0]))
    walls.append(np.array([x, height - 1]))

for y in range(width):
    walls.append(np.array([0, y]))
    walls.append(np.array([width - 1, y]))

snakeColor = (0,255,128)

isAlive = True

snake = [np.array([5,10])]

snakeLength = 10

def drawSnake():
    for s in snake:
        pygame.draw.rect(screen, snakeColor,
                         (s[0] * pixelScale, s[1] * pixelScale, pixelScale, pixelScale)
        )
def drawWalls():
    for w in walls:
        pygame.draw.rect(screen, (255,0,0),
                         (w[0] * pixelScale, w[1] * pixelScale, pixelScale, pixelScale)
        )

def didDie():
    global snake
    global isAlive
    global snakeColor
    for w in walls:
        if np.array_equal(w, snake[-1]):
            isAlive = False
            snakeColor = (238,130,238)
            return

while True:
    screen.fill((0,0,0))
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == JOYAXISMOTION:
            oldVel = snakeVel.copy()

            if snakeVel[(event.axis + 1) % 2] == 0:
                snakeVel[event.axis] = event.value

            if np.array_equal(snakeVel, [0,0]):
                snakeVel = oldVel

        if event.type == JOYBUTTONDOWN:
            isAlive = True
            snakeColor = (0,255,128)
            snake = [np.array([5,10])]

    didDie()

    drawWalls()

    drawSnake()

    pygame.display.update()

    if isAlive:
        newPos = snake[-1] + snakeVel
        snake.append(newPos)

    if len(snake) > snakeLength:
        snake = snake[1:]


    time.sleep(0.15)