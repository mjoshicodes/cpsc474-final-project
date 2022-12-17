import random
from abc import ABC, abstractmethod
from itertools import combinations, product
import scoring

class ChopsticksPolicy(ABC):
    def __init__(self, game):
        self._game = game


    @abstractmethod
    def split(self, hand, scores, am_current_player):
        pass


    @abstractmethod
    def attack(self, cards, history, scores, am_current_player):
        pass


    def divide(self, cards, history, scores, am_current_player):
        pass

class SplitPolicy(ABC):
    def __init__(self, game):
        self._game = game


    @abstractmethod
    def split(self, hand, scores, am_current_player):
        pass


class AttackPolicy(ABC):
    def __init__(self, game):
        self._game = game


    @abstractmethod
    def attack(self, cards, history, scores, am_current_player):
        pass


class DividePolicy(ABC):
    def __init__(self, game):
        self._game = game


    @abstractmethod
    def divide(self, hand, scores, am_current_player):
        pass

class CompositePolicy(ChopsticksPolicy):

    def __init__(self, game, splitter, attacker, divider):
        super().__init__(game)
        self._splitter = splitter
        self._attacker = attacker
        self._divider = divider


    def split(self, hand, scores, am_current_player):
        return self._splitter.split(hand, scores, am_current_player)

    def attack(self, cards, history, scores, am_current_player):
        return self._attacker.attack(cards, history, scores, am_current_player)

    def divide(self, cards, history, scores, am_current_player):
        return self._divider.divide(cards, history, scores, am_current_player)

class RandomSplitter(SplitPolicy):
    def __init__(self, game):
        super().__init__(game)


    def split(self, left_hand, right_hand):
        possible_choices = []
        if left_hand > 0 and right_hand > 0:
            if right_hand < 4:
                possible_choices.append((left_hand - 1, right_hand + 1))
            else:
                possible_choices.append((left_hand + 1, right_hand - 1))

        return random.choice(possible_choices)


class RandomAttacker(AttackPolicy):
    def __init__(self, game):
        super().__init__(game)


    def attack(self, left_hand, right_hand, opponent_left_hand, opponent_right_hand):
        possible_attacks = [left_hand, right_hand]
        hands_available_for_attack = [1 if opponent_left_hand != 0 else None, 2 if opponent_right_hand != 0 else None]
        attack_combinations = list(product(possible_attacks, hands_available_for_attack))
        return random.choice(attack_combinations)


class RandomDivider(DividePolicy):
    def __init__(self, game):
        super().__init__(game)


    def divide(self, left_hand, right_hand):
        my_hand_sum = left_hand + right_hand
        possible_hand_values = range(0, my_hand_sum + 1)
        divide_combinations = [combo for combo in combinations(possible_hand_values, 2) if sum(combo) == my_hand_sum]
        return random.choice(divide_combinations)

class GreedySplit(SplitPolicy):
    def __init__(self, game):
        super().__init__(game)


    def split(self, hand, scores, am_current_player):
        pass

class GreedyAttacker(AttackPolicy):
    def __init__(self, game):
        super().__init__(game)


    def attack(self):
        attack_value, attacked_hand_idx, reward = scoring.greedy_attack(self._game.p1, self._game.p2)
        return attack_value, attacked_hand_idx

class GreedyDivider(DividePolicy):
    def __init__(self, game):
        super().__init__(game)


    def divide(self):
        pass
