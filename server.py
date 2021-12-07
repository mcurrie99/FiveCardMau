import socket
from _thread import *
import pickle
import sys
import struct
from Spoons import *
from Blackjack import *

server = ''
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Sets up networking socket

spoons = Spoons(0) # Creates a game of Spoons
blackjack = Blackjacks(0) # Creates a game of Blackjack


try:
    s.bind((server, port)) # Binds to a port on the network
except socket.error as e:
    str(e)

s.listen(6) # Set maximum amount of connections
print('Waiting for a connection, Server Started')

connected = set() # Creates an empty set
games = {} # Games that are created
idCount = 0 # Creates the initial id for a player
players = [] # Holds names of all player in all games

def threaded_client(conn, p):
    global idCount # Call upon the idCount
    valid = True
    connection = True

    while True:
        # Checks if name is already taken
        try: # Constantly allows the server to handle an disconnection
            valid = True
            name = conn.recv(4096).decode() # Waits for name from player
            if name == 'Dealer': # Cannot let someone come in with Dealer as name
                valid = False 
            elif len(players) > 0:
                for i in players:
                    if name == i: # Checks if the player has the same name as someone else
                        valid = False
                        break
            if valid == True:
                # Allows person to join game
                conn.send(str.encode('Good'))
                players.append(name)
                print(f'{name} joined')
                break
            else:
                # Denies person from connecting to the game
                conn.send(str.encode('Not'))
        except:
            connection = False
    
    while True:
        if connection == True:
            try:
                game_join = conn.recv(2048).decode() # Accepts what gamemode the player has chosen
                # print(game_join)
                if game_join == 'Spoons':
                    spoons.add_player(name, p) # Adds player to game
                    print(name, 'Was added to a Spoons game')
                    packet = pickle.dumps(spoons)
                    length = struct.pack('!I', len(packet))
                    packet = length + packet
                    conn.sendall(packet)
                    reply = ''
                    while True:
                        try:
                            data = conn.recv(4096).decode()
                            if data == 'get_game': # Sends game data to player
                                packet = pickle.dumps(spoons)
                                length = struct.pack('!I', len(packet))
                                packet = length + packet
                                conn.sendall(packet)
                            elif data == 'voted': # Player has voted to start the game
                                spoons.vote(name)
                                packet = pickle.dumps(spoons)
                                length = struct.pack('!I', len(packet))
                                packet = length + packet
                                conn.sendall(packet)
                            elif data == 'change_hand': # Person is exchanging the passed card for a card in his hand
                                conn.send(str.encode('receive 1'))
                                new_wait = conn.recv(2048).decode()
                                conn.send(str.encode('receive 2'))
                                new_hand = conn.recv(2048).decode()
                                spoons.change_hand(name, new_wait, new_hand)
                                packet = pickle.dumps(spoons)
                                length = struct.pack('!I', len(packet))
                                packet = length + packet
                                conn.sendall(packet)
                            elif data == 'Winner': # Declares winner of the game
                                print('Winner')
                                spoons.change_winner(name)
                                packet = pickle.dumps(spoons)
                                length = struct.pack('!I', len(packet))
                                packet = length + packet
                                conn.sendall(packet)
                            elif not data:
                                break
                        except:
                            break # Allows for disconnection at any point
                    spoons.remove_player(name) # Removes player if connection is lost
                    print(spoons.players)
                    spoons.empty_lobby() # Checks if the lobby of a game is empy

                elif game_join == 'Blackjack':
                    blackjack.add_player(name, p) # Adds player to blackjack game
                    print(name, 'Was added to a Blackjack game')
                    packet = pickle.dumps(blackjack)
                    length = struct.pack('!I', len(packet))
                    packet = length + packet
                    conn.sendall(packet)
                    reply = ''
                    while True:
                        try:
                            data = conn.recv(4096).decode()
                            if data == 'get_game': # Sends game data to player
                                blackjack.check_points()
                                packet = pickle.dumps(blackjack)
                                length = struct.pack('!I', len(packet))
                                packet = length + packet
                                conn.sendall(packet)
                            elif data == 'voted': # Player has voted to start the game
                                blackjack.vote(name)
                                packet = pickle.dumps(blackjack)
                                length = struct.pack('!I', len(packet))
                                packet = length + packet
                                conn.sendall(packet)
                            elif data == 'Hit': # Player has selected to hit and receives another card
                                blackjack.deal(name)
                                packet = pickle.dumps(blackjack)
                                length = struct.pack('!I', len(packet))
                                packet = length + packet
                                conn.sendall(packet)
                            elif data == 'Stand': # Player has selected to stand and the turns move on
                                blackjack.stand(name)
                                packet = pickle.dumps(blackjack)
                                length = struct.pack('!I', len(packet))
                                packet = length + packet
                                conn.sendall(packet)
                            elif data == 'Winner': # Player is the winner of the game
                                print('Winner')
                                packet = pickle.dumps(blackjack)
                                length = struct.pack('!I', len(packet))
                                packet = length + packet
                                conn.sendall(packet)
                            elif not data:
                                break
                        except:
                            break # Allows for player to disconnect at any point in the game
                        
                    blackjack.remove_player(name) # Removes player from the game
                    print(blackjack.players) # Print players in game
                    blackjack.empty_lobby() # Checks if the lobby if the game lobby is empty
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
    conn.close() # Closes connection with the IP Addresses that had joined
    players.remove(name) # Removes players name from the list of joined people
            
    print(f'{name} Lost Connection')
    print(players)



while True:
    conn, addr = s.accept() # Waits for connection
    print('Connected to', addr) # Prints to the server console what IP address has joined

    idCount += 1
    p = 0
    # gameId = (idCount - 1) // 2

    # if idCount % 2 == 1:
    #     # games[gameId] = Game(gameId)
    #     print('Creating a New Game')
    # else:
    #     games[gameId].ready = True
    #     p = 1

    start_new_thread(threaded_client, (conn, p)) # Creates a proccess that works for that individual person.
    p += 1
    if p == 255:
        p = 0
