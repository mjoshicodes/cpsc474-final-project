import sys

from policy import CompositePolicy, RandomSplitter, RandomAttacker, RandomDivider, GreedyAttacker
from chopsticks import Game, evaluate_policies

if __name__ == "__main__":
    games = 2
    if len(sys.argv) > 1:
        games = int(sys.argv[1])

    game = Game()
    benchmark = CompositePolicy(game, RandomSplitter(game), RandomAttacker(game), RandomDivider(game))
    submission = CompositePolicy(game, RandomSplitter(game), GreedyAttacker(game), RandomDivider(game))

    results = evaluate_policies(game, benchmark, submission, games)
    print("NET:", results[0])
    print(results)

