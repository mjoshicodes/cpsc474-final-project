import time
import sys
import random
import chopsticks_strategy as chopsticks_QL

import chopsticks_qfl

if __name__ == "__main__":
    limit = 9
    n = 250000
    model = chopsticks_QL.ChopsticksStrategy()
    start = time.time()
    policy = chopsticks_qfl.q_learn(model, limit)
    t = time.time() - start

    #################################################################################
    #   Q-LEARNING VS. RANDOM AGENT

    print ("TEST 1: Q-Learning against a Random Agent")
    
    # print("We are using Q-learning to play Chopsticks against a Random Strategy. Here is my winning percentage over", n, "games:", model.simulate(policy, n))

    #################################################################################
    #   Q-LEARNING VS. GREEDY AGENT

    print ("TEST 2: Q-Learning against a Greedy Agent")

    test_limit = 10
    t = time.time()
    model.simulate_greedy(policy, n)
    # while t < test_limit:
    #     val, n = model.simulate_greedy(policy, n)
    # print("val", val)
    # print("Running against a greedy strategy, which our optimal solution, and therefore will run indefintely")