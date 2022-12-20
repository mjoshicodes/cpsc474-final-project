from sys import argv
from mcts import mcts_policy
from argparse import ArgumentParser
from policy import CompositePolicy, RandomSplitter, RandomAttacker, RandomDivider, GreedyAttacker, GreedySplitter, GreedyDivider, RulesAttacker, RulesSplitter, RulesDivider
from chopsticks import Game, evaluate_policies, evaluate_mcts_policies

if __name__ == "__main__":
    parser = ArgumentParser(description="Test MCTS Agent")
    parser.add_argument('--games', dest='games', type=int, action="store", default=10, help='number of games to play (default=10')
    parser.add_argument('--time', dest='time', type=float, action="store", default=0.1, help='time for MCTS per move')
    args = parser.parse_args()

    #################################################################################
    # MCTS VS GREEDY AGENT HERE
    game = Game()
    benchmark = CompositePolicy(game, GreedySplitter(game), GreedyAttacker(game), GreedyDivider(game))
    submission = mcts_policy(args.time)

    results = evaluate_mcts_policies(game, lambda: submission, benchmark, args.games)
    print(f"Playing chopsticks with {args.games} games")
    print(f"P1: MCTS Agent won {results[0]} percent of games")
    print(f"P2: Greedy Agent won {results[1]} percent of games")
    print()
    #################################################################################

    #################################################################################
    # MCTS VS RANDOM AGENT HERE
    game = Game()
    benchmark = CompositePolicy(game, RandomSplitter(game), RandomAttacker(game), RandomDivider(game))
    submission = mcts_policy(args.time)

    results = evaluate_mcts_policies(game, lambda: submission, benchmark, args.games)
    print(f"Playing chopsticks with {args.games} games")
    print(f"P1: MCTS Agent won {results[0]} percent of games")
    print(f"P2: Random Agent won {results[1]} percent of games")
    print()
    #################################################################################