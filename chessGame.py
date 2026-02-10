import pygame
import sys
import chess
import chess.svg

width = 640
height = 640
square_size = width // 8

white = (240,217,181)
black = (181,136,99)

pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Chess Game')
clock = pygame.time.Clock()

board = chess.Board()
def draw_board():
    for row in range(8):
        for col in range(8):
            color = white if (row + col) % 2 == 0 else black
            pygame.draw.rect(screen, color, (col * square_size, row * square_size, square_size, square_size))   
        
        