import pygame
import random

# Initialisation de Pygame
pygame.init()

# Taille de la fenêtre
largeur, hauteur = 800, 600
fenetre = pygame.display.set_mode((largeur, hauteur))
pygame.display.set_caption("Animation de particules")

# Couleurs
BLANC = (255, 255, 255)
NOIR = (0, 0, 0)
ROUGE = (255, 0, 0)
VERT = (0, 255, 0)

# Classe de particule
class Particule:
    def __init__(self, x, y, couleur):
        self.x = x
        self.y = y
        self.couleur = couleur
        self.vitesse_x = random.uniform(-1, 1)
        self.vitesse_y = random.uniform(-5, -1)
        self.duree_vie = random.randint(30, 60)

    def mettre_a_jour(self):
        self.x += self.vitesse_x
        self.y += self.vitesse_y
        self.duree_vie -= 1

    def afficher(self, surface):
        pygame.draw.circle(surface, self.couleur, (int(self.x), int(self.y)), 5)

# Génération de particules
def generer_particules(nombre):
    particules = []
    for _ in range(nombre):
        x = largeur // 2
        y = hauteur
        couleur = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))
        particule = Particule(x, y, couleur)
        particules.append(particule)
    return particules

# Fonction principale
def animation_particules():
    particules = generer_particules(100)

    running = True
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        fenetre.fill(NOIR)

        # Mise à jour et affichage des particules
        for particule in particules:
            particule.mettre_a_jour()
            particule.afficher(fenetre)

        # Suppression des particules éteintes
        particules = [particule for particule in particules if particule.duree_vie > 0]

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

# Lancer l'animation
animation_particules()
