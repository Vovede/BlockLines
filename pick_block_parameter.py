import pygame
import random

shapes = [
    [[1]],

    [[1, 1],
     [1, 0]],

    [[1, 1],
     [0, 1]],

    [[1, 0],
     [1, 1]],

    [[0, 1],
     [1, 1]],

    [[1, 1],
     [1, 1]],

    [[1, 1],
     [1, 0],
     [1, 0]],

    [[1, 1],
     [0, 1],
     [0, 1]],

    [[1, 0],
     [1, 0],
     [1, 1]],

    [[0, 1],
     [0, 1],
     [1, 1]],

    [[1, 1],
     [1, 1],
     [1, 1]],

    [[1, 1, 1],
     [1, 1, 1]],

    [[1, 1, 1],
     [0, 1, 0]],

    [[0, 1, 0],
     [1, 1, 1]],

    [[0, 1],
     [1, 1],
     [0, 1]],

    [[1, 0],
     [1, 1],
     [1, 0]],

    [[0, 1],
     [1, 1],
     [1, 0]],

    [[1, 0],
     [1, 1],
     [0, 1]],

    [[0, 1, 1],
     [1, 1, 0]],

    [[1, 1, 0],
     [0, 1, 1]],

    [[1, 1, 1],
     [1, 1, 1],
     [1, 1, 1]],

    [[1, 1, 1, 1]],

    [[1, 1, 1, 1, 1]],

    [[1],
     [1],
     [1],
     [1]],

    [[1],
     [1],
     [1],
     [1],
     [1]]
]

colors = [
    pygame.Color("red"),
    pygame.Color("green"),
    pygame.Color("blue"),
    pygame.Color("yellow"),
    pygame.Color("violet"),
    pygame.Color("cyan"),
    pygame.Color("gold"),
    pygame.Color("orange"),
    pygame.Color("purple")
]


def pick_shape():
    return random.choice(shapes)


def pick_color():
    return random.choice(colors)
