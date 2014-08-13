from collections import deque

class Queue(object):
    '''
        A basic implementation of a queue using a Deque
        O(1) addition and removal

        enqueue(self, item) => Add an item to back of the queue
        dequeue(self, item) => Remove an item from the front of the queue, raise IndexError if empty
        is_empty(self) => return True if empty
    '''

    def __init__(self):
        self.items = deque()

    def __str__(self):
        return str(self.items)

    def __iter__(self):
        return iter(self.items)

    def enqueue(self, item):
        self.items.append(item)

    def dequeue(self):
        return self.items.popleft()

    def is_empty(self):
        return len(self.items) == 0

    def __len__(self):
        return len(self.items)

class Vector2(object):
    '''
        A basic implementation of a Vector2. Holding x,y coordinates.
        supports addition and subtraction of vectors, and multiplication and division by a scalar
    '''
    def __init__(self, x, y):
        self.pos = (x, y)

    def __repr__(self):
        return 'Vector2({}, {})'.format(*[a for a in self.pos])

    def __iter__(self):
        return iter(self.pos)

    def __eq__(self, other):
        for v, w in zip(self, other):
            if v != w:
                return False
        return True

    def __hash__(self):
        return sum(self.pos)

    # Basic operations

    def __add__(self, other):
        return Vector2(*tuple(v + w for v, w in zip(self, other)))

    def __radd__(self, other):
        return Vector2(*tuple(w + v for v, w in zip(self, other)))

    def __sub__(self, other):
        return Vector2(*tuple(v - w for v, w in zip(self, other)))

    def __rsub__(self, other):
        return Vector2(*tuple(w - v for v, w in zip(self, other)))

    def __mul__(self, s):
        return Vector2(*tuple(v*s for v in self))

    def __rmul__(self, s):
        return Vector2(*tuple(v*s for v in self))

    def __neg__(self):
        return -1 * self


if __name__ == '__main__':
    a = Vector2(2, 3)
    v = Vector2(3, 5)
    print(a+v)