
import unittest

from app.game.field import Field

class FieldTest(unittest.TestCase):

    def setUp(self):
        pass

    def test_Field_should_create(self):
        field = Field(8, 10, ["user1", "user2"])
        field.objects[0][0]
        field.objects[7][9]
        with self.assertRaises(IndexError) as error:
            field.objects[8][9]
        with self.assertRaises(IndexError) as error:
            field.objects[7][10]

