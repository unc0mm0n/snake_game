SNAKE_SPEED_INITIAL = 5
SNAKE_SPEED_INCREMENT = 0.25

from utils import *

class Snake(object):
    '''
        The Snake game object. Controls the snake's directions and
        handles movement and growth of the snake.
        Positions are represented using utils.Vector2

        __init__(self, start, length, direction) => sets initial location and length for the snake
                                                    default movement direction is up

    '''

    def __init__(self, start, length, direction = Vector2(0, -1)):
        self.speed = SNAKE_SPEED_INITIAL
        self.growth_pending = 0
        self.direction = direction
        
        # Initialize snake
        self.segments = Queue()
        for i in range(length):
            self.segments.enqueue(start - i*direction)

    def __iter__(self):
        return iter(self.segments)

    def __str__(self):
        res = 'Snake object:'
        for seg in self:
            res += '( {}, {} )'.format(*[idx for idx in seg])
        return res

if __name__ == '__main__':
    s = Snake(Vector2(0,0), 5)
    print(s)