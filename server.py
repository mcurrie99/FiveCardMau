import socket
from _thread import *
from game import *
import pickle
import sys
import struct

server = ''
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

game = Spoons(0)


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
            name = conn.recv(2048).decode()
            if len(players) > 0:
                for i in players:
                    if name == i:
                        valid == False
                        break
            if valid == True:
                conn.send(str.encode('Good'))
                players.append(name)
                break
            else:
                conn.send(str.encode('Not'))
        except:
            connection = False
    
    while True:
        if connection == True:
            try:
                game_join = conn.recv(2048).decode()
            except:
                break
        else:
            break


    if game_join == 'Spoons':
        spoons_server(name, p)

    # try:
    #     del games[gameId]
    #     print('Closing Game: ', gameId)
    # except:
    #     pass
    idCount -= 1
    conn.close()
    game.remove_player(name)
    game.empty_lobby()
    players.pop(name)
            
    print(f'{name} Lost Connection')
    print(game.players)


def spoons_server(name, p):
    game.add_player(name, p)
    reply = ''
    while True:
        try:
            data = conn.recv(4096).decode()
            if data == 'get_game':
                packet = pickle.dumps(game)
                length = struct.pack('!I', len(packet))
                packet = length + packet
                conn.sendall(packet)
            elif data == 'voted':
                game.vote(name)
                packet = pickle.dumps(game)
                length = struct.pack('!I', len(packet))
                packet = length + packet
                conn.sendall(packet)
            elif data == 'change_hand':
                conn.send(str.encode('receive 1'))
                new_wait = conn.recv(2048).decode()
                conn.send(str.encode('receive 2'))
                new_hand = conn.recv(2048).decode()
                game.change_hand(name, new_wait, new_hand)
                packet = pickle.dumps(game)
                length = struct.pack('!I', len(packet))
                packet = length + packet
                conn.sendall(packet)
            elif data == 'Winner':
                print('Winner')
                game.change_winner(name)
                packet = pickle.dumps(game)
                length = struct.pack('!I', len(packet))
                packet = length + packet
                conn.sendall(packet)
            elif not data:
                break

        #     if gameId in games:
        #         game = games[gameId]
        #         if not data:
        #             break
        #         else:
        #             if data == 'reset':
        #                 game.resetWent()
        #             elif data != 'get':
        #                 game.play(p, data)
        #             reply = game
        #             conn.sendall(pickle.dumps(reply))
        #     else:
        #         break
        except:
            break


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
