
import unittest
from unittest.mock import Mock, patch

from app.game.field_outputter import FieldOutputter

class FieldOutputterTest(unittest.TestCase):

    def setUp(self):
        pass

    @patch("app.game.field_outputter.slacker")
    def test_outputter_send_new_message(self, mocked_slacker):
        FieldOutputter.recent_field_ts = {}
        mock = Mock()
        mock.body = {"ts": "tsvalue"}
        mocked_slacker.chat.post_message.return_value = mock
        mocked_slacker.chat.update.return_value = None
        FieldOutputter.post_field("channel", None)
        self.assertTrue(mocked_slacker.chat.post_message.called)
        self.assertFalse(mocked_slacker.chat.update.called)

    @patch("app.game.field_outputter.slacker")
    def test_Field_should_edit_in_second_post(self, mocked_slacker):
        FieldOutputter.recent_field_ts = {}
        mock = Mock()
        mock.body = {"ts": "tsvalue"}
        mocked_slacker.chat.post_message.return_value = mock
        mocked_slacker.chat.update.return_value = None
        FieldOutputter.post_field("channel", None)
        self.assertTrue(mocked_slacker.chat.post_message.called)
        self.assertFalse(mocked_slacker.chat.update.called)
        FieldOutputter.post_field("channel", None)
        self.assertTrue(mocked_slacker.chat.update.called)

    @patch("app.game.field_outputter.slacker")
    def test_Field_should_post_to_other_channel(self, mocked_slacker):
        FieldOutputter.recent_field_ts = {}
        mock = Mock()
        mock.body = {"ts": "tsvalue"}
        mocked_slacker.chat.post_message.return_value = mock
        mocked_slacker.chat.update.return_value = None
        FieldOutputter.post_field("channel", None)
        self.assertTrue(mocked_slacker.chat.post_message.called)
        self.assertFalse(mocked_slacker.chat.update.called)
        mocked_slacker.chat.post_message.called = False
        FieldOutputter.post_field("channel2", None)
        self.assertTrue(mocked_slacker.chat.post_message.called)
        self.assertFalse(mocked_slacker.chat.update.called)

