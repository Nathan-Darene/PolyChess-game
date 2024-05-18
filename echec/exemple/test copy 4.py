import pygame
import engine  # Assurez-vous d'importer le module contenant votre logique de jeu (engine.py)

class JeuJcJ:
    def __init__(self):
        self.WIDTH = self.HEIGHT = 950
        self.DIMENSION = 8
        self.SQ_SIZE = self.HEIGHT // self.DIMENSION
        self.MAX_FPS = 130
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

    def animate_move(self, move, screen, board, clock):
        # Implémentez ici votre animation de mouvement
        pass  # Placeholder pour l'implémentation réelle

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
        checkmate_image = pygame.image.load("images/victoire/fortnite-victory-royale-la-royale-png-file-8.png")
        checkmate_rect = checkmate_image.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2))

        font = pygame.font.Font(None, 36)  # Définition de la police pour le texte

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
                        screen.blit(checkmate_image, checkmate_rect)
                        text_surface = font.render("Victoire de Noir par ECHEC ET MATE", True, pygame.Color('black'))
                        text_rect = text_surface.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2))
                        screen.blit(text_surface, text_rect)
                        pygame.display.flip()
                        print('Victoire de Noir par ECHEC ET MATE')
                    else:
                        screen.blit(checkmate_image, checkmate_rect)
                        text_surface = font.render("Victoire de Blanc par ECHEC ET MATE", True, pygame.Color('black'))
                        text_rect = text_surface.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2))
                        screen.blit(text_surface, text_rect)
                        pygame.display.flip()
                        print('Victoire de  Blanc par ECHEC ET MATE')

                elif game_state.stalemate:
                    screen.blit(stalemate_image, (0, 0))
                    text_surface = font.render("Stalemate", True, pygame.Color('black'))
                    text_rect = text_surface.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2))
                    screen.blit(text_surface, text_rect)
                    pygame.display.flip()
                    print('Stalemate')

                move_made = False

            self.draw_game_state(screen, game_state, valid_moves, selected_square)
            clock.tick(self.MAX_FPS)
                
            pygame.display.flip()

        pygame.quit()

# Instanciation de la classe JeuJcJ et appel de la méthode jouer()
jeu = JeuJcJ()
jeu.jouer()
