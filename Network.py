import socket
import pickle

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = '192.168.1.184'
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
                print('1')
                self.client.send(str.encode(new_wait))
                print('work 1')
            else:
                return 'error 1'
            if self.client.recv(2048).decode() == 'receive 2':
                self.client.send(str.encode(new_hand))
                print('work 2')
            else:
                return 'error 2'
            return pickle.loads(self.client.recv(8192*2))
        except socket.error as e:
            print(e)
    def get_game(self):
        try:
            self.client.send(str.encode('get_game'))
            return pickle.loads(self.client.recv(8192*2))
        except socket.error as e:
            print(e)

    def send(self, data):
        try:
            self.client.send(str.encode(data))
            return pickle.loads(self.client.recv(8192*2))
        except socket.error as e:
            print(e)

    def send_hand(self, hand):
        # Further investigation might conclude that this is not needed if processing is done on server side.
        for i in range(0, len(hand)):
            self.client.send(str.encode(hand[i]))

    def alter_hand(self):
        pass