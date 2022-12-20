import sys

from policy import CompositePolicy, RandomSplitter, RandomAttacker, RandomDivider, GreedyAttacker, GreedySplitter, GreedyDivider, RulesAttacker, RulesSplitter, RulesDivider
from chopsticks import Game, evaluate_policies

if __name__ == "__main__":
    games = 2
    if len(sys.argv) > 1:
        games = int(sys.argv[1])


    #################################################################################
    # GREEDY VS RANDOM AGENT HERE
    game = Game()
    benchmark = CompositePolicy(game, RandomSplitter(game), RandomAttacker(game), RandomDivider(game))
    # benchmark = CompositePolicy(game, GreedySplitter(game), GreedyAttacker(game), GreedyDivider(game))
    submission = CompositePolicy(game, GreedySplitter(game), GreedyAttacker(game), GreedyDivider(game))

    results = evaluate_policies(game, benchmark, submission, games)
    print(f"Playing chopsticks with {games} games")
    print(f"P1: Random Agent won {results[0]} percent of games")
    print(f"P2: Greedy Agent won {results[1]} percent of games")
    print()
    #################################################################################


    #################################################################################
    # RULES BASED VS GREEDY AGENT HERE
    game = Game()
    benchmark = CompositePolicy(game, RandomSplitter(game), RandomAttacker(game), RandomDivider(game))
    submission = CompositePolicy(game, RulesSplitter(game), RulesAttacker(game), RulesDivider(game))

    results = evaluate_policies(game, benchmark, submission, games)
    print(f"Playing chopsticks with {games} games")
    print(f"P1: Random Agent won {results[0]} percent of games")
    print(f"P2: Rules Based Agent won {results[1]} percent of games")
    print()
    #################################################################################


    #################################################################################
    # MCTS VS GREEDY AGENT HERE
    game = Game()
    #################################################################################


    #################################################################################
    # Q-LEARN VS GREEDY AGENT HERE
    #################################################################################