from itertools import combinations_with_replacement


def get_split_combinations(left_hand, right_hand):
    my_hand_sum = left_hand + right_hand
    possible_hand_values = [hand for hand in list(range(0, my_hand_sum + 1)) if hand < 5]

    combos = list(combinations_with_replacement(possible_hand_values, 2))
    split_combinations = [combo for combo in combos if sum(combo) == my_hand_sum and (combo != (left_hand, right_hand) and combo != (right_hand, left_hand))]
    return split_combinations

def get_divide_combinations(left_hand, right_hand):
    my_hand_sum = left_hand + right_hand
    possible_hand_values = possible_hand_values = list(range(1, max(left_hand, right_hand)))

    combos = list(combinations_with_replacement(possible_hand_values, 2))
    divide_combinations = [combo for combo in combos if sum(combo) == my_hand_sum and (combo != (left_hand, right_hand) and combo != (right_hand, left_hand))]
    return divide_combinations