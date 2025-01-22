import sys

from Message import Message
from NetworkAgent import NetworkAgent
from MessageHandler import MessageHandler


def main():
    if len(sys.argv) < 5:
        print('Incorrect number of arguments!')
        print(f'Use case: {sys.argv[0]} hosting_port forwarding_port forwarding_addr is_initiating')
        return

    hosting_port = int(sys.argv[1])
    forwarding_port = int(sys.argv[2])
    forwarding_addr = sys.argv[3]
    is_initiating = sys.argv[4] == 'true'

    na = NetworkAgent(forwarding_addr, forwarding_port, hosting_port)

    mh = MessageHandler(na)

    if is_initiating:
        na.bind()
        na.connect()
        print('Initiating...')
        na.send(1)
        na.send(-1)
    else:
        na.connect()
        na.bind()

    while True:
        data = na.receive()
        if not data:
            na.close()
            break

        for num in data.split():
            mh.handleMsg(Message(int(num)))

    na.close()


if __name__ == '__main__':
    main()
