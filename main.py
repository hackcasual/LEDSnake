__author__ = 'charles'

width, height = 64, 64

pixelScale = 20

import pygame, sys
from pygame.locals import *
import numpy as np
import random
import time
import math

# set up pygame
pygame.init()

# set up the window
real_screen = pygame.display.set_mode((width * pixelScale, height * pixelScale), 0, 32)

screen = pygame.Surface((64, 64))

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

fruits = [np.array([20,20])]

def drawRect(x, y, color):
    screen.set_at((int(x),int(y)), color)

def drawSnake():
    for s in snake:
        drawRect(s[0], s[1], snakeColor)

def drawWalls():
    for w in walls:
        drawRect(w[0], w[1], (255,0,0))


def drawFruit():
    for f in fruits:
        drawRect(f[0], f[1], (255, 255, 0))

def didDie():
    global snake
    global isAlive
    global snakeColor

    for w in walls:
        if np.array_equal(w, snake[-1]):
            isAlive = False
            snakeColor = (238,130,238)
            return

    if len(snake) > 10:
        for s in snake[:-1]:
            if np.array_equal(s, snake[-1]):
                isAlive = False
                snakeColor = (238,130,238)
                return

def caughtFruit():
    global snakeLength

    for i in range(len(fruits)):
        if np.array_equal(fruits[i], snake[-1]):
            fruits[i] = np.array([random.randint(1, 62),random.randint(1, 62)])
            snakeLength += 5

def main():
    global isAlive
    global snake
    global snakeVel
    global snakeColor
    global snakeLength

    font = pygame.font.Font("5x5_pixel.ttf", 8)


    while True:
        oldVel = snakeVel
        screen.fill((0,0,0))
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == JOYAXISMOTION:
                if math.fabs(event.value) > 0.5 and oldVel[event.axis % 2] == 0:
                    snakeVel = [0, 0]
                    snakeVel[event.axis % 2] = math.copysign(1, event.value)


            if event.type == JOYBUTTONDOWN:
                isAlive = True
                snakeColor = (0,255,128)
                snake = [np.array([5,10])]
                snakeVel = np.array([0,0])
                snakeLength = 10

        didDie()

        drawWalls()

        drawSnake()

        text = font.render(str((snakeLength - 10) / 5), False, (255, 255, 255))

        screen.blit(text, (50,2))

        drawFruit()

        caughtFruit()

        pygame.transform.scale(screen, (64 * pixelScale, 64 * pixelScale), real_screen)

        pygame.display.update()

        if isAlive:
            newPos = snake[-1] + snakeVel
            snake.append(newPos)

        if len(snake) > snakeLength:
            snake = snake[1:]

        time.sleep(0.08)


if __name__ == "__main__":
    main()