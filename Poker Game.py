#Game functions
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



def main():
    deck = makeDeck()
    hand = playerPreFlopHand(deck)
    print(hand)

if __name__ == "__main__":
    main()
