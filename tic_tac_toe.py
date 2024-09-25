import pygame
import sys
import numpy as np

# Definimos colores
WHITE = (255, 255, 255)
BLUE = (0, 123, 255)
RED = (255, 71, 87)
DARK_BLUE = (0, 99, 178)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
LIGHT_GRAY = (230, 230, 230)

# Inicializamos Pygame
pygame.init()

# Configuramos la ventana
WIDTH, HEIGHT = 600, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Tic Tac Toe')

# Configuramos el tablero
board = np.full((3, 3), None)
current_player = 'X'
font = pygame.font.Font(None, 74)

def draw_board():
    screen.fill(LIGHT_GRAY)  # Fondo más atractivo
    for i in range(1, 3):
        pygame.draw.line(screen, BLUE, (0, i * 200), (WIDTH, i * 200), 5)
        pygame.draw.line(screen, BLUE, (i * 200, 0), (i * 200, HEIGHT - 100), 5)

    for i in range(3):
        for j in range(3):
            x_pos = j * 200 + 50  # Ajustamos la posición de X
            y_pos = i * 200 + 50  # Ajustamos la posición de Y
            if board[i][j] == 'X':
                text = font.render('X', True, RED)
                screen.blit(text, (x_pos + 50, y_pos))  # Centrar X
            elif board[i][j] == 'O':
                text = font.render('O', True, DARK_BLUE)
                screen.blit(text, (x_pos + 50, y_pos))  # Centrar O

def reset_game():
    global board, current_player
    board = np.full((3, 3), None)
    current_player = 'X'

def check_winner():
    for row in range(3):
        if board[row][0] == board[row][1] == board[row][2] != None:
            return board[row][0]
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] != None:
            return board[0][col]
    if board[0][0] == board[1][1] == board[2][2] != None:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != None:
        return board[0][2]
    if None not in board:
        return 'Tie'
    return None

def minimax(state, is_maximizing):
    winner = check_winner()
    if winner == 'X':
        return -1
    if winner == 'O':
        return 1
    if winner == 'Tie':
        return 0

    if is_maximizing:
        best_score = -float('inf')
        for i in range(3):
            for j in range(3):
                if state[i][j] is None:
                    state[i][j] = 'O'
                    score = minimax(state, False)
                    state[i][j] = None
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for i in range(3):
            for j in range(3):
                if state[i][j] is None:
                    state[i][j] = 'X'
                    score = minimax(state, True)
                    state[i][j] = None
                    best_score = min(score, best_score)
        return best_score

def bot_move():
    best_score = -float('inf')
    move = None
    for i in range(3):
        for j in range(3):
            if board[i][j] is None:
                board[i][j] = 'O'
                score = minimax(board, False)
                board[i][j] = None
                if score > best_score:
                    best_score = score
                    move = (i, j)
    if move:
        board[move[0]][move[1]] = 'O'

def draw_text(text, size, color, x, y):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)

def draw_button(text, x, y, width, height, color, hover_color):
    mouse_pos = pygame.mouse.get_pos()
    button_rect = pygame.Rect(x, y, width, height)

    # Efecto de hover
    if button_hover(mouse_pos, button_rect):
        pygame.draw.rect(screen, hover_color, button_rect, border_radius=10)
    else:
        pygame.draw.rect(screen, color, button_rect, border_radius=10)

    # Dibuja el texto centrado en el botón
    draw_text(text, 30, WHITE, x + width // 2, y + height // 2)

def button_hover(mouse_pos, button_rect):
    return button_rect.collidepoint(mouse_pos)

def show_menu():
    while True:
        screen.fill(WHITE)
        draw_text("Tic Tac Toe", 80, BLUE, WIDTH // 2, HEIGHT // 4)
        draw_text("Presiona 'Enter' para empezar a jugar", 40, BLACK, WIDTH // 2, HEIGHT // 2)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return

def show_game_over(winner):
    while True:
        screen.fill(WHITE)
        draw_board()  # Mantener la vista del tablero
        if winner == 'Tie':
            message = "¡Empate!"
        else:
            message = f"¡{winner} ganó!"

        # Mensaje centrado con borde
        message_rect = pygame.Rect(0, HEIGHT // 4 - 30, WIDTH, 60)
        pygame.draw.rect(screen, BLACK, message_rect, 2)  # Dibuja un borde alrededor del mensaje
        draw_text(message, 40, BLUE, WIDTH // 2, HEIGHT // 4)

        # Botones de reiniciar y salir en horizontal
        button_rect_restart = pygame.Rect(WIDTH // 2 - 120, HEIGHT - 80, 100, 50)
        button_rect_exit = pygame.Rect(WIDTH // 2 + 20, HEIGHT - 80, 100, 50)

        draw_button("Reiniciar", button_rect_restart.x, button_rect_restart.y, button_rect_restart.width, button_rect_restart.height, DARK_BLUE, GRAY)
        draw_button("Salir", button_rect_exit.x, button_rect_exit.y, button_rect_exit.width, button_rect_exit.height, RED, GRAY)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if button_hover(event.pos, button_rect_restart):
                    reset_game()
                    return
                if button_hover(event.pos, button_rect_exit):
                    pygame.quit()
                    sys.exit()

# Loop principal del juego
show_menu()
reset_game()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x, y = event.pos
            row = y // 200
            col = x // 200
            if board[row][col] is None:
                board[row][col] = current_player
                winner = check_winner()
                if winner is None:
                    pygame.display.flip()  # Actualizar pantalla antes del retraso
                    pygame.time.delay(500)  # Retraso para ver el movimiento del jugador
                    current_player = 'O'
                    bot_move()
                    current_player = 'X'

    draw_board()
    winner = check_winner()
    if winner:
        show_game_over(winner)  # Mostrar pantalla de fin de juego
    pygame.display.flip()
