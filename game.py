import json

class Game:
    def __init__(self, id):
        with open('Cards.json') as json_file:
            self.cards = json.load(json_file)
        self.players = {}
        self.hand = {}
        self.moves = []
        self.wins = []
        self.topCard = 'ace_of_spades'
        self.started = False
        self.player_count = 0
        self.votes = 0

    def deal(self):
        """
        :param p: [0,1]
        :return: Move
        """
        return self.moves[p]

    def play(self, player, move):
        self.moves[player] = move
        if player == 0:
            self.p1Went = True
        else:
            self.p2Went = True
        
    def player_went(self):
        return self.started

    def bothWent(self):
        return self.p1Went and self.p2Went

    def add_player(self, Name, playerid):
        self.players.update({Name:[playerid, False]})
        host = False
        for i, j in enumerate(self.players):
            if self.players[j][1] == True:
                host = True
        if host == False:
            self.players[Name][1] = True

    def remove_player(self, Name):
        try:
            if self.players[Name][1] == True:
                self.find_new_host()
            del self.players['Matt']
        except:
            pass

    def find_new_host(self):
        try:
            for i, j in enumerate(self.players):
                if self.players[j][1] == False:
                    self.players[j][1] = True
                    break
        except:
            # return game back preparing state
            pass

    def winner(self):
        p1 = self.moves[0].upper()[0]
        p2 = self.moves[1].upper()[1]

        winner = -1
        if p1 == 'R' and p2 =='S':
            winner = 0
        elif p1 == 'S' and p2 == 'R':
            winner = 1
        elif p1 == 'P' and p2 =='R':
            winner = 0
        elif p1 == 'R' and p2 == 'P':
            winner = 1
        elif p1 == 'S' and p2 == 'P':
            winner = 0
        elif p1 == 'P' and p2 =='S':
            winner = 1

        return winner
    
    def end_game(self):
        self.started = False
        for i, j in enumerate(self.hand):
            for k in range(0, len(self.hand[j])):
                del self.hand[j][0]
        return self.started

    def start_game(self):
        self.started = True
        with open('Cards.json') as json_file:
            self.cards = json.load(json_file)
        return self.started

    def vote(self):
        self.votes += 1