from itertools import combinations, product, combinations_with_replacement
from hand import Hands
import random

P1 = 1
P2 = 2

Left = 1
Right = 2

def greedy_split(left_hand, right_hand, opponent_left_hand, opponent_right_hand):
    my_hand_sum = left_hand + right_hand
    possible_hand_values = list(range(0, my_hand_sum+1))

    if 5 in possible_hand_values:
        possible_hand_values.remove(5)

    split_combinations = [combo for combo in combinations_with_replacement(possible_hand_values, 2) if sum(combo) == my_hand_sum]

    def score(split):
        left_hand, right_hand = split

        if left_hand + opponent_left_hand == 5 or left_hand + opponent_right_hand == 5:
            return left_hand, right_hand, -1
        else:
            return left_hand, right_hand, 1

    return max(map(lambda split: score(split), split_combinations), key=lambda t: t[2])


def greedy_attack(left_hand, right_hand, opponent_left_hand, opponent_right_hand):
    possible_attacks = [left_hand, right_hand]
    hands_available_for_attack = [1 if opponent_left_hand != 0 else None, 2 if opponent_right_hand != 0 else None]
    attack_combinations = list(product(possible_attacks, hands_available_for_attack))

    def score(attack):
        attack_value, attacked_hand_idx = attack
        attacked_hand = opponent_left_hand if attacked_hand_idx == Left else opponent_right_hand
        resulting_attack_value = (attack_value + attacked_hand) % 5

        if resulting_attack_value == 0:
            return attack_value, attacked_hand_idx, 1
        elif (5 - resulting_attack_value) == left_hand or (5 - resulting_attack_value) == right_hand:
            return attack_value, attacked_hand_idx, -1
        else:
            return attack_value, attacked_hand_idx, 0

    return max(map(lambda attack: score(attack), attack_combinations), key=lambda t: t[2])

def greedy_divison(myself, opponent):
    pass

def does_attack_kill_hand(attack_value, opponent):
    if opponent.left_hand() != 0:
        if attack_value + opponent.left_hand == 5:
            return True

    if opponent.right_hand() != 0:
        if attack_value + opponent.right_hand == 5:
            return True