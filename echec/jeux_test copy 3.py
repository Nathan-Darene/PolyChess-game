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
    def __init__(self, x, y, couleur, direction):
        self.x = x
        self.y = y
        self.couleur = couleur
        self.vitesse_x = random.uniform(-1, 1) * direction
        self.vitesse_y = random.uniform(-5, -1)
        self.duree_vie = random.randint(30, 60)

    def mettre_a_jour(self):
        self.x += self.vitesse_x
        self.y += self.vitesse_y
        self.duree_vie -= 1

    def afficher(self, surface):
        pygame.draw.circle(surface, self.couleur, (int(self.x), int(self.y)), 5)

# Génération de particules
def generer_particules(nombre, direction):
    particules = []
    for _ in range(nombre):
        x = random.randint(0, largeur) if direction == 1 else random.randint(0, largeur)  # Générer aléatoirement à gauche ou à droite
        y = hauteur
        couleur = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))
        particule = Particule(x, y, couleur, direction)
        particules.append(particule)
    return particules

# Fonction principale
def animation_particules():
    particules_gauche = generer_particules(100, -1)
    particules_droite = generer_particules(100, 1)

    running = True
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        fenetre.fill(NOIR)

        # Mise à jour et affichage des particules à gauche
        for particule in particules_gauche:
            particule.mettre_a_jour()
            particule.afficher(fenetre)

        # Mise à jour et affichage des particules à droite
        for particule in particules_droite:
            particule.mettre_a_jour()
            particule.afficher(fenetre)

        # Suppression des particules éteintes à gauche
        particules_gauche = [particule for particule in particules_gauche if particule.duree_vie > 0]

        # Suppression des particules éteintes à droite
        particules_droite = [particule for particule in particules_droite if particule.duree_vie > 0]

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

# Lancer l'animation
animation_particules()
