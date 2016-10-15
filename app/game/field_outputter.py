
from app.slack import slacker

class FieldOutputter:
    recent_field_ts = {}

    @classmethod
    def post_field(cls, channel, field, new_message=False):
        field_text = "TODO: create this by field"
        if new_message or channel not in cls.recent_field_ts:
            res = slacker.chat.post_message(channel, field_text)
            cls.recent_field_ts[channel] = res.body["ts"]
            cls.add_controller(channel, res.body["ts"])
        else:
            ts = cls.recent_field_ts[channel]
            import random
            slacker.chat.update(channel, ts, field_text+"(edited)"+str(random.random())) # TODO: remove this string

    @classmethod
    def add_controller(cls, channel, ts):
        for reaction in  [
            "arrow_left",
            "arrow_up",
            "arrow_down",
            "arrow_right",
            "a",
        ]:
            # It should run in parallel? Think and Implement if needed.
            slacker.reactions.add(reaction, channel=channel, timestamp=ts)

