
from app.slack import slacker
from app.game.field import Object, Bomb, Fire, Item, Person, FiredPerson, Point

object_emoji_map = {
    Object.wall: ":black_square_for_stop:",
    Object.empty: ":white_large_square:",
    Object.block: ":package:"
}

item_emoji_map = {
    Item.add_bomb: ":b:",
    Item.fire: ":fire:",
    Item.speed: ":ice_skate:"
}

person_emoji_map = {
    0: ":joy:",
    1: ":sunglasses:",
    2: ":wink:",
    3: ":heart_eyes:"
}


def object_to_emoji(object):
    if isinstance(object, Bomb):
        return ":bomb:"

    if isinstance(object, Fire):
        return ":boom:"

    if isinstance(object, Item):
        return item_emoji_map[object]

    if isinstance(object, FiredPerson):
        return ":skull:"

    if isinstance(object, Person):
        return person_emoji_map[object.num]

    return object_emoji_map[object]

class FieldOutputter:
    recent_field_ts = {}

    @classmethod
    def post_field(cls, channel, field, new_message=False):

        field_text = ""
        
        # TODO remove this 3 line after implement output person infomation
        for person in field.persons:
            field_text += object_to_emoji(person) + "×" + str(person.life_num) + " "
        field_text += "\n"

        point = Point(0, 0)
        for y in range(field.y_size):
            for x in range(field.x_size):
                point.x = x
                point.y = y
                field_text += object_to_emoji(field.get_field_object(point))
            field_text += "\n"

        if new_message or channel not in cls.recent_field_ts:
            if new_message:
                ts = cls.recent_field_ts[channel]
                slacker.chat.update(channel, ts, "The field is expired.\nPlease scroll to bottom for next field")
            res = slacker.chat.post_message(channel, field_text)
            cls.recent_field_ts[channel] = res.body["ts"]
            cls.add_controller(channel, res.body["ts"])
        else:
            ts = cls.recent_field_ts[channel]
            slacker.chat.update(channel, ts, field_text)

    @classmethod
    def add_controller(cls, channel, ts):
        for reaction in [
            "arrow_left",
            "arrow_up",
            "arrow_down",
            "arrow_right",
            "a",
        ]:
            # It should run in parallel? Think and Implement if needed.
            slacker.reactions.add(reaction, channel=channel, timestamp=ts)
