from itertools import combinations, product, combinations_with_replacement
from action_combinations import get_split_combinations, get_divide_combinations
from hand import Hands
import random

P1 = 1
P2 = 2

Left = 1
Right = 2


def greedy_split(left_hand, right_hand, opponent_left_hand, opponent_right_hand):
    if left_hand == 0 or right_hand == 0:
        return None

    old_hand = (left_hand, right_hand)

    # my_hand_sum = left_hand + right_hand
    # possible_hand_values = [hand for hand in list(range(0, my_hand_sum + 1)) if hand < 5]

    # combos = list(combinations_with_replacement(possible_hand_values, 2))
    # split_combinations = [combo for combo in combos if sum(combo) == my_hand_sum and (combo != (left_hand, right_hand) and combo != (right_hand, left_hand))]
    split_combinations = get_split_combinations(left_hand, right_hand)

    # print(left_hand, right_hand, split_combinations)
    if len(split_combinations) == 0:
            return None

    def score(old_hand, split):
        old_left_hand, old_right_hand = old_hand
        left_hand, right_hand = split

        if left_hand + opponent_left_hand == 5 or left_hand + opponent_right_hand == 5 or right_hand + opponent_left_hand == 5 or right_hand + opponent_right_hand == 5:
            return (left_hand, right_hand, -1)
        elif old_left_hand + opponent_left_hand == 5 or old_left_hand + opponent_right_hand == 5 or old_right_hand + opponent_left_hand == 5 or old_right_hand + opponent_right_hand == 5:
            return (left_hand, right_hand, 1)
        else:
            return (left_hand, right_hand, 0)

    return max(map(lambda split: score(old_hand, split), split_combinations), key=lambda t: t[2])

def get_valid_attacks(left_hand, right_hand):
    valid_attacks = []
    if left_hand != 0:
        valid_attacks.append(left_hand)
    if right_hand != 0:
        valid_attacks.append(right_hand)

    return valid_attacks

def get_hands_available_for_attack(left_hand, right_hand):
    valid_hands = []
    if left_hand != 0:
        valid_hands.append(1)
    if right_hand != 0:
        valid_hands.append(2)

    return valid_hands

def greedy_attack(left_hand, right_hand, opponent_left_hand, opponent_right_hand):
    possible_attacks = get_valid_attacks(left_hand, right_hand)
    hands_available_for_attack = get_hands_available_for_attack(opponent_left_hand, opponent_right_hand)
    attack_combinations = list(set(list(product(possible_attacks, hands_available_for_attack))))

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


def greedy_division(left_hand, right_hand, opponent_left_hand, opponent_right_hand):
    if left_hand == 0 or right_hand == 0:
        return None

    old_hand = (left_hand, right_hand)

    # my_hand_sum = left_hand + right_hand
    # possible_hand_values = possible_hand_values = list(range(1, max(left_hand, right_hand)))

    # combos = list(combinations_with_replacement(possible_hand_values, 2))
    # divide_combinations = [combo for combo in combos if sum(combo) == my_hand_sum and (combo != (left_hand, right_hand) and combo != (right_hand, left_hand))]

    divide_combinations = get_divide_combinations(left_hand, right_hand)

    if len(divide_combinations) == 0:
        return None

    def score(old_hand, split):
        old_left_hand, old_right_hand = old_hand
        left_hand, right_hand = split

        if left_hand + opponent_left_hand == 5 or left_hand + opponent_right_hand == 5 or right_hand + opponent_left_hand == 5 or right_hand + opponent_right_hand == 5:
            return (left_hand, right_hand, -1)
        elif old_left_hand + opponent_left_hand == 5 or old_left_hand + opponent_right_hand == 5 or old_right_hand + opponent_left_hand == 5 or old_right_hand + opponent_right_hand == 5:
            return (left_hand, right_hand, 1)
        else:
            return (left_hand, right_hand, 0)


    return max(map(lambda divide: score(old_hand, divide), divide_combinations), key=lambda t: t[2])


def does_attack_kill_hand(attack_value, opponent):
    if opponent.left_hand() != 0 and attack_value + opponent.left_hand == 5:
        return True
    if opponent.right_hand() != 0 and attack_value + opponent.right_hand == 5:
        return True
    return False
