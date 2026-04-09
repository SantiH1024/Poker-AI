import time

from pokergame import Game

poker_game = Game()

# EDIT TESTING PARAMETERS HERE
# depth of agent simulation, number of hands, 
# agents aggressiveness (.85+.6 = super passive, .65+.4 = average, .4+.15 = super aggresive)
TEST_SIMULATIONS = 100
MAX_HANDS = 100
RAISE_THRESHOLD = 0.65
CALL_THRESHOLD = 0.4

poker_game.player1.simulations = TEST_SIMULATIONS 
poker_game.player1.raise_thresh = RAISE_THRESHOLD
poker_game.player1.call_thresh = CALL_THRESHOLD

start_time = time.time()

hands_played = 0
ai_wins = 0
random_wins = 0

for i in range(MAX_HANDS):

    poker_game.resetHand()
    poker_game.play()
    
    # record the data
    hands_played += 1
    if poker_game.winner == 1:
        ai_wins += 1
    elif poker_game.winner == 2:
        random_wins += 1
        
    # check if either player is out of chips and end early if true
    if poker_game.player1.stack <= 0 or poker_game.player2.stack <= 0:
        break

# calculate testing time
total_time = time.time() - start_time
time_per_hand = total_time / hands_played

# test report print statements
print(f"\nTest results for: \n{TEST_SIMULATIONS} Simulation Depth, \n{RAISE_THRESHOLD} Raise Threshold, \n{CALL_THRESHOLD} Call Threshold")
print(f"\nTotal Hands Played: {hands_played} out of {MAX_HANDS}")
print(f"Time Per Hand: {time_per_hand:.3f} seconds")
print(f"AI Win Rate:   {(ai_wins/hands_played)*100:.2f}%")
print(f"Random Bot Win Rate: {(random_wins/hands_played)*100:.2f}%")
print("FINAL CHIP STACKS")
print(f"{poker_game.player1.name}: {poker_game.player1.stack} chips")
print(f"{poker_game.player2.name}: {poker_game.player2.stack} chips")

chip_diff = poker_game.player1.stack - poker_game.player2.stack
if chip_diff > 0:
    print(f"\nAI won by a margin of {chip_diff} chips.")
else:
    print(f"\nAI lost by a margin of {abs(chip_diff)} chips.")
