import pygame
import engine
import chessboard
import math
import sys

# Initialisation de Pygame
pygame.init()

# Couleurs
BLANC = (255, 255, 255)
NOIR = (0, 0, 0)
ROUGE = (255, 0, 0)

# Taille de la fenêtre
largeur, hauteur = 960, 640
fenetre = pygame.display.set_mode((largeur, hauteur))
pygame.display.set_caption("Menu de Jeux")

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
        fenetre.fill(BLANC)
        self._afficher_titre()
        self._afficher_options()
        pygame.display.flip()

    def _afficher_titre(self):
        taille_police = 80  # Définissez la taille de police souhaitée
        police = pygame.font.Font(None, taille_police)  # Créez une police avec la taille spécifiée
        
        titre_surface = police.render("PolyChess Game", True, NOIR)
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
                shape.fill(pygame.Color('blue'))
                screen.blit(shape, (column * self.SQ_SIZE, row * self.SQ_SIZE))

                for move in valid_moves:
                    if move.start_row == row and move.start_column == column:
                        if game_state.board[move.end_row][move.end_column] != '--':
                            shape.fill(pygame.Color('red'))
                            screen.blit(shape, (move.end_column * self.SQ_SIZE, move.end_row * self.SQ_SIZE))
                        else:
                            shape.fill(pygame.Color('yellow'))
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

        game_state = chessboard.GameState()
        valid_moves = game_state.get_valid_moves()
        move_made = False
        self.load_images()
        running = True
        selected_square = ()
        player_clicks = []
        game_over = False

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
                            move = chessboard.Move(player_clicks[0], player_clicks[1], game_state.board)

                            for i in range(len(valid_moves)):
                                if move == valid_moves[i]:
                                    if self.LOG_MOVES:
                                        print(f'MOVED: {move.get_chess_notation()}')

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
                        game_state = chessboard.GameState()
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

                elif game_state.stalemate:
                    game_over = True
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
    jeu_jcj = JeuJcJ()  # Ajout de l'instance de la classe JeuJcJ

    while True:
        if ecran_actuel == "Menu":
            menu.afficher()
        elif ecran_actuel == "Jeu":
            jeu_jcj.jouer()  # Afficher le jeu JeuJcJ lorsque ecran_actuel est "Jeu"
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
