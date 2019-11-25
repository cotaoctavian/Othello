# Othello Project
# Team: Băcăoanu Adriana-Bianca, Chiperi Andrei, Coța Ștefan-Octavian, Pătrașcu Deny
# Group: 3A1

import pygame
import os
from components import Board

os.environ['SDL_VIDEO_CENTERED'] = '1'

pygame.display.init()

surface = pygame.display.set_mode((800, 800))
pygame.display.set_caption('Othello')

table = Board.Board()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        surface.fill((255, 255, 255))

        Board.draw_table(surface)
        table.draw(surface)

        pygame.display.flip()
