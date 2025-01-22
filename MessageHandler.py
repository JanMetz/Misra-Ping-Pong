import time
from enum import Enum
from Message import Message


class MessageHandler:
    class State(Enum):
        RECEIVED_PING = 1
        RECEIVED_PONG = 2
        RECEIVED_BOTH = 3
        RECEIVED_NONE = 4

    def __init__(self, na):
        self.state = self.State.RECEIVED_NONE
        self.last_value = 0
        self.network_adapter = na

    def produceMsg(self, msg_type):
        val = 0
        if msg_type == Message.MsgType.PING:
            val = self.last_value
            if self.state == self.State.RECEIVED_PING:
                self.state = self.State.RECEIVED_NONE
            elif self.state == self.State.RECEIVED_BOTH:
                self.state = self.State.RECEIVED_PONG
        elif msg_type == Message.MsgType.PONG:
            val = -self.last_value
            if self.state == self.State.RECEIVED_PONG:
                self.state = self.State.RECEIVED_NONE
            elif self.state == self.State.RECEIVED_BOTH:
                self.state = self.State.RECEIVED_PING

        self.network_adapter.send(val)

    def handleMsg(self, msg):
        self.consumeMsg(msg)

        if self.state == self.State.RECEIVED_PING:
            time.sleep(1)
            if self.state != self.State.RECEIVED_PONG and self.state != self.State.RECEIVED_BOTH:
                self.produceMsg(Message.MsgType.PING)
        elif self.state == self.State.RECEIVED_PONG:
            self.produceMsg(Message.MsgType.PONG)
        elif self.state == self.State.RECEIVED_BOTH:
            self.incarnate(msg.value)
            self.produceMsg(Message.MsgType.PING)
            self.produceMsg(Message.MsgType.PONG)
            self.state = self.State.RECEIVED_NONE

    def consumeMsg(self, msg):
        if abs(msg.value) < abs(self.last_value):  # old token
            pass
        elif msg.value == self.last_value:  # token has been lost
            self.regenerate(msg.value)
            self.produceMsg(Message.MsgType.PONG)
        else:  # new token
            self.last_value = msg.value

            if msg.type == Message.MsgType.PONG:
                if self.state == self.State.RECEIVED_PING:
                    self.state = self.State.RECEIVED_BOTH
                elif self.state == self.State.RECEIVED_NONE:
                    self.state = self.State.RECEIVED_PONG
                else:
                    print('error')

            if msg.type == Message.MsgType.PING:
                if self.state == self.State.RECEIVED_PONG:
                    self.state = self.State.RECEIVED_BOTH
                elif self.state == self.State.RECEIVED_NONE:
                    self.state = self.State.RECEIVED_PING
                else:
                    print('error')

    def regenerate(self, val):
        self.last_value = abs(val) + 1
        self.state = self.State.RECEIVED_NONE

    def incarnate(self, val):
        self.last_value = abs(val) + 1