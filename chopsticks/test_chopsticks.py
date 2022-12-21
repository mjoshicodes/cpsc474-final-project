import sys
import time
import sys
import random
import chopsticks_strategy as chopsticks_QL

import chopsticks_qfl

from policy import CompositePolicy, RandomSplitter, RandomAttacker, RandomDivider, GreedyAttacker, GreedySplitter, GreedyDivider, RulesAttacker, RulesSplitter, RulesDivider
from chopsticks import Game, evaluate_policies

if __name__ == "__main__":
    #################################################################################
    # GREEDY VS RANDOM AGENT HERE
    game = Game()
    benchmark = CompositePolicy(game, RandomSplitter(game), RandomAttacker(game), RandomDivider(game))
    submission = CompositePolicy(game, GreedySplitter(game), GreedyAttacker(game), GreedyDivider(game))

    games = 10000
    results = evaluate_policies(game, benchmark, submission, games)
    print("TEST 1: Greedy against a Random Agent")
    print(f"We are using a Greedy agent to play Chopsticks against a Random agent. Here's our winning ratio over {games} games: {results[1]}")
    print()
    #################################################################################


    #################################################################################
    # RULES BASED VS RANDOM HERE
    game = Game()

    benchmark = CompositePolicy(game, RandomSplitter(game), RandomAttacker(game), RandomDivider(game))
    submission = CompositePolicy(game, RulesSplitter(game), RulesAttacker(game), RulesDivider(game))

    games = 10000
    results = evaluate_policies(game, benchmark, submission, games)
    print("TEST 2: Rules-based against a Random Agent")
    print(f"We are using a Rules-based agent to play Chopsticks against a Random agent. Here's our winning ratio over {games} games: {results[1]}")
    print()
    #################################################################################


    #################################################################################
    # RULES BASED VS GREEDY AGENT HERE
    game = Game()
    benchmark = CompositePolicy(game, GreedySplitter(game), GreedyAttacker(game),GreedyDivider(game))
    submission = CompositePolicy(game, RulesSplitter(game), RulesAttacker(game), RulesDivider(game))

    games = 10000
    results = evaluate_policies(game, benchmark, submission, games)
    print("TEST 3: Rules-based against a Greedy Agent")
    print(f"We are using a Rules-based agent to play Chopsticks against a Greedy agent. Here's our winning ratio over {games} games: {results[1]}")
    print()
    #################################################################################


    #################################################################################
    # MCTS VS RANDOM AGENT HERE




    #################################################################################


    #################################################################################
    # MCTS VS GREEDY AGENT HERE





    #################################################################################


    #################################################################################
    # Q-LEARN VS RANDOM AGENT HERE
    limit = 9
    games = 250000
    model = chopsticks_QL.ChopsticksStrategy()
    start = time.time()
    policy = chopsticks_qfl.q_learn(model, limit)
    t = time.time() - start

    result = model.simulate(policy, games)
    print("TEST 4: Q-Learning against a Random Agent")
    print(f"We are using Q-learning to play Chopsticks against a Random Strategy. Here is my winning percentage over {games} games: {result}")
    print()
    #################################################################################


    #################################################################################
    # Q-LEARNING VS. GREEDY AGENT
    limit = 9
    n = 250000
    model = chopsticks_QL.ChopsticksStrategy()
    start = time.time()
    policy = chopsticks_qfl.q_learn(model, limit)
    t = time.time() - start


    test_limit = 10
    t = time.time()
    while t < test_limit:
        val, n = model.simulate_greedy(policy, n)

    print("TEST 5: Q-Learning against a Greedy Agent")
    print("Q-learning running against a greedy strategy, which is an optimal solution, will therefore run indefintely")
    print()
    #################################################################################
