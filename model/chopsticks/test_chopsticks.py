import sys

from policy import CompositePolicy
from chopsticks import Game


if __name__ == "__main__":
    games = 2
    if len(sys.argv) > 1:
        games = int(sys.argv[1])

    game = Game()
    game.play()
    # benchmark = CompositePolicy(game, GreedyThrower(game), GreedyPegger(game))
    # submission = MyPolicy(game)

    # results = evaluate_policies(game, submission, benchmark, games)
    # print("NET:", results[0])
    # print(results)

