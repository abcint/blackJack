import random

def printIntro(): 
	print("BlackJack AI - Final Project") 
	print("https://github.com/brs80/blackjack\n")

def startGame(): 
    playscore = 0
    dealscore = 0
    deck = Deck()
    deck.shuffle()
    player = Player()
    player.draw(deck)
    print("\nPlayer Hand:")
    player.showHand()
    dealer = Dealer()
    dealer.draw(deck)
    print("\nDealer Hand:")
    dealer.showHand()

def hand_total(hand):
    total = 0
    ace_found = False
    soft = False

    for card in hand:
        if card.value >= 10:
            total += 10
        else:
            total += card.value

        if card.value == 1:
            ace_found = True;

    if total < 12 and ace_found:
        total += 10
        soft = True

    return total, soft

class Card(object):
    def __init__(self,suit,value):
        self.suit = suit
        self.value = value
    def show(self):
        if self.value==1:
            print("{} of {}".format('A', self.suit))
        elif self.value==11:
            print("{} of {}".format('J', self.suit))
        elif self.value==12:
            print("{} of {}".format('Q', self.suit))
        elif self.value==13:
            print("{} of {}".format('K', self.suit))
        else:
            print("{} of {}".format(self.value,self.suit))

class Deck(object):
    def __init__(self):
        self.cards = []
        self.build()
    def build(self):
        for suit in ("Spades","Clubs","Diamonds","Hearts"):
            for value in range(1,14):
                self.cards.append(Card(suit,value))
    def show(self):
        for card in self.cards:
            card.show()
    def shuffle(self):
        random.shuffle(self.cards)
    def drawCard(self):
        return self.cards.pop()

class Player(object):
    def __init__(self):
        self.hand = []
    def draw(self,deck):
        for num in range(1,3):
            self.hand.append(deck.drawCard())
    def showHand(self):
        total = hand_total(self.hand)
        for card in self.hand:
            card.show()
        print("Score: {}\nAce in hand: {}".format(total[0], total[1]))

class Dealer(object):
    def __init__(self):
        self.hand = []
    def draw(self,deck):
        for num in range(1,3):
            self.hand.append(deck.drawCard())
    def showHand(self):
        total = hand_total(self.hand)
        for card in self.hand:
            card.show()
        print("Score: {}\nAce in hand: {}".format(total[0], total[1]))
