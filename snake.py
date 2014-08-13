SNAKE_SPEED_INITIAL = 5
SNAKE_SPEED_INCREMENT = 0.25

from utils import *

class Snake(object):
    '''
        The Snake game object. Controls the snake's directions and
        handles movement and growth of the snake.
        Positions are represented using utils.Vector2

        Snake(start, length, direction) =>  sets initial location and length for the snake
                                            default movement direction is up
        update(dt, [new_direction]) =>  Update the snake given time difference (dt) from last update.
                                        change direction if required
        change_direction(direction) =>  Changes the snake's direction if legal

    '''

    def __init__(self, start, length, direction = Vector2(0, -1)):
        self.speed = SNAKE_SPEED_INITIAL
        self.growth_pending = 0
        self.timer = 1000 / self.speed # How many miliseconds should pass between each frame
        self.direction = direction
        self.head = start
        
        # Initialize snake
        self.segments = Queue()
        for i in range(length -1 , -1, -1): # enqueue the starting segments from tail to head
            self.segments.enqueue(start - i*direction)

    def __iter__(self):
        return iter(self.segments)

    def __str__(self):
        res = 'Snake object: '
        for seg in self:
            res += '({}, {})'.format(*[idx for idx in seg])
        return res

    def change_direction(self, direction):
        if direction != -self.direction:
            self.direction = direction

    def update(self, dt, new_direction = None):
        self.timer -= dt

        if self.timer > 0:
            return

        self.timer = 1000 / self.speed

        if new_direction:
            change_direction(new_direction)

        self.head = self.head + self.direction
        self.segments.enqueue(self.head)
        if self.growth_pending > 0:
            self.growth_pending -= 1
        else:
            self.segments.dequeue()




if __name__ == '__main__':
    s = Snake(Vector2(0,0), 5)
    print(s)
    for _ in range(5):
        s.update(300)
        print(s)
    s.change_direction(Vector2(1, 0))
    s.change_direction(Vector2(-1, 0))
    for _ in range(5):
        s.update(300)
        print(s)