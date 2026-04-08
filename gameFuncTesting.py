#game function testing

from pokergame import Game

game = Game()

game.resetHand()
game.playerPreFlopHand()

print("Player 1 hand:", game.player1.hand)
print("Player 2 hand:", game.player2.hand)

game.flop()
print("Flop:", game.flop_cards)

print("Pot before action:", game.pot)
print("Player 1 stack before action:", game.player1.stack)
print("Player 2 stack before action:", game.player2.stack)

print("\nPlayer 1 raises 50")
game.action("raise", 50)

print("Pot:", game.pot)
print("Current bet:", game.current_bet)
print("Player 1 stack:", game.player1.stack)
print("Player 1 current bet:", game.player1.current_bet)
print("Current player:", game.current_player)

print("\nPlayer 2 calls")
game.action("call")

print("Pot after call:", game.pot)
print("Hand over:", game.hand_over)
print("Winner:", game.winner)
print("Player 1 stack:", game.player1.stack)
print("Player 2 stack:", game.player2.stack)