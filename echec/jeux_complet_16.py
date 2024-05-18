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
        clock.tick(160) #160 FPS (temp de rafrachissement)

    pygame.mixer.Sound.play(son_selection)  # Jouer le son après le déplacement de la pièce
