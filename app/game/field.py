
from enum import Enum

class Object(Enum):
    wall = 0
    empty = 1
    block = 2

class Item(Enum):
    speed = 0
    add_bomb = 1
    fire = 2

class Point:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def diff(self, x, y):
        return Point(self.x + x, self.y + y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return "Point({}, {})".format(self.x, self.y)

class Bomb:

    def __init__(self, owner, fire):
        self.owner = owner
        self.fire = fire

class Person:

    def __init__(self, user, point=Point(0, 0)):
        self.user = user
        self.position = point
        self.bomb_count = 1
        self.speed_count = 1
        self.fire_count = 1
        self._used_bomb = 0

    def get_bomb(self):
        if self._used_bomb >= self.bomb_count:
            return None
        self._used_bomb += 1
        return Bomb(self, self.fire_count)

class Field:
    """
        Access each field like _fields[x][y]
        left-top is _fields[0][0]
    """
    def __init__(self, x_size, y_size, users):
        self.x_size = x_size
        self.y_size = y_size
        self.bombs = [ [None]*y_size for x in range(x_size)]
        map_ = FieldCreater.generate_map(x_size, y_size, len(users))
        self.objects = map_["objects"]
        self.items = map_["items"]
        self.persons = [ Person(user, initial_pos)
              for user, initial_pos in zip(users, map_["person_initial_positions"])
            ]

    def person_by_user(self, user):
        for person in self.persons:
            if person.user == user:
                return person
        return None

    def put_bomb(self, person):
        if field_object(self.bombs, person.point) is None:
            bomb = person.get_bomb()
            if bomb is not None:
                put_object_to_field(self.bombs, person.point, bomb)

    def move_top(self, person):
        self.move(person, 0, -1)

    def move_left(self, person):
        self.move(person, -1, 0)

    def move_right(self, person):
        self.move(person, 1, 0)

    def move_bottom(self, person):
        self.move(person, 0, 1)

    def move(self, person, x, y):
        dest = person.point.diff(x, y)
        if self.check_obstacle(dest):
            person.point = dest

    def check_obstacle(self, point):
        if point.x < 0 or self.x_size <= point.x or \
           point.y < 0 or self.y_size <= point.y:
            return False
        object = field_object(self.objects, point)
        if object == Object.wall or object == Object.block:
            return False
        bomb = field_object(self.bombs, point)
        if bomb is not None:
            return False
        return True

def put_object_to_field(source, point, obj):
    source[point.x][point.y] = obj

def field_object(source, point):
    return source[point.x][point.y]

class FieldCreater:

    @staticmethod
    def generate_map(x_size, y_size, person_num):
        # TODO: create a real map
        return {
            "objects":  [ [Object.empty]*y_size for x in range(x_size)],
            "items": [ [None]*y_size for x in range(x_size)],
            "person_initial_positions": [
                Point(0, 0),
                Point(x_size-1, y_size-1),
            ],
        }

