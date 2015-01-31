__author__ = 'charles'

width, height = 64, 64

pixelScale = 20

import pygame, sys
from pygame.locals import *
import time
import numpy as np
import socket
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

subFrameCount = 2
subFrameHeight = 128 / subFrameCount
subFrameSize = 1 + subFrameHeight*256*3

# LEDscape message setup
message = np.zeros(subFrameSize*subFrameCount, np.uint8)
for subFrame in range(0, subFrameCount):
    message[subFrame*subFrameSize] = subFrame

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET,socket.SO_SNDBUF,int(subFrameSize))

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

def sendScreen():
    global sock

    frame = np.zeros((128,256,3), np.uint8)

    for y in range(0,32):
        for x in range(0,64):
            col = screen.get_at((x * pixelScale,y * pixelScale))
            frame[y + 64][x + 64] = (col[0],col[1],col[2])

    for y in range(32,64):
        for x in range(0,64):
            print(31 - y) * pixelScale
            col = screen.get_at((x * pixelScale,((63 -y) + 32) * pixelScale))
            frame[y + 32][63 - x] = (col[0],col[1],col[2])


    flattenedFrame = frame.reshape(128, 256*3)

    copyWidth = 256
    copyHeight = 128

    copyLength = copyWidth*3

    for row in range(0, copyHeight):
        offset = 1 + (row / subFrameHeight)
        messageOffset = (row*256)*3 + offset

        message[messageOffset:messageOffset+copyLength] = flattenedFrame[row, 0:copyLength]


    for subFrame in range(0, subFrameCount):
        sock.sendto(zlib.compress(message[subFrame*subFrameSize:(subFrame+1)*subFrameSize].tostring()), ("192.168.7.2", 9999))


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

    sendScreen()

    pygame.display.update()

    if isAlive:
        newPos = snake[-1] + snakeVel
        snake.append(newPos)

    if len(snake) > snakeLength:
        snake = snake[1:]


    time.sleep(0.15)