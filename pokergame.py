#Game functions
#test
import random
import math
from agents import Player

SUITS = ["Hearts", "Diamonds", "Clubs", "Spades"]
RANKS = list(range(1, 14))

def makeDeck():
    deck = []

    for suit in SUITS:
        for rank in RANKS:
            deck.append((rank, suit))

    random.shuffle(deck)
    return deck

class Game:
    def __init__(self):
        self.deck = makeDeck()
        self.player1 = Player("Human", 1000)
        self.player2 = Player("Bot", 1000)
        self.flop_cards = []
        self.pot = 0

    def playerPreFlopHand(self):
        # gives player classes created by game preflop cards
        self.player1.receive_card(self.deck.pop())
        self.player1.receive_card(self.deck.pop())
    
        self.player2.receive_card(self.deck.pop())
        self.player2.receive_card(self.deck.pop())

    def flop(self):
        # draws 3 cards for the flop
        self.flop_cards.append(self.deck.pop())
        self.flop_cards.append(self.deck.pop())
        self.flop_cards.append(self.deck.pop())

    def fullHand(self, player):
        # gets cards in player hand and community flop cards
        full_hand = player.hand + self.flop_cards
        return full_hand

    def evaluateHand(self, full_hand):
        
        #checks cards for hand type and returns number rank 1 greatest, 10 weakest
        def isPair(full_hand):
            ranks = []

            for card in full_hand:
                ranks.append(card[0])

            for rank in ranks:
                if ranks.count(rank) == 2:
                    return True

            return False
        
        def isTwoPair(full_hand):
            ranks = []

            for card in full_hand:
                ranks.append(card[0])

            pair_count = 0

            for rank in set(ranks):
                if ranks.count(rank) == 2:
                    pair_count += 1

            return pair_count == 2
        
        def isThreeOfAKind(full_hand):
            ranks = []

            for card in full_hand:
                ranks.append(card[0])

            for rank in ranks:
                if ranks.count(rank) == 3:
                    return True
                
            return False
        
        def isFourOfAKind(full_hand):
            ranks = []

            for card in full_hand:
                ranks.append(card[0])

            for rank in ranks:
                if ranks.count(rank) == 4:
                    return True
            return False
        
        def isStraight(full_hand):
            ranks = []

            for card in full_hand:
                ranks.append(card[0])

            ranks.sort()

            if ranks == [1, 10, 11, 12, 13]:
                return True

            if len(set(ranks)) != 5:
                return False
            for i in range(4):
                if ranks[i + 1] != ranks[i] + 1:
                    return False            
            return True

        def isFlush(full_hand):
            suits = []

            for card in full_hand:
                suits.append(card[1])

            return len(set(suits)) == 1
        
        def isRoyalFlush(full_hand):
             if isFlush(full_hand):
                 ranks = []

                 for card in full_hand:
                    ranks.append(card[0])

                 ranks.sort()
                 if ranks == [1,10,11,12,13]:
                     return True
                 
             return False
        
        def isStraightFlush(full_hand):
            if isFlush(full_hand) and isStraight(full_hand):
                return True
            return False
        
        def isFullHouse(full_hand):
            if isThreeOfAKind(full_hand) and isPair(full_hand):
                return True
            return False
        
        if isRoyalFlush(full_hand):
            return 1
        elif isStraightFlush(full_hand):
            return 2
        elif isFourOfAKind(full_hand):
            return 3
        elif isFullHouse(full_hand):
            return 4
        elif isFlush(full_hand):
            return 5
        elif isStraight(full_hand):
            return 6
        elif isThreeOfAKind(full_hand):
            return 7
        elif isTwoPair(full_hand):
            return 8
        elif isPair(full_hand):
            return 9
        else:
            return 10

