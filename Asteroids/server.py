import socket
import threading

class Server:
    def __init__(self):
        self.MAX_CONNECTIONS = 3
        self.active_connections = 0

        self.listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
        self.listen_socket.bind((socket.gethostname(), 8654))

        self.client_sockets = []

    def start(self):
        print('Server listening for connections...')
        x = threading.Thread(target=self.listen(), daemon=True)

    def listen(self):
        self.listen_socket.listen(5)

        while True:
            if self.active_connections == self.MAX_CONNECTIONS:
                continue

            self.client_sockets[self.active_connections], address = self.listen_socket.accept()
            self.active_connections += 1

            print('Client connected from', address)