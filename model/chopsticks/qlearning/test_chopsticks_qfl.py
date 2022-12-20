import time
import sys
import random
import chopsticks_strategy as chopsticks

import chopsticks_qfl

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("USAGE: {python3 | pypy3}", sys.argv[0], "learning-time num-games")
        sys.exit(1)

    try:
        limit = float(sys.argv[1])
        n = int(sys.argv[2])
    except:
        print("USAGE: {python3 | pypy3}", sys.argv[0], "learning-time num-games")
        sys.exit(1)

    model = chopsticks.ChopsticksStrategy()
    start = time.time()
    policy = chopsticks_qfl.q_learn(model, limit)
    t = time.time() - start
    # if t > limit:
    #     print("WARNING: Q-learning ran for", t, "seconds; allowed", limit)

    print ("TEST 1: Q-Learning against a Random Agent")
    
    print("We are using Q-learning to play Chopsticks against a Random Strategy. Here is my winning percentage over ", n, "games:", model.simulate(policy, n))

    print ("TEST 2: Q-Learning against a Greedy Agent")

    print("We are using Q-learning to play Chopsticks against a Greedy Strategy. Here is my winning percentage over ", n, "games:", model.simulate_greedy(policy, n))
