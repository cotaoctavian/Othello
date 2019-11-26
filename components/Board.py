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


def draw_possible_moves(surface, positions):
    for item in positions:
        pygame.draw.circle(surface, (178, 184, 180), (item[1] * 100 + 49, item[0] * 100 + 49), 38, 1)


class Board:
    def __init__(self):
        self.board = np.array([
            ['-', '-', '-', '-', '-', '-', '-', '-'],
            ['-', '-', '-', '-', '-', '-', '-', '-'],
            ['-', '-', '-', '-', '-', '-', '-', '-'],
            ['-', '-', '-', 'W', 'B', '-', '-', '-'],
            ['-', '-', '-', 'B', 'W', '-', '-', '-'],
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

    def horizontal_line(self, pos_x, pos_y, opposite_color):
        positions = list()

        # RIGHT SIDE
        elements = list()
        for i in range(pos_y, 8):
            elements.append(self.board[pos_x, i])

        for i in range(pos_y + 1, 8):
            if self.board[pos_x, i] == '-':
                flag = True
                if i - 1 > pos_y:
                    for j in range(i - 1, pos_y, -1):
                        if self.board[pos_x, j] != opposite_color:
                            flag = False
                else:
                    flag = False
                if flag:
                    positions.append((pos_x, i))

        # LEFT SIDE
        elements.clear()
        for i in range(pos_y, -1, -1):
            elements.append(self.board[pos_x, i])

        for i in range(pos_y - 1, -1, -1):
            if self.board[pos_x, i] == '-':
                flag = True
                if i + 1 < pos_y:
                    for j in range(i + 1, pos_y):
                        if self.board[pos_x, j] != opposite_color:
                            flag = False
                else:
                    flag = False
                if flag:
                    positions.append((pos_x, i))

        return positions

    def vertical_line(self, pos_x, pos_y, opposite_color):
        positions = list()

        # DOWN SIDE
        elements = list()
        for i in range(pos_x, 8):
            elements.append(self.board[i, pos_y])

        for i in range(pos_x + 1, 8):
            if self.board[i, pos_y] == '-':
                flag = True
                if i - 1 > pos_x:
                    for j in range(i - 1, pos_x, -1):
                        if self.board[j, pos_y] != opposite_color:
                            flag = False
                else:
                    flag = False
                if flag:
                    positions.append((i, pos_y))

        # UPPER SIDE
        elements.clear()
        for i in range(pos_x, -1, -1):
            elements.append(self.board[i, pos_y])

        for i in range(pos_x - 1, -1, -1):
            if self.board[i, pos_y] == '-':
                flag = True
                if i + 1 < pos_x:
                    for j in range(i + 1, pos_x):
                        if self.board[j, pos_y] != opposite_color:
                            flag = False
                else:
                    flag = False
                if flag:
                    positions.append((i, pos_y))

        return positions

    def principal_diagonal_line(self, pos_x, pos_y, opposite_color):
        positions = list()

        # Ascending
        i, j = pos_x, pos_y

        elements = list()
        while i < 8 and j < 8:
            elements.append(self.board[i, j])
            i += 1
            j += 1

        i, j = pos_x, pos_y
        while i < 8 and j < 8:
            if self.board[i, j] == '-':
                flag = True
                if i - 1 > pos_x:
                    row = i - 1
                    col = j - 1
                    while row > pos_x:
                        if self.board[row, col] != opposite_color:
                            flag = False
                        row -= 1
                        col -= 1
                else:
                    flag = False
                if flag:
                    positions.append((i, j))
            i += 1
            j += 1

        # Descending
        i, j = pos_x, pos_y
        elements.clear()
        while i > -1 and j > -1:
            elements.append(self.board[i, j])
            i -= 1
            j -= 1

        i, j = pos_x, pos_y
        while i > -1 and j > -1:
            if self.board[i, j] == '-':
                flag = True
                if i + 1 < pos_x:
                    row = i + 1
                    col = j + 1
                    while row < pos_x:
                        if self.board[row, col] != opposite_color:
                            flag = False
                        row += 1
                        col += 1
                else:
                    flag = False
                if flag:
                    positions.append((i, j))
            i -= 1
            j -= 1

        return positions

    def secondary_diagonal_line(self, pos_x, pos_y, opposite_color):
        positions = list()

        # Ascending
        i, j = pos_x, pos_y

        elements = list()
        while i < 8 and j > -1:
            elements.append(self.board[i, j])
            i += 1
            j -= 1

        i, j = pos_x, pos_y
        while i < 8 and j > -1:
            if self.board[i, j] == '-':
                flag = True
                if i - 1 > pos_x:
                    row = i - 1
                    col = j + 1
                    while row > pos_x:
                        if self.board[row, col] != opposite_color:
                            flag = False
                        row -= 1
                        col += 1
                else:
                    flag = False
                if flag:
                    positions.append((i, j))
            i += 1
            j -= 1

        # Descending
        i, j = pos_x, pos_y
        elements.clear()
        while i > -1 and j < 8:
            elements.append(self.board[i, j])
            i -= 1
            j += 1

        i, j = pos_x, pos_y
        while i > -1 and j < 8:
            if self.board[i, j] == '-':
                flag = True
                if i + 1 < pos_x:
                    row = i + 1
                    col = j - 1
                    while row < pos_x:
                        if self.board[row, col] != opposite_color:
                            flag = False
                        row += 1
                        col -= 1
                else:
                    flag = False
                if flag:
                    positions.append((i, j))
            i -= 1
            j += 1

        return positions

    def generate_possible_moves(self, color):
        all_moves = list()
        if color == 'B':
            opposite_color = 'W'
        else:
            opposite_color = 'B'

        for i in range(8):
            for j in range(8):
                if self.board[i, j] == color:
                    h_l = self.horizontal_line(i, j, opposite_color)
                    v_l = self.vertical_line(i, j, opposite_color)
                    p_l = self.principal_diagonal_line(i, j, opposite_color)
                    s_l = self.secondary_diagonal_line(i, j, opposite_color)

                    if len(h_l) > 0:
                        for item in h_l:
                            all_moves.append(item)

                    if len(v_l) > 0:
                        for item in v_l:
                            all_moves.append(item)

                    if len(p_l) > 0:
                        for item in p_l:
                            all_moves.append(item)

                    if len(s_l) > 0:
                        for item in s_l:
                            all_moves.append(item)

        return set(all_moves)

    # TODO -> changing piece's color on every direction (diagonal, vertical, horizontal)
    #  at the same time after placing a piece
    def change_color(self, pos_x, pos_y, color, opposite_color):
        return self.board

    def print_matrix(self):
        for i in range(8):
            for j in range(8):
                print(self.board[i, j], (i, j), end='')
            print()

    def set_move(self, pos_x, pos_y, color):
        self.board[pos_x, pos_y] = color
        """if color == 'B':
            opposite_color = 'W'
        else:
            opposite_color = 'B'
        self.change_color(pos_x, pos_y, color, opposite_color)"""
