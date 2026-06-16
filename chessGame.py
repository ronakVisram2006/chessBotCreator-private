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

PIECE_VAL = {
    chess.PAWN: 10,
    chess.KNIGHT: 31,
    chess.BISHOP: 32,
    chess.ROOK: 50,
    chess.QUEEN: 90,
    chess.KING: 100
}

KNIGHT_TABLE = [
    -5,-4,-3,-3,-3,-3,-4,-5,
    -4,-2, 0, 0, 0, 0,-2,-4,
    -3, 0, 1, 1.5,1.5,1, 0,-3,
    -3,0.5,1.5,2,2,1.5,0.5,-3,
    -3, 0,1.5,2,2,1.5,0,-3,
    -3,0.5,1,1.5,1.5,1,0.5,-3,
    -4,-2,0,0.5,0.5,0,-2,-4,
    -5,-4,-3,-3,-3,-3,-4,-5
]

BISHOP_TABLE = [
    -2,-1,-1,-1,-1,-1,-1,-2,
    -1,0,0,0,0,0,0,-1,
    -1,0,0.5,1,1,0.5,0,-1,
    -1,0.5,1,1.5,1.5,1,0.5,-1,
    -1,0.5,1,1.5,1.5,1,0.5,-1,
    -1,0,0.5,1,1,0.5,0,-1,
    -1,0,0,0,0,0,0,-1,
    -2,-1,-1,-1,-1,-1,-1,-2
]

PAWN_TABLE = [
     0, 0, 0, 0, 0, 0, 0, 0,
     5, 5, 5, 5, 5, 5, 5, 5,
     1, 1, 2, 3, 3, 2, 1, 1,
     0, 0, 0, 5, 5, 0, 0, 0,
     1, 0, 1, 2, 2, 1, 0, 1,
     1, 1, 1,-2,-2, 1, 1, 1,
     1, 1, 1, 0, 0, 1, 1, 1,
     0, 0, 0, 0, 0, 0, 0, 0,
]

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

def draw_overbar():
    pygame.draw.rect(screen, (30, 30, 30), (0, 0, 150, height))
    
def draw_bottom_box():
    box_width = 200
    box_height = 150
    x = 640 + 10
    y = 640 - box_height - 10
    
    pygame.draw.rect(screen, (0, 0, 0), (x, y, box_width, box_height))
    display_turn(x+10,y+10)
  
def display_move_history(scroll_offset):

    font = pygame.font.SysFont(None, 24)
    temp_board = chess.Board() 

    moves = list(board.move_stack)
    san_moves = []

    for move in moves:
        san_moves.append(temp_board.san(move))
        temp_board.push(move)

    new_sans = san_moves[::-1]
    text2 = font.render("Move History", True, (255, 255, 255))
    screen.blit(text2, (650, 10))
    MAX_TOP = 40
    MAX_BOTTOM = 640 - 200
    Allowed = MAX_BOTTOM - MAX_TOP
    content_height = len(new_sans) * 30
    
    max_scroll = 0
    min_scroll = min(0, Allowed - content_height)
    scroll_offset = max(min_scroll, min(max_scroll, scroll_offset))
    
    for i, san in enumerate(new_sans[:150]):

        move_number = len(san_moves) - i
        y = 40 + i * 30 + scroll_offset
        if MAX_TOP <= y <= MAX_BOTTOM:
            text = font.render(f"{move_number}. {san}", True, (255, 255, 255))
            screen.blit(text, (650, y))
        
    return scroll_offset

def draw_promotion_menu():
    font = pygame.font.SysFont(None, 32)
    pieces = ["Q", "R", "B", "N"]
    if board.turn == chess.WHITE:
        labels = ["Q2.png","B2.png","N2.png","R2.png"]
    else:
        labels = ["q2.png","b2.png","n2.png","r2.png"]

    for i, label in enumerate(labels):
        y = 50 + i * 80
        pygame.draw.rect(screen, (80, 80, 80), (10, y, 130, 60))
        text = font.render(label, True, (200, 200, 255))
        screen.blit(text, (20, y + 15))


            
def highlight_square(square, color):
    row = 7 - (square // 8)
    col = square % 8
    pygame.draw.rect(screen, color, (col * square_size, row * square_size, square_size, square_size), 5)
    
def evaluate(board):
    if board.is_checkmate():
        return float('-inf') if board.turn == chess.WHITE else float('inf')
    elif board.is_stalemate():
        return 0

    score = 0
    for square in chess.SQUARES:
        CENTER = [chess.D4, chess.E4, chess.D5, chess.E5]

        piece = board.piece_at(square)
        if piece:
            value = PIECE_VAL[piece.piece_type]
            if piece.piece_type == chess.KNIGHT and piece.color == chess.WHITE:
                value += KNIGHT_TABLE[square]
            elif piece.piece_type == chess.KNIGHT and piece.color == chess.BLACK:
                value += KNIGHT_TABLE[chess.square_mirror(square)]
                
            if piece.piece_type == chess.BISHOP and piece.color == chess.WHITE:
                value += BISHOP_TABLE[square]
            elif piece.piece_type == chess.BISHOP and piece.color == chess.BLACK:
                value += BISHOP_TABLE[chess.square_mirror(square)]
                
            if piece.piece_type == chess.PAWN:
                if square in CENTER:
                    value += 5
                if piece.color == chess.WHITE:
                    value += PAWN_TABLE[square]
                elif piece.color == chess.BLACK:
                    value += PAWN_TABLE[chess.square_mirror(square)]
                
            if piece.color == chess.WHITE:
                score += value
            else:
                score -= value
    return score
    
def minimax(board, depth, maximising, alpha=float('-inf'), beta=float('inf')):
    if depth == 0 or board.is_game_over():
            return evaluate(board)

    if maximising:
        best = float('-inf')
        for move in board.legal_moves:
            board.push(move)
            score = minimax(board, depth - 1, False, alpha, beta)  
            board.pop()
            best = max(best, score)
            alpha = max(alpha, best)
            if alpha >= beta:
                break
        return best
    else:
        best = float('inf')
        for move in board.legal_moves:
            board.push(move)
            score = minimax(board, depth - 1, True, alpha, beta)     
            board.pop()
            best = min(best, score)
            beta = min(beta, best)
            if beta <= alpha:
                break
        return best

def get_best_move(board, depth):
    best_move = None
    best_score = float('-inf')
    is_white_turn = board.turn == chess.WHITE

    for move in board.legal_moves:
        board.push(move)
        score = minimax(board, depth - 1, not is_white_turn)
        board.pop()
        
        print(move, score)
        adjusted = score if is_white_turn else -score
        if adjusted > best_score:
            best_score = adjusted
            best_move = move

    return best_move

def main():
    scroll_offset = 0
    highlight_color = (255, 255, 0)
    selected_square = None
    selected_piece = None
    clicked_square = None
    x, y = 0, 0  
    promotion_mode = False
    promotion_square = None
    bot_needs_to_move = False  
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEWHEEL:
                scroll_offset += event.y * 20

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()

                if promotion_mode:
                    if x < 150:
                        options = ["Q", "R", "B", "N"]
                        for i, piece_symbol in enumerate(options):
                            box_y = 50 + i * 80
                            if box_y <= y <= box_y + 60:
                                from_sq, to_sq = promotion_square
                                promo_piece = {
                                    "Q": chess.QUEEN,
                                    "R": chess.ROOK,
                                    "B": chess.BISHOP,
                                    "N": chess.KNIGHT
                                }[piece_symbol]
                                board.push(chess.Move(from_sq, to_sq, promotion=promo_piece))
                                promotion_mode = False
                                promotion_square = None
                                selected_square = None
                                selected_piece = None
                                bot_needs_to_move = True 
                                break
                    continue  
                
                if x >= 640:
                    continue

                col = x // square_size
                row = 7 - (y // square_size)

                if not (0 <= col <= 7 and 0 <= row <= 7):
                    continue

                clicked_square = chess.square(col, row)

                if selected_square is None:
                    piece = board.piece_at(clicked_square)
                    if piece and piece.color == board.turn:
                        selected_square = clicked_square
                        selected_piece = piece
                else:
                    move = chess.Move(selected_square, clicked_square)

                    if selected_piece.piece_type == chess.PAWN:
                        target_rank = chess.square_rank(clicked_square)
                        promotion_rank = 7 if selected_piece.color == chess.WHITE else 0
                        if target_rank == promotion_rank:
                            promotion_mode = True
                            promotion_square = (selected_square, clicked_square)
                            selected_square = None
                            selected_piece = None
                            continue

                    if move in board.legal_moves:
                        board.push(move)
                        if board.is_checkmate():
                            print("Checkmate! Game Over.")
                        if board.is_stalemate():
                            print("Stalemate! Game Over.")
                        bot_needs_to_move = True  

                    selected_square = None
                    selected_piece = None

        if bot_needs_to_move and not board.is_game_over() and board.turn == chess.BLACK:
            move = get_best_move(board, depth=3)
            if move:
                board.push(move)
            bot_needs_to_move = False

        # Drawing
        draw_board()
        if selected_square is not None and clicked_square is not None and x < 640:
            highlight_square(clicked_square, highlight_color)
        draw_pieces()
        draw_sidebar()
        draw_bottom_box()
        scroll_offset = display_move_history(scroll_offset)  
        if promotion_mode:
            draw_overbar()
            draw_promotion_menu()

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    sys.exit()
    
if __name__ == "__main__":
    main()

        
        
        