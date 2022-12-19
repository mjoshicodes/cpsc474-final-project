import random
from abc import ABC, abstractmethod
from itertools import combinations, product, combinations_with_replacement
import scoring


class ChopsticksPolicy(ABC):
    def __init__(self, game):
        self._game = game

    @abstractmethod
    def split(self, left_hand, right_hand, opponent_left_hand, opponent_right_hand):
        pass

    @abstractmethod
    def attack(self, left_hand, right_hand, opponent_left_hand, opponent_right_hand):
        pass

    def divide(self, left_hand, right_hand, opponent_left_hand, opponent_right_hand):
        pass


class SplitPolicy(ABC):
    def __init__(self, game):
        self._game = game

    @abstractmethod
    def split(self, left_hand, right_hand, opponent_left_hand, opponent_right_hand):
        pass


class AttackPolicy(ABC):
    def __init__(self, game):
        self._game = game

    @abstractmethod
    def attack(self, left_hand, right_hand, opponent_left_hand, opponent_right_hand):
        pass


class DividePolicy(ABC):
    def __init__(self, game):
        self._game = game

    @abstractmethod
    def divide(self, left_hand, right_hand, opponent_left_hand, opponent_right_hand):
        pass


class CompositePolicy(ChopsticksPolicy):

    def __init__(self, game, splitter, attacker, divider):
        super().__init__(game)
        self._splitter = splitter
        self._attacker = attacker
        self._divider = divider

    def split(self, left_hand, right_hand, opponent_left_hand, opponent_right_hand):
        return self._splitter.split(left_hand, right_hand, opponent_left_hand, opponent_right_hand)

    def attack(self, left_hand, right_hand, opponent_left_hand, opponent_right_hand):
        return self._attacker.attack(left_hand, right_hand, opponent_left_hand, opponent_right_hand)

    def divide(self, left_hand, right_hand, opponent_left_hand, opponent_right_hand):
        return self._divider.divide(left_hand, right_hand, opponent_left_hand, opponent_right_hand)


class RandomSplitter(SplitPolicy):
    def __init__(self, game):
        super().__init__(game)

    def split(self, left_hand, right_hand, opponent_left_hand, opponent_right_hand):
        my_hand_sum = left_hand + right_hand
        possible_hand_values = list(range(0, my_hand_sum+1))

        if 5 in possible_hand_values:
            possible_hand_values.remove(5)

        split_combinations = [combo for combo in combinations_with_replacement(possible_hand_values, 2) if sum(combo) == my_hand_sum]
        return random.choice(split_combinations)


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

    def divide(self, left_hand, right_hand, opponent_left_hand, opponent_right_hand):
        my_hand_sum = left_hand + right_hand
        possible_hand_values = list(range(1, my_hand_sum + 1))

        if 5 in possible_hand_values:
            possible_hand_values.remove(5)

        divide_combinations = [combo for combo in combinations_with_replacement(possible_hand_values, 2) if sum(combo) == my_hand_sum]

        if len(divide_combinations) == 0:
            return None

        return random.choice(divide_combinations)


class GreedySplitter(SplitPolicy):
    def __init__(self, game):
        super().__init__(game)

    def split(self, left_hand, right_hand, opponent_left_hand, opponent_right_hand):
        new_left_hand, new_right_hand, reward = scoring.greedy_split(left_hand, right_hand, opponent_left_hand, opponent_right_hand)
        return new_left_hand, new_right_hand


class GreedyAttacker(AttackPolicy):
    def __init__(self, game):
        super().__init__(game)

    def attack(self, left_hand, right_hand, opponent_left_hand, opponent_right_hand):
        attack_value, attacked_hand_idx, reward = scoring.greedy_attack(left_hand, right_hand, opponent_left_hand, opponent_right_hand)
        return attack_value, attacked_hand_idx


class GreedyDivider(DividePolicy):
    def __init__(self, game):
        super().__init__(game)

    def divide(self, left_hand, right_hand, opponent_left_hand, opponent_right_hand):
        resulting_hand_values = scoring.greedy_division(left_hand, right_hand, opponent_left_hand, opponent_right_hand)

        if resulting_hand_values is None:
            return None

        new_left_hand, new_right_hand, reward = resulting_hand_values
        return new_left_hand, new_right_hand
