import pygame
import sys
import chess
import chess.svg

width = 640
height = 640
square_size = width // 8
piece_to_file = {
    "P": "P2.png",
    "N": "N2.png",
    "B": "B2.png",
    "R": "R2.png",
    "Q": "Q2.png",
    "K": "K2.png",
    "p": "p.png",
    "n": "n.png",
    "b": "b.png",
    "r": "r.png",
    "q": "q.png",
    "k": "k.png"
}

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

def draw_pieces():
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            filename = piece_to_file[piece.symbol()]
            pieceImg = pygame.image.load(f'assets/{filename}')
            pieceImg = pygame.transform.scale(pieceImg, (square_size, square_size))
            row = 7 - (square // 8)
            col = square % 8
            screen.blit(pieceImg, (col * square_size, row * square_size))
            
def main():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        draw_board()
        draw_pieces()
        pygame.display.flip()
        clock.tick(30)
    pygame.quit()
    sys.exit()
    
if __name__ == "__main__":
    main()

        
        
        