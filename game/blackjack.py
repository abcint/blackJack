import random
import numpy as np


def printIntro():
    print("BlackJack AI December 2018")
    print("https://github.com/brs80/blackjack.git\n")
    print("You are given 500 chips to start.")


def printWager(player):
    print("Chips remaining: {}".format(player.getMoney()))
    print("(1) 5 chips")
    print("(2) 10 chips")
    print("(3) 50 chips")
    print("(4) 100 chips")
    print("(5) other")
    wager = input("Place your wager-> ")
    int(wager)
    if int(wager) > player.getMoney():
        print("wager too high")
        printWager(player)
    if int(wager) < 0:
        print("wager too low")
        printWager(player)
    return wager


def startGame():
    deck = Deck()
    player = Player()
    dealer = Dealer()
    while player.getMoney() > 0:
        player.draw(deck)
        dealer.draw(deck)
        printTable(player, dealer)
        wager = printWager(player)
        player.setMoney(wager)


def printTable(player, dealer):
    print("\nPlayer Hand:")
    player.showHand()
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
            ace_found = True
    if total < 12 and ace_found:
        total += 10
        soft = True
    return total, ace_found


class Card(object):
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

    def show(self):
        if self.value == 1:
            print("{} of {}".format('A', self.suit))
        elif self.value == 11:
            print("{} of {}".format('J', self.suit))
        elif self.value == 12:
            print("{} of {}".format('Q', self.suit))
        elif self.value == 13:
            print("{} of {}".format('K', self.suit))
        else:
            print("{} of {}".format(self.value, self.suit))


class DeckEmptyError(Exception):
    pass


class Deck(object):
    def __init__(self):
        self.cards = []
        self.discardCount = [0 for i in range(14)]
        self.build()

    def build(self):
        self.cards = []
        self.discardCount = [0 for i in range(14)]
        for suit in ("Spades", "Clubs", "Diamonds", "Hearts"):
            for value in range(1, 14):
                self.cards.append(Card(suit, value))
        random.shuffle(self.cards)

    def show(self):
        for card in self.cards:
            card.show()

    def addtoDiscard(self, card):
        self.discardCount[card.value] += 1

    def cardsRemaining(self):
        return len(self.cards)

    def drawCard(self):
        if not self.cardsRemaining():
            raise DeckEmptyError
        return self.cards.pop()


class CardHolder(object):
    def __init__(self):
        self.hand = []

    def draw(self, deck):
        for num in range(1, 3):
            self.hand.append(deck.drawCard())

    def hit(self, deck):
        self.hand.append(deck.drawCard())

    def discardHand(self, deck):
        for c in self.hand:
            deck.addtoDiscard(c)
        self.hand = []

    def handScore(self):
        return hand_total(self.hand)

    def showHand(self):
        total = hand_total(self.hand)
        for card in self.hand:
            card.show()
        print("Score: {}\nAce in hand: {}".format(total[0], total[1]))


class Player(CardHolder, object):
    def getMoney(self):
        return self.money

    def setMoney(self, wager):
        self.money = self.money - int(wager)


class Dealer(CardHolder, object):
    def gameHandValue(self):
        return self.hand[0].value


class Game(object):
    def __init__(self):
        self.dealer = Dealer()
        self.player = Player()
        self.deck = Deck()
        self.n_actions = 2
        self.n_features = 17
        self.wins = 0
        self.games = 0

    def showState(self):
        self.dealer.showHand()
        self.player.showHand()

    def new_round(self):
        self.player.discardHand(self.deck)
        self.dealer.discardHand(self.deck)
        self.dealer.draw(self.deck)
        self.player.draw(self.deck)
        h, s = self.player.handScore()
        return (np.append(np.array([h/21, s, self.dealer.gameHandValue()/21]),
                          [x/4 for x in self.deck.discardCount]))

    def shuffle(self):
        winRate = self.wins/self.games
        self.games = 0
        self.wins = 0
        self.deck.build()
        return winRate

    def step(self, action):
        # hit
        done = False
        reward = 0
        if action == 0:
            self.player.hit(self.deck)
            if self.player.handScore()[0] > 21:
                reward = -1
                done = True
                self.games += 1

        # stay
        elif action == 1:
            done = True
            self.games += 1
            score = self.player.handScore()[0]
            while True:
                if self.dealer.handScore()[0] >= 17:
                    break
                self.dealer.hit(self.deck)
            d_score = self.dealer.handScore()[0]
            if score > d_score or d_score > 21:
                reward = 1
                self.wins += 1
            elif score == d_score:
                reward = 0
            else:
                reward = -1
        else:
            raise ValueError('Illegal action passed')

        h, s = self.player.handScore()
        s_ = (np.append(np.array([h/21, s, self.dealer.gameHandValue()/21]),
              [x/4 for x in self.deck.discardCount]))
        return s_, reward, done


if __name__ == '__main__':
    NewGame = Game()
    NewGame.reset()
    while True:
        a = int(input())
        s_, reward, done = NewGame.step(a)
        print(s_)
        print(reward, done)
        if done:
            print("round over drawing new hand")
            input()
            NewGame.new_round()
