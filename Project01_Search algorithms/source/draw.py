import sys
from pygame.locals import *
import pygame
import vidmaker
import time

white = (255, 255, 255)
black = (0, 0, 0)
yellow = (200, 200, 0)
red = (200, 0, 0)
blue = (30, 144, 255)
green = (54, 179, 72)
grey = (100, 100, 100)
darkSlateGray = (151, 255, 255)

def outputTxt(route, pathOutTxt, res):
    with open(pathOutTxt, 'w') as outfile:
        if len(route) == 0:
            outfile.write('NO')
        else:
            outfile.write((str)(res))

def drawByPygame(matrix, bonus, start, end, pathOutMp4, route=None, locationVisit=None):
    # cài đặt màn hình pygame
    pygame.init()
    line_width = 30
    size = 25
    m = len(matrix)  # chiều dài của matrix
    n = len(matrix[0])  # chiều rộng của matrix
    window = pygame.display.set_mode((n*line_width, m*line_width))
    pygame.display.set_caption('pygame window')

    # khai báo video để xuất
    video = vidmaker.Video(pathOutMp4, late_export=True)  

    # tìm những ô là tường
    walls = [(i, j) for i in range(len(matrix))
            for j in range(len(matrix[0])) if matrix[i][j] == 'x']


    # vẽ cái map trước
    for i in range(len(walls)):
        pygame.draw.rect(window, yellow, pygame.Rect(
            walls[i][1] * line_width, walls[i][0] * line_width, size, size))

    pygame.draw.rect(window, red, pygame.Rect(
        start[1] * line_width, start[0] * line_width, size, size))
    pygame.draw.rect(window, blue, pygame.Rect(
        end[1] * line_width, end[0] * line_width, size, size))

    for i in range(len(bonus)):
        pygame.draw.rect(window, green, pygame.Rect(
            bonus[i][1] * line_width, bonus[i][0] * line_width, size, size))


    # bắt đầu chạy đường đi
    for i in range(len(locationVisit)):
        if (locationVisit[i] != end and locationVisit[i] != start):
            pygame.draw.rect(window, grey, pygame.Rect(
                locationVisit[i][1] * line_width, locationVisit[i][0] * line_width, size, size))
            video.update(pygame.surfarray.pixels3d(window).swapaxes(0, 1), inverted=False)  # THIS LINE
            pygame.display.update()
            pygame.time.Clock().tick(40)

    for i in range(len(route)):
        if (route[i] != end):
            pygame.draw.rect(window, red, pygame.Rect(
                route[i][1] * line_width, route[i][0] * line_width, size, size))
            for j in range(len(bonus)):
                if (route[i][0] == bonus[j][0] and route[i][1] == bonus[j][1]):
                    pygame.draw.rect(window, darkSlateGray, pygame.Rect(
                        route[i][1] * line_width, route[i][0] * line_width, size, size))
            video.update(pygame.surfarray.pixels3d(window).swapaxes(0, 1), inverted=False)  # THIS LINE
            pygame.display.update()
            pygame.time.Clock().tick(40)

    video.update(pygame.surfarray.pixels3d(window).swapaxes(0, 1), inverted=False)  # THIS LINE
    pygame.display.update()

    # xuất video 
    video.export(verbose=True)
