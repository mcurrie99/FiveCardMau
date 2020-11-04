import socket
from _thread import *
import pickle
import sys
import struct
from Spoons import *
from Blackjack import *

server = ''
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

spoons = Spoons(0)
blackjack = Blackjacks(0)


try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(6)
print('Waiting for a connection, Server Started')

connected = set()
games = {}
idCount = 0
players = []

def threaded_client(conn, p):
    global idCount
    valid = True
    connection = True

    while True:
        try:
            valid = True
            name = conn.recv(4096).decode()
            if name == 'Dealer':
                valid = False
            elif len(players) > 0:
                for i in players:
                    if name == i:
                        valid = False
                        break
            if valid == True:
                conn.send(str.encode('Good'))
                players.append(name)
                print(f'{name} joined')
                break
            else:
                conn.send(str.encode('Not'))
        except:
            connection = False
    
    while True:
        if connection == True:
            try:
                game_join = conn.recv(2048).decode()
                # print(game_join)
                if game_join == 'Spoons':
                    spoons.add_player(name, p)
                    print(name, 'Was added to a Spoons game')
                    packet = pickle.dumps(spoons)
                    length = struct.pack('!I', len(packet))
                    packet = length + packet
                    conn.sendall(packet)
                    reply = ''
                    while True:
                        try:
                            data = conn.recv(4096).decode()
                            if data == 'get_game':
                                packet = pickle.dumps(spoons)
                                length = struct.pack('!I', len(packet))
                                packet = length + packet
                                conn.sendall(packet)
                            elif data == 'voted':
                                spoons.vote(name)
                                packet = pickle.dumps(spoons)
                                length = struct.pack('!I', len(packet))
                                packet = length + packet
                                conn.sendall(packet)
                            elif data == 'change_hand':
                                conn.send(str.encode('receive 1'))
                                new_wait = conn.recv(2048).decode()
                                conn.send(str.encode('receive 2'))
                                new_hand = conn.recv(2048).decode()
                                spoons.change_hand(name, new_wait, new_hand)
                                packet = pickle.dumps(spoons)
                                length = struct.pack('!I', len(packet))
                                packet = length + packet
                                conn.sendall(packet)
                            elif data == 'Winner':
                                print('Winner')
                                spoons.change_winner(name)
                                packet = pickle.dumps(spoons)
                                length = struct.pack('!I', len(packet))
                                packet = length + packet
                                conn.sendall(packet)
                            elif not data:
                                break
                        except:
                            break
    
                        spoons.remove_player(name)
                        print(spoons.players)
                        spoons.empty_lobby()

                elif game_join == 'Blackjack':
                    blackjack.add_player(name, p)
                    print(name, 'Was added to a Blackjack game')
                    packet = pickle.dumps(blackjack)
                    length = struct.pack('!I', len(packet))
                    packet = length + packet
                    conn.sendall(packet)
                    reply = ''
                    while True:
                        try:
                            data = conn.recv(4096).decode()
                            if data == 'get_game':
                                blackjack.check_points()
                                packet = pickle.dumps(blackjack)
                                length = struct.pack('!I', len(packet))
                                packet = length + packet
                                conn.sendall(packet)
                            elif data == 'voted':
                                blackjack.vote(name)
                                packet = pickle.dumps(blackjack)
                                length = struct.pack('!I', len(packet))
                                packet = length + packet
                                conn.sendall(packet)
                            elif data == 'Hit':
                                blackjack.deal(name)
                                packet = pickle.dumps(blackjack)
                                length = struct.pack('!I', len(packet))
                                packet = length + packet
                                conn.sendall(packet)
                            elif data == 'Stand':
                                blackjack.stand(name)
                                packet = pickle.dumps(blackjack)
                                length = struct.pack('!I', len(packet))
                                packet = length + packet
                                conn.sendall(packet)
                            elif data == 'Winner':
                                print('Winner')
                                packet = pickle.dumps(blackjack)
                                length = struct.pack('!I', len(packet))
                                packet = length + packet
                                conn.sendall(packet)
                            elif not data:
                                break
                        except:
                            break
                        
                    blackjack.remove_player(name)
                    print(blackjack.players)
                    blackjack.empty_lobby()
                elif not game_join:
                    break
                # else:
                #     break
            except:
                connection = False
                break
        else:
            break

    idCount -= 1
    conn.close()
    players.remove(name)
            
    print(f'{name} Lost Connection')
    print(players)


def spoons_server(name, p):
    spoons.add_player(name, p)
    print(name, 'Was added to a Spoons game')
    packet = pickle.dumps(spoons)
    length = struct.pack('!I', len(packet))
    packet = length + packet
    conn.sendall(packet)
    reply = ''
    while True:
        try:
            data = conn.recv(4096).decode()
            if data == 'get_game':
                packet = pickle.dumps(spoons)
                length = struct.pack('!I', len(packet))
                packet = length + packet
                conn.sendall(packet)
            elif data == 'voted':
                spoons.vote(name)
                packet = pickle.dumps(spoons)
                length = struct.pack('!I', len(packet))
                packet = length + packet
                conn.sendall(packet)
            elif data == 'change_hand':
                conn.send(str.encode('receive 1'))
                new_wait = conn.recv(2048).decode()
                conn.send(str.encode('receive 2'))
                new_hand = conn.recv(2048).decode()
                spoons.change_hand(name, new_wait, new_hand)
                packet = pickle.dumps(spoons)
                length = struct.pack('!I', len(packet))
                packet = length + packet
                conn.sendall(packet)
            elif data == 'Winner':
                print('Winner')
                spoons.change_winner(name)
                packet = pickle.dumps(spoons)
                length = struct.pack('!I', len(packet))
                packet = length + packet
                conn.sendall(packet)
            elif not data:
                break
        except:
            break
    
    spoons.remove_player(name)
    print(spoons.players)
    spoons.empty_lobby()

def blackjack_server(name, p):
    blackjack.add_player(name, p)
    print(name, 'Was added to a Blackjack game')
    packet = pickle.dumps(blackjack)
    length = struct.pack('!I', len(packet))
    packet = length + packet
    conn.sendall(packet)
    reply = ''
    while True:
        try:
            data = conn.recv(4096).decode()
            if data == 'get_game':
                blackjack.check_points()
                packet = pickle.dumps(blackjack)
                length = struct.pack('!I', len(packet))
                packet = length + packet
                conn.sendall(packet)
            elif data == 'voted':
                blackjack.vote(name)
                packet = pickle.dumps(blackjack)
                length = struct.pack('!I', len(packet))
                packet = length + packet
                conn.sendall(packet)
            elif data == 'Hit':
                blackjack.deal(name)
                packet = pickle.dumps(blackjack)
                length = struct.pack('!I', len(packet))
                packet = length + packet
                conn.sendall(packet)
            elif data == 'Stand':
                blackjack.stand(name)
                packet = pickle.dumps(blackjack)
                length = struct.pack('!I', len(packet))
                packet = length + packet
                conn.sendall(packet)
            elif data == 'Winner':
                print('Winner')
                packet = pickle.dumps(blackjack)
                length = struct.pack('!I', len(packet))
                packet = length + packet
                conn.sendall(packet)
            elif not data:
                break
        except:
            break
    
    blackjack.remove_player(name)
    print(blackjack.players)
    blackjack.empty_lobby()

while True:
    conn, addr = s.accept()
    print('Connected to', addr)

    idCount += 1
    p = 0
    # gameId = (idCount - 1) // 2

    # if idCount % 2 == 1:
    #     # games[gameId] = Game(gameId)
    #     print('Creating a New Game')
    # else:
    #     games[gameId].ready = True
    #     p = 1

    start_new_thread(threaded_client, (conn, p))
    p += 1
    if p == 255:
        p = 0
