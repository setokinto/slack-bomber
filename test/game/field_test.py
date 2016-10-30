
import unittest

from app.game.field import Field, Point, Bomb, Fire, FiredPerson, Object, Item

class FieldTest(unittest.TestCase):

    def setUp(self):
        pass

    def test_person_should_move_in_Field(self):
        field = Field(11, 11, ["user1", "user2"])
        person1 = field.person_by_user("user1")
        self.assertIsNotNone(person1)
        person1.point = Point(1, 1)
        person2 = field.person_by_user("user2")
        self.assertIsNotNone(person2)
        person2.point = Point(6, 8)

        field.move_top(person1)
        self.assertEqual(person1.point, Point(1, 1))
        field.move_bottom(person1)
        self.assertEqual(person1.point, Point(1, 2))
        field.put_bomb(person1)
        bomb_point = person1.point
        self.assertIsNotNone(field.bombs[1][2])
        field.move_top(person1)
        self.assertEqual(person1.point, Point(1, 1))
        field.put_bomb(person1)
        self.assertIsNone(field.bombs[1][1], "It should not put a bomb because a bomb is not remained")

        field.move_right(person1)
        self.assertEqual(person1.point, Point(2, 1))
        field.move_left(person1)
        self.assertEqual(person1.point, Point(1, 1))

        field.fire_bomb(bomb_point)
        field.put_bomb(person1)
        self.assertIsNotNone(field.bombs[1][1], "It should put a bomb")

    def test_dead_person_should_not_move_in_Field(self):
        field = Field(8, 10, ["user1", "user2"])
        field.objects = [
            [None, None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None],
        ]
        person1 = field.person_by_user("user1")
        self.assertIsNotNone(person1)
        person1.point = Point(1, 1)
        field.move_bottom(person1)
        self.assertEqual(person1.point, Point(1, 2))

        person1.life_num = 2

        bom2 = Bomb("user1", 1)
        field.bombs[1][1] = bom2
        field.fire_bomb(Point(1, 1))
        field.move_bottom(person1)
        self.assertEqual(person1.point, Point(1, 3))

        field.bombs[1][2] = bom2
        field.fire_bomb(Point(1, 2))
        field.move_bottom(person1)
        self.assertEqual(person1.point, Point(1, 3))

    def test_put_two_bomb_at_one_pos(self):
        field = Field(8, 11, ["user1", "user2"])
        person1 = field.person_by_user("user1")
        person1.point = Point(1, 1)
        field.objects[1][1] = Object.empty
        person1.bomb_count = 2
        field.put_bomb(person1)
        self.assertEqual(person1._used_bomb, 1)
        field.put_bomb(person1)
        self.assertEqual(person1._used_bomb, 1)

    def test_Field_should_create(self):
        field = Field(8, 10, ["user1", "user2"])
        field.objects[0][0]
        field.objects[7][9]
        with self.assertRaises(IndexError) as error:
            field.objects[8][9]
        with self.assertRaises(IndexError) as error:
            field.objects[7][10]

    def test_bomb_should_fire(self):
        field = Field(8, 10, ["user1", "user2"])
        bom1 = Bomb("user1", 3)
        fire = Fire()
        field.bombs = [
            [None, None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None],
            [None, None, bom1, None, None, None, None, None, None, None],
        ]
        wall = Object.wall
        block = Object.block
        field.objects = [
            [None, None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None],
            [None, wall, None, None, block, None, None, None, None, None],
        ]
        field.fire_bomb(Point(7, 2)) # bom1

        self.assertAllField(field.bombs, [
            [None, None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None],
            [None, None, fire, None, None, None, None, None, None, None],
            [None, None, fire, None, None, None, None, None, None, None],
            [None, None, fire, None, None, None, None, None, None, None],
            [None, None, fire, fire, fire, None, None, None, None, None],
        ])

    def test_Field_should_proceed_time(self):
        field = Field(8, 10, ["user1", "user2"])
        field.persons[0].point = Point(7, 9)
        bom1 = Bomb("user1", 1)
        field.objects = [
            [None, None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None],
        ]
        field.bombs[0][0] = bom1
        field.proceed_time(3)
        self.assertEqual(field.bombs[0][0], bom1)
        field.proceed_time(1)
        self.assertEqual(field.bombs[0][0], bom1)
        field.proceed_time(1)
        self.assertEqual(field.bombs[0][0], Fire())
        field.proceed_time(2)
        self.assertEqual(field.bombs[0][0], None)

        bom2 = Bomb("user1", 2)
        field.bombs[5][5] = bom2
        field.proceed_time(0.3)
        self.assertEqual(field.bombs[5][5], bom2)
        field.proceed_time(0.7)
        self.assertEqual(field.bombs[5][5], bom2)
        field.proceed_time(4.3)
        self.assertEqual(field.bombs[5][5], Fire())
        field.proceed_time(1.5)
        self.assertEqual(field.bombs[5][5], Fire())
        field.proceed_time(0.6)
        self.assertEqual(field.bombs[5][5], None)

    def test_Field_items_should_get_by_person(self):
        field = Field(8, 10, ["user1", "user2"])

        fire = Item.fire
        bomb = Item.add_bomb
        sped = Item.speed
        person = field.persons[0]

        person.point = Point(1, 1)
        field.items = [
            [None, None, None, None, None, None, None, None, None, None],
            [None, None, fire, bomb, sped, fire, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None],
        ]
        field.objects[1][1] = Object.empty
        field.objects[1][2] = Object.empty
        field.objects[1][3] = Object.empty
        field.objects[1][4] = Object.empty
        field.objects[1][5] = Object.empty

        self.assertEqual(person.fire_count, 1)
        self.assertEqual(person.bomb_count, 1)
        self.assertEqual(person.speed_count, 1)

        field.move_bottom(person)
        self.assertEqual(person.fire_count, 2)
        self.assertEqual(person.bomb_count, 1)
        self.assertEqual(person.speed_count, 1)

        field.move_bottom(person)
        self.assertEqual(person.fire_count, 2)
        self.assertEqual(person.bomb_count, 2)
        self.assertEqual(person.speed_count, 1)

        field.move_bottom(person)
        self.assertEqual(person.fire_count, 2)
        self.assertEqual(person.bomb_count, 2)
        self.assertEqual(person.speed_count, 2)

        field.move_bottom(person)
        self.assertEqual(person.fire_count, 3)
        self.assertEqual(person.bomb_count, 2)
        self.assertEqual(person.speed_count, 2)

        field.move_top(person)
        field.move_top(person)
        field.move_top(person)
        field.move_top(person)
        self.assertEqual(person.fire_count, 3)
        self.assertEqual(person.bomb_count, 2)
        self.assertEqual(person.speed_count, 2)

    def test_Person_should_put_bomb_after_fired(self):
        field = Field(8, 10, ["user1", "user2"])
        bom1 = Bomb("user1", 1)
        bom2 = Bomb("user1", 2)
        person = field.persons[0]
        person.bomb_count = 2

        person.get_bomb()
        person.get_bomb()
        self.assertEqual(person._used_bomb, 2)
        field.objects = [
            [None, None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None],
        ]
        field.bombs = [
            [None, None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None],
            [None, None, bom1, bom2, None, None, None, None, None, None],
        ]
        field.fire_bomb(Point(7, 2)) # bom1
        self.assertEqual(person._used_bomb, 0)

    def test_Field_should_fire_with_other_bomb(self):
        field = Field(8, 10, ["user1", "user2"])
        bom1 = Bomb("user1", 1)
        bom2 = Bomb("user1", 2)
        bom3 = Bomb("user1", 3)
        bom4 = Bomb("user1", 4)
        bom5 = Bomb("user1", 5)
        fire = Fire()
        fired_person = FiredPerson(field.persons[0])
        field.objects = [
            [None, None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None],
        ]
        field.bombs = [
            [None, None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None],
            [None, bom3, None, None, bom5, None, None, bom2, None, None],
            [None, None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, bom1, None, None],
            [None, None, None, None, None, None, None, None, None, None],
            [None, None, bom4, None, None, None, None, None, None, None],
        ]
        field.fire_bomb(Point(7, 2)) # bom4
        self.assertAllField(field.bombs, field.bombs, "assertAllField works")

        self.assertAllField(field.bombs, [
            [None, None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None],
            [None, bom3, fire, None, bom5, None, None, bom2, None, None],
            [None, None, fire, None, None, None, None, None, None, None],
            [None, None, fire, None, None, None, None, bom1, None, None],
            [None, None, fire, None, None, None, None, None, None, None],
            [fire, fire, fire, fire, fire, fire, fire, None, None, None],
        ])

        field.persons[0].point = Point(3, 9)
        field.persons[0].life_num = 1
        field.objects[1][7] = Object.block

        field.fire_bomb(Point(3, 1)) # bom3

        self.assertAllField(field.bombs, [
            [None, fire, None, None, fire, None, None, None, None, None],
            [None, fire, None, None, fire, None, None, fire, None, None],
            [None, fire, None, None, fire, None, None, fire, None, None],
            [fire, fire, fire, fire, fire, fire, fire, fire, fire, fired_person],
            [None, fire, fire, None, fire, None, None, fire, None, None],
            [None, fire, fire, None, fire, None, fire, fire, fire, None],
            [None, fire, fire, None, fire, None, None, fire, None, None],
            [fire, fire, fire, fire, fire, fire, fire, None, None, None],
        ])

        self.assertEqual(field.objects[1][7], Object.empty)

    def test_field_should_get_field_object(self):
        field = Field(8, 10, ["user1", "user2"])

        wall = Object.wall
        block = Object.block
        emp = Object.empty
        bomb = Bomb("user1", 1)
        item = Item.speed

        field.objects = [
            [wall, block, emp, emp, emp, emp, emp, emp, emp, emp],
            [None, emp, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None],
        ]

        field.bombs = [
            [bomb, bomb, bomb, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None],
        ]

        field.items = [
            [item, item, item, item, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None],
        ]

        point = Point(0,0)
        self.assertEqual(Field.get_field_object(field, point), wall)
        point = Point(0,1)
        self.assertEqual(Field.get_field_object(field, point), block)
        point = Point(0,2)
        self.assertEqual(Field.get_field_object(field, point), bomb)
        point = Point(0,3)
        self.assertEqual(Field.get_field_object(field, point), item)
        point = Point(1,1)
        self.assertEqual(Field.get_field_object(field, point), field.person_by_user("user1"))
        point = Point(0,4)
        self.assertEqual(Field.get_field_object(field, point), emp)

    def assertAllField(self, field_a, field_b, description=""):
        y = 0
        for y_a, y_b in zip(field_a, field_b):
            x = 0
            for a, b in zip(y_a, y_b):
                self.assertEqual(a, b, "at Point({}, {}) {}".format(x, y, description))
                x += 1
            y += 1
