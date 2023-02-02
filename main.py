import math
import time
from typing import *
import sys
import pygame
import random

pygame.init()
pygame.mixer.init()

FPS = 60
clock = pygame.time.Clock()
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
SCREEN_SURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
STONE_SOUND = pygame.mixer.Sound('stone-dropping.wav')

IS_THERE_SOUND = True

class Panel:

    def __init__(self,
                 pos: Tuple[int, int],
                 font_size: int,
                 font_color: Tuple[int, int, int],
                 font=None) -> None:
        self.pos = pos
        self.font_size = font_size
        self.font_color = font_color
        if font is None:
            self.font = pygame.font.SysFont(None, font_size)

    def draw(self, surf: pygame.Surface, sentence: str) -> None:
        surf.blit(self.font.render(sentence, True, self.font_color), self.pos)


class Board:

    def __init__(self, size: int, pos: Tuple[int, int]) -> None:
        self.size = size
        self.pos = pos
        self.matrix = [[''] * 3 for _ in range(3)]
        self.surf = pygame.Surface((size, size))
        self.line_width = self.size // 40
        self.circle_radius = int(self.size / 3 - self.line_width * 2) // 2
        self.is_status_changed = False
        self.last_tick = pygame.time.get_ticks()

        if random.randint(0, 1) == 0:
            self.player_shape = 'o'
            self.ai_shape = 'x'
        else:
            self.player_shape = 'x'
            self.ai_shape = 'o'

        if random.randint(0, 1) == 0:
            self.turn = 'o'
        else:
            self.turn = 'x'

    def draw(self, dest_surf: pygame.Surface) -> None:
        self.surf.fill((255, 255, 255))

        # horizontal lines
        for i in range(0, 4):
            pygame.draw.line(self.surf, (0, 0, 0),
                             (0, int(i * (self.size / 3))),
                             (self.size, int(i * (self.size / 3))),
                             self.line_width)

        # vertical lines
        for i in range(0, 4):
            pygame.draw.line(self.surf, (0, 0, 0),
                             (int(i * (self.size / 3)), 0),
                             (int(i * (self.size / 3)), self.size),
                             self.line_width)

        # draw board
        for i in range(3):
            for j in range(3):
                if self.matrix[i][j] == 'o':
                    pygame.draw.circle(
                        self.surf, (255, 0, 0),
                        (i * (self.size // 3) + self.circle_radius +
                         self.line_width, j * (self.size // 3) +
                         self.circle_radius + self.line_width),
                        self.circle_radius, self.line_width)
                elif self.matrix[i][j] == 'x':
                    pygame.draw.line(
                        self.surf, (0, 0, 255),
                        (i * (self.size // 3) + self.line_width, j *
                         (self.size // 3) + self.line_width),
                        ((i + 1) * (self.size // 3) - self.line_width,
                         (j + 1) * (self.size // 3) - self.line_width),
                        self.line_width)
                    pygame.draw.line(
                        self.surf, (0, 0, 255),
                        (((i + 1) * (self.size // 3) - self.line_width, j *
                          (self.size // 3) + self.line_width)),
                        (i * (self.size // 3) + self.line_width,
                         (j + 1) * (self.size // 3) - self.line_width),
                        self.line_width)

        dest_surf.blit(self.surf, self.pos)

    def get_input(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    x, y = pygame.mouse.get_pos()
                    m_x, m_y = int(x / (self.size / 3)), int(y /
                                                             (self.size / 3))

                    if self.matrix[m_x][m_y] == '':
                        self.matrix[m_x][m_y] = self.turn
                        self.is_status_changed = True

                        if IS_THERE_SOUND:
                            STONE_SOUND.play()
                    break

    def get_winner(self):
        # vertical
        for i in range(3):
            if self.matrix[i][0] != '':
                prev_shape = self.matrix[i][0]

                for j in range(1, 3):
                    if prev_shape != self.matrix[i][j]:
                        break
                else:
                    return prev_shape

        # horizontal
        for i in range(3):
            if self.matrix[0][i] != '':
                prev_shape = self.matrix[0][i]

                for j in range(1, 3):
                    if prev_shape != self.matrix[j][i]:
                        break
                else:
                    return prev_shape

        # left-top to right-bottom
        if self.matrix[0][0] != '':
            prev_shape = self.matrix[0][0]

            if prev_shape == self.matrix[1][1] == self.matrix[2][2]:
                return prev_shape

        # right-top to left-bottom
        if self.matrix[2][0] != '':
            prev_shape = self.matrix[2][0]

            if prev_shape == self.matrix[1][1] == self.matrix[0][2]:
                return prev_shape

        is_there_blank_space = False

        for i in range(3):
            for j in range(3):
                if self.matrix[i][j] == '':
                    is_there_blank_space = True

        if not is_there_blank_space:
            return 'd'

        return None

    def minimax(self, depth: int, alpha: int, beta: int, is_maximizing: bool) -> int:
        winner = self.get_winner()

        if winner == self.turn:
            return 1
        elif winner == self.get_reversed_turn():
            return -1
        elif winner == 'd':
            return 0

        if depth == 0:
            return 0

        if is_maximizing:
            max_evel = -99999

            for i in range(3):
                for j in range(3):
                    if self.matrix[i][j] == '':
                        self.matrix[i][
                            j] = self.turn

                        evel = self.minimax(depth - 1, alpha, beta, not is_maximizing)

                        self.matrix[i][j] = ''

                        max_evel = max(max_evel, evel)

                        alpha = max(alpha, evel)

                        if beta <= alpha:
                            break

            return max_evel
        else:
            min_evel = 99999

            for i in range(3):
                for j in range(3):
                    if self.matrix[i][j] == '':
                        self.matrix[i][j] = self.get_reversed_turn()

                        evel = self.minimax(depth - 1, alpha, beta, not is_maximizing)

                        self.matrix[i][j] = ''

                        min_evel = min(min_evel, evel)

                        beta = min(beta, evel)

                        if beta <= alpha:
                            break

            return min_evel

    def ai(self):
        optimal_x, optimal_y = 0, 0
        max_val = -99999

        for i in range(3):
            for j in range(3):
                if self.matrix[i][j] == '':
                    self.matrix[i][j] = self.turn

                    r = self.minimax(-1, -99999, 99999, False)

                    if max_val < r:
                        max_val = r
                        optimal_x, optimal_y = i, j

                    self.matrix[i][j] = ''

        self.matrix[optimal_x][optimal_y] = self.turn

        self.is_status_changed = True

        if IS_THERE_SOUND:
            STONE_SOUND.play()

    def get_reversed_turn(self):
        if self.turn == 'o':
            return 'x'
        else:
            return 'o'

    def change_turn(self):
        self.turn = self.get_reversed_turn()

    def update(self, events):
        if self.turn == self.ai_shape:
            # delay 500ms
            if pygame.time.get_ticks() - self.last_tick >= 500:
                self.ai()
        else:
            self.get_input(events)

        if self.is_status_changed:
            self.change_turn()
            self.last_tick = pygame.time.get_ticks()

        self.is_status_changed = False


def main() -> None:
    board = Board(SCREEN_WIDTH, (0, 0))
    winner_panel = Panel((int(SCREEN_WIDTH / 2 - SCREEN_WIDTH / 2.5),
                          int(SCREEN_HEIGHT / 2 - SCREEN_WIDTH / 14)),
                         int(SCREEN_WIDTH / 5), (30, 155, 100), None)
    last_tick = pygame.time.get_ticks()

    board.draw(SCREEN_SURF)
    pygame.display.update()

    while True:
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                print('bye~')
                pygame.quit()
                sys.exit()

        SCREEN_SURF.fill((0, 0, 0))

        if (winner := board.get_winner()) is not None:
            board.draw(SCREEN_SURF)

            if winner == 'd':
                winner_panel.draw(SCREEN_SURF, '     DRAW')
            else:
                winner_panel.draw(SCREEN_SURF, f'WINNER : {winner}')

            # delay 3s
            if pygame.time.get_ticks() - last_tick >= 3000:
                board = Board(SCREEN_WIDTH, (0, 0))
        else:
            board.update(events)
            board.draw(SCREEN_SURF)

            last_tick = pygame.time.get_ticks()

        pygame.display.update()
        clock.tick()


if __name__ == '__main__':
    main()
