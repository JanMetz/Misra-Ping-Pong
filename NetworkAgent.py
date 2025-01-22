import socket


class NetworkAgent:
    def __init__(self, forwarding_addr, forwarding_port, host_port):
        self.forwarding_addr = forwarding_addr
        self.host_port = host_port
        self.forwarding_port = forwarding_port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn = None

    def send(self, msg):
        return self.client_socket.send(bytes(str(msg) + '\n', 'utf-8'))

    def receive(self):
        return self.conn.recv(1024)

    def connect(self):
        self.client_socket.connect((self.forwarding_addr, self.forwarding_port))
        print('Connected to ', self.forwarding_addr, self.forwarding_port)

    def close(self):
        self.client_socket.close()
        self.server_socket.close()

    def bind(self):
        self.server_socket.bind(('0.0.0.0', self.host_port))
        self.server_socket.listen()
        self.conn, addr = self.server_socket.accept()
        print('Connected by ', addr)
