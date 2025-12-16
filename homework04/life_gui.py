import pygame
import pygame
from pygame.locals import K_SPACE, QUIT
from life import GameOfLife
from ui import UI


class GUI(UI):
    def __init__(self, life: GameOfLife, cell_size: int = 10, speed: int = 10) -> None:
        super().__init__(life)
        self.cell_size = cell_size
        self.speed = speed

        self.width = self.life.cols * self.cell_size
        self.height = self.life.rows * self.cell_size
        self.screen = pygame.display.set_mode((self.width, self.height))

        self.paused = False

    def draw_lines(self) -> None:
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (self.width, y))

    def draw_grid(self) -> None:
        for r in range(self.life.rows):
            for c in range(self.life.cols):
                is_alive = self.life.curr_generation[r][c] == 1
                color = pygame.Color("green") if is_alive else pygame.Color("white")
                rect = pygame.Rect(
                    c * self.cell_size,
                    r * self.cell_size,
                    self.cell_size,
                    self.cell_size,
                )
                pygame.draw.rect(self.screen, color, rect)

    def run(self) -> None:
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False

                if event.type == pygame.KEYDOWN and event.key == K_SPACE:
                    self.paused = not self.paused

                if self.paused and event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    c = x // self.cell_size
                    r = y // self.cell_size
                    if 0 <= r < self.life.rows and 0 <= c < self.life.cols:
                        self.life.curr_generation[r][c] = 1 - self.life.curr_generation[r][c]

            if not self.paused and self.life.is_changing and not self.life.is_max_generations_exceeded:
                self.life.step()

            self.screen.fill(pygame.Color("white"))
            self.draw_grid()
            self.draw_lines()

            pygame.display.flip()
            clock.tick(self.speed)

        pygame.quit()
