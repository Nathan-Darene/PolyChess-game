import pygame
import sys

# Initialisation de Pygame
pygame.init()

# Taille de la fenêtre
WIDTH, HEIGHT = 800, 600
# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
# Taille de la case
SQUARE_SIZE = HEIGHT // 8

# Création de la fenêtre
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jeu d'échecs")

# Chargement des images des pièces
images = {}
for piece in ['Tour', 'Cavalier', 'Fou', 'Reine', 'Roi', 'Pion']:
    images[piece] = pygame.image.load(f'images/piece/{piece}.png')

# Création de l'échiquier initial
board =[
    ['Tour', 'Cavalier', 'Fou', 'Reine', 'Roi', 'Fou', 'Cavalier', 'Tour'],
    ['Pion', 'Pion', 'Pion', 'Pion', 'Pion', 'Pion', 'Pion', 'Pion'],
    ['__', '__', '__', '__', '__', '__', '__', '__'],
    ['__', '__', '__', '__', '__', '__', '__', '__'],
    ['__', '__', '__', '__', '__', '__', '__', '__'],
    ['__', '__', '__', '__', '__', '__', '__', '__'],
    ['Pion', 'Pion', 'Pion', 'Pion', 'Pion', 'Pion', 'Pion', 'Pion'],
    ['Tour', 'Cavalier', 'Fou', 'Reine', 'Roi', 'Fou', 'Cavalier', 'Tour']
]


# Fonction pour dessiner l'échiquier
def draw_board():
    for row in range(8):
        for col in range(8):
            color = WHITE if (row + col) % 2 == 0 else BLACK
            pygame.draw.rect(screen, color, pygame.Rect(col*SQUARE_SIZE, row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            piece = board[row][col]
            if piece != '__':
                screen.blit(images[piece], pygame.Rect(col*SQUARE_SIZE, row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

# Fonction pour obtenir la case de la souris
def get_square(mouse_pos):
    col = mouse_pos[0] // SQUARE_SIZE
    row = mouse_pos[1] // SQUARE_SIZE
    return row, col

# Boucle principale
running = True
selected_piece = None
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                mouse_pos = pygame.mouse.get_pos()
                row, col = get_square(mouse_pos)
                selected_piece = (row, col)
        elif event.type == pygame.MOUSEBUTTONUP:
            if pygame.mouse.get_pressed()[0] and selected_piece is not None:
                mouse_pos = pygame.mouse.get_pos()
                new_row, new_col = get_square(mouse_pos)
                # Vérifie si le mouvement est valide (pour l'instant, juste vérifier si la case de destination est vide)
                if board[new_row][new_col] == '__':
                    # Déplacer la pièce
                    board[new_row][new_col] = board[selected_piece[0]][selected_piece[1]]
                    board[selected_piece[0]][selected_piece[1]] = '__'
                selected_piece = None

    screen.fill(WHITE)
    draw_board()
    pygame.display.flip()

pygame.quit()
sys.exit()
