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
            val = abs(self.last_value) + 1
            if self.state == self.State.RECEIVED_PING:
                self.state = self.State.RECEIVED_NONE
            elif self.state == self.State.RECEIVED_BOTH:
                self.state = self.State.RECEIVED_PONG
            print('Sent PING ', val)
        elif msg_type == Message.MsgType.PONG:
            val = -1 * abs(self.last_value) - 1
            if self.state == self.State.RECEIVED_PONG:
                self.state = self.State.RECEIVED_NONE
            elif self.state == self.State.RECEIVED_BOTH:
                self.state = self.State.RECEIVED_PING
            print('Sent PONG ', val)

        self.network_adapter.send(val)

    def handleMsg(self, msg):
        self.consumeMsg(msg)

        if self.state == self.State.RECEIVED_PING:
            print('Entered critical section')
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
            self.produceMsg(Message.MsgType.PING)
            self.produceMsg(Message.MsgType.PONG)
        else:  # new token
            self.last_value = msg.value

            if msg.type == Message.MsgType.PONG:
                print('Received PONG ', msg.value)
                if self.state == self.State.RECEIVED_PING:
                    self.state = self.State.RECEIVED_BOTH
                elif self.state == self.State.RECEIVED_NONE:
                    self.state = self.State.RECEIVED_PONG
                else:
                    print('error')

            if msg.type == Message.MsgType.PING:
                print('Received PING ', msg.value)
                if self.state == self.State.RECEIVED_PONG:
                    self.state = self.State.RECEIVED_BOTH
                elif self.state == self.State.RECEIVED_NONE:
                    self.state = self.State.RECEIVED_PING
                else:
                    print('error')

    def regenerate(self, val):
        self.incarnate(val)
        self.state = self.State.RECEIVED_NONE

    def incarnate(self, val):
        if val > 0:
            self.last_value = val + 1
        else:
            self.last_value = val - 1
