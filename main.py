from typing import *
import sys
import pygame
import random
import time

FPS = 60
clock = pygame.time.Clock()
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 700


class Panel:
    def __init__(self, pos: Tuple[int, int], font_size: int, font_color: Tuple[int, int, int], font=None) -> None:
        self.pos = pos
        self.font_size = font_size
        self.font_color = font_color
        if font == None:
            self.font = pygame.font.SysFont(None, font_size)

    def draw(self, surf:                    pygame.Surface, str: str) -> None:
        surf.blit(self.font.render(str, True, self.font_color), self.pos)


class Borad:
    def __init__(self, size: int, pos: Tuple[int, int]) -> None:
        self.size = size
        self.pos = pos
        self.matrix = [[''] * self.size for i in range(self.size)]
        self.surf = pygame.Surface((size, size))
        self.line_width = self.size // 40
        self.circle_radius = int(self.size / 3 - self.line_width * 2) // 2
        self.is_status_changed = False

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

        # horizental lines
        for i in range(0, 4):
            pygame.draw.line(self.surf, (0, 0, 0), (0, int(
                i * (self.size / 3))), (self.size, int(i * (self.size / 3))), self.line_width)

        # vertical lines
        for i in range(0, 4):
            pygame.draw.line(self.surf, (0, 0, 0), (int(
                i * (self.size / 3)), 0),  (int(i * (self.size / 3)), self.size), self.line_width)

        # draw borad
        for i in range(3):
            for j in range(3):
                if self.matrix[i][j] == 'o':
                    pygame.draw.circle(self.surf, (255, 0, 0),
                                       (i * (self.size // 3) + self.circle_radius + self.line_width,
                                        j * (self.size // 3) + self.circle_radius + self.line_width),
                                       self.circle_radius, self.line_width)
                elif self.matrix[i][j] == 'x':
                    pygame.draw.line(self.surf, (0, 0, 255), ((i * (self.size // 3) + self.line_width, j * (self.size // 3) + self.line_width)), ((
                        i + 1) * (self.size // 3) - self.line_width, (j + 1) * (self.size // 3) - self.line_width), self.line_width)
                    pygame.draw.line(self.surf, (0, 0, 255), (((i+1) * (self.size // 3) - self.line_width, j * (self.size // 3) + self.line_width)), (
                        i * (self.size // 3) + self.line_width, (j + 1) * (self.size // 3) - self.line_width), self.line_width)

        dest_surf.blit(self.surf, (self.pos))

    def get_input(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    pos = pygame.mouse.get_pos()

                    self.matrix[int(pos[0] / (self.size / 3))][int(pos[1] /
                                                                   (self.size / 3))] = self.player_shape

                    self.is_status_changed = True
                    break

    def ai(self):
        self.matrix[random.randint(0, 2)][random.randint(0, 2)] = self.ai_shape

        self.is_status_changed = True

    def get_reversed_turn(self):
        if self.turn == 'o':
            return 'x'
        else:
            return 'o'

    def change_turn(self):
        self.turn = self.get_reversed_turn()

    def update(self, events):
        if self.turn == self.ai_shape:
            time.sleep(0.5)
            self.ai()
        else:
            self.get_input(events)

        if self.is_status_changed:
            self.change_turn()

        self.is_status_changed = False


def main() -> None:
    pygame.init()
    screen_surf = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    borad = Borad(SCREEN_WIDTH, (0, 0))

    borad.draw(screen_surf)
    pygame.display.update()

    while True:
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen_surf.fill((0, 0, 0))

        borad.update(events)
        borad.draw(screen_surf)

        pygame.display.update()
        clock.tick()


main()
