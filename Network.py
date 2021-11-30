import socket
import pickle
import struct

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Public IP at Home
        # self.server = '98.109.48.234'

        # IP address of computer at home
        # self.server = '71.187.211.242' # Public IP Address of the server (do not include port)

        # Test Port for Domain
        self.server = 'game.currspice.com'

        # IP address at Purdue
        #self.server = '128.211.222.85'

        # Port to access on server network
        self.port = 5555
        self.addr = (self.server, self.port)

    def connect(self, name):
        try:
            self.client.connect(self.addr) # Connect to server
            self.client.send(str.encode(name)) # Sends name of person
            return self.client.recv(2048).decode() # Receives validation of name
        except:
            pass
    def change_hand(self, new_wait, new_hand ):
        try: # Sends change hand command
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
            # Asks for updated version of game
            self.client.send(str.encode('get_game')) # Asks server for game object
            buf = b''
            while len(buf) < 4: # Gets size of game
                buf += self.client.recv(4-len(buf))
            length = struct.unpack('!I', buf)[0] # size of incoming file !I identifies that it will be seen as an integer
            return pickle.loads(self.client.recv(length)) # Receices game file
        except socket.error as e:
            print(e)

    def send(self, data):
        try:
            print(data)
            self.client.send(str.encode(data))
            buf = b''
            while len(buf) < 4:# Gets size of game
                buf += self.client.recv(4-len(buf))
            length = struct.unpack('!I', buf)[0]# size of incoming file
            return pickle.loads(self.client.recv(length))# Receices game file
        except socket.error as e:
            print(e)
    
    def send_name(self, data):
        try:
            self.client.send(str.encode(data)) # Sends name
            return self.client.recv(2048).decode() # Receives data
        except socket.error as e:
            print(e)
    
    def send_only(self, data):
        try:
            self.client.send(str.encode(data)) # Sends data
        except socket.error as e:
            print(e)
    def send_hand(self, hand):
        # Further investigation might conclude that this is not needed if processing is done on server side.
        for i in range(0, len(hand)):
            self.client.send(str.encode(hand[i]))