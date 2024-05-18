import pygame
import sys
import os

class ChessApp:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1000, 1000))
        pygame.display.set_caption("Polychess Create BY Nathan")
        self.clock = pygame.time.Clock()
        self.board = ChessboardWidget()

    def run(self):
        # Afficher le message pendant 5 secondes
        self.display_message()

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.VIDEORESIZE:
                    self.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

            self.screen.fill((240, 217, 181))
            self.board.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(60)

    def display_message(self):
        font = pygame.font.Font("font/arial.ttf", 18)  # Spécifiez le chemin absolu vers la police Arial ou une autre police prenant en charge les caractères spéciaux
        text_polychess_2 = [
            "██████╗  ██████╗ ██╗  ██╗   ██╗ ██████╗██╗  ██╗███████╗███████╗███████╗",
            "██╔══██╗██╔═══██╗██║  ╚██╗ ██╔╝██╔════╝██║  ██║██╔════╝██╔════╝██╔════╝",
            "██████╔╝██║   ██║██║   ╚████╔╝ ██║     ███████║█████╗  ███████╗███████╗",
            "██╔═══╝ ██║   ██║██║    ╚██╔╝  ██║     ██╔══██║██╔══╝  ╚════██║╚════██║",
            "██║     ╚██████╔╝███████╗██║   ╚██████╗██║  ██║███████╗███████║███████║",
            "╚═╝      ╚═════╝ ╚══════╝╚═╝    ╚═════╝╚═╝  ╚═╝╚══════╝╚══════╝╚══════╝",
            "",
            "                          ██████╗ ██╗   ██╗",
            "                          ██╔══██╗╚██╗ ██╔╝",
            "                          ██████╔╝ ╚████╔╝",
            "                          ██╔══██╗  ╚██╔╝",
            "                          ██████╔╝   ██║",
            "                          ╚═════╝    ╚═╝",
            "",
            "██╗     ██╗████████╗██████████╗██╗  ██╗████████╗██╗     ██╗",
            "██╚██╗  ██║██║   ██║    ██╔═══╝██║  ██║██║   ██║██╚██╗  ██║",
            "██║╚██  ██║████████║    ██║    ███████║████████║██║╚██  ██║",
            "██║ ╚██ ██║██╔═══██║    ██║    ██╔══██║██╔═══██║██║ ╚██ ██║",
            "██║   ╚═██║██║   ██║    ██║    ██║  ██║██║   ██║██║   ╚═██║",
            "╚═╝     ╚═╝╚═╝   ╚═╝    ╚═╝    ╚═╝  ╚═╝╚═╝   ╚═╝╚═╝     ╚═╝",]

        # Remplir l'écran avec une couleur bleue
        self.screen.fill(pygame.Color('blue'))

        # Créer une surface pour chaque ligne de texte
        text_surfaces = []
        for line in text_polychess_2:
            text_surface = font.render(line, True, pygame.Color('white'))
            text_surfaces.append(text_surface)

        # Calculer les positions x et y pour centrer le texte dans la fenêtre
        x = (self.screen.get_width() - max(surface.get_width() for surface in text_surfaces)) // 2
        y = (self.screen.get_height() - sum(surface.get_height() for surface in text_surfaces)) // 2

        # Dessiner chaque ligne de texte
        for text_surface in text_surfaces:
            # Créer une surface rectangulaire avec la couleur d'arrière-plan désirée
            text_background = pygame.Surface((text_surface.get_width(), text_surface.get_height()))
            text_background.fill(pygame.Color('blue'))  # Remplacez 'blue' par la couleur de votre choix

            # Rendre la surface du texte transparente
            text_background.set_alpha(128)  # Réglez la transparence ici (0 pour complètement transparent, 255 pour opaque)

            # Superposer la surface de texte transparente sur la surface de l'écran
            self.screen.blit(text_background, (x, y))
            self.screen.blit(text_surface, (x, y))
            y += text_surface.get_height()

        pygame.display.flip()
        pygame.time.delay(1000)  # Mettre en pause pendant 5 secondes avant de démarrer le jeu

        self.screen.fill((240, 217, 181))  # Effacer l'écran après l'affichage du message initial

        pygame.display.flip()  # Mettre à jour l'écran

class ChessboardWidget:
    def __init__(self):
        self.square_size = 100
        self.colors = [(181, 136, 98), (240, 217, 181)]
        self.board_size = self.square_size * 8
        self.offset_x = (1000 - self.board_size) // 2
        self.offset_y = (1000 - self.board_size) // 2
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
                    if row < 4:
                        piece_image = self.piece_images_noirs[piece_name]
                    else:
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

if __name__ == "__main__":
    app = ChessApp()
    app.run()
