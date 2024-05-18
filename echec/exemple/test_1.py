    
import pygame
import sys

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()
        self.load_images()

    def load_images(self):
        self.image_true = pygame.image.load("images/victoire/fortnite-logo-transparent-symbol-2.png").convert_alpha()
        self.image_false = pygame.image.load("images/victoire/138-1384473_clipart-travaux.png").convert_alpha()

         # Redimensionner les images à une taille plus petite
        self.image_true = pygame.transform.scale(self.image_true, (100, 100))
        self.image_false = pygame.transform.scale(self.image_false, (100, 100))
    def is_even(self, number):
        return number % 2 == 0

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.screen.fill((255, 255, 255))  # Fond blanc

            # Demander à l'utilisateur d'entrer deux nombres
            number1 = int(input("Entrez le premier nombre entier : "))
            number2 = int(input("Entrez le deuxième nombre entier : "))

            # Calculer la somme des deux nombres
            sum_numbers = number1 + number2

            # Vérifier si la somme est paire ou impaire
            if self.is_even(sum_numbers):
                self.screen.blit(self.image_true, (100, 100))  # Afficher l'image_true si la somme est paire
            else:
                self.screen.blit(self.image_false, (100, 100))  # Afficher l'image_false si la somme est impaire

            pygame.display.flip()
            self.clock.tick(60)

if __name__ == "__main__":
    game = Game()
    game.run()
