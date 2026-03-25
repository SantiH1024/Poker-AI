#Game functions
#test
import random
import math

SUITS = ["Hearts", "Diamonds", "Clubs", "Spades"]
RANKS = list(range(1, 14))

def makeDeck():
    deck = []

    for suit in SUITS:
        for rank in RANKS:
            deck.append((rank, suit))

    random.shuffle(deck)
    return deck

def playerPreFlopHand(deck):
    card1 = deck.pop()
    card2 = deck.pop()
    player_pre_flop_hand = [card1,card2]
    return player_pre_flop_hand

def flop(deck):
    card1 = deck.pop()
    card2 = deck.pop()
    card3 = deck.pop()
    flop =  [card1,card2,card3]
    return flop

def fullHand(player_pre_flop_hand,flop):
    full_hand = player_pre_flop_hand + flop
    return full_hand

def evaluateHand(full_hand):

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
            if rank.count(rank) == 4:
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



def main():
    deck = makeDeck()
    hand = playerPreFlopHand(deck)
    print(hand)

if __name__ == "__main__":
    main()
