# random player and eventually ai player

import random

SUITS = ["Hearts", "Diamonds", "Clubs", "Spades"]
RANKS = list(range(1, 14))

class Player:
    def __init__(self, name, starting_chips):
        self.name = name
        self.stack = starting_chips
        self.hand = []
        self.current_bet = 0
        self.is_active = True

    def receive_card(self, card):
        # takes a card and holds it
        self.hand.append(card)

    def reset_hand(self):
        # resets the player hand and bets once folded
        self.hand = []
        self.current_bet = 0
        self.is_active = True

    def place_bet(self, amount):
        # moves chips from player stack to pot, this will have to be in game class
        self.stack -= amount
        self.current_bet += amount

    def take_action(self, game_state):
        # make a random move, could be changed to allow someone to make the decision manually
        valid_moves = ["check", "fold", "call", "raise"]
        return random.choice(valid_moves)
    
# inherits reused player functions
class MonteCarloAgent(Player):
    def __init__(self, name, starting_chips, simulations = 50, raise_thresh=0.60, call_thresh=0.35):
        self.name = name
        self.stack = starting_chips
        self.hand = []
        self.current_bet = 0
        self.is_active = True
        self.simulations = simulations 
        self.raise_thresh = raise_thresh
        self.call_thresh = call_thresh

    # here is the brain of the agent
    def take_action(self, game_state):
        
        my_cards = self.hand
        board_cards = game_state.flop_cards
        known_cards = my_cards + board_cards
        
        # create simulation deck without cards agent can see
        fake_deck = []
        for suit in SUITS:
            for rank in RANKS:
                card = (rank, suit)
                if card not in known_cards:
                    fake_deck.append(card)

        # win counter           
        wins = 0
        
        for _ in range(self.simulations):
            random.shuffle(fake_deck)
            
            opp_cards = [fake_deck[0], fake_deck[1]]
            
            # deals cards to table if pre flop and doesnt if flop
            cards_needed_for_board = 3 - len(board_cards)
            simulated_board = board_cards + fake_deck[2 : 2 + cards_needed_for_board]
            
            my_full_hand = my_cards + simulated_board
            opp_full_hand = opp_cards + simulated_board
            
            # using the full hands, we immediately evaluate and showdown, 
            # where the winner gets added to the counter, and tie counts as half a point
            my_val = game_state.evaluateHand(my_full_hand)
            opp_val = game_state.evaluateHand(opp_full_hand)
            
            if my_val[0] < opp_val[0]:
                wins += 1
            elif my_val[0] == opp_val[0]:
                if my_val[1:] > opp_val[1:]:
                    wins += 1
                elif my_val[1:] == opp_val[1:]:
                    wins += 0.5 

        # now check the probability of a win based on number of simulations, 
        # and play based on win rate           
        win_rate = wins / self.simulations
        print(f"[{self.name}] Simulated Win Probability: {win_rate*100:.1f}%")
        
        chips_needed = game_state.current_bet - self.current_bet
        
        if win_rate > self.raise_thresh:
            return "raise"
        elif win_rate > self.call_thresh:
            if chips_needed == 0:
                return "check"
            return "call"
        else:
            if chips_needed == 0:
                return "check" 
            return "fold"