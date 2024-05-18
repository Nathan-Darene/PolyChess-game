import pygame
import sys
import os

# from chessboard import Echiquier
# from rules import Piece
# from ia import IA
# import copy
# import time

class ChessApp:
    def __init__(self):
        pygame.init()
        self.screen_width = 1500
        self.screen_height = 1000
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Polychess Create BY Nathan")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)  # Définir la police ici
        self.board = ChessboardWidget(self.font)  # Passer la police à ChessboardWidget
        self.selected_piece = None
        self.selected_square = None
        self.help_text = None
        self.help_visible = False

    def run(self):
        self.display_image()

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.VIDEORESIZE:
                    self.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mouse_pos = pygame.mouse.get_pos()
                        col = (mouse_pos[0] - self.board.offset_x) // self.board.square_size
                        row = (mouse_pos[1] - self.board.offset_y) // self.board.square_size
                        if 0 <= row < 8 and 0 <= col < 8:
                            if self.selected_piece is None:
                                self.selected_piece = self.board.get_piece_name(row, col)
                                self.selected_square = (row, col)
                                if self.selected_piece:
                                    self.help_text = "Possible moves: " + ", ".join(self.board.get_possible_moves(row, col))
                                else:
                                    self.help_text = "No piece selected"
                            else:
                                target_square = (row, col)
                                if self.selected_piece and self.selected_square != target_square:
                                    # Move the piece
                                    if self.board.move_piece(self.selected_square, target_square):
                                        self.selected_piece = None
                                        self.selected_square = None
                                        self.help_text = None

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_h:
                        self.help_visible = not self.help_visible

            self.screen.fill((240, 217, 181))
            self.board.draw(self.screen, self.selected_square)
            if self.help_visible:
                self.display_help()
            pygame.display.flip()
            self.clock.tick(60)

    def display_image(self):
        image_path = "images/assets/logo2.png"  # Spécifiez le chemin absolu de votre image
        image = pygame.image.load(image_path)
        self.screen.fill(pygame.Color('#272a34'))
        image_rect = image.get_rect(center=(self.screen_width // 2, self.screen_height // 2))
        self.screen.blit(image, image_rect)
        pygame.display.flip()
        pygame.time.delay(5000)
        self.screen.fill((0, 0, 0))
        pygame.display.flip()

    def display_help(self):
        if self.help_text:
            text_surface = self.font.render(self.help_text, True, (255, 255, 255))
            text_rect = text_surface.get_rect(midbottom=(self.screen_width // 2, self.screen_height - 10))
            pygame.draw.rect(self.screen, (0, 0, 0), (text_rect.x - 5, text_rect.y - 5, text_rect.width + 10, text_rect.height + 10))
            self.screen.blit(text_surface, text_rect)


class ChessboardWidget:
    def __init__(self, font):
        self.square_size = 100
        self.colors = [(181, 136, 98), (240, 217, 181)]
        self.board_size = self.square_size * 8
        self.border_size = 2
        self.total_size = self.board_size + 3 * self.border_size
        self.offset_x = (1500 - self.total_size) // 2 + self.border_size
        self.offset_y = (1000 - self.total_size) // 2 + self.border_size
        self.font = font  # Stocker la police comme attribut
        self.load_pieces()

    def load_pieces(self):
        self.piece_images_blancs = {}
        self.piece_images_noirs = {}
        for couleur in ["noirs", "blancs"]:
            for filename in os.listdir(f"images/{couleur}"):
                name = filename.split(".")[0]
                if couleur == "blancs":
                    self.piece_images_blancs[name] = pygame.image.load(f"images/{couleur}/{filename}")
                else:
                    self.piece_images_noirs[name] = pygame.image.load(f"images/{couleur}/{filename}")

    def draw(self, screen, selected_square):
        border_rect = pygame.Rect((self.offset_x - self.border_size, self.offset_y - self.border_size),
                                  (self.total_size + 2 * self.border_size, self.total_size + 2 * self.border_size))

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
                    if row < 4:
                        piece_image = self.piece_images_noirs[piece_name]
                    else:
                        piece_image = self.piece_images_blancs[piece_name]
                    piece_rect = piece_image.get_rect(center=(rect[0] + self.square_size // 2, rect[1] + self.square_size // 2))
                    screen.blit(piece_image, piece_rect)

                    if (row, col) == selected_square:
                        pygame.draw.rect(screen, pygame.Color('green'), rect, 4)
            
            for i in range(8):
                number_surface = self.font.render(str(i), True, (0, 0, 0))
                screen.blit(number_surface, (self.offset_x - 40, self.offset_y + i * self.square_size + self.square_size // 2 - 15))
                screen.blit(number_surface, (self.offset_x + self.board_size + 20, self.offset_y + i * self.square_size + self.square_size // 2 - 15))
                letter_surface = self.font.render(chr(ord('A') + i), True, (0, 0, 0))
                screen.blit(letter_surface, (self.offset_x + i * self.square_size + self.square_size // 2 - 10, self.offset_y - 40))

    def get_piece_name(self, row, col):
        pieces_noires = {
            (0, 0): "Tour", (0, 1): "Cavalier", (0, 2): "Fou", (0, 3): "Reine",
            (0, 4): "Roi", (0, 5): "Fou", (0, 6): "Cavalier", (0, 7): "Tour",
            (1, 0): "Pion", (1, 1): "Pion", (1, 2): "Pion", (1, 3): "Pion",
            (1, 4): "Pion", (1, 5): "Pion", (1, 6): "Pion", (1, 7): "Pion"
        }
        pieces_blanches  = {
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

    def get_possible_moves(self, row, col):
        # Dummy implementation for getting possible moves
        return ["(0, 0)", "(0, 1)", "(0, 2)"]  # Example moves

    def move_piece(self, start_square, target_square):
        # Dummy implementation for moving the piece
        print(f"Déplacement de  {start_square} vers {target_square}")
        return True  # Return True for successful move, False otherwise

if __name__ == "__main__":
    app = ChessApp()
    app.run()