from itertools import combinations, product, combinations_with_replacement
from hand import Hands
import random

P1 = 1
P2 = 2

Left = 1
Right = 2


def rules_split(left_hand, right_hand, opponent_left_hand, opponent_right_hand):
    if left_hand == 0 or right_hand == 0:
        return None

    my_hand_sum = left_hand + right_hand
    possible_hand_values = [hand for hand in list(range(0, my_hand_sum)) if hand < 5]

    combos = list(combinations_with_replacement(possible_hand_values, 2))
    split_combinations = [combo for combo in combos if sum(combo) == my_hand_sum and (combo != (left_hand, right_hand) and combo != (right_hand, left_hand))]
    
    if len(split_combinations) == 0:
        return None

    def score(split):
        left_hand, right_hand = split
        if left_hand + opponent_left_hand == 5 or left_hand + opponent_right_hand == 5:
            return (left_hand, right_hand, -1)
        else:
            return (left_hand, right_hand, 1)

    # all_actions = map(lambda split: score(split), split_combinations)
    # return max(map(lambda split: score(split), split_combinations), key=lambda t: t[2])


    left_hand, right_hand, best_score = max(map(lambda split: score(split), split_combinations), key = lambda t: t[2])
    # print("left_hand", left_hand)
    return (left_hand, right_hand, best_score)
    # best_score = float('-inf')
    # best_index = None
    # for index, split_score in enumerate(all_scores):
    #     if split_score > best_score:
    #         best_score = split_score 
    #         best_index = index 
    # new_left_hand, new_right_hand = all_scores[best_index]
    # return (new_left_hand, new_right_hand, best_score)


    
    # best_action, best_score = all_actions[0], float('-inf')
    # for action in all_actions:
    #     new_left_hand, new_right_hand, action_score = action

    #     if (left_hand == 0 or right_hand == 0) and (new_left_hand != 0 and new_right_hand != 0):
    #         action_score += 0.5

    #     if action_score > best_score:
    #         best_action = (new_left_hand, new_right_hand, action_score)
    #         best_score = action_score

    # return best_action


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

def rules_attack(left_hand, right_hand, opponent_left_hand, opponent_right_hand):
    possible_attacks = get_valid_attacks(left_hand, right_hand)
    hands_available_for_attack = get_hands_available_for_attack(opponent_left_hand, opponent_right_hand)
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

    all_actions = list(map(lambda attack: score(attack), attack_combinations))

    best_action, best_score = all_actions[0], float('-inf')
    for action in all_actions:
        attack_value, attacked_hand_idx, action_score = action

        # if does_attack_kill_hand(attack_value, opponent_left_hand, opponent_right_hand):
        #     action_score += 1.0
        # else:
        #     action_score -= 1.0

        if action_score > best_score:
            best_action = (attack_value, attacked_hand_idx, action_score)
            best_score = action_score

    return best_action


def rules_division(left_hand, right_hand, opponent_left_hand, opponent_right_hand):
    if left_hand == 0 or right_hand == 0:
        return None

    my_hand_sum = left_hand + right_hand
    possible_hand_values = possible_hand_values = list(range(1, max(left_hand, right_hand)))

    combos = list(combinations_with_replacement(possible_hand_values, 2))
    divide_combinations = [combo for combo in combos if sum(combo) == my_hand_sum and (combo != (left_hand, right_hand) and combo != (right_hand, left_hand))]

    if len(divide_combinations) == 0:
        return None

    def score(divide):
        left_hand, right_hand = divide

        if left_hand + opponent_left_hand == 5 or left_hand + opponent_right_hand == 5:
            return left_hand, right_hand, -1
        else:
            return left_hand, right_hand, 1

    all_actions = list(map(lambda divide: score(divide), divide_combinations))

    best_action, best_score = all_actions[0], float('-inf')

    for action in all_actions:
        new_left_hand, new_right_hand, action_score = action
        action_score += 1.0

        if action_score > best_score:
            best_action = (new_left_hand, new_right_hand, action_score)
            best_score = action_score


    return best_action

def does_attack_kill_hand(attack_value, left_hand, right_hand):
    if left_hand != 0 and attack_value + right_hand == 5:
        return True
    if left_hand != 0 and attack_value + right_hand == 5:
        return True
    return False
