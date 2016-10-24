
import unittest
from unittest.mock import Mock, patch

from app.game.field_outputter import FieldOutputter
from app.game.field import Field

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
        mocked_slacker.reactions.add.return_value = None
        field = Field(10, 8, ["user1", "user2"])
        FieldOutputter.post_field("channel",field)
        self.assertTrue(mocked_slacker.chat.post_message.called)
        self.assertFalse(mocked_slacker.chat.update.called)

    @patch("app.game.field_outputter.slacker")
    def test_Field_should_edit_in_second_post(self, mocked_slacker):
        FieldOutputter.recent_field_ts = {}
        mock = Mock()
        mock.body = {"ts": "tsvalue"}
        mocked_slacker.chat.post_message.return_value = mock
        mocked_slacker.chat.update.return_value = None
        mocked_slacker.reactions.add.return_value = None
        field = Field(10, 8, ["user1", "user2"])
        FieldOutputter.post_field("channel", field)
        self.assertTrue(mocked_slacker.chat.post_message.called)
        self.assertFalse(mocked_slacker.chat.update.called)
        FieldOutputter.post_field("channel", field)
        self.assertTrue(mocked_slacker.chat.update.called)

    @patch("app.game.field_outputter.slacker")
    def test_Field_should_post_to_other_channel(self, mocked_slacker):
        FieldOutputter.recent_field_ts = {}
        mock = Mock()
        mock.body = {"ts": "tsvalue"}
        mocked_slacker.chat.post_message.return_value = mock
        mocked_slacker.chat.update.return_value = None
        mocked_slacker.reactions.add.return_value = None
        field = Field(11, 15, ["user1", "user2"])
        FieldOutputter.post_field("channel", field)
        self.assertTrue(mocked_slacker.chat.post_message.called)
        self.assertFalse(mocked_slacker.chat.update.called)
        mocked_slacker.chat.post_message.called = False
        FieldOutputter.post_field("channel2", field)
        self.assertTrue(mocked_slacker.chat.post_message.called)
        self.assertFalse(mocked_slacker.chat.update.called)
