from enum import Enum


class Message:
    class MsgType(Enum):
        PING = 1
        PONG = 2

    type = None
    value = None

    def __init__(self, a_value):
        self.value = a_value

        if a_value > 0:
            self.type = Message.MsgType.PING
        else:
            self.type = Message.MsgType.PONG
