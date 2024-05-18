import pygame

BLANC = (255, 255, 255)
NOIR = (0, 0, 0)
ROUGE = (255, 0, 0)

class EcranOptions:
    def __init__(self, options):
        self.message = "Options"
        self.options = options
        self.checkboxes = [False] * len(options)
        self.bouton_retour = pygame.Rect(20, 20, 100, 40)
        self.checkbox_size = 20  # Taille de la case à cocher
        self.checkbox_padding = 10  # Marge entre la case à cocher et le texte
        self.bouton_confirmation = pygame.Rect(300, 900, 300, 50)  # Ajout du bouton de confirmation

    def afficher(self):
        fenetre.fill(BLANC)
        self._afficher_message()
        self._afficher_options()
        self._afficher_boutons()
        pygame.display.flip()

    def _afficher_message(self):
        message_surface = police.render(self.message, True, NOIR)
        message_rect = message_surface.get_rect()
        message_rect.center = (400, 100)  # Position fixe pour l'affichage horizontal
        fenetre.blit(message_surface, message_rect)

    def _afficher_options(self):
        y = 150
        for i, (option, checkbox_state) in enumerate(zip(self.options[:-1], self.checkboxes[:-1])):  # Ignorer le dernier élément qui est le bouton "Confirmer"
            option_surface = police.render(option, True, NOIR)
            option_rect = option_surface.get_rect()
            option_rect.topleft = (self.checkbox_padding + self.checkbox_size + 10, y)
            fenetre.blit(option_surface, option_rect)
            
            # Dessiner la case à cocher
            checkbox_rect = pygame.Rect(self.checkbox_padding, y, self.checkbox_size, self.checkbox_size)
            pygame.draw.rect(fenetre, NOIR, checkbox_rect, 2)  # Dessiner le contour de la case à cocher
            if checkbox_state:
                pygame.draw.rect(fenetre, "green", checkbox_rect.inflate(-4, -4))  # Remplir la case si elle est cochée
            
            y += 30

    def _afficher_boutons(self):
        pygame.draw.rect(fenetre, ROUGE, self.bouton_retour)
        texte_surface = police.render("Retour", True, BLANC)
        texte_rect = texte_surface.get_rect()
        texte_rect.center = self.bouton_retour.center
        fenetre.blit(texte_surface, texte_rect)

        pygame.draw.rect(fenetre, ROUGE, self.bouton_confirmation)
        texte_surface = police.render("Confirmer les options", True, BLANC)  # Modifier le texte du bouton "Confirmer"
        texte_rect = texte_surface.get_rect()
        texte_rect.center = self.bouton_confirmation.center
        fenetre.blit(texte_surface, texte_rect)

    def verifier_clic_retour(self, pos):
        if self.bouton_retour.collidepoint(pos):
            return True
        return False

    def verifier_clic_confirmation(self, pos):
        if self.bouton_confirmation.collidepoint(pos):
            return True
        return False

    def verifier_clic_checkbox(self, pos):
        for i, checkbox_rect in enumerate(self._checkbox_rects()):
            if checkbox_rect.collidepoint(pos):
                self.checkboxes[i] = not self.checkboxes[i]  # Inverser l'état de la case à cocher

    def _checkbox_rects(self):
        y = 150
        rects = []
        for _ in self.options[:-1]:  # Ignorer le dernier élément qui est le bouton "Confirmer"
            checkbox_rect = pygame.Rect(self.checkbox_padding, y, self.checkbox_size, self.checkbox_size)
            rects.append(checkbox_rect)
            y += 30
        return rects


options_jeu = [
    "Mode solo contre l'ordinateur",
    "Mode multijoueur local",
    "Mode multijoueur en ligne",
    "Facile",
    "Moyen",
    "Difficile",
    "Afficher les indications de déplacement possible des pièces",
    "Masquer les indications de déplacement possible des pièces",
    "Classique",
    "Moderne",
    "Fantaisie",
    "Français",
    "Anglais",
    "Espagnol",
    "Activer le chronomètre",
    "Désactiver le chronomètre",
    "Activer les effets sonores",
    "Désactiver les effets sonores",
    "Activer la sauvegarde automatique de la partie en cours",
    "Désactiver la sauvegarde automatique de la partie en cours",
    "Clair",
    "Sombre",
    "Activer la rotation automatique de la vue pour le joueur opposé",
    "Désactiver la rotation automatique de la vue pour le joueur opposé",
    "Confirmer"  # Bouton "Confirmer les options" à la fin de la liste des options
]

pygame.init()
fenetre = pygame.display.set_mode((1000, 1000))
police = pygame.font.SysFont(None, 30)

ecran_options = EcranOptions(options_jeu)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if ecran_options.verifier_clic_retour(event.pos):
                running = False
            elif ecran_options.verifier_clic_confirmation(event.pos):
                # Insérer ici la logique pour confirmer les options sélectionnées
                pass
            else:
                ecran_options.verifier_clic_checkbox(event.pos)
    ecran_options.afficher()

pygame.quit()
