import pygame
from pygame.locals import *

import sys
from random import randrange

from utils import *
from snake import *

FPS = 60                            # Game fps
SNAKE_START_LENGTH = 6

DIRECTION_UP    = Vector2(0, -1)
DIRECTION_DOWN  = Vector2(0, 1)
DIRECTION_LEFT  = Vector2(-1, 0)
DIRECTION_RIGHT = Vector2(1, 0)

WORLD_SIZE = Vector2(36, 24)
BLOCK_SIZE = 10

# Colors
BACKGROUD_COLOR = 0, 0, 0
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
        pygame.display.set_caption('PyGame Snaaaakes!')
        self.block_size = BLOCK_SIZE
        self.window = pygame.display.set_mode(tuple(WORLD_SIZE * self.block_size))
        self.screen = pygame.display.get_surface()
        self.clock = pygame.time.Clock()
        self.world = Rect((0,0), tuple(WORLD_SIZE))
        self.reset()

    def reset(self):
        """Start a new Game."""
        self.playing = True
        self.next_direction = DIRECTION_UP
        self.score = 0
        self.snake = Snake(self.world.center, SNAKE_START_LENGTH)
        self.food = set()
        self.add_food()

    def add_food(self):
        """ adds a food piece to the world map """
        food = Vector2(*map(randrange, self.world.bottomright))
        while food in self.food or food in self.snake:
            food = Vector2(*map(randrange, self.world.bottomright))

        self.food.add(food)

    def input(self, e):
        """Process keyboard event e."""
        if e.key in KEY_DIRECTION:
            self.next_direction = KEY_DIRECTION[e.key]
        elif e.key == K_SPACE and not self.playing:
            self.reset()

    def update(self, dt):
        """Update the game by dt seconds."""
        self.snake.update(dt, self.next_direction)

        # If hitting a food block
        head = self.snake.head
        if head in self.food:
            self.food.remove(head)
            self.add_food()
            self.snake.grow()

        # If hitting boundaries or self
        if self.snake.self_intersecting() or not self.world.collidepoint(*self.snake.head):
            self.playing = False

    def block(self, p):
        """Return the screen rectangle corresponding to position p."""
        width = DIRECTION_RIGHT * self.block_size
        height = DIRECTION_DOWN * self.block_size
        rect = [tuple(t) for t in (p * self.block_size, width + height)]
        return Rect(rect)

    def draw(self):
        """Draw game (while playing)"""
        self.screen.fill(BACKGROUD_COLOR)
        for p in self.snake:
            pygame.draw.rect(self.screen, SNAKE_COLOR, self.block(p))
        for f in self.food:
            pygame.draw.rect(self.screen, FOOD_COLOR, self.block(f))

    def draw_death(self):
        """Draw game over."""
        self.screen.fill(BACKGROUD_COLOR)
        for p in self.snake:
            pygame.draw.rect(self.screen, DEATH_COLOR, self.block(p))

    def play(self):
        """Play game until QUIT, main game loop"""
        while True:
            dt = self.clock.tick(60)
            for e in pygame.event.get():
                if e.type == QUIT:
                    return
                elif e.type == KEYUP:
                    self.input (e)
            if self.playing:
                self.update(dt)
                self.draw()
            else:
                self.draw_death()
            pygame.display.flip()

def main():
    pygame.init()
    SnakeGame().play()
    pygame.quit()

if __name__ == '__main__':
    main()