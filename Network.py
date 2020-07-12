import socket
import pickle
import struct

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = '98.109.68.217'
        self.port = 5555
        self.addr = (self.server, self.port)

    def connect(self, name):
        try:
            self.client.connect(self.addr)
            self.client.send(str.encode(name))
            return self.client.recv(2048).decode()
        except:
            pass
    def change_hand(self, new_wait, new_hand ):
        try:
            self.client.send(str.encode('change_hand'))
            if self.client.recv(2048).decode() == 'receive 1':
                self.client.send(str.encode(new_wait))
            else:
                return 'error 1'
            if self.client.recv(2048).decode() == 'receive 2':
                self.client.send(str.encode(new_hand))
            else:
                return 'error 2'
            buf = b''
            while len(buf) < 4:
                buf += self.client.recv(4-len(buf))
            length = struct.unpack('!I', buf)[0]
            print(length)
            return pickle.loads(self.client.recv(length))
        except socket.error as e:
            print(e)
    def get_game(self):
        try:
            # Testing new sending details to avoid random crashing
            self.client.send(str.encode('get_game'))
            buf = b''
            while len(buf) < 4:
                buf += self.client.recv(4-len(buf))
            length = struct.unpack('!I', buf)[0]
            return pickle.loads(self.client.recv(length))
        except socket.error as e:
            print(e)

    def send(self, data):
        try:
            self.client.send(str.encode(data))
            buf = b''
            while len(buf) < 4:
                buf += self.client.recv(4-len(buf))
            length = struct.unpack('!I', buf)[0]
            return pickle.loads(self.client.recv(length))
        except socket.error as e:
            print(e)

    def send_hand(self, hand):
        # Further investigation might conclude that this is not needed if processing is done on server side.
        for i in range(0, len(hand)):
            self.client.send(str.encode(hand[i]))

    def alter_hand(self):
        pass