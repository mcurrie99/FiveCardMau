import json
import random

class Game:
    def __init__(self, id):
        with open('Cards.json') as json_file:
            self.cards = json.load(json_file)
        self.players = {}
        self.hand = {}
        self.started = False
        self.player_count = 0
        self.votes = {}
        self.voters = 0
        self.order = []
        self.winner = False
        self.winner_name = ''

    def deal(self):
        """
        :param p: [0,1]
        :return: Move
        """
        for i, j in enumerate(self.hand):
            for k in range(0,4):
                r = random.randint(0, len(self.cards['Cards']))
                self.hand[j]['Hand'].append(self.cards['Cards'][r])
                self.cards['Cards'].pop(r)
        self.rotate_cards()
        print('Dealt Cards')

    def rotate_cards(self):
        if len(self.hand[self.order[0]]['Waiting']) == 0:
            r = random.randint(0, len(self.cards['Cards']))
            self.hand[self.order[0]]['Waiting'].append(self.cards['Cards'][r])
            self.cards['Cards'].pop(r)

    def play(self, player, move):
        if player == 0:
            self.p1Went = True
        else:
            self.p2Went = True
        
    def player_went(self):
        return self.started


    def add_player(self, Name, playerid):
        self.players.update({Name:[playerid, False]})
        self.hand.update({Name:{'Hand':[],'Waiting':[]}})
        self.votes.update({Name: [False]})
        self.order.append(Name)
        host = False
        for i, j in enumerate(self.players):
            if self.players[j][1] == True:
                host = True
        if host == False:
            self.players[Name][1] = True

    def remove_player(self, Name):
        new_host = False
        temp = []
        try:
            print(1)
            if self.players[Name][1] == True:
                new_host = True
            del self.players[Name]
            del self.votes[Name]
            self.order.remove(Name)
            if self.started == True:
                try:
                    for i in self.hand[Name]['Hand']:
                        temp.append(i)
                    for i in self.hand[Name]['Waiting']:
                        temp.append(i)
                    for i in range(0, len(temp)):
                        self.cards['Cards'].append(i)
                    del self.hand[Name]
                except:
                    pass
            elif self.started == False:
                self.check_votes()
            if new_host == True:
                self.find_new_host()
            for i in range(0, len(temp)):
                temp.pop(0)
        except:
            print(f'Could not delete player: {Name}')

    def find_new_host(self):
        try:
            if len(self.players > 1):
                for i, j in enumerate(self.players):
                    if self.players[j][1] == False:
                        self.players[j][1] = True
                        break
            else:
                pass
        except:
            # return game back preparing state
            pass

    def change_winner(self, name):
        self.winner = True
        self.winner_name = name
        self.end_game
        
    
    def end_game(self):
        self.started = False
        for i, j in enumerate(self.hand):
            for k in range(0, len(self.hand[j])):
                del self.hand[j][0]
        print('Game Ended')
        print(len(self.cards['Cards']))
        return self.started

    def start_game(self):
        self.started = True
        self.deal()
        self.voters = 0
        print('Starting Game')
        return self.started

    def vote(self, Name):
        self.votes[Name][0] = True
        print(f'{Name} has voted')
        self.check_votes()

    def get_host_name(self):
        for i, j in enumerate(self.players):
            if self.players[j][1] == True:
                return j

    def check_votes(self):
        self.voters = 0
        for i, j in enumerate(self.votes):
            if self.votes[j][0] == True:
                self.voters += 1
        if self.voters == len(self.votes):
            self.start_game()

    def empty_lobby(self):
        if len(self.players) == 0:
            self.end_game()

    def change_hand(self, name, new_wait, new_hand):
        if new_hand != 'Pass':
            spot_hand = self.hand[name]['Hand'].index(new_wait)
            spot_wait = self.hand[name]['Waiting'].index(new_hand)
            self.hand[name]['Waiting'][spot_wait] = new_wait
            self.hand[name]['Hand'][spot_hand] = new_hand
        else:
            self.hand[name]['Waiting'].remove(new_hand)
            on_deck = self.order.index(name)
            on_deck += 1
            try:
                on_deck_person = self.order[on_deck]
                self.hand[on_deck_person]['Waiting'].append(new_hand)
            except:
                self.cards['Cards'].append(new_hand)
        if self.order.index(name) == 0:
            self.rotate_cards()