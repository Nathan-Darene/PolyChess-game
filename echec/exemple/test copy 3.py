import pygame
from moviepy.editor import VideoFileClip
import numpy as np
import engine
import math
import sys
import time

# Initialisation de Pygame
pygame.init()

# Taille de la fenêtre
largeur, hauteur = 950, 950
fenetre = pygame.display.set_mode((largeur, hauteur))
pygame.display.set_caption("PolyChess")

# Couleurs
BLANC = (255, 255, 255)
NOIR = (0, 0, 0)

class JeuJcJ:
    def __init__(self):
        self.DIMENSION = 8
        self.SQ_SIZE = largeur // self.DIMENSION
        self.MAX_FPS = 15
        self.LOG_MOVES = True
        self.IMAGES = {}

    def load_images(self):
        pieces = ['wP', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bP', 'bR', 'bN', 'bB', 'bK', 'bQ']
        for piece in pieces:
            self.IMAGES[piece] = pygame.transform.scale(pygame.image.load(f'images/{piece}.png'), (self.SQ_SIZE, self.SQ_SIZE))

    def draw_board(self, screen):
        colors = [pygame.Color(181, 136, 98), (240, 217, 181)]
        for row in range(self.DIMENSION):
            for column in range(self.DIMENSION):
                color = colors[((row + column) % 2)]
                pygame.draw.rect(screen, color, pygame.Rect(column * self.SQ_SIZE, row * self.SQ_SIZE, self.SQ_SIZE, self.SQ_SIZE))

    def draw_pieces(self, screen, board):
        for row in range(self.DIMENSION):
            for column in range(self.DIMENSION):
                piece = board[row][column]
                if piece != '--':
                    screen.blit(self.IMAGES[piece], pygame.Rect(column * self.SQ_SIZE, row * self.SQ_SIZE, self.SQ_SIZE, self.SQ_SIZE))

    def jouer(self):
        pygame.init()
        screen = pygame.display.set_mode((largeur, hauteur))
        clock = pygame.time.Clock()

        screen.fill(pygame.Color('white'))

        game_state = engine.GameState()
        valid_moves = game_state.get_valid_moves()
        move_made = False
        self.load_images()
        running = True
        selected_square = ()
        player_clicks = []
        game_over = False

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if not game_over:
                        location = pygame.mouse.get_pos()
                        column = location[0] // self.SQ_SIZE
                        row = location[1] // self.SQ_SIZE
                        if 0 <= row < self.DIMENSION and 0 <= column < self.DIMENSION:  # Vérifiez les limites du plateau de jeu
                            piece = game_state.board[row][column]

                            if (len(player_clicks) == 0) and (
                                    (piece == '--' or piece[0] == 'w' and not game_state.white_to_move) or (
                                    piece[0] == 'b' and game_state.white_to_move)):
                                player_clicks.append((row, column))

                            elif selected_square == (row, column):
                                selected_square = ()
                                player_clicks = []

                            else:
                                selected_square = (row, column)
                                player_clicks.append(selected_square)

                            if len(player_clicks) == 2:
                                move = engine.Move(player_clicks[0], player_clicks[1], game_state.board)

                                for i in range(len(valid_moves)):
                                    if move == valid_moves[i]:
                                        if self.LOG_MOVES:
                                            print(f'Déplacement vers: {move.get_chess_notation()}')

                                        game_state.make_move(valid_moves[i])
                                        move_made = True
                                        selected_square = ()
                                        player_clicks = []

                                if not move_made:
                                    player_clicks = [selected_square]

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_z:
                        game_state.undo_move()
                        valid_moves = game_state.get_valid_moves()
                        move_made = False

                    elif event.key == pygame.K_s:
                        pygame.image.save(screen, 'capture.jpeg')
                        print('Captured screen.')

                    elif event.key == pygame.K_r:
                        game_state = engine.GameState()
                        valid_moves = game_state.get_valid_moves()
                        selected_square = ()
                        player_clicks = []
                        move_made = False

            if move_made:
                valid_moves = game_state.get_valid_moves()
                if game_state.checkmate:
                    game_over = True
                    if game_state.white_to_move:
                        print('Black wins by checkmate')
                    else:
                        print('White wins by checkmate')

                elif game_state.stalemate:  # Nouvelle condition pour le stalemate
                    print('Stalemate')

                move_made = False

            self.draw_board(screen)
            self.draw_pieces(screen, game_state.board)
            pygame.display.flip()
            clock.tick(self.MAX_FPS)

        pygame.quit()


if __name__ == "__main__":
    jeu_jcj = JeuJcJ()
    jeu_jcj.jouer()

