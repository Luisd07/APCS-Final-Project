import pygame
import sys
import random

from pygame.locals import *

FPS = 10
pygame.init()
fpsClock = pygame.time.Clock()

width, height = 500, 500
screen = pygame.display.set_mode((width, height), 0, 32)
surface = pygame.Surface(screen.get_size())
surface = surface.convert()
surface.fill((255, 255, 255))
clock = pygame.time.Clock()
pygame.display.set_caption("Snake Game")


gridSize = 25
gWidth = width / gridSize
gHeight = height / gridSize
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

screen.blit(surface, (0, 0))


def draw_box(surf, color, pos):
    r = pygame.Rect((pos[0], pos[1]), (gridSize, gridSize))
    pygame.draw.rect(surf, color, r)


class Snake(object):
    def __init__(self):
        self.lose()
        self.color = (255, 0, 0)

    def get_head_position(self):
        return self.positions[0]

    def lose(self):
        self.length = 1
        self.positions = [((width / 2), (height / 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])

    def point(self, pt):
        if self.length > 1 and (pt[0] * -1, pt[1] * -1) == self.direction:
            return
        else:
            self.direction = pt

    def move(self):
        cur = self.positions[0]
        x, y = self.direction
        new = (((cur[0] + (x * gridSize)) % width), (cur[1] + (y * gridSize)) % height)
        if len(self.positions) > 2 and new in self.positions[1:]:
            self.lose()
        else:
            self.positions.insert(0, new)
            if len(self.positions) > self.length:
                self.positions.pop()

    def draw(self, surf):
        for p in self.positions:
            draw_box(surf, self.color, p)


class Apple(object):
    def __init__(self):
        self.position = (0, 0)
        self.color = (0, 255, 0)
        self.randomize()

    def randomize(self):
        self.position = (random.randint(0, gWidth - 1) * gridSize, random.randint(0, gHeight - 1) * gridSize)

    def draw(self, surf):
        draw_box(surf, self.color, self.position)


def check_eat(snake, apple):
    if snake.get_head_position() == apple.position:
        snake.length += 1
        apple.randomize()


if __name__ == '__main__':
    snake = Snake()
    apple = Apple()
    while True:

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_w:
                    snake.point(UP)
                elif event.key == K_s:
                    snake.point(DOWN)
                elif event.key == K_a:
                    snake.point(LEFT)
                elif event.key == K_d:
                    snake.point(RIGHT)

        surface.fill((255, 255, 255))
        snake.move()
        check_eat(snake, apple)
        snake.draw(surface)
        apple.draw(surface)
        font = pygame.font.Font(None, 36)
        text = font.render(str(snake.length), 5, (10, 10, 10))
        textpos = text.get_rect()
        textpos.centerx = 20
        surface.blit(text, textpos)
        screen.blit(surface, (0, 0))

        pygame.display.flip()
        pygame.display.update()
        fpsClock.tick(FPS + snake.length / 3)
