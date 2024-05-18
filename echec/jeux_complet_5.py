import pygame
import sys

# Initialisation de Pygame
pygame.init()

# Couleurs
BLANC = (255, 255, 255)
NOIR = (0, 0, 0)
ROUGE = (255, 0, 0)

# Taille de la fenêtre
largeur, hauteur = 800, 600
fenetre = pygame.display.set_mode((largeur, hauteur))
pygame.display.set_caption("Menu de Jeux")

# Police de texte
police = pygame.font.SysFont(None, 40)

class Menu:
    def __init__(self, options):
        self.options = options
        self.selected_option = 0

    def afficher(self):
        fenetre.fill(BLANC)
        self._afficher_titre()
        self._afficher_options()
        pygame.display.flip()

    def _afficher_titre(self):
        titre_surface = police.render("Menu Principal", True, NOIR)
        titre_rect = titre_surface.get_rect()
        titre_rect.center = (largeur // 2, 100)
        fenetre.blit(titre_surface, titre_rect)

    def _afficher_options(self):
        for i, option_texte in enumerate(self.options):
            couleur = NOIR if i != self.selected_option else ROUGE
            self._afficher_texte(option_texte, largeur // 2, 250 + i * 70, couleur)

    def _afficher_texte(self, texte, x, y, couleur):
        texte_surface = police.render(texte, True, couleur)
        texte_rect = texte_surface.get_rect()
        texte_rect.center = (x, y)
        fenetre.blit(texte_surface, texte_rect)

    def selectionner_option_suivante(self):
        self.selected_option = (self.selected_option + 1) % len(self.options)

    def selectionner_option_precedente(self):
        self.selected_option = (self.selected_option - 1) % len(self.options)

    def executer_action(self):
        option = self.options[self.selected_option]
        if option == "Jouer JcJ":
            return "Jeu"
        elif option == "Jouer JcIA":
            return "jeu_JcIA"
        elif option == "Options":
            return "Options"
        elif option == "Quitter":
            pygame.quit()
            sys.exit()

class EcranJeu:
    def __init__(self):
        self.message = "Jeu en cours..."

    def afficher(self):
        fenetre.fill(BLANC)
        self._afficher_message()
        pygame.display.flip()

    def _afficher_message(self):
        message_surface = police.render(self.message, True, NOIR)
        message_rect = message_surface.get_rect()
        message_rect.center = (largeur // 2, hauteur // 2)
        fenetre.blit(message_surface, message_rect)


class EcranJeuAI:
    def __init__(self):
        self.message = "Jeu en cours avec Ai..."

    def afficher(self):
        fenetre.fill(BLANC)
        self._afficher_message()
        pygame.display.flip()

    def _afficher_message(self):
        message_surface = police.render(self.message, True, NOIR)
        message_rect = message_surface.get_rect()
        message_rect.center = (largeur // 2, hauteur // 2)
        fenetre.blit(message_surface, message_rect)

class EcranOptions:
    def __init__(self):
        self.message = "Options"
        self.bouton_retour = pygame.Rect(20, 20, 100, 40)

    def afficher(self):
        fenetre.fill(BLANC)
        self._afficher_message()
        self._afficher_bouton_retour()
        pygame.display.flip()

    def _afficher_message(self):
        message_surface = police.render(self.message, True, NOIR)
        message_rect = message_surface.get_rect()
        message_rect.center = (largeur // 2, 100)
        fenetre.blit(message_surface, message_rect)

    def _afficher_bouton_retour(self):
        pygame.draw.rect(fenetre, ROUGE, self.bouton_retour)
        texte_surface = police.render("Retour", True, BLANC)
        texte_rect = texte_surface.get_rect()
        texte_rect.center = self.bouton_retour.center
        fenetre.blit(texte_surface, texte_rect)

    def verifier_clic_retour(self, pos):
        if self.bouton_retour.collidepoint(pos):
            return True
        return False

if __name__ == "__main__":
    menu = Menu(["Jouer JcJ", "Jouer JcIA", "Options", "Quitter"])
    ecran_jeu = EcranJeu()
    ecran_jeu_ai = EcranJeuAI()
    ecran_options = EcranOptions()
    ecran_actuel = "Menu"

    while True:
        if ecran_actuel == "Menu":
            menu.afficher()
        elif ecran_actuel == "Jeu":
            ecran_jeu.afficher()
        elif ecran_actuel == "jeu_JcIA":
            ecran_jeu_ai.afficher()
        elif ecran_actuel == "Options":
            ecran_options.afficher()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if ecran_actuel == "Menu":
                    if event.key == pygame.K_DOWN:
                        menu.selectionner_option_suivante()
                    elif event.key == pygame.K_UP:
                        menu.selectionner_option_precedente()
                    elif event.key == pygame.K_RETURN:
                        ecran_actuel = menu.executer_action()
                elif ecran_actuel == "Jeu":
                    if event.key == pygame.K_ESCAPE:
                        ecran_actuel = "Menu"
                elif ecran_actuel == "jeu_JcIA":
                    if event.key == pygame.K_ESCAPE:
                        ecran_actuel = "Menu"
                elif ecran_actuel == "Options":
                    if event.key == pygame.K_ESCAPE:
                        ecran_actuel = "Menu"
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if ecran_actuel == "Menu":
                    if event.button == 1:  # Clic gauche de la souris
                        if 250 <= event.pos[1] <= 320:
                            ecran_actuel = menu.executer_action()
                        elif 320 < event.pos[1] <= 390:
                            ecran_actuel = "Options"
                        elif 390 < event.pos[1] <= 460:
                            pygame.quit()
                            sys.exit()
                elif ecran_actuel == "Options":
                    if event.button == 1:  # Clic gauche de la souris
                        if ecran_options.verifier_clic_retour(event.pos):
                            ecran_actuel = "Menu"

