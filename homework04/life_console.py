import curses
import time

from life import GameOfLife
from ui import UI


class Console(UI):
    def __init__(self, life: GameOfLife) -> None:
        super().__init__(life)

    def draw_borders(self, screen) -> None:
        screen.clear()
        h = self.life.rows + 2
        w = self.life.cols + 2
        screen.border()
        for x in range(w):
            screen.addch(0, x, "-")
            screen.addch(h - 1, x, "-")
        for y in range(h):
            screen.addch(y, 0, "|")
            screen.addch(y, w - 1, "|")
        screen.addch(0, 0, "+")
        screen.addch(0, w - 1, "+")
        screen.addch(h - 1, 0, "+")
        screen.addch(h - 1, w - 1, "+")

    def draw_grid(self, screen) -> None:
        for r in range(self.life.rows):
            for c in range(self.life.cols):
                ch = "█" if self.life.curr_generation[r][c] == 1 else " "
                screen.addch(r + 1, c + 1, ch)

    def run(self) -> None:
        screen = curses.initscr()
        curses.noecho()
        curses.cbreak()
        screen.keypad(True)
        screen.nodelay(True)

        try:
            while self.life.is_changing and (not self.life.is_max_generations_exceeded):
                key = screen.getch()
                if key in (ord("q"), ord("Q")):
                    break

                self.draw_borders(screen)
                self.draw_grid(screen)
                screen.addstr(
                    self.life.rows + 3,
                    1,
                    f"gen={self.life.generations}  (q to quit)",
                )
                screen.refresh()

                self.life.step()
                time.sleep(0.05)

        finally:
            curses.nocbreak()
            screen.keypad(False)
            curses.echo()
            curses.endwin()
