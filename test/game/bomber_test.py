
import unittest

from app.game.bomber import BomberFactory, Bomber

class InputTest(unittest.TestCase):

    def setUp(self):
        pass

    def test_BomberFactory_should_create_bomber_instance(self):
        bomber = BomberFactory.create("channel", [])
        self.assertIsInstance(bomber, Bomber)

    def test_BomberFactory_should_return_same_instance_in_same_channel(self):
        bomber1 = BomberFactory.create("channel", [])
        bomber2 = BomberFactory.create("channel", [])
        self.assertIs(bomber1, bomber2)

    def test_BomberFactory_should_create_each_bomber_instance_in_other_channel(self):
        bomber1 = BomberFactory.create("channel1", [])
        bomber2 = BomberFactory.create("channel2", [])
        self.assertIsNot(bomber1, bomber2)

