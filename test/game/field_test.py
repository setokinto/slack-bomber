
import unittest

from app.game.field import Field, Point

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

