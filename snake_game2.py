import pygame
from pygame.locals import *
from random import randrange

from utils import *
from snake import *

FPS = 60                            # Game fps

SNAKE_START_LENGTH = 6
FOOD_SCORE = 50

DIRECTION_UP = Vector2(0, -1)
DIRECTION_DOWN = Vector2(0, 1)
DIRECTION_LEFT = Vector2(-1, 0)
DIRECTION_RIGHT = Vector2(1, 0)
DIRECTION_RD = DIRECTION_RIGHT + DIRECTION_DOWN

WORLD_SIZE = Vector2(36, 24)
BLOCK_SIZE = 15

# Colors
BG_COLOR = 0, 0, 0
SNAKE_COLOR = 0, 255, 0
FOOD_COLOR = 255, 255, 255
DEATH_COLOR = 255, 0, 0
TEXT_COLOR = 255, 255, 255

# Map from python key even to direction
KEY_DIRECTION = {
    K_w: DIRECTION_UP,   K_UP: DIRECTION_UP,
    K_s: DIRECTION_DOWN, K_DOWN: DIRECTION_DOWN,
    K_a: DIRECTION_LEFT, K_LEFT: DIRECTION_LEFT,
    K_d: DIRECTION_RIGHT, K_RIGHT: DIRECTION_RIGHT,
}


class SnakeGame(object):

    def __init__(self):
        self.screen = pygame.display.set_mode(tuple(WORLD_SIZE * BLOCK_SIZE))
        self.world = Rect((0, 0), tuple(WORLD_SIZE))
        self.timer = pygame.time.Clock()
        self.font = pygame.font.Font(pygame.font.get_default_font(), 22)
        print(self.font)

        self.reset()

    def reset(self):
        self.next_direction = DIRECTION_UP

        self.snake = Snake(self.world.center, SNAKE_START_LENGTH)
        self.score = 0

        self.food = set()
        self.add_food()

        self.playing = True

    def block(self, vect, padding = 0):
        ''' Return a rect that correspondes to vect on screen.
            Optionally add padding from both sides (Will add double the amount specified in total).'''
        padding = Vector2(padding, padding)
        rect = tuple(vect * BLOCK_SIZE + padding ), tuple(BLOCK_SIZE * DIRECTION_RD - padding * 2)
        return Rect(rect)

    def add_food(self):
        while not self.food:
            food = Vector2(*map(randrange, self.world.bottomright))
            if food not in self.snake:
                self.food.add(food)

    def input(self, e):
        if e.key in KEY_DIRECTION:
            self.next_direction = KEY_DIRECTION[e.key]
        elif e.key == K_SPACE and not self.playing:
            self.reset()

    def draw(self):
        ''' Draw game if player is alive '''
        self.screen.fill(BG_COLOR)
        for seg in self.snake:
            pygame.draw.rect(self.screen, SNAKE_COLOR, self.block(seg))
        for f in self.food:
            pygame.draw.rect(self.screen, FOOD_COLOR, self.block(f, 4))

        self.draw_text(str(self.score), self.block(Vector2(1, 1)))

    def draw_text(self, text, p):
        ''' Draw text at position p.'''
        self.screen.blit(self.font.render(text, 1, TEXT_COLOR), p)

    def death_draw(self):
        ''' Draw game if player is dead. '''
        self.screen.fill(BG_COLOR)
        for seg in self.snake:
            pygame.draw.rect(self.screen, DEATH_COLOR, self.block(seg))

    def update(self, dt):
        ''' Updates all game objects and game state.'''
        self.snake.update(dt, self.next_direction)

        head = self.snake.head
        if head in self.food:
            self.food.remove(head)
            self.add_food()
            self.snake.grow()
            self.score += FOOD_SCORE

        if self.snake.self_intersecting() or not self.world.collidepoint(*head):
            self.playing = False

    def play(self):
        while True:
            dt = self.timer.tick(FPS)

            for e in pygame.event.get():
                if e.type == QUIT:
                    return
                elif e.type == KEYUP:
                    self.input(e)

            if self.playing:
                self.update(dt)
                self.draw()
            else:
                self.death_draw()

            pygame.display.flip()






def main():
    pygame.init()
    s = SnakeGame()
    s.play()
    pygame.quit()

if __name__ == '__main__':
    main()
