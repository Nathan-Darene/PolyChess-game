import pygame
from moviepy.editor import VideoFileClip
import numpy as np
import engine
import math
import sys
import time

# Initialisation de Pygame
pygame.init()

# Couleurs
BLANC = (255, 255, 255)
NOIR = (0, 0, 0)
MARRON_CLAIR = (240, 217, 181)
MARRON = (181, 136, 98)
ROUGE = (255, 0, 0)
VERT = (0, 255, 0)
FOND=(255,221,204)

# Taille de la fenêtre
largeur, hauteur = 1500, 1000
fenetre = pygame.display.set_mode((largeur, hauteur))
pygame.display.set_caption("PolyChess")

# Police de texte
police = pygame.font.SysFont(None, 40)

# Son
pygame.mixer.init()
effet="sounds/choix2.mp3"
son_selection = pygame.mixer.Sound(effet)

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
        self.WIDTH = self.HEIGHT = 950
        self.DIMENSION = 8
        self.SQ_SIZE = self.HEIGHT // self.DIMENSION
        self.MAX_FPS = 15
        self.LOG_MOVES = True
        self.IMAGES = {}

    def load_images(self):
        pieces = ['wP', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bP', 'bR', 'bN', 'bB', 'bK', 'bQ']
        for piece in pieces:
            self.IMAGES[piece] = pygame.transform.scale(pygame.image.load(f'images/{piece}.png'), (self.SQ_SIZE, self.SQ_SIZE))

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
        self.load_images()
        running = True
        selected_square = ()
        player_clicks = []
        game_over = False

        stalemate_image = pygame.image.load("images/victoire/fortnite-logo-transparent-symbol-2.png")
        game_over_image = pygame.image.load("images/victoire/fortnite-victory-royale-la-royale-png-file-8.png")
        game_over_rect = game_over_image.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2))

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

                if game_state.checkmate:
                    game_over = True
                    if game_state.white_to_move:
                        print('Black wins by checkmate')
                    else:
                        print('White wins by checkmate')

                elif game_state.stalemate:  # Nouvelle condition pour le stalemate
                    # screen.fill(pygame.Color("white"))  # Efface l'écran
                    screen.blit(stalemate_image, (0, 0))  # Affiche l'image de stalemate
                    font = pygame.font.Font(None, 36)
                    text_surface = font.render("Stalemate", True, pygame.Color("black"))
                    text_rect = text_surface.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2))
                    screen.blit(text_surface, text_rect)
                    pygame.display.flip()
                    print('Stalemate')

                move_made = False

            self.draw_game_state(screen, game_state, valid_moves, selected_square)
            clock.tick(self.MAX_FPS)
                
            pygame.display.flip()

        pygame.quit()

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
            clock.tick(160) #160 FPS temp de rafrachissement

    def afficher_video_chargement(self):
        # Charger et afficher la vidéo de chargement
        video = pygame.movie.Movie("video/chargement.mp4")  # Chemin vers votre vidéo de chargement
        video_screen = pygame.Surface((largeur, hauteur))
        video.set_display(video_screen, (0, 0, largeur, hauteur))
        video.play()

        time.sleep(10)  # Afficher la vidéo pendant 10 secondes



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

class EcranChargement:
    def __init__(self):
        self.video = VideoFileClip("video/6824-196344457_small.mp4")
        self.video_surface = pygame.Surface((self.video.size[0], self.video.size[1])).convert()
        self.video.set_duration(10)  # Définition la durée de la vidéo à 3 secondes
        self.video.set_position(("center", "center"))
        self.video.set_audio(None)  # Désactiveation de l'audio de la vidéo

    def afficher(self):
        fenetre.fill(BLANC)
        self.video_blit = self.video.get_frame(pygame.time.get_ticks() / 1000)  # Obtention du cadre actuel de la vidéo
        self.video_surface.blit(pygame.image.frombuffer(self.video_blit, self.video.size, 'RGB'), (0, 0))
        fenetre.blit(self.video_surface, (0, 0))
        pygame.display.flip()

    def video_terminee(self):
        return not self.video.is_playing(pygame.time.get_ticks() / 1000)

# class EcranChargement:
#     def __init__(self):
#         self.video = VideoFileClip("video/6824-196344457_small.mp4")
#         self.video_surface = pygame.Surface((largeur, hauteur)).convert()
#         self.video_duration = 6  # Durée de la vidéo en secondes
#         self.video_play_time = 6  # Temps écoulé depuis le début de la vidéo

#     def afficher(self):
#         fenetre.fill(BLANC)
#         self.video_play_time += pygame.time.get_ticks() / 1000  # Mise à jour du temps écoulé
#         if self.video_play_time >= self.video_duration:
#             self.video_play_time = self.video_duration
#         self.video_blit = self.video.get_frame(self.video_play_time)  # Obtention du cadre actuel de la vidéo
#         self.video_surface.blit(pygame.image.frombuffer(self.video_blit, self.video.size, 'RGB'), (0, 0))
#         fenetre.blit(self.video_surface, (0, 0))
#         pygame.display.flip()

#     def video_terminee(self):
#         return self.video_play_time >= self.video_duration



# Ajouter une instance de la classe EcranChargement
# ecran_chargement = EcranChargement()

class EcranJeuAI:
    def __init__(self):
        self.message = "Jeu en cours de travaux..."

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
