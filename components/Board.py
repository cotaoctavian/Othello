import pygame
import os
import numpy as np

white_circle = pygame.image.load(os.path.join('../assets', 'white.png'))
black_circle = pygame.image.load(os.path.join('../assets', 'black.png'))


def draw_table(surface):
    col = 0
    for i in range(8):
        row = 0
        for j in range(8):
            if (i + j) % 2 == 0:
                pygame.draw.rect(surface, (14, 92, 23), (row, col, 100, 100))
            else:
                pygame.draw.rect(surface, (8, 163, 27), (row, col, 100, 100))
            row += 100
        col += 100


class Board:
    def __init__(self):
        self.board = np.array([
            ['-', '-', '-', '-', '-', '-', '-', '-'],
            ['-', '-', '-', '-', '-', '-', '-', '-'],
            ['-', '-', '-', '-', '-', '-', '-', '-'],
            ['-', '-', '-', 'B', 'W', '-', '-', '-'],
            ['-', '-', '-', 'W', 'B', '-', '-', '-'],
            ['-', '-', '-', '-', '-', '-', '-', '-'],
            ['-', '-', '-', '-', '-', '-', '-', '-'],
            ['-', '-', '-', '-', '-', '-', '-', '-'],
        ])

    def draw(self, surface):
        for i in range(8):
            for j in range(8):
                if self.board[i, j] == 'B':
                    surface.blit(black_circle, (j * 100 + 12.5, i * 100 + 12.5))
                elif self.board[i, j] == 'W':
                    surface.blit(white_circle, (j * 100 + 12.5, i * 100 + 12.5))


