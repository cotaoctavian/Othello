# Othello Project
# Team: Băcăoanu Adriana-Bianca, Chiperi Andrei, Coța Ștefan-Octavian, Pătrașcu Deny
# Group: 3A1

import pygame
import os
import Board

os.environ['SDL_VIDEO_CENTERED'] = '1'

pygame.display.init()

surface = pygame.display.set_mode((800, 800))
pygame.display.set_caption('Othello')

table = Board.Board()
running = True
player = 'B'
positions = None

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if not table.is_final():
            if player == "B":
                positions = table.generate_possible_moves(player, None, False)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos_x, pos_y = pygame.mouse.get_pos()
                    pos_x //= 100
                    pos_y //= 100
                    if (pos_y, pos_x) in positions:
                        table.set_move(pos_y, pos_x, player)
                        if player == 'B':
                            player = 'W'
            else:
                #table.mini_max_strategy()
                table.random_strategy()
                player = "B"
        else:
            running = False

        surface.fill((255, 255, 255))

        Board.draw_table(surface)
        table.draw(surface)
        if len(positions) > 0:
            Board.draw_possible_moves(surface, positions)

        pygame.display.flip()
