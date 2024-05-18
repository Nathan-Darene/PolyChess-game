import pygame
import sys

class ChessApp:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 800))
        pygame.display.set_caption("Polychess")
        self.clock = pygame.time.Clock()
        self.board = ChessboardWidget()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.VIDEORESIZE:
                    self.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

            self.screen.fill((240, 217, 181))
            self.board.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(60)

class ChessboardWidget:
    def __init__(self):
        self.square_size = 100
        self.colors = [(181, 136, 98), (240, 217, 181)]
        self.board_size = self.square_size * 8
        self.offset_x = (800 - self.board_size) // 2
        self.offset_y = (800 - self.board_size) // 2

    def draw(self, screen):
        for row in range(8):
            for col in range(8):
                color = self.colors[(row + col) % 2]
                rect = (self.offset_x + col * self.square_size, 
                        self.offset_y + row * self.square_size, 
                        self.square_size, 
                        self.square_size)
                pygame.draw.rect(screen, color, rect)

if __name__ == "__main__":
    app = ChessApp()
    app.run()

