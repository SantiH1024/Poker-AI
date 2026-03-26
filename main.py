# start game

from pokergame import Game

def main():
    print("Starting Poker Game...")
    poker_game = Game()

    for i in range(5):
        poker_game.resetHand()
        poker_game.play()
        
        user_choice = input("\nPress Enter for the next hand, or type 'q' and press Enter to quit: ")
    
        if user_choice.lower() == 'q':
            print("\nExiting...")
            break

if __name__ == "__main__":
    main()