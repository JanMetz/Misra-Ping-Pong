import socket

class NetworkAgent:
    def __init__(self, ip_address, port):
        self.ip_address = ip_address
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn = None

    def send(self, msg):
        return self.socket.send(bytes(str(msg) + '\n', 'utf-8'))

    def receive(self):
        return self.socket.recv(1024)

    def connect(self):
        self.socket.connect((self.ip_address, self.port))

    def close(self):
        self.socket.close()

    def bind(self):
        self.socket.bind((self.ip_address, self.port))
        self.socket.listen()
        self.conn, addr = self.socket.accept()
        print('Connected by', addr)
