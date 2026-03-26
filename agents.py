# random player and eventually ai player

import random
import math

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