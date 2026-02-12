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
            
def highlight_square(square, color):
    row = 7 - (square // 8)
    col = square % 8
    pygame.draw.rect(screen, color, (col * square_size, row * square_size, square_size, square_size), 5)
        
def main():
    higlight_color = (255, 255, 0)
    selected_square = None
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                x,y = pygame.mouse.get_pos()
                col = x // square_size  
                row = 7 - (y // square_size)
                clicked_square = chess.square(col, row)
                
                if selected_square is None: 
                    piece = board.piece_at(clicked_square)
                    if piece and piece.color == board.turn:
                        selected_square = clicked_square
                    
                elif selected_square is not None: 
                    
                    m_piece = board.piece_at(clicked_square)
                    move = chess.Move(selected_square, clicked_square) 
                    if piece.piece_type == chess.PAWN :
                        target_rank = chess.square_rank(clicked_square)
                        promotion_rank = 7 if piece.color == chess.WHITE else 0
                        
                        if target_rank == promotion_rank:
                            move = chess.Move(selected_square, clicked_square, promotion=chess.QUEEN)

                    if move in board.legal_moves : 
                        board.push(move)
                        if board.is_checkmate(): 
                            print("Checkmate! Game Over.")
                        if board.is_stalemate(): 
                            print("Stalemate! Game Over.")
                    selected_square = None
        draw_board()
        highlight_square(clicked_square, higlight_color) if selected_square is not None else None
        draw_pieces()
        pygame.display.flip()
        clock.tick(30)
    pygame.quit()
    sys.exit()
    
if __name__ == "__main__":
    main()

        
        
        