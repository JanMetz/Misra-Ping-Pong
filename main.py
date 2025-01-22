from Message import Message
from NetworkAgent import NetworkAgent
from MessageHandler import MessageHandler


def setup_server(port):
    na = NetworkAgent('0.0.0.0', port)
    na.bind()
    mh = MessageHandler(na)

    with na.conn:
        na.send(1)
        while True:
            data = na.receive()
            if not data:
                na.close()
                break

            mh.handleMsg(Message(int(data[0])))


def setup_client(addr, port):
    na = NetworkAgent(addr, port)
    na.connect()
    mh = MessageHandler(na)

    with na.conn:
        while True:
            data = na.receive()
            if data is not None:
                mh.handleMsg(Message(int(data[0])))

    na.close()


def main():
    addr = '127.0.0.1'
    port = 8000
    is_initiating = False

    if is_initiating:
        setup_server(port)
    else:
        setup_client(addr, port)


if __name__ == '__main__':
    main()
