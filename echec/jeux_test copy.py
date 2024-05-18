import pygame
import random

# Initialisation de Pygame
pygame.init()

# Taille de la fenêtre
largeur, hauteur = 800, 600
fenetre = pygame.display.set_mode((largeur, hauteur))
pygame.display.set_caption("Feu d'artifice Pygame")

# Chargement des sons
explosion_sound = pygame.mixer.Sound("sounds/firework-show-short-64657.mp3")
explosion_sound1 = pygame.mixer.Sound("sounds/new-years-eve-in-peru-fireworks-fire-crackers-and-rockets-to-celebrate-the-new-year-pisco-peru-2012-17692.mp3")


# Classe pour les particules
class Particule(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.size = random.randint(5, 10)
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.image = pygame.Surface((self.size, self.size))
        self.image.fill(self.color)
        self.rect = self.image.get_rect(center=(x, y))
        self.vel_x = random.randint(-5, 5)
        self.vel_y = random.randint(-5, 5)
        self.gravity = 0.1

    def update(self):
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y
        self.vel_y += self.gravity

# Groupe pour les particules
particules = pygame.sprite.Group()

# Horloge pour contrôler le rythme des effets
horloge = pygame.time.Clock()
temps_ecoule = 0
temps_interval = 10  # Intervalle de temps en millisecondes

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Générer des particules à chaque intervalle de temps
    temps_ecoule += horloge.tick()
    if temps_ecoule >= temps_interval:
        temps_ecoule -= temps_interval
        # Générer des particules à une position aléatoire
        for _ in range(20):
            particule = Particule(random.randint(0, largeur), random.randint(0, hauteur))
            particules.add(particule)
        # Jouer le son d'explosion à chaque intervalle de temps
        explosion_sound.play()

    # Effacer l'écran
    fenetre.fill((0, 0, 0))

    # Mise à jour et affichage des particules
    particules.update()
    particules.draw(fenetre)

    # Rafraîchir l'écran
    pygame.display.flip()

# Quitter Pygame
pygame.quit()
