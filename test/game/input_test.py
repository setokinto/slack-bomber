
import unittest

from app.game.input import Command, Input

class InputTest(unittest.TestCase):

    def setUp(self):
        pass

    def test_input_should_return_up(self):
        self.called = False
        def handler(user, command):
            self.assertEqual(command, Command.up)
            self.called = True

        input_ = Input("channel", handler)
        up = input_._fetcher_handler("user", "arrow_up", "channel")
        self.assertTrue(self.called)

    def test_input_should_return_down(self):
        self.called = False
        def handler(user, command):
            self.assertEqual(command, Command.down)
            self.assertEqual(user, "user")
            self.called = True

        input_ = Input("channel", handler)
        up = input_._fetcher_handler("user", "arrow_down", "channel")
        self.assertTrue(self.called)

    def test_input_should_return_left(self):
        self.called = False
        def handler(user, command):
            self.assertEqual(command, Command.left)
            self.assertEqual(user, "user")
            self.called = True

        input_ = Input("channel", handler)
        up = input_._fetcher_handler("user", "arrow_left", "channel")
        self.assertTrue(self.called)


    def test_input_should_return_right(self):
        self.called = False
        def handler(user, command):
            self.assertEqual(command, Command.right)
            self.assertEqual(user, "user")
            self.called = True

        input_ = Input("channel", handler)
        up = input_._fetcher_handler("user", "arrow_right", "channel")
        self.assertTrue(self.called)

    def test_input_should_return_a(self):
        self.called = False
        def handler(user, command):
            self.assertEqual(command, Command.a)
            self.assertEqual(user, "user")
            self.called = True

        input_ = Input("channel", handler)
        up = input_._fetcher_handler("user", "a", "channel")
        self.assertTrue(self.called)

    def test_input_should_not_return_the_other_reactions(self):
        self.called = False
        def handler(user, command):
            self.called = True

        input_ = Input("channel", handler)
        up = input_._fetcher_handler("user", "the_other_reaction", "channel")
        self.assertFalse(self.called)

