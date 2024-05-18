import pygame
import sys
import os
from chessboard import Echiquier  # Importez les classes du jeu
from ia import IA

class ChessApp:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 800))
        pygame.display.set_caption("Polychess")
        self.clock = pygame.time.Clock()
        self.echiquier = Echiquier()  # Initialisez l'échiquier
        self.ia = IA(self.echiquier, 'noir')  # Initialisez l'IA pour le mode JcIA
        self.modeDeJeu = None  # Initialisez la variable de mode de jeu

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.VIDEORESIZE:
                    self.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

            self.screen.fill((240, 217, 181))
            self.echiquier.afficher()  # Affichez l'échiquier dans la fenêtre

            # Exécutez le tour du joueur pour le mode JcJ ou JcIA
            if self.modeDeJeu == "JcJ":
                self.tourDuJoueur('blanc')
            elif self.modeDeJeu == "JcIA":
                self.tourDuJoueurIA('blanc')

            pygame.display.flip()
            self.clock.tick(60)

    # Autres méthodes de la classe ChessApp

if __name__ == "__main__":
    app = ChessApp()
    app.modeDeJeu = input("Voulez-vous jouer contre l'ordinateur (entrez : JcIA) ou contre un joueur (entrez : JcJ) ?\n\n")
    app.run()

