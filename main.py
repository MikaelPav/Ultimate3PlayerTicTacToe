import pygame
import sys

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 600
GRID_SIZE = 3
CELL_SIZE = WIDTH // (GRID_SIZE * GRID_SIZE)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
HIGHLIGHT_COLOR = (255, 255, 0)  # Yellow for highlighting

# Players and symbols
players = ["X", "O", "Δ"]
colors = [RED, GREEN, BLUE]
current_player = 0

# Game board (9 mini-boards, each 3x3)
board = [[[None for _ in range(3)] for _ in range(3)] for _ in range(9)]
mini_grid_winners = [None] * 9  # Track which mini-grid has been won
forced_board = None  # Mini-grid where the next move must be played

# Pygame setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("3-Player Ultimate Tic-Tac-Toe")
screen.fill(WHITE)

def draw_grid():
    """Draws the main and sub-grids"""
    for i in range(1, GRID_SIZE * GRID_SIZE):
        thickness = 5 if i % GRID_SIZE == 0 else 2
        pygame.draw.line(screen, BLACK, (i * CELL_SIZE, 0), (i * CELL_SIZE, HEIGHT), thickness)
        pygame.draw.line(screen, BLACK, (0, i * CELL_SIZE), (WIDTH, i * CELL_SIZE), thickness)

    # Highlight the forced mini-grid (3x3 box)
    if forced_board is not None and mini_grid_winners[forced_board[0] * 3 + forced_board[1]] is None:
        big_r, big_c = forced_board
        highlight_x = big_c * 3 * CELL_SIZE
        highlight_y = big_r * 3 * CELL_SIZE
        highlight_rect = pygame.Rect(highlight_x, highlight_y, CELL_SIZE * 3, CELL_SIZE * 3)
        pygame.draw.rect(screen, HIGHLIGHT_COLOR, highlight_rect, 5)  # 5 is the border thickness

    # Highlight won mini-grids
    for i in range(9):
        if mini_grid_winners[i]:
            big_r, big_c = i // 3, i % 3
            highlight_x = big_c * 3 * CELL_SIZE
            highlight_y = big_r * 3 * CELL_SIZE
            highlight_rect = pygame.Rect(highlight_x, highlight_y, CELL_SIZE * 3, CELL_SIZE * 3)
            pygame.draw.rect(screen, colors[players.index(mini_grid_winners[i])], highlight_rect, 5)

def draw_board():
    """Draws the current board state"""
    for big_r in range(3):
        for big_c in range(3):
            for small_r in range(3):
                for small_c in range(3):
                    symbol = board[big_r * 3 + big_c][small_r][small_c]
                    if symbol:
                        x = (big_c * 3 + small_c) * CELL_SIZE + CELL_SIZE // 3
                        y = (big_r * 3 + small_r) * CELL_SIZE + CELL_SIZE // 3
                        text = pygame.font.Font(None, 50).render(symbol, True, colors[players.index(symbol)])
                        screen.blit(text, (x, y))

def check_mini_grid_winner(big_r, big_c):
    """Checks if a mini-grid is won by a player"""
    grid = board[big_r * 3 + big_c]
    for p in players:
        # Check rows, columns, and diagonals
        for r in range(3):
            if all(grid[r][c] == p for c in range(3)): return p
        for c in range(3):
            if all(grid[r][c] == p for r in range(3)): return p
        if all(grid[i][i] == p for i in range(3)): return p
        if all(grid[i][2 - i] == p for i in range(3)): return p
    return None

draw_grid()
pygame.display.update()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x, y = event.pos
            big_c, small_c = (x // CELL_SIZE) // 3, (x // CELL_SIZE) % 3
            big_r, small_r = (y // CELL_SIZE) // 3, (y // CELL_SIZE) % 3
            mini_grid_index = big_r * 3 + big_c

            # If a mini-grid is won, allow free play
            if mini_grid_winners[mini_grid_index] is not None:
                forced_board = None  # Free play

            # Check if move is allowed
            if (forced_board is None or forced_board == (big_r, big_c)) and board[mini_grid_index][small_r][small_c] is None:
                board[mini_grid_index][small_r][small_c] = players[current_player]

                # Check if this mini-grid is now won
                winner = check_mini_grid_winner(big_r, big_c)
                if winner:
                    mini_grid_winners[mini_grid_index] = winner  # Mark the mini-grid as won

                # Set forced board unless the target mini-grid is won
                forced_board = (small_r, small_c)
                if mini_grid_winners[small_r * 3 + small_c] is not None:
                    forced_board = None  # Free play if the next grid is won

                current_player = (current_player + 1) % 3  # Next player
                screen.fill(WHITE)
                draw_grid()
                draw_board()
                pygame.display.update()

pygame.quit()
sys.exit()
