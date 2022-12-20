import random
from abc import ABC, abstractmethod
from itertools import combinations, product, combinations_with_replacement
from action_combinations import get_split_combinations, get_divide_combinations
import greedy, rules_based


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
        if left_hand == 0 or right_hand == 0:
            return None

        split_combinations = get_split_combinations(left_hand, right_hand)

        if len(split_combinations) == 0:
            return None

        new_left_hand, new_right_hand = random.choice(split_combinations)
        return ("SPLIT", new_left_hand, new_right_hand, 0)


class RandomAttacker(AttackPolicy):
    def __init__(self, game):
        super().__init__(game)

    def get_valid_attacks(self, left_hand, right_hand):
        valid_attacks = []
        if left_hand != 0:
            valid_attacks.append(left_hand)
        if right_hand != 0:
            valid_attacks.append(right_hand)

        return valid_attacks

    def get_hands_available_for_attack(self, left_hand, right_hand):
        valid_hands = []
        if left_hand != 0:
            valid_hands.append(1)
        if right_hand != 0:
            valid_hands.append(2)

        return valid_hands

    def attack(self, left_hand, right_hand, opponent_left_hand, opponent_right_hand):
        possible_attacks = self.get_valid_attacks(left_hand, right_hand)
        hands_available_for_attack = self.get_hands_available_for_attack(opponent_left_hand, opponent_right_hand)
        attack_combinations = list(set(list(product(possible_attacks, hands_available_for_attack))))
        attack_value, attacked_hand_idx = random.choice(attack_combinations)
        return ("ATTACK", attack_value, attacked_hand_idx, 0)


class RandomDivider(DividePolicy):
    def __init__(self, game):
        super().__init__(game)

    def divide(self, left_hand, right_hand, opponent_left_hand, opponent_right_hand):
        if left_hand != 0 and right_hand != 0:
            return None

        divide_combinations = get_divide_combinations(left_hand, right_hand)

        if len(divide_combinations) == 0:
            return None

        new_left_hand, new_right_hand = random.choice(divide_combinations)
        return ("DIVIDE", new_left_hand, new_right_hand, 0)

class GreedySplitter(SplitPolicy):
    def __init__(self, game):
        super().__init__(game)

    def split(self, left_hand, right_hand, opponent_left_hand, opponent_right_hand):
        resulting_hand_values = greedy.greedy_split(left_hand, right_hand, opponent_left_hand, opponent_right_hand)

        if resulting_hand_values is None:
            return None

        new_left_hand, new_right_hand, reward = resulting_hand_values
        return ("SPLIT", new_left_hand, new_right_hand, reward)


class GreedyAttacker(AttackPolicy):
    def __init__(self, game):
        super().__init__(game)

    def attack(self, left_hand, right_hand, opponent_left_hand, opponent_right_hand):
        attack_value, attacked_hand_idx, reward = greedy.greedy_attack(left_hand, right_hand, opponent_left_hand, opponent_right_hand)
        return ("ATTACK", attack_value, attacked_hand_idx, reward)


class GreedyDivider(DividePolicy):
    def __init__(self, game):
        super().__init__(game)

    def divide(self, left_hand, right_hand, opponent_left_hand, opponent_right_hand):
        resulting_hand_values = greedy.greedy_division(left_hand, right_hand, opponent_left_hand, opponent_right_hand)

        if resulting_hand_values is None:
            return None

        new_left_hand, new_right_hand, reward = resulting_hand_values
        return ("DIVIDE", new_left_hand, new_right_hand, reward)


class MyPolicy(ChopsticksPolicy):
    def __init__(self, game):
        super().__init__(game)
        # Change one to the GreedyThrower and change one for GreedyPegger and make your c
        self._policy = CompositePolicy(game, RulesSplitter(game), RulesAttacker(game), RulesDivider(game))

    def split(self, left_hand, right_hand, opponent_left_hand, opponent_right_hand):
        return self._policy.split(self, left_hand, right_hand, opponent_left_hand, opponent_right_hand)


    def attack (self, left_hand, right_hand, opponent_left_hand, opponent_right_hand):
        # Prioritize playing cards that cannot make a 15 in the beginning
        # Can build on top of the greedy algorithm for this one
        return self._policy.attack(self, left_hand, right_hand, opponent_left_hand, opponent_right_hand)

    def divide(self, left_hand, right_hand, opponent_left_hand, opponent_right_hand):
        # Prioritize playing cards that cannot make a 15 in the beginning
        # Can build on top of the greedy algorithm for this one
        return self._policy.divide(self, left_hand, right_hand, opponent_left_hand, opponent_right_hand)

class RulesSplitter(SplitPolicy):
    def __init__(self, game):
        super().__init__(game)

    def split(self, left_hand, right_hand, opponent_left_hand, opponent_right_hand):
        resulting_hand_values = rules_based.rules_split(left_hand, right_hand, opponent_left_hand, opponent_right_hand)

        if resulting_hand_values is None:
            return None

        new_left_hand, new_right_hand, reward = resulting_hand_values
        return ("SPLIT", new_left_hand, new_right_hand, reward)


class RulesAttacker(AttackPolicy):
    def __init__(self, game):
        super().__init__(game)

    def attack(self, left_hand, right_hand, opponent_left_hand, opponent_right_hand):
        attack_value, attacked_hand_idx, reward = rules_based.rules_attack(left_hand, right_hand, opponent_left_hand, opponent_right_hand)
        return ("ATTACK", attack_value, attacked_hand_idx, reward)


class RulesDivider(DividePolicy):
    def __init__(self, game):
        super().__init__(game)

    def divide(self, left_hand, right_hand, opponent_left_hand, opponent_right_hand):
        resulting_hand_values = rules_based.rules_division(left_hand, right_hand, opponent_left_hand, opponent_right_hand)

        if resulting_hand_values is None:
            return None

        new_left_hand, new_right_hand, reward = resulting_hand_values
        return ("DIVIDE", new_left_hand, new_right_hand, reward)