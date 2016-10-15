
from app.slack import slacker

class FieldOutputter:
    recent_field_ts = {}

    @classmethod
    def post_field(cls, channel, field, new_message=False):
        field_text = "TODO: create this by field"
        if new_message or channel not in cls.recent_field_ts:
            res = slacker.chat.post_message(channel, field_text)
            cls.recent_field_ts[channel] = res.body["ts"]
        else:
            ts = cls.recent_field_ts[channel]
            slacker.chat.update(channel, ts, field_text+"(edited)") # TODO: remove this string

