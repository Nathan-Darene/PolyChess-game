import pygame
from moviepy.editor import VideoFileClip
import numpy as np
import engine
import math
import sys
import random
import time

# Initialisation de Pygameygame.init()

# Couleurs
BLANC = (255, 255, 255)
NOIR = (0, 0, 0)
MARRON_CLAIR = (240, 217, 181)
MARRON = (181, 136, 98)
ROUGE = (255, 0, 0)
VERT = (0, 255, 0)
FOND=(255,221,204)
FOND1=(4,5,8,255)
FOND2=(31,37,40,255)
OR = (255,215,0)
ORANGE = (214, 125, 8)
NOIR_DOUCE = (29, 29, 28)
# Taille de la fenêtre
largeur, hauteur = 1920, 1080
fenetre = pygame.display.set_mode((largeur, hauteur))
pygame.display.set_caption("PolyChess")

# Police de texte
police = pygame.font.SysFont(None, 40)

# Son
pygame.mixer.init()
effet="sounds/choix.mp3"
effet_1 = "sounds/choix2.mp3"
effet_2 = "sounds/choix3.mp3"
effet_3 = "sounds/choix4.mp3"
effet_4 = "sounds/choix5.mp3"
effet_5 = "sounds/choix6.mp3"
effet_6 = "sounds/choix7.mp3"



son_selection = pygame.mixer.Sound(effet)
son_selection_move = pygame.mixer.Sound(effet_2)
son_selection_capture2 = pygame.mixer.Sound(effet_5)


class Menu:
    def __init__(self, options):
        self.options = options
        self.selected_option = 0

    def afficher(self):
        fenetre.fill(FOND)
        self._afficher_titre()
        self._afficher_options()
        pygame.display.flip()

    def _afficher_titre(self):
        chemin_police = "font/font_7/ka1.ttf"
        chemin_police1 = "font/font_4/Coffee Normal.ttf"
        chemin_police2 = "font/font_3/Deep Hero.ttf"
        chemin_police3 = "font/font_2/Romania.ttf"
        chemin_police4 = "font/font_1/LasAmericas_PERSONAL_USE_ONLY.otf"

#taille  et police du texte
        taille_police_0 = 50
        police_0 = pygame.font.Font(chemin_police, taille_police_0)  # Chargement de la police depuis le chemin spécifié

        #taille  et police du texte1
        taille_police = 80
        police = pygame.font.Font(chemin_police, taille_police)  # Chargement de la police depuis le chemin spécifié

        #taille  et police du texte2
        taille_police_1 = 30
        police_1 = pygame.font.Font(chemin_police, taille_police_1)  # Chargement de la police depuis le chemin spécifié

        #taille  et police du texte3
        taille_police_2 = 50
        police_2 = pygame.font.Font(chemin_police, taille_police_2)  # Chargement de la police depuis le chemin spécifié

        #texte
        first_surface = police_0.render("WELCOM TO", True, NOIR)
        
        #texte1
        titre_surface = police.render("PolyChess Game", True, NOIR)
        #texte2
        createur = police_1.render("Create By ", True, NOIR)
        #texte3
        auteur = police_2.render("Nathan Et Sana", True, MARRON)

        #position du texte
        first_surface_rect = first_surface.get_rect()
        titre_rect = titre_surface.get_rect()
        createur_rect = createur.get_rect()
        auteur_rect = auteur.get_rect()


        #position du texte
        first_surface_rect.center = (largeur // 2, 50) 
        titre_rect.center = (largeur // 2, 160)
        createur_rect.center = (largeur // 2, 250)
        auteur_rect.center = (largeur // 2, 350)


        #affiche du texte
        fenetre.blit(first_surface, first_surface_rect)
        fenetre.blit(titre_surface ,titre_rect)
        fenetre.blit(createur ,createur_rect)
        fenetre.blit(auteur ,auteur_rect)


    def _afficher_options(self):
        chemin_police = "font/font_7/ka1.ttf"
        taille_police = 50
        police = pygame.font.Font(chemin_police, taille_police)
        for i, option_texte in enumerate(self.options):
            couleur = NOIR if i != self.selected_option else VERT
            self._afficher_texte(option_texte, largeur // 2, 500 + i * 100, couleur,police)

    def _afficher_texte(self, texte, x, y, couleur,police):
        texte_surface = police.render(texte, True, couleur)
        texte_rect = texte_surface.get_rect()
        texte_rect.center = (x, y)
        fenetre.blit(texte_surface, texte_rect)

    def selectionner_option_suivante(self):
        self.selected_option = (self.selected_option + 1) % len(self.options)
        son_selection.play()  # Jouer le son de sélection

    def selectionner_option_precedente(self):
        self.selected_option = (self.selected_option - 1) % len(self.options)
        son_selection.play()  # Jouer le son de sélection

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

class JeuJcJ:
    def __init__(self):
        self.WIDTH = self.HEIGHT = 900
        self.DIMENSION = 8
        self.SQ_SIZE = self.HEIGHT // self.DIMENSION
        self.MAX_FPS = 15
        self.LOG_MOVES = True
        self.IMAGES = {}
        self.clock = pygame.time.Clock()
        self.load_images()
        self.load_victory_images()  # Ensure images are loaded when the instance is created

    def load_images(self):
        pieces = ['wP', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bP', 'bR', 'bN', 'bB', 'bK', 'bQ']
        for piece in pieces:
            self.IMAGES[piece] = pygame.transform.scale(pygame.image.load(f'images/{piece}.png'), (self.SQ_SIZE, self.SQ_SIZE))

    def load_victory_images(self):
        try:
            self.image_checkmate = pygame.image.load("images/victoire/fortnite-logo-transparent-symbol-2.png").convert_alpha()
            self.image_stalemate = pygame.image.load("images/victoire/fortnite-victory-royale-la-royale-png-file-8.png").convert_alpha()

            # Redimensionner les images à une taille plus petite
            self.image_checkmate = pygame.transform.scale(self.image_checkmate, (300, 300))
            self.image_stalemate = pygame.transform.scale(self.image_stalemate, (300, 300))
            print("Images loaded successfully.")
        except pygame.error as e:
            print(f"Error loading images: {e}")

    def draw_board(self, screen):
        colors = [pygame.Color(181, 136, 98), (240, 217, 181)]
        for row in range(self.DIMENSION):
            for column in range(self.DIMENSION):
                color = colors[((row + column) % 2)]
                pygame.draw.rect(screen, color, pygame.Rect(column * self.SQ_SIZE, row * self.SQ_SIZE, self.SQ_SIZE, self.SQ_SIZE))

    def draw_pieces(self, screen, board):
        for row in range(self.DIMENSION):
            for column in range(self.DIMENSION):
                piece = board[row][column]
                if piece != '--':
                    screen.blit(self.IMAGES[piece], pygame.Rect(column * self.SQ_SIZE, row * self.SQ_SIZE, self.SQ_SIZE, self.SQ_SIZE))

    def highlight_squares(self, screen, game_state, valid_moves, selected_square):
        if selected_square != ():
            row, column = selected_square
            if game_state.board[row][column][0] == ('w' if game_state.white_to_move else 'b'):
                shape = pygame.Surface((self.SQ_SIZE, self.SQ_SIZE))
                shape.set_alpha(100)
                shape.fill(pygame.Color('#0000FF'))
                screen.blit(shape, (column * self.SQ_SIZE, row * self.SQ_SIZE))

                for move in valid_moves:
                    if move.start_row == row and move.start_column == column:
                        if game_state.board[move.end_row][move.end_column] != '--':
                            shape.fill(pygame.Color('#19FF19'))
                            screen.blit(shape, (move.end_column * self.SQ_SIZE, move.end_row * self.SQ_SIZE))
                        else:
                            shape.fill(pygame.Color('#2BFF00'))
                            screen.blit(shape, (move.end_column * self.SQ_SIZE, move.end_row * self.SQ_SIZE))

    def draw_game_state(self, screen, game_state, valid_moves, selected_square):
        self.draw_board(screen)
        self.highlight_squares(screen, game_state, valid_moves, selected_square)
        self.draw_pieces(screen, game_state.board)

    def jouer(self):
        pygame.init()
        screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        clock = pygame.time.Clock()

        screen.fill(pygame.Color('white'))

        game_state = engine.GameState()
        valid_moves = game_state.get_valid_moves()
        move_made = False
        running = True
        selected_square = ()
        player_clicks = []
        game_over = False

        chemin_police_victoire = "font/font_4/Coffee Normal.ttf"
        taille_police_victoire = 45
        police_victoire = pygame.font.Font(chemin_police_victoire, taille_police_victoire)

        # couleur = "#7c3c24"


        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if not game_over:
                        location = pygame.mouse.get_pos()
                        column = location[0] // self.SQ_SIZE
                        row = location[1] // self.SQ_SIZE
                        piece = game_state.board[row][column]

                        if (len(player_clicks) == 0) and (
                                (piece == '--' or piece[0] == 'w' and not game_state.white_to_move) or (
                                piece[0] == 'b' and game_state.white_to_move)):
                            player_clicks.append((row, column))

                        elif selected_square == (row, column):
                            selected_square = ()
                            player_clicks = []

                        else:
                            selected_square = (row, column)
                            player_clicks.append(selected_square)

                        if len(player_clicks) == 2:
                            move = engine.Move(player_clicks[0], player_clicks[1], game_state.board)

                            for i in range(len(valid_moves)):
                                if move == valid_moves[i]:
                                    if self.LOG_MOVES:
                                        print(f'Déplacement vers: {move.get_chess_notation()}')

                                    game_state.make_move(valid_moves[i])
                                    move_made = True
                                    selected_square = ()
                                    player_clicks = []

                            if not move_made:
                                player_clicks = [selected_square]

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_z:
                        game_state.undo_move()
                        valid_moves = game_state.get_valid_moves()
                        move_made = False

                    elif event.key == pygame.K_s:
                        pygame.image.save(screen, 'capture.jpeg')
                        print('Captured screen.')

                    elif event.key == pygame.K_r:
                        game_state = engine.GameState()
                        valid_moves = game_state.get_valid_moves()
                        selected_square = ()
                        player_clicks = []
                        move_made = False

            if move_made:
                if not game_state.move_log[-1].is_enpassant_move and not game_state.move_log[-1].is_castle_move:
                    self.animate_move(game_state.move_log[-1], screen, game_state.board, clock)

                valid_moves = game_state.get_valid_moves()

                if game_state.checkmate or game_state.stalemate:
                    game_over = True

                move_made = False

            self.draw_game_state(screen, game_state, valid_moves, selected_square)
            
            if game_over:
                if game_state.checkmate:
                    print("Checkmate! Displaying checkmate image.")
                    if game_state.white_to_move:
                        text_surface = police_victoire.render("Victoire des Noirs", True, NOIR_DOUCE)
                        text_rect = text_surface.get_rect()
                        text_rect.center = (900 // 2, 300)  # Positionnez le texte sous l'image de victoire
                        screen.blit(text_surface, text_rect)
                        print('Victoire des Noirs par ECHEC et MATE')  # Affiche un message correspondant à la victoire des Noirs
                    else:
                        text_surface = police_victoire.render("Victoire des Blancs", True, NOIR_DOUCE)
                        text_rect = text_surface.get_rect()
                        text_rect.center = (900 // 2, 500)  # Positionnez le texte sous l'image de victoire
                        screen.blit(text_surface, text_rect)
                        print('Victoire des Blancs par ECHEC et MATE')
                    screen.blit(self.image_checkmate, (300, 200))  # Afficher l'image en cas d'échec et mat
                elif game_state.stalemate:
                    print("Stalemate! Displaying stalemate image.")
                    print('Stalemate')
                    screen.blit(self.image_stalemate, (300, 230))  # Afficher l'image en cas de stalemate

            clock.tick(self.MAX_FPS)
            pygame.display.flip()

        pygame.quit()

        # Pour centrer l'image horizontalement :

        # La marge gauche sera (largeur de la fenêtre - largeur de l'image) / 2
        # Dans ce cas, (900 - 300) / 2 = 300 pixels de marge à gauche
        # Pour centrer l'image verticalement :

        # La marge supérieure sera (hauteur de la fenêtre - hauteur de l'image) / 2
        # Dans ce cas, (900 - 300) / 2 = 300 pixels de marge en haut

    def animate_move(self, move, screen, board, clock):
        colors = [pygame.Color(181, 136, 98), (240, 217, 181)]
        delta_row = move.end_row - move.start_row
        delta_column = move.end_column - move.start_column
        frames_per_square = round(math.sqrt(abs(delta_row) ** 2 + abs(delta_column) ** 2))
        frames_per_square = (frames_per_square + (round(self.DIMENSION / 2) - frames_per_square) * 2) if (frames_per_square + (round(self.DIMENSION / 2) - frames_per_square) * 2) > 0 else 1
        frame_count = (abs(delta_row) + abs(delta_column)) * frames_per_square

        for frame in range(frame_count + 1):
            row, column = (move.start_row + delta_row * frame / frame_count, move.start_column + delta_column * frame / frame_count)
            self.draw_board(screen)
            self.draw_pieces(screen, board)
            color = colors[(move.end_row + move.end_column) % 2]
            end_square = pygame.Rect(move.end_column * self.SQ_SIZE, move.end_row * self.SQ_SIZE, self.SQ_SIZE, self.SQ_SIZE)
            pygame.draw.rect(screen, color, end_square)

            if move.piece_captured != '--':
                screen.blit(self.IMAGES[move.piece_captured], end_square)

            screen.blit(self.IMAGES[move.piece_moved], pygame.Rect(column * self.SQ_SIZE, row * self.SQ_SIZE, self.SQ_SIZE, self.SQ_SIZE))
            pygame.display.flip()
            clock.tick(60)

        pygame.mixer.Sound.play(son_selection_move)  # Jouer le son après le déplacement de la pièce

class EcranChargement:
    def __init__(self):
        char1 = "video/75436-556022149_small.mp4"
        char2 = "video/6824-196344457_small.mp4"
        char3 = "video/49740-459802154_small.mp4"
        char4 = "video/111036-689918641_small.mp4"
        char5 = "video/6824-196344457.mp4"
        
        self.video = VideoFileClip(char5)
        self.video_surface = pygame.Surface((self.video.size[0], self.video.size[1])).convert()
        self.video.set_duration(30)  # Définition de la durée de la vidéo à 30 secondes
        self.video.set_position(("center", "center"))
        self.video.set_audio(None)  # Désactivation de l'audio de la vidéo
        self.start_time = pygame.time.get_ticks()  # Temps de démarrage de l'affichage de la vidéo
        self.loop_count = 0  # Initialisation du compteur de boucles

    def afficher(self):
        fenetre.fill(FOND2)
        # Calcul de l'instant actuel dans la vidéo en secondes
        video_time = (pygame.time.get_ticks() - self.start_time) / 1000
        # Vérification si le temps écoulé a atteint ou dépassé la durée de la vidéo
        if video_time >= self.video.duration:
            # Incrémenter le compteur de boucles
            self.loop_count += 1
            # Vérifier si le nombre de boucles est atteint
            if self.loop_count >= 2:
                # Arrêter la vidéo
                return
            # Réinitialiser le temps de démarrage pour afficher la vidéo en boucle
            self.start_time = pygame.time.get_ticks()
        # Obtention du cadre actuel de la vidéo
        self.video_blit = self.video.get_frame(video_time % self.video.duration)  # Utiliser le reste de la division pour boucler la vidéo
        self.video_surface.blit(pygame.image.frombuffer(self.video_blit, self.video.size, 'RGB'), (0, 0))
        fenetre.blit(self.video_surface, (0, 0))
        pygame.display.flip()

    def video_terminee(self):
        # La vidéo est considérée comme terminée après avoir bouclé trois fois
        return self.loop_count >= 2


class EcranJeuAI:
    def __init__(self):
        self.message = "partie du jeux en cours de travaux ..."
        self.message1 = "Merci de votre patience"
        self.police1 = pygame.font.Font(None, 36)  # Charger une police par défaut avec une taille de 36 points
        self.police = pygame.font.Font("font/font_4/Coffee Normal.ttf", 48)  # Charger une police personnalisée
        self.image = pygame.image.load("images/victoire/138-1384473_clipart-travaux.png")  # Charger votre image
        self.largeur_image=300
        self.hauteur_image=280
        self.image = pygame.transform.scale(self.image, (self.largeur_image, self.hauteur_image))  # Redimensionner l'image
        self.image_rect = self.image.get_rect()
        self.image_rect.center = (largeur // 2, hauteur // 3)  # Positionner l'image au centre de l'écran

    def afficher(self):
        fenetre.fill(BLANC)
        self._afficher_image()  # Afficher l'image en premier
        self._afficher_message()  # Afficher le message par-dessus l'image
        pygame.display.flip()

    def _afficher_image(self):
        fenetre.blit(self.image, self.image_rect)

    def _afficher_message(self):
        message_surface = self.police.render(self.message, True, ROUGE)
        message_surface_1= self.police.render(self.message1, True, NOIR)
        message_rect = message_surface.get_rect()
        message_rect_1 = message_surface_1.get_rect()
        message_rect.center = (largeur // 2, hauteur // 2)
        message_rect_1.center = (largeur // 2, hauteur // 1.80)

        fenetre.blit(message_surface, message_rect)
        fenetre.blit(message_surface_1, message_rect_1)


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
    # ecran_jeu = EcranJeu()
    ecran_jeu_ai = EcranJeuAI()
    ecran_options = EcranOptions()
    ecran_chargement = EcranChargement()  # Ajoutez une instance de la classe EcranChargement

    ecran_actuel = "Menu"
    jeu_jcj = JeuJcJ()  # Ajout de l'instance de la classe JeuJcJ

    while True:
        if ecran_actuel == "Menu":
            menu.afficher()
        elif ecran_actuel == "Jeu":
            if ecran_chargement.video_terminee():
                jeu_jcj.jouer()  # Afficher le jeu JeuJcJ lorsque ecran_actuel est "Jeu"
            else:
                ecran_chargement.afficher()
        elif ecran_actuel == "jeu_JcIA":
            if ecran_chargement.video_terminee():
                ecran_jeu_ai.afficher() # Afficher le jeu JeuJcJ lorsque ecran_actuel est "Jeu"
            else:
                ecran_chargement.afficher()
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
