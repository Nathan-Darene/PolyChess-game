import pygame
import sys
import os
from chessboard import Echiquier  # Importez les classes du jeu
from ia import IA
import main

class ChessApp:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 800))
        pygame.display.set_caption("Polychess Create BY Nathan")
        self.clock = pygame.time.Clock()
        self.board = ChessboardWidget()
        self.echiquier = Echiquier()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.VIDEORESIZE:
                    self.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    col = (x - self.board.offset_x) // self.board.square_size
                    row = (y - self.board.offset_y) // self.board.square_size
                    if 0 <= row < 8 and 0 <= col < 8:
                        position = chr(ord('A') + col) + str(8 - row)
                        if self.echiquier.get_piece_at_position(position):
                            main(self.echiquier, position)
                            self.board.update_board(self.echiquier)

            self.screen.fill((240, 217, 181))
            self.board.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(60)

class ChessboardWidget:
    def __init__(self):
        self.square_size = 100
        self.colors = [(181, 136, 98), (240, 217, 181)]
        self.board_size = self.square_size * 8
        self.offset_x = (800 - self.board_size) // 2
        self.offset_y = (800 - self.board_size) // 2
        self.load_pieces()

    def load_pieces(self):
        self.piece_images_blancs = {}
        self.piece_images_noirs = {}
        for couleur in ["noirs", "blancs"]:  # Inversion de l'ordre de chargement
            for filename in os.listdir(f"images/{couleur}"):
                name = filename.split(".")[0]
                if couleur == "blancs":
                    self.piece_images_blancs[name] = pygame.image.load(f"images/{couleur}/{filename}")
                else:
                    self.piece_images_noirs[name] = pygame.image.load(f"images/{couleur}/{filename}")


    def draw(self, screen):
        for row in range(8):
            for col in range(8):
                color = self.colors[(row + col) % 2]
                rect = (self.offset_x + col * self.square_size, 
                        self.offset_y + row * self.square_size, 
                        self.square_size, 
                        self.square_size)
                pygame.draw.rect(screen, color, rect)
                piece_name = self.get_piece_name(row, col)
                if piece_name:
                    if row < 4:  # Afficher les pièces noires en haut
                        piece_image = self.piece_images_noirs[piece_name]
                    else:  # Afficher les pièces blanches en bas
                        piece_image = self.piece_images_blancs[piece_name]
                    piece_rect = piece_image.get_rect(center=(rect[0] + self.square_size // 2, rect[1] + self.square_size // 2))
                    screen.blit(piece_image, piece_rect)


    def get_piece_name(self, row, col):
        pieces_blanches = {
            (0, 0): "Tour", (0, 1): "Cavalier", (0, 2): "Fou", (0, 3): "Reine",
            (0, 4): "Roi", (0, 5): "Fou", (0, 6): "Cavalier", (0, 7): "Tour",
            (1, 0): "Pion", (1, 1): "Pion", (1, 2): "Pion", (1, 3): "Pion",
            (1, 4): "Pion", (1, 5): "Pion", (1, 6): "Pion", (1, 7): "Pion"
        }
        pieces_noires = {
            (6, 0): "Pion", (6, 1): "Pion", (6, 2): "Pion", (6, 3): "Pion",
            (6, 4): "Pion", (6, 5): "Pion", (6, 6): "Pion", (6, 7): "Pion",
            (7, 0): "Tour", (7, 1): "Cavalier", (7, 2): "Fou", (7, 3): "Reine",
            (7, 4): "Roi", (7, 5): "Fou", (7, 6): "Cavalier", (7, 7): "Tour",
        }
        if (row, col) in pieces_blanches:
            return pieces_blanches[(row, col)]
        elif (row, col) in pieces_noires:
            return pieces_noires[(row, col)]
        return None

    def update_board(self, echiquier):
        # Mise à jour de l'échiquier affiché
        pass

if __name__ == "__main__":
    app = ChessApp()
    app.run()
