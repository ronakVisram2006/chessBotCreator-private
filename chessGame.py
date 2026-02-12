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

white = (237, 237, 237)
black = (137,207,240)

pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Chess Game')
clock = pygame.time.Clock()
panel_width = 200
screen = pygame.display.set_mode((width + panel_width, height))

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

def display_turn(val1, val2):
    font = pygame.font.SysFont(None, 36)
    if board.turn == chess.WHITE: 
        text = font.render("White's Turn", True, (255,255,255))
    if board.turn == chess.BLACK: 
        text = font.render("Black's Turn", True, (255,255,255)) 
    if board.is_check():
        text = font.render("Check!", True, (255, 0, 0)) 
    if board.is_checkmate():
        if board.turn == chess.WHITE:
            text = font.render("Black Wins!", True, (255, 0, 0))
        else:
            text = font.render("White Wins!", True, (255, 0, 0))
    if board.is_stalemate():
        text = font.render("Stalemate!", True, (255, 0, 0)) 
    screen.blit(text, (val1, val2))
    
def draw_sidebar():
    pygame.draw.rect(screen, (0, 0, 0), (640, 0, panel_width, height))
    
def draw_bottom_box():
    box_width = 200
    box_height = 150
    x = 640 + 10
    y = 640 - box_height - 10
    
    pygame.draw.rect(screen, (0, 0, 0), (x, y, box_width, box_height))
    display_turn(x+10,y+10)
  
def display_move_history():
    font = pygame.font.SysFont(None, 24)
    temp_board = chess.Board() 

    moves = list(board.move_stack)
    san_moves = []

    for move in moves:
        san_moves.append(temp_board.san(move))
        temp_board.push(move)
        
    new_sans = san_moves[::-1]
    for i, san in enumerate(new_sans[:20]):

        move_number = len(san_moves) - i
        text = font.render(f" Move {move_number} : {san}", True, (255, 255, 255))
        screen.blit(text, (650, 20 + i * 30))
            
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
        draw_sidebar()
        draw_bottom_box()
        display_move_history()
        pygame.display.flip()
        clock.tick(30)
    pygame.quit()
    sys.exit()
    
if __name__ == "__main__":
    main()

        
        
        