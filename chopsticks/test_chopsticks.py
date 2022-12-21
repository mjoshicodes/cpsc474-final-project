import sys
import time
import sys
import random
import chopsticks_strategy as chopsticks_QL

import chopsticks_qfl

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
    submission = CompositePolicy(game, GreedySplitter(game), GreedyAttacker(game), GreedyDivider(game))

    results = evaluate_policies(game, benchmark, submission, games)
    print(f"Playing chopsticks with {games} games")
    print(f"P1: Random Agent won {results[0]} percent of games")
    print(f"P2: Greedy Agent won {results[1]} percent of games")
    print()
    #################################################################################


    #################################################################################
    # RANDOM VS RULE BASED HERE
    game = Game()
    # benchmark = CompositePolicy(game, RulesSplitter(game), RulesAttacker(game), RulesDivider(game))

    benchmark = CompositePolicy(game, RandomSplitter(game), RandomAttacker(game), RandomDivider(game))
    submission = CompositePolicy(game, RulesSplitter(game), RulesAttacker(game), RulesDivider(game))

    results = evaluate_policies(game, benchmark, submission, games)
    print(f"Playing chopsticks with {games} games")
    print(f"P1: Random Agent won {results[0]} percent of games")
    print(f"P2: Rules Based Agent won {results[1]} percent of games")
    print()
    #################################################################################


    #################################################################################
    # RULES BASED VS GREEDY AGENT HERE
    game = Game()
    benchmark = CompositePolicy(game, GreedySplitter(game), GreedyAttacker(game),GreedyDivider(game))
    submission = CompositePolicy(game, RulesSplitter(game), RulesAttacker(game), RulesDivider(game))

    results = evaluate_policies(game, benchmark, submission, games)
    print(f"Playing chopsticks with {games} games")
    print(f"P1: Greedy Agent won {results[0]} percent of games")
    print(f"P2: Rules Based Agent won {results[1]} percent of games")
    print()
    #################################################################################


    #################################################################################
    # MCTS VS GREEDY AGENT HERE
    #################################################################################


    #################################################################################
    # Q-LEARN VS GREEDY AGENT HERE
    #################################################################################



    limit = 9
    n = 250000
    model = chopsticks_QL.ChopsticksStrategy()
    start = time.time()
    policy = chopsticks_qfl.q_learn(model, limit)
    t = time.time() - start

    #################################################################################
    #   Q-LEARNING VS. RANDOM AGENT
    #################################################################################

    print ("TEST 1: Q-Learning against a Random Agent")
    
    print("We are using Q-learning to play Chopsticks against a Random Strategy. Here is my winning percentage over", n, "games:", model.simulate(policy, n))

    #################################################################################
    #   Q-LEARNING VS. GREEDY AGENT
    #################################################################################

    print ("TEST 2: Q-Learning against a Greedy Agent")

    test_limit = 10
    t = time.time()
    while t < test_limit:
        val, n = model.simulate_greedy(policy, n)
    print("Running against a greedy strategy, which our optimal solution, and therefore will run indefintely")