import pygame
import os
import random
import copy
import numpy as np

white_circle = pygame.image.load(os.path.join('../assets', 'white.png'))
black_circle = pygame.image.load(os.path.join('../assets', 'black.png'))


# Draw table
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


# Draw circles for possible moves
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

    # Draw pieces
    def draw(self, surface, last_position=None):
        for i in range(8):
            for j in range(8):
                if self.board[i, j] == 'B':
                    surface.blit(black_circle, (j * 100 + 12.5, i * 100 + 12.5))
                elif self.board[i, j] == 'W':
                    surface.blit(white_circle, (j * 100 + 12.5, i * 100 + 12.5))
        if last_position is not None:
            i, j = last_position
            pygame.draw.circle(surface, (255, 0, 0), (j * 100 + 50, i * 100 + 50), 4)

    # Print score and check if your state is final
    def is_final(self):
        no_of_whites, no_of_blacks = 0, 0
        if self.final_state(self.board):
            for i in range(8):
                for j in range(8):
                    if self.board[i, j] == "W":
                        no_of_whites += 1
                    elif self.board[i, j] == "B":
                        no_of_blacks += 1

            if no_of_whites > no_of_blacks:
                print("The bot won!")
            elif no_of_whites < no_of_blacks:
                print("You won!")
            elif no_of_whites == no_of_blacks:
                print("Tie!")

            print(f"Final score: \nB = {no_of_blacks} - W = {no_of_whites}")
            return True
        else:
            # The game is done before the table is complete
            whites, blacks = 0, 0
            for i in range(8):
                for j in range(8):
                    if self.board[i, j] == "W":
                        whites += 1
                    elif self.board[i, j] == "B":
                        blacks += 1

            if whites + blacks == abs(whites - blacks):
                if whites != 0:
                    print("The bot won!")
                    print(f"Final score: \nB = {blacks} - W = {whites}")
                else:
                    print("You won!")
                    print(f"Final score: \nB = {blacks} - W = {whites}")

                return True

        return False

    # Used to check on horizontal line for possible places
    def horizontal_line(self, pos_x, pos_y, opposite_color, current_state):
        positions = list()

        if current_state is not None:
            table = current_state
        else:
            table = self.board

        # RIGHT SIDE
        elements = list()
        for i in range(pos_y, 8):
            elements.append(table[pos_x, i])

        for i in range(pos_y + 1, 8):
            if table[pos_x, i] == '-':
                flag = True
                if i - 1 > pos_y:
                    for j in range(i - 1, pos_y, -1):
                        if table[pos_x, j] != opposite_color:
                            flag = False
                else:
                    flag = False
                if flag:
                    positions.append((pos_x, i))

        # LEFT SIDE
        elements.clear()
        for i in range(pos_y, -1, -1):
            elements.append(table[pos_x, i])

        for i in range(pos_y - 1, -1, -1):
            if table[pos_x, i] == '-':
                flag = True
                if i + 1 < pos_y:
                    for j in range(i + 1, pos_y):
                        if table[pos_x, j] != opposite_color:
                            flag = False
                else:
                    flag = False
                if flag:
                    positions.append((pos_x, i))

        return positions

    # Used to check on vertical line for possible places
    def vertical_line(self, pos_x, pos_y, opposite_color, current_state):
        positions = list()

        if current_state is not None:
            table = current_state
        else:
            table = self.board

        # DOWN SIDE
        elements = list()
        for i in range(pos_x, 8):
            elements.append(table[i, pos_y])

        for i in range(pos_x + 1, 8):
            if table[i, pos_y] == '-':
                flag = True
                if i - 1 > pos_x:
                    for j in range(i - 1, pos_x, -1):
                        if table[j, pos_y] != opposite_color:
                            flag = False
                else:
                    flag = False
                if flag:
                    positions.append((i, pos_y))

        # UPPER SIDE
        elements.clear()
        for i in range(pos_x, -1, -1):
            elements.append(table[i, pos_y])

        for i in range(pos_x - 1, -1, -1):
            if table[i, pos_y] == '-':
                flag = True
                if i + 1 < pos_x:
                    for j in range(i + 1, pos_x):
                        if table[j, pos_y] != opposite_color:
                            flag = False
                else:
                    flag = False
                if flag:
                    positions.append((i, pos_y))

        return positions

    # Used to check on principal diagonal for possible places
    def principal_diagonal_line(self, pos_x, pos_y, opposite_color, current_state):
        positions = list()

        if current_state is not None:
            table = current_state
        else:
            table = self.board

        # Ascending
        i, j = pos_x, pos_y

        elements = list()
        while i < 8 and j < 8:
            elements.append(table[i, j])
            i += 1
            j += 1

        i, j = pos_x, pos_y
        while i < 8 and j < 8:
            if table[i, j] == '-':
                flag = True
                if i - 1 > pos_x:
                    row = i - 1
                    col = j - 1
                    while row > pos_x:
                        if table[row, col] != opposite_color:
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
            elements.append(table[i, j])
            i -= 1
            j -= 1

        i, j = pos_x, pos_y
        while i > -1 and j > -1:
            if table[i, j] == '-':
                flag = True
                if i + 1 < pos_x:
                    row = i + 1
                    col = j + 1
                    while row < pos_x:
                        if table[row, col] != opposite_color:
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

    # Used to check on secondary diagonal for possible places
    def secondary_diagonal_line(self, pos_x, pos_y, opposite_color, current_state):
        positions = list()

        if current_state is not None:
            table = current_state
        else:
            table = self.board

        # Ascending
        i, j = pos_x, pos_y

        elements = list()
        while i < 8 and j > -1:
            elements.append(table[i, j])
            i += 1
            j -= 1

        i, j = pos_x, pos_y
        while i < 8 and j > -1:
            if table[i, j] == '-':
                flag = True
                if i - 1 > pos_x:
                    row = i - 1
                    col = j + 1
                    while row > pos_x:
                        if table[row, col] != opposite_color:
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
            elements.append(table[i, j])
            i -= 1
            j += 1

        i, j = pos_x, pos_y
        while i > -1 and j < 8:
            if table[i, j] == '-':
                flag = True
                if i + 1 < pos_x:
                    row = i + 1
                    col = j - 1
                    while row < pos_x:
                        if table[row, col] != opposite_color:
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

    # Return positions of possible places where you can place a piece
    def generate_possible_moves(self, color, current_state, strategy):
        all_moves = list()
        if color == 'B':
            opposite_color = 'W'
        else:
            opposite_color = 'B'

        if strategy is True:
            value = current_state
        else:
            value = None

        for i in range(8):
            for j in range(8):
                if self.board[i, j] == color:
                    h_l = self.horizontal_line(i, j, opposite_color, value)
                    v_l = self.vertical_line(i, j, opposite_color, value)
                    p_l = self.principal_diagonal_line(i, j, opposite_color, value)
                    s_l = self.secondary_diagonal_line(i, j, opposite_color, value)

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

    # Change the color of pieces for Black / White
    def change_color(self, pos_x, pos_y, color):
        directions = dict()
        if pos_x + 1 < 8:
            if self.board[pos_x + 1][pos_y] != color and self.board[pos_x + 1][pos_y] != "-":
                flag = True
                for i in range(pos_x + 2, 8):
                    if self.board[i][pos_y] == '-':
                        flag = False
                    if self.board[i][pos_y] == color and flag is True:
                        directions['vertical_jos'] = (i, pos_y)
                        break

        if pos_x - 1 > -1:
            if self.board[pos_x - 1][pos_y] != color and self.board[pos_x - 1][pos_y] != "-":
                flag = True
                for i in range(pos_x - 2, -1, -1):
                    if self.board[i][pos_y] == '-':
                        flag = False
                    if self.board[i][pos_y] == color and flag is True:
                        directions['vertical_sus'] = (i, pos_y)
                        break

        if pos_y + 1 < 8:
            if self.board[pos_x][pos_y + 1] != color and self.board[pos_x][pos_y + 1] != "-":
                flag = True
                for i in range(pos_y + 2, 8):
                    if self.board[pos_x][i] == "-":
                        flag = False
                    if self.board[pos_x][i] == color and flag is True:
                        directions['orizontal_dreapta'] = (pos_x, i)
                        break

        if pos_y - 1 > -1:
            if self.board[pos_x][pos_y - 1] != color and self.board[pos_x][pos_y - 1] != "-":
                flag = True
                for i in range(pos_y - 2, -1, -1):
                    if self.board[pos_x][i] == "-":
                        flag = False
                    if self.board[pos_x][i] == color and flag is True:
                        directions['orizontal_stanga'] = (pos_x, i)
                        break

        if pos_x + 1 < 8 and pos_y + 1 < 8:
            if self.board[pos_x + 1][pos_y + 1] != color and self.board[pos_x + 1][pos_y + 1] != "-":
                flag = True
                i, j = pos_x + 2, pos_y + 2
                while i < 8 and j < 8:
                    if self.board[i][j] == "-":
                        flag = False
                    if self.board[i][j] == color and flag is True:
                        directions['dp_descendent'] = (i, j)
                        break
                    i += 1
                    j += 1

        if pos_x - 1 > -1 and pos_y - 1 > -1:
            if self.board[pos_x - 1][pos_y - 1] != color and self.board[pos_x - 1][pos_y - 1] != "-":
                flag = True
                i, j = pos_x - 2, pos_y - 2
                while i > -1 and j > - 1:
                    if self.board[i][j] == "-":
                        flag = False
                    if self.board[i][j] == color and flag is True:
                        directions['dp_ascendent'] = (i, j)
                        break
                    i -= 1
                    j -= 1

        if pos_x + 1 < 8 and pos_y - 1 > -1:
            if self.board[pos_x + 1][pos_y - 1] != color and self.board[pos_x + 1][pos_y - 1] != "-":
                flag = True
                i, j = pos_x + 2, pos_y - 2
                while i < 8 and j > -1:
                    if self.board[i][j] == "-":
                        flag = False
                    if self.board[i][j] == color and flag is True:
                        directions['ds_descendent'] = (i, j)
                        break
                    i += 1
                    j -= 1

        if pos_x - 1 > -1 and pos_y + 1 < 8:
            if self.board[pos_x - 1][pos_y + 1] != color and self.board[pos_x - 1][pos_y + 1] != "-":
                flag = True
                i, j = pos_x - 2, pos_y + 2
                while i > -1 and j < 8:
                    if self.board[i][j] == "-":
                        flag = False
                    if self.board[i][j] == color and flag is True:
                        directions['ds_ascendent'] = (i, j)
                        break
                    i -= 1
                    j += 1

        if 'vertical_jos' in directions.keys():
            x, y = directions['vertical_jos']
            for i in range(pos_x + 1, x):
                self.board[i][pos_y] = color

        if 'vertical_sus' in directions.keys():
            x, y = directions['vertical_sus']
            for i in range(pos_x - 1, x, -1):
                self.board[i][pos_y] = color

        if 'orizontal_dreapta' in directions.keys():
            x, y = directions['orizontal_dreapta']
            for i in range(pos_y + 1, y):
                self.board[pos_x][i] = color

        if 'orizontal_stanga' in directions.keys():
            x, y = directions['orizontal_stanga']
            for i in range(pos_y - 1, y, -1):
                self.board[pos_x][i] = color

        if 'dp_descendent' in directions.keys():
            x, y = directions['dp_descendent']
            i, j = pos_x + 1, pos_y + 1
            while i < x and j < y:
                self.board[i][j] = color
                i += 1
                j += 1

        if 'dp_ascendent' in directions.keys():
            x, y = directions['dp_ascendent']
            i, j = pos_x - 1, pos_y - 1
            while i > x and j > y:
                self.board[i][j] = color
                i -= 1
                j -= 1

        if 'ds_descendent' in directions.keys():
            x, y = directions['ds_descendent']
            i, j = pos_x + 1, pos_y - 1
            while i < x and j > y:
                self.board[i][j] = color
                i += 1
                j -= 1

        if 'ds_ascendent' in directions.keys():
            x, y = directions['ds_ascendent']
            i, j = pos_x - 1, pos_y + 1
            while i > x and j < y:
                self.board[i][j] = color
                i -= 1
                j += 1

        return self.board

    # Set move
    def set_move(self, pos_x, pos_y, color):
        self.board[pos_x, pos_y] = color
        self.change_color(pos_x, pos_y, color)

    # --------------------  STRATEGIES ------------------------------------------

    # ---------------------- RANDOM -------------------------------------------

    def random_piece_pick(self):
        possible_moves = list(self.generate_possible_moves("B", self.board, True))
        result_move = random.choice(possible_moves)
        return result_move

    def random_strategy(self):
        move = list(self.random_piece_pick())
        x = move[0]
        y = move[1]
        self.board[x, y] = "W"
        return x, y

    # ---------------- LOCAL MAXIMIZATION -------------------------------------

    # Returns the number of white and black pieces
    def count_pieces(self):
        return np.count_nonzero(self.board == 'W'), np.count_nonzero(self.board == 'B')

    # Takes decisions for computer, every move has a certain reward
    def local_maximization_strategy(self, current_player='W'):
        possible_moves = list(self.generate_possible_moves(current_player, self.board, True))
        rewards = list()
        backup_board = copy.deepcopy(self.board)

        for position in possible_moves:
            self.set_move(position[0], position[1], current_player)
            no_of_whites, no_of_blacks = self.count_pieces()

            if current_player == 'W':
                rewards.append(no_of_whites)
            else:
                rewards.append(no_of_blacks)

            self.board = copy.deepcopy(backup_board)

        if len(rewards) > 0:
            best_move = possible_moves[np.argmax(rewards)]
            self.set_move(best_move[0], best_move[1], current_player)
            return best_move

        return None

    # ---------------------- MINI MAX -------------------------------------------

    # Transform a position from possible moves into a state for computer
    @staticmethod
    def create_state(current_state, pos_x, pos_y, color):
        directions = dict()
        if pos_x + 1 < 8:
            if current_state[pos_x + 1][pos_y] != color and current_state[pos_x + 1][pos_y] != "-":
                flag = True
                for i in range(pos_x + 2, 8):
                    if current_state[i][pos_y] == '-':
                        flag = False
                    if current_state[i][pos_y] == color and flag is True:
                        directions['vertical_jos'] = (i, pos_y)
                        break

        if pos_x - 1 > -1:
            if current_state[pos_x - 1][pos_y] != color and current_state[pos_x - 1][pos_y] != "-":
                flag = True
                for i in range(pos_x - 2, -1, -1):
                    if current_state[i][pos_y] == '-':
                        flag = False
                    if current_state[i][pos_y] == color and flag is True:
                        directions['vertical_sus'] = (i, pos_y)
                        break

        if pos_y + 1 < 8:
            if current_state[pos_x][pos_y + 1] != color and current_state[pos_x][pos_y + 1] != "-":
                flag = True
                for i in range(pos_y + 2, 8):
                    if current_state[pos_x][i] == "-":
                        flag = False
                    if current_state[pos_x][i] == color and flag is True:
                        directions['orizontal_dreapta'] = (pos_x, i)
                        break

        if pos_y - 1 > -1:
            if current_state[pos_x][pos_y - 1] != color and current_state[pos_x][pos_y - 1] != "-":
                flag = True
                for i in range(pos_y - 2, -1, -1):
                    if current_state[pos_x][i] == "-":
                        flag = False
                    if current_state[pos_x][i] == color and flag is True:
                        directions['orizontal_stanga'] = (pos_x, i)
                        break

        if pos_x + 1 < 8 and pos_y + 1 < 8:
            if current_state[pos_x + 1][pos_y + 1] != color and current_state[pos_x + 1][pos_y + 1] != "-":
                flag = True
                i, j = pos_x + 2, pos_y + 2
                while i < 8 and j < 8:
                    if current_state[i][j] == "-":
                        flag = False
                    if current_state[i][j] == color and flag is True:
                        directions['dp_descendent'] = (i, j)
                        break
                    i += 1
                    j += 1

        if pos_x - 1 > -1 and pos_y - 1 > -1:
            if current_state[pos_x - 1][pos_y - 1] != color and current_state[pos_x - 1][pos_y - 1] != "-":
                flag = True
                i, j = pos_x - 2, pos_y - 2
                while i > -1 and j > - 1:
                    if current_state[i][j] == "-":
                        flag = False
                    if current_state[i][j] == color and flag is True:
                        directions['dp_ascendent'] = (i, j)
                        break
                    i -= 1
                    j -= 1

        if pos_x + 1 < 8 and pos_y - 1 > -1:
            if current_state[pos_x + 1][pos_y - 1] != color and current_state[pos_x + 1][pos_y - 1] != "-":
                flag = True
                i, j = pos_x + 2, pos_y - 2
                while i < 8 and j > -1:
                    if current_state[i][j] == "-":
                        flag = False
                    if current_state[i][j] == color and flag is True:
                        directions['ds_descendent'] = (i, j)
                        break
                    i += 1
                    j -= 1

        if pos_x - 1 > -1 and pos_y + 1 < 8:
            if current_state[pos_x - 1][pos_y + 1] != color and current_state[pos_x - 1][pos_y + 1] != "-":
                flag = True
                i, j = pos_x - 2, pos_y + 2
                while i > -1 and j < 8:
                    if current_state[i][j] == "-":
                        flag = False
                    if current_state[i][j] == color and flag is True:
                        directions['ds_ascendent'] = (i, j)
                        break
                    i -= 1
                    j += 1

        if 'vertical_jos' in directions.keys():
            x, y = directions['vertical_jos']
            for i in range(pos_x + 1, x):
                current_state[i][pos_y] = color

        if 'vertical_sus' in directions.keys():
            x, y = directions['vertical_sus']
            for i in range(pos_x - 1, x, -1):
                current_state[i][pos_y] = color

        if 'orizontal_dreapta' in directions.keys():
            x, y = directions['orizontal_dreapta']
            for i in range(pos_y + 1, y):
                current_state[pos_x][i] = color

        if 'orizontal_stanga' in directions.keys():
            x, y = directions['orizontal_stanga']
            for i in range(pos_y - 1, y, -1):
                current_state[pos_x][i] = color

        if 'dp_descendent' in directions.keys():
            x, y = directions['dp_descendent']
            i, j = pos_x + 1, pos_y + 1
            while i < x and j < y:
                current_state[i][j] = color
                i += 1
                j += 1

        if 'dp_ascendent' in directions.keys():
            x, y = directions['dp_ascendent']
            i, j = pos_x - 1, pos_y - 1
            while i > x and j > y:
                current_state[i][j] = color
                i -= 1
                j -= 1

        if 'ds_descendent' in directions.keys():
            x, y = directions['ds_descendent']
            i, j = pos_x + 1, pos_y - 1
            while i < x and j > y:
                current_state[i][j] = color
                i += 1
                j -= 1

        if 'ds_ascendent' in directions.keys():
            x, y = directions['ds_ascendent']
            i, j = pos_x - 1, pos_y + 1
            while i > x and j < y:
                current_state[i][j] = color
                i -= 1
                j += 1

        return current_state

    # Make a move as computer
    def set_state_move(self, current_state, pos_x, pos_y, color):
        current_state[pos_x, pos_y] = color
        return self.create_state(current_state, pos_x, pos_y, color)

    # Used in mini max algorithm to check if the state is final or not
    @staticmethod
    def final_state(current_state):
        if current_state is None:
            return False

        empty_slot = False
        for i in range(8):
            for j in range(8):
                if current_state[i][j] == '-':
                    empty_slot = True

        if empty_slot:
            return False
        return True

    # Heuristic method
    @staticmethod
    def heuristic_function(current_state):
        whites, blacks = 0, 0
        for i in range(8):
            for j in range(8):
                if current_state[i][j] == "W":
                    whites += 1
                elif current_state[i][j] == "B":
                    blacks += 1
        return whites - blacks

    # Mini max algorithm
    def mini_max(self, current_state, maximized_level, current_depth, best_one):
        if current_depth == 0 or self.final_state(current_state) is True:
            return None, self.heuristic_function(current_state)

        if maximized_level is True:
            value = -float('Inf')
            possible_states = self.generate_possible_moves("W", current_state, True)
            for i in possible_states:
                copy_of_current_state = copy.deepcopy(current_state)
                new_state = self.set_state_move(copy_of_current_state, i[0], i[1], "W")
                _, new_val = self.mini_max(new_state, False, current_depth - 1, best_one)
                if new_val > value:
                    value = new_val
                    best_one = new_state
            return best_one, value
        else:
            value = float('Inf')
            possible_states = self.generate_possible_moves("B", current_state, True)
            for i in possible_states:
                copy_of_current_state = copy.deepcopy(current_state)
                new_state = self.set_state_move(copy_of_current_state, i[0], i[1], "B")
                _, new_val = self.mini_max(new_state, True, current_depth - 1, best_one)
                if new_val < value:
                    value = new_val
                    best_one = new_state
            return best_one, value

    # Function to call the mini max algorithm
    def mini_max_strategy(self):
        best_state, value = self.mini_max(self.board, True, 1, None)
        if best_state is None:
            for i in range(8):
                for j in range(8):
                    if self.board[i, j] == "-":
                        self.board[i, j] = "W"
                        break
        else:
            last_position = self.compare_states(best_state)
            self.board = best_state
            return last_position

    # -------------------- α-β Pruning ----------------------------------------

    def compare_states(self, state):
        last_position = None
        for i in range(8):
            for j in range(8):
                if self.board[i, j] == '-':
                    if state[i, j] == 'W' or state[i, j] == 'B':
                        last_position = (i, j)
        return last_position

    def alpha_beta(self, current_state, maximized_level, current_depth, alpha, beta, best_one):
        if current_depth == 0 or self.final_state(current_state) is True:
            return None, self.heuristic_function(current_state)

        if maximized_level is True:
            value = -np.Inf
            possible_states = self.generate_possible_moves('W', current_state, True)
            for i in possible_states:
                copy_of_current_state = copy.deepcopy(current_state)
                new_state = self.set_state_move(copy_of_current_state, i[0], i[1], 'W')
                _, new_val = self.alpha_beta(new_state, False, current_depth - 1, alpha, beta, best_one)
                if new_val > value:
                    value = new_val
                    best_one = new_state
                if value > alpha:
                    alpha = value
                if alpha >= beta:
                    break
            return best_one, value
        else:
            value = np.Inf
            possible_states = self.generate_possible_moves('B', current_state, True)
            for i in possible_states:
                copy_of_current_state = copy.deepcopy(current_state)
                new_state = self.set_state_move(copy_of_current_state, i[0], i[1], 'B')
                _, new_val = self.alpha_beta(new_state, True, current_depth - 1, alpha, beta, best_one)
                if new_val < value:
                    value = new_val
                    best_one = new_state
                if value < beta:
                    beta = value
                if beta <= alpha:
                    break
            return best_one, value

    # Function to call the mini max algorithm
    def alpha_beta_strategy(self):
        best_state, value = self.alpha_beta(self.board, True, 1, -np.Inf, np.Inf, None)
        if best_state is None:
            for i in range(8):
                for j in range(8):
                    if self.board[i, j] == "-":
                        self.board[i, j] = "W"
                        break
        else:
            last_position = self.compare_states(best_state)
            self.board = best_state
            return last_position

    # -----------------------------NEGAMAX-------------------------------------
    def negamax(self, current_state, current_depth, color, best_one):
        if current_depth == 0 or self.final_state(current_state) is True:
            return None, self.heuristic_function(current_state)
        if color == "W":
            value = -np.Inf
            possible_states = self.generate_possible_moves("W", current_state, True)
            for i in possible_states:
                copy_of_current_state = copy.deepcopy(current_state)
                new_state = self.set_state_move(copy_of_current_state, i[0], i[1], "W")
                _, new_val = self.negamax(new_state, current_depth - 1, "B", best_one)
                if -new_val > value:
                    value = new_val
                    best_one = new_state

            return best_one, value
        elif color == "B":
            value = -np.Inf
            possible_states = self.generate_possible_moves("B", current_state, True)
            for i in possible_states:
                copy_of_current_state = copy.deepcopy(current_state)
                new_state = self.set_state_move(copy_of_current_state, i[0], i[1], "B")
                _, new_val = self.negamax(new_state, current_depth - 1, "W", best_one)
                if -new_val > value:
                    value = new_val
                    best_one = new_state

            return best_one, value

    def negamax_strategy(self):
        best_state, value = self.negamax(self.board, 1, "W", None)
        if best_state is None:
            for i in range(8):
                for j in range(8):
                    if self.board[i, j] == "-":
                        self.board[i, j] = "W"
                        break
        else:
            last_position = self.compare_states(best_state)
            self.board = best_state
            return last_position

    # --------------------------- DEBUG ---------------------------------------

    def print_matrix(self):
        for i in range(8):
            for j in range(8):
                print('[({}, {}) {}] '.format(i, j, self.board[i, j], ), end='')
            print()
