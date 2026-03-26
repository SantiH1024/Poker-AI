#Game functions
#test
import random
from agents import Player

SUITS = ["Hearts", "Diamonds", "Clubs", "Spades"]
RANKS = list(range(1, 14))


def makeDeck():
    #generates deck array with 52 cards containing rank and suit
    deck = []

    for suit in SUITS:
        for rank in RANKS:
            deck.append((rank, suit))

    random.shuffle(deck)
    return deck


class Game:
    def __init__(self):
        #game variables
        self.deck = makeDeck()

        self.player1 = Player("Human", 1000)
        self.player2 = Player("Bot", 1000)
        self.players = [self.player1, self.player2]

        self.flop_cards = []
        self.pot = 0

        self.current_player = 0
        self.current_bet = 0
        self.hand_over = False
        self.winner = None
        self.checks_in_row = 0
        self.phase_over = False

    def resetHand(self):
        #resets pots, bets, actions, hands, and shuffles deck
        self.deck = makeDeck()
        self.flop_cards = []
        self.pot = 0

        self.current_player = 0
        self.current_bet = 0
        self.hand_over = False
        self.winner = None
        self.checks_in_row = 0

        self.player1.reset_hand()
        self.player2.reset_hand()

    def playerPreFlopHand(self):
        #creates player's pre-flop hands from deck array
        self.player1.reset_hand()
        self.player2.reset_hand()

        self.player1.receive_card(self.deck.pop())
        self.player1.receive_card(self.deck.pop())

        self.player2.receive_card(self.deck.pop())
        self.player2.receive_card(self.deck.pop())

    def flop(self):
        #creates flop hand from deck array
        self.flop_cards = []

        self.flop_cards.append(self.deck.pop())
        self.flop_cards.append(self.deck.pop())
        self.flop_cards.append(self.deck.pop())

    def fullHand(self, player):
        #combines player pre-flop hand with flop to create full hand
        return player.hand + self.flop_cards
    
    def awardPot(self):
        #awards pot to player that wins
        if self.winner == 1:
            self.player1.stack += self.pot

        elif self.winner == 2:
            self.player2.stack += self.pot
        #in case of a tie splits pot and player 1 gets extra chip if applicable
        elif self.winner == 0:
            split_amount = self.pot // 2
            extra_chip = self.pot % 2

            self.player1.stack += split_amount
            self.player2.stack += split_amount

            if extra_chip == 1:
                self.player1.stack += 1

        self.pot = 0

    def action(self, choice, raise_amount=0):
        #checks player choice and adjusts pot
        if self.hand_over:
            return False

        p = self.current_player
        opp = 1 - p
        player = self.players[p]

        if choice == "fold":
            player.is_active = False
            self.hand_over = True
            return True

        elif choice == "check":
            if player.current_bet != self.current_bet:
                return False

            self.checks_in_row += 1

            if self.checks_in_row == 2:
                self.phase_over = True
                return True

            self.current_player = opp
            return True

        elif choice == "call":
            chips_needed = self.current_bet - player.current_bet

            if chips_needed <= 0 or chips_needed > player.stack:
                return False

            player.place_bet(chips_needed)
            self.pot += chips_needed

            self.phase_over = True
            return True


        elif choice == "raise":
            if raise_amount <= 0:
                return False

            chips_needed = (self.current_bet - player.current_bet) + raise_amount

            if chips_needed > player.stack:
                return False # Illegal move

            player.place_bet(chips_needed)
            self.pot += chips_needed
            self.current_bet = player.current_bet
            
            # Reset checks since a bet was made
            self.checks_in_row = 0 
            self.current_player = opp
            return True
        
        return False
    
    def evaluateHand(self, full_hand):
        
        #checks cards for hand type and returns number rank, 1 greatest, 10 weakest
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

            if ranks == [1, 2, 3, 4, 5]:
                return True

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
        #evaluates player hands and returns 1 for player1 win, 2 for player2 win, and 0 for tie
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
            

    def betting_round(self):
        # Reset the switch at the start of every betting round
        self.phase_over = False
        
        # Keep asking for moves until the phase finishes OR someone folds
        while not self.phase_over and not self.hand_over:
            
            # Figure out whose turn it is
            active_player = self.players[self.current_player]
            
            # Ask the player for their move
            choice = active_player.take_action(None)
            
            # Feed choice into action function
            if choice == "raise":
                # hard coding a raise amount for now temporarily
                success = self.action(choice, 50) 
            else:
                success = self.action(choice)
                
            # Print choice
            if success:
                print(f"{active_player.name} chose to {choice}!")
            else:
                print(f"Illegal move, please input move again")
                pass