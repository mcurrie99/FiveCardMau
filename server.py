import socket
from _thread import *
from game import Game
import pickle
import sys

server = "192.168.1.184"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

game = Game(0)

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
    conn.send(str.encode(str(p)))
    name = conn.recv(4096).decode()
    game.add_player(name, p)
    print(name)

    reply = ''
    while True:
        try:
            data = conn.recv(4096).decode()
            if data == 'get_game':
                conn.sendall(pickle.dumps(game))
            elif data == 'voted':
                game.vote(name)
                conn.sendall(pickle.dumps(game))
            elif data == 'change_hand':
                conn.send(str.encode('receive 1'))
                new_wait = conn.recv(2048).decode()
                conn.send(str.encode('receive 2'))
                new_hand = conn.recv(2048).decode()
                game.change_hand(name, new_wait, new_hand)
                conn.sendall(pickle.dumps(game))
            elif data == 'Winner':
                game.change_winner(name)
                print(len(conn.sendall(pickle.dumps(game))))
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

    # try:
    #     del games[gameId]
    #     print('Closing Game: ', gameId)
    # except:
    #     pass
    idCount -= 1
    conn.close()
    game.remove_player(name)
            
    print(f'{name} Lost Connection')
    print(game.players)
    game.empty_lobby()

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
