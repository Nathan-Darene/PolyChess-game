import pygame
import sys

# Définir quelques couleurs
BLANC = (255, 255, 255)
NOIR = (0, 0, 0)
BLEU = (0, 0, 255)

class ChessGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Jeu d'échecs")
        self.clock = pygame.time.Clock()
        self.board = ChessBoard()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.screen.fill(BLANC)
            self.board.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(60)

class ChessBoard:
    def __init__(self):
        self.square_size = 80
        self.board_size = self.square_size * 8
        self.piece_font = pygame.font.SysFont(None, 40)

    def draw(self, screen):
        for row in range(8):
            for col in range(8):
                color = BLANC if (row + col) % 2 == 0 else NOIR
                rect = pygame.Rect(col * self.square_size, row * self.square_size, self.square_size, self.square_size)
                pygame.draw.rect(screen, color, rect)
                # Dessiner des pièces fictives pour l'exemple
                if row == 0 and col == 0:
                    text_surface = self.piece_font.render("R", True, BLEU)
                    screen.blit(text_surface, rect.topleft)

if __name__ == "__main__":
    game = ChessGame()
    game.run()
