# Poker-AI

This project uses a simplified version of poker in whic two players(a random bot and an AI agent) play against each other using basic poker rules and game flow. 

## File Structure

- `main.py`  
  Starts the game and runs hands in a loop until the user quits.

- `pokergame.py`  
  Contains the main `Game` class and most of the game logic, including:
  - creating and shuffling the deck
  - dealing cards
  - handling betting actions
  - evaluating hands
  - determining the winner
  - awarding the pot

- `agents.py`  
  Contains the player classes:
  - `Player` makes random moves
  - `MonteCarloAgent` is the AI player

- `agentTesting.py`  
  Runs many hands automatically to test the AI against the random bot and measure win rate.

- `gameFuncTesting.py`  
  Contains simple tests for game functions such as dealing, betting, hand evaluation, and full game flow.

## How the Game Works

Each player starts the round with 5000 chips used for betting. Each player will receive their two pre-flop cards followed by an initial round of betting. If neither player folds, the game continous onto the flop stage and the players will do one last round of betting. Finally, if both players make it to showdown their cards are evaluated and winner takes the pot. User can keep spectatng games until one of the players has no chips left.

## AI Component

The AI uses a Monte Carlo approach. It looks at its current cards and the board, then simulates many possible opponent hands and outcomes. Based on its estimated win probability, it decides whether to raise, call, check, or fold.

## Notes

This is still a simplified poker project and does not include every rule from full Texas Hold’em. The main goal of the project is to build the game flow, hand evaluation system, and a basic AI decision-making model.