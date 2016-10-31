
import unittest
import time
from unittest.mock import patch

from app.game.bomber import BomberFactory, Bomber

class BomberTest(unittest.TestCase):

    def setUp(self):
        self.patcher = patch("app.game.bomber.slacker")
        self.patcher.start()
        self.patcher2 = patch("app.game.bomber.Bomber.start")
        self.patcher2.start()

    def tearDown(self):
        self.patcher.stop()
        self.patcher2.stop()

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

    @patch("app.game.bomber.FieldOutputter")
    def test_send_new_message_after_8_chats(self, mocked_outputter):
        bomber = BomberFactory.create("channel2", [])
        bomber.prev_tick = time.time()
        self.assertEqual(bomber.should_send_as_new_message, False)
        bomber.add_chat_count()
        bomber.add_chat_count()
        bomber.add_chat_count()
        bomber.add_chat_count()
        bomber.add_chat_count()
        bomber.add_chat_count()
        bomber.add_chat_count()
        self.assertEqual(bomber.should_send_as_new_message, False)
        bomber.tick()
        bomber.add_chat_count()
        self.assertEqual(bomber.should_send_as_new_message, True)
        bomber.tick()
        self.assertEqual(bomber.should_send_as_new_message, False)
        bomber.add_chat_count()
        self.assertEqual(bomber.should_send_as_new_message, False)

