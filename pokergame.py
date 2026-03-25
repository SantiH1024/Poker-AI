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
        
        #checks cards for hand type and returns number rank, 10 greatest, 1 weakest
        #if there is a hand type tie, checks which hand has higher made hand or kicker
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
        
        def convertRanks(full_hand):
            ranks = []

            for card in full_hand:
                rank = card[0]

                if rank == 1:
                    ranks.append(14)
                else:
                    ranks.append(rank)

            return ranks


        def getHighCardValue(full_hand):
            ranks = convertRanks(full_hand)
            ranks.sort(reverse=True)
            return (10, ranks[0], ranks[1], ranks[2], ranks[3], ranks[4])


        def getPairValue(full_hand):
            ranks = convertRanks(full_hand)

            pair_rank = None
            for rank in set(ranks):
                if ranks.count(rank) == 2:
                    pair_rank = rank
                    break

            kickers = []
            for rank in ranks:
                if rank != pair_rank:
                    kickers.append(rank)

            kickers.sort(reverse=True)

            return (9, pair_rank, kickers[0], kickers[1], kickers[2])


        def getTwoPairValue(full_hand):
            ranks = convertRanks(full_hand)

            pair_ranks = []
            kicker = None

            for rank in set(ranks):
                if ranks.count(rank) == 2:
                    pair_ranks.append(rank)
                elif ranks.count(rank) == 1:
                    kicker = rank

            pair_ranks.sort(reverse=True)

            return (8, pair_ranks[0], pair_ranks[1], kicker)


        def getThreeOfAKindValue(full_hand):
            ranks = convertRanks(full_hand)

            trip_rank = None
            for rank in set(ranks):
                if ranks.count(rank) == 3:
                    trip_rank = rank
                    break

            kickers = []
            for rank in ranks:
                if rank != trip_rank:
                    kickers.append(rank)

            kickers.sort(reverse=True)

            return (7, trip_rank, kickers[0], kickers[1])


        def getStraightValue(full_hand):
            ranks = convertRanks(full_hand)
            ranks = sorted(set(ranks))

            if ranks == [2, 3, 4, 5, 14]:
                return (6, 5)

            return (6, ranks[-1])


        def getFlushValue(full_hand):
            ranks = convertRanks(full_hand)
            ranks.sort(reverse=True)
            return (5, ranks[0], ranks[1], ranks[2], ranks[3], ranks[4])


        def getFullHouseValue(full_hand):
            ranks = convertRanks(full_hand)

            trip_rank = None
            pair_rank = None

            for rank in set(ranks):
                if ranks.count(rank) == 3:
                    trip_rank = rank
                elif ranks.count(rank) == 2:
                    pair_rank = rank

            return (4, trip_rank, pair_rank)


        def getFourOfAKindValue(full_hand):
            ranks = convertRanks(full_hand)

            four_rank = None
            kicker = None

            for rank in set(ranks):
                if ranks.count(rank) == 4:
                    four_rank = rank
                elif ranks.count(rank) == 1:
                    kicker = rank

            return (3, four_rank, kicker)


        def getStraightFlushValue(full_hand):
            ranks = convertRanks(full_hand)
            ranks = sorted(set(ranks))

            if ranks == [2, 3, 4, 5, 14]:
                return (2, 5)

            return (2, ranks[-1])


        def getRoyalFlushValue(full_hand):
            return (1,)
        
        if isRoyalFlush(full_hand):
            return getRoyalFlushValue(full_hand)
        elif isStraightFlush(full_hand):
            return getStraightFlushValue(full_hand)
        elif isFourOfAKind(full_hand):
            return getFourOfAKindValue(full_hand)
        elif isFullHouse(full_hand):
            return getFullHouseValue(full_hand)
        elif isFlush(full_hand):
            return getFlushValue(full_hand)
        elif isStraight(full_hand):
            return getStraightValue(full_hand)
        elif isThreeOfAKind(full_hand):
            return getThreeOfAKindValue(full_hand)
        elif isTwoPair(full_hand):
            return getTwoPairValue(full_hand)
        elif isPair(full_hand):
            return getPairValue(full_hand)
        else:
            return getHighCardValue(full_hand)

    def showDown(self, full_hand1, full_hand2):
        player1_value = self.evaluateHand(full_hand1)
        player2_value = self.evaluateHand(full_hand2)

        player1_rank = player1_value[0]
        player2_rank = player2_value[0]

        if player1_rank < player2_rank:
            return 1
        elif player2_rank < player1_rank:
            return 2
        else:
            if player1_value[1:] > player2_value[1:]:
                return 1
            elif player2_value[1:] > player1_value[1:]:
                return 2
            else:
                return 0
