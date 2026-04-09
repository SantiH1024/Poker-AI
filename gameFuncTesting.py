from pokergame import Game, makeDeck
from agents import Player


# Simple fake player so we can control actions in betting_round() and play()
class ScriptedPlayer(Player):
    def __init__(self, name, starting_chips, moves):
        super().__init__(name, starting_chips)
        self.moves = moves[:]

    def take_action(self, game_state):
        return self.moves.pop(0)


# Runs one test and prints PASSED or FAILED
def run_test(name, test_func):
    try:
        test_func()
        print(f"{name}: PASSED")
    except AssertionError as e:
        print(f"{name}: FAILED -> {e}")


# Tests that makeDeck creates a full 52-card deck with no duplicates
def test_make_deck():
    deck = makeDeck()
    assert len(deck) == 52, "Deck should have 52 cards"
    assert len(set(deck)) == 52, "Deck should have 52 unique cards"


# Tests that resetHand clears hand state, pot, flop, and winner info
def test_reset_hand():
    game = Game()

    game.pot = 200
    game.current_bet = 50
    game.hand_over = True
    game.winner = 1
    game.flop_cards = [(1, "Hearts")]
    game.player1.hand = [(2, "Clubs")]
    game.player2.hand = [(3, "Spades")]

    game.resetHand()

    assert game.pot == 0
    assert game.current_bet == 0
    assert game.hand_over == False
    assert game.winner is None
    assert game.flop_cards == []
    assert game.player1.hand == []
    assert game.player2.hand == []


# Tests dealing 2 hole cards each, 3 flop cards, and making a full 5-card hand
def test_dealing_and_full_hand():
    game = Game()
    game.resetHand()
    game.playerPreFlopHand()

    assert len(game.player1.hand) == 2
    assert len(game.player2.hand) == 2
    assert len(game.deck) == 48

    game.flop()
    assert len(game.flop_cards) == 3
    assert len(game.deck) == 45

    full_hand = game.fullHand(game.player1)
    assert len(full_hand) == 5


# Tests raise then call and checks pot, bets, stacks, and round ending
def test_raise_and_call():
    game = Game()

    ok1 = game.action("raise", 50)
    assert ok1 == True
    assert game.pot == 50
    assert game.current_bet == 50
    assert game.player1.current_bet == 50
    assert game.player1.stack == 950
    assert game.current_player == 1

    ok2 = game.action("call")
    assert ok2 == True
    assert game.pot == 100
    assert game.player2.current_bet == 50
    assert game.player2.stack == 950
    assert game.phase_over == True


# Tests check/check ending round, illegal check facing a bet, and fold ending hand
def test_check_fold_and_illegal_move():
    game = Game()

    ok1 = game.action("check")
    assert ok1 == True
    assert game.current_player == 1

    ok2 = game.action("check")
    assert ok2 == True
    assert game.phase_over == True

    game = Game()
    game.current_bet = 50
    bad_check = game.action("check")
    assert bad_check == False, "Check should be illegal if player has not matched bet"

    game = Game()
    fold_ok = game.action("fold")
    assert fold_ok == True
    assert game.hand_over == True
    assert game.player1.is_active == False


# Tests awarding full pot to winner and splitting odd-chip tie correctly
def test_award_pot():
    game = Game()
    game.pot = 100
    game.winner = 1
    game.awardPot()

    assert game.player1.stack == 1100
    assert game.player2.stack == 1000
    assert game.pot == 0

    game = Game()
    game.pot = 101
    game.winner = 0
    game.awardPot()

    assert game.player1.stack == 1051
    assert game.player2.stack == 1050
    assert game.pot == 0


# Tests evaluateHand on many different poker hand types
def test_evaluate_hand_types():
    game = Game()

    high_card = [(1, "Hearts"), (11, "Clubs"), (8, "Spades"), (5, "Diamonds"), (2, "Clubs")]
    pair = [(8, "Hearts"), (8, "Clubs"), (1, "Spades"), (13, "Diamonds"), (2, "Clubs")]
    two_pair = [(10, "Hearts"), (10, "Clubs"), (4, "Spades"), (4, "Diamonds"), (13, "Clubs")]
    three_kind = [(7, "Hearts"), (7, "Clubs"), (7, "Spades"), (13, "Diamonds"), (2, "Clubs")]
    straight = [(5, "Hearts"), (6, "Clubs"), (7, "Spades"), (8, "Diamonds"), (9, "Clubs")]
    flush = [(1, "Hearts"), (11, "Hearts"), (8, "Hearts"), (5, "Hearts"), (2, "Hearts")]
    full_house = [(6, "Hearts"), (6, "Clubs"), (6, "Spades"), (9, "Diamonds"), (9, "Clubs")]
    four_kind = [(3, "Hearts"), (3, "Clubs"), (3, "Spades"), (3, "Diamonds"), (13, "Clubs")]
    straight_flush = [(5, "Hearts"), (6, "Hearts"), (7, "Hearts"), (8, "Hearts"), (9, "Hearts")]
    royal_flush = [(1, "Hearts"), (10, "Hearts"), (11, "Hearts"), (12, "Hearts"), (13, "Hearts")]

    assert game.evaluateHand(high_card) == (10, 14, 11, 8, 5, 2)
    assert game.evaluateHand(pair) == (9, 8, 14, 13, 2)
    assert game.evaluateHand(two_pair) == (8, 10, 4, 13)
    assert game.evaluateHand(three_kind) == (7, 7, 13, 2)
    assert game.evaluateHand(straight) == (6, 9)
    assert game.evaluateHand(flush) == (5, 14, 11, 8, 5, 2)
    assert game.evaluateHand(full_house) == (4, 6, 9)
    assert game.evaluateHand(four_kind) == (3, 3, 13)
    assert game.evaluateHand(straight_flush) == (2, 9)
    assert game.evaluateHand(royal_flush) == (1,)


# Tests showdown winner using kicker/tiebreak logic
def test_showdown():
    game = Game()

    pair_hand_1 = [(8, "Hearts"), (8, "Clubs"), (1, "Spades"), (13, "Diamonds"), (2, "Clubs")]
    pair_hand_2 = [(8, "Diamonds"), (8, "Spades"), (12, "Hearts"), (11, "Clubs"), (2, "Hearts")]

    assert game.showDown(pair_hand_1, pair_hand_2) == 1


# Tests resetBettingRound resets betting values and swaps to first_player
def test_reset_betting_round():
    game = Game()

    game.current_bet = 75
    game.checks_in_row = 1
    game.phase_over = True
    game.player1.current_bet = 75
    game.player2.current_bet = 75
    game.first_player = 1

    game.resetBettingRound()

    assert game.current_bet == 0
    assert game.checks_in_row == 0
    assert game.phase_over == False
    assert game.player1.current_bet == 0
    assert game.player2.current_bet == 0
    assert game.current_player == 1


# Tests betting_round with scripted raise then call
def test_betting_round():
    game = Game()
    game.player1 = ScriptedPlayer("P1", 1000, ["raise"])
    game.player2 = ScriptedPlayer("P2", 1000, ["call"])
    game.players = [game.player1, game.player2]

    game.betting_round()

    assert game.pot == 100
    assert game.phase_over == True
    assert game.player1.current_bet == 50
    assert game.player2.current_bet == 50


# Tests full play() flow where game reaches showdown
def test_play_showdown():
    game = Game()
    game.player1 = ScriptedPlayer("P1", 1000, ["check", "check"])
    game.player2 = ScriptedPlayer("P2", 1000, ["check", "check"])
    game.players = [game.player1, game.player2]

    def fixed_preflop():
        game.player1.reset_hand()
        game.player2.reset_hand()
        game.player1.hand = [(1, "Hearts"), (13, "Spades")]
        game.player2.hand = [(9, "Clubs"), (9, "Diamonds")]

    def fixed_flop():
        game.flop_cards = [(1, "Clubs"), (7, "Hearts"), (2, "Spades")]

    game.playerPreFlopHand = fixed_preflop
    game.flop = fixed_flop

    game.play()

    assert game.winner == 1
    assert game.pot == 0


# Tests full play() flow where one player folds before showdown
def test_play_fold():
    game = Game()
    game.player1 = ScriptedPlayer("P1", 1000, ["raise"])
    game.player2 = ScriptedPlayer("P2", 1000, ["fold"])
    game.players = [game.player1, game.player2]

    game.play()

    assert game.winner == 1
    assert game.pot == 0


run_test("makeDeck", test_make_deck)
run_test("resetHand", test_reset_hand)
run_test("dealing + fullHand", test_dealing_and_full_hand)
run_test("raise + call", test_raise_and_call)
run_test("check/fold/illegal move", test_check_fold_and_illegal_move)
run_test("awardPot", test_award_pot)
run_test("evaluateHand types", test_evaluate_hand_types)
run_test("showDown", test_showdown)
run_test("resetBettingRound", test_reset_betting_round)
run_test("betting_round", test_betting_round)
run_test("play showdown", test_play_showdown)
run_test("play fold", test_play_fold)