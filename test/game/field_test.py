
import unittest

from app.game.field import Field, Point, Bomb, Fire

class FieldTest(unittest.TestCase):

    def setUp(self):
        pass

    def test_person_should_move_in_Field(self):
        field = Field(8, 10, ["user1", "user2"])
        person1 = field.person_by_user("user1")
        self.assertIsNotNone(person1)
        person1.point = Point(0, 0)
        person2 = field.person_by_user("user2")
        self.assertIsNotNone(person2)
        person2.point = Point(7, 9)

        field.move_top(person1)
        self.assertEqual(person1.point, Point(0, 0))
        field.move_bottom(person1)
        self.assertEqual(person1.point, Point(0, 1))
        field.put_bomb(person1)
        self.assertIsNotNone(field.bombs[0][1])
        field.move_top(person1)
        self.assertEqual(person1.point, Point(0, 0))
        field.put_bomb(person1)
        self.assertIsNone(field.bombs[0][0], "It should not put a bomb because a bomb is not remained")

        field.move_right(person1)
        self.assertEqual(person1.point, Point(1, 0))
        field.move_left(person1)
        self.assertEqual(person1.point, Point(0, 0))

    def test_Field_should_create(self):
        field = Field(8, 10, ["user1", "user2"])
        field.objects[0][0]
        field.objects[7][9]
        with self.assertRaises(IndexError) as error:
            field.objects[8][9]
        with self.assertRaises(IndexError) as error:
            field.objects[7][10]

    def test_bomb_should_fire(self):
        bomb = Bomb("user1", 2)
        fire_points = bomb.fire()
        self.assertEqual(len(fire_points), 2*4+1)

        self.assertTrue(Point(0, 0) in fire_points)

    def test_Field_should_proceed_time(self):
        field = Field(8, 10, ["user1", "user2"])
        bom1 = Bomb("user1", 1)
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


    def test_Field_should_fire_with_other_bomb(self):
        field = Field(8, 10, ["user1", "user2"])
        bom1 = Bomb("user1", 1)
        bom2 = Bomb("user1", 2)
        bom3 = Bomb("user1", 3)
        bom4 = Bomb("user1", 4)
        bom5 = Bomb("user1", 5)
        fire = Fire()
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

        field.fire_bomb(Point(3, 1)) # bom3
        self.assertAllField(field.bombs, [
            [None, fire, None, None, fire, None, None, None, None, None],
            [None, fire, None, None, fire, None, None, fire, None, None],
            [None, fire, None, None, fire, None, None, fire, None, None],
            [fire, fire, fire, fire, fire, fire, fire, fire, fire, fire],
            [None, fire, fire, None, fire, None, None, fire, None, None],
            [None, fire, fire, None, fire, None, fire, fire, fire, None],
            [None, fire, fire, None, fire, None, None, fire, None, None],
            [fire, fire, fire, fire, fire, fire, fire, None, None, None],
        ])

    def assertAllField(self, field_a, field_b, description=""):
        y = 0
        for y_a, y_b in zip(field_a, field_b):
            x = 0
            for a, b in zip(y_a, y_b):
                self.assertEqual(a, b, "at Point({}, {}) {}".format(x, y, description))
                x += 1
            y += 1

