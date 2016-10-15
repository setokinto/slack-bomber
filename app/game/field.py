
from enum import Enum

class Object(Enum):
    wall = 0
    empty = 1
    block = 2
    bomb = 3

class Item(Enum):
    speed = 0
    add_bomb = 1
    fire = 2

class Point:

    def __init__(self, x, y):
        self.x = x
        self.y = y

class Person:

    def __init__(self, user, point=Point(0, 0)):
        self.user = user
        self.position = point


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

