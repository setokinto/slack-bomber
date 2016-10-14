
import unittest

from app.rtm.emoji_fetcher import EmojiFetcher, fire_emoji_fetcher, get_content_from_message, connect, on_message


called_flag = False

fetcher1_called = lambda user, reaction, channel: None
def fetcher1_handler(user, reaction, channel):
    fetcher1_called(user, reaction, channel)

fetcher2_called = lambda user, reaction, channel: None
def fetcher2_handler(user, reaction, channel):
    fetcher2_called(user, reaction, channel)

class TestTest(unittest.TestCase):

    def setUp(self):
        self.fetcher1 = EmojiFetcher("channel1", fetcher1_handler)
        self.fetcher2 = EmojiFetcher("channel2", fetcher2_handler)
        global connect
        connect = lambda: None

    def test_get_content_from_message_should_return_reaction_when_received_reaction_removed(self):
        content = get_content_from_message({"type":"reaction_removed","user":"U03B2FKN7","item":{"type":"message","channel":"C2NPVNFGX","ts":"1476371851.000617"},"reaction":"test","event_ts":"1476372995.594852"})
        self.assertEqual(content["user"], "U03B2FKN7")
        self.assertEqual(content["channel"], "C2NPVNFGX")
        self.assertEqual(content["reaction"], "test")

    def test_get_content_from_message_should_return_reaction_when_received_reaction_added(self):
        content = get_content_from_message({"type":"reaction_added","user":"U03B2FKN1","item":{"type":"message","channel":"C2NPVMFGX","ts":"1476371851.000617"},"reaction":"test2","event_ts":"1476372995.594852"})
        self.assertEqual(content["user"], "U03B2FKN1")
        self.assertEqual(content["channel"], "C2NPVMFGX")
        self.assertEqual(content["reaction"], "test2")

    def test_get_content_from_message_should_return_None_when_received_the_other_type(self):
        content = get_content_from_message({"type":"other_type","user":"U03B2FKN7","item":{"type":"message","channel":"C2NPVNFGX","ts":"1476371851.000617"},"event_ts":"1476372995.594852"})
        self.assertIsNone(content)

    def test_fetcher_is_called_when_called_fire(self):
        global fetcher1_called
        global called_flag
        called_flag = False
        def fetcher(user, reaction, channel):
            global called_flag
            called_flag = True
            self.assertEqual(user, "user1")
            self.assertEqual(reaction, "reaction1")
            self.assertEqual(channel, "channel1")
        fetcher1_called = fetcher

        fire_emoji_fetcher("user1", "reaction1", "channel1")
        self.assertTrue(called_flag)

    def test_fetcher_is_called_when_called_fire2(self):
        global fetcher2_called
        global called_flag
        called_flag = False
        def fetcher(user, reaction, channel):
            global called_flag
            called_flag = True
            self.assertEqual(user, "user1")
            self.assertEqual(reaction, "reaction1")
            self.assertEqual(channel, "channel2")
        fetcher2_called = fetcher

        fire_emoji_fetcher("user1", "reaction1", "channel2")
        self.assertTrue(called_flag)

    def test_fetcher_is_not_called_when_called_fire_to_non_registerd_channel(self):
        global fetcher1_called
        def fetcher(user, reaction, channel):
            self.fail()
        fetcher1_called = fetcher

        fire_emoji_fetcher("user1", "reaction1", "non_registerd_channel")

    def test_fetcher_is_work(self):
        global called_flag
        called_flag = False
        def handler(user, emoji, channel):
            global called_flag
            called_flag = True
            self.assertEqual(user, "U03B2FKN7")

        fetcher = EmojiFetcher("test_fetcher_is_work", handler)
        on_message(None, """{"type":"reaction_removed","user":"U03B2FKN7","item":{"type":"message","channel":"test_fetcher_is_work","ts":"1476371851.000617"},"reaction":"test","event_ts":"1476372995.594852"}""")
        self.assertTrue(called_flag)


