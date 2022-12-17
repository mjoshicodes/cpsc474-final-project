from itertools import combinations, product
import random
import chopsticks

def greedy_split(game, myself, opponent):
    # my_hand_sum = myself.left_hand() + myself.right_hand()
    # possible_hand_values = range(0, my_hand_sum+1)
    # split_combinations = [combo for combo in combinations(possible_hand_values, 2) if sum(combo) == my_hand_sum]
    pass

def greedy_attack(myself, opponent):
    possible_attacks = [myself.left_hand(), myself.right_hand()]
    hands_available_for_attack = [1 if opponent.left_hand() != 0 else None, 2 if opponent.right_hand() != 0 else None]
    attack_combinations = list(product(possible_attacks, hands_available_for_attack))

    def score(attack):
        attack_value, attacked_hand_idx = attack
        attacked_hand = None

        if attacked_hand_idx == chopsticks.Left:
            attacked_hand = opponent.left_hand()
        else:
            attacked_hand = opponent.right_hand()

        resulting_hand_value = attack_value + attacked_hand
        resulting_attack_value = resulting_hand_value if resulting_hand_value <= 5 else resulting_hand_value % 5

        if resulting_attack_value == 5:
            return attack_value, attacked_hand_idx, 1
        elif (5 - resulting_attack_value) == myself.left_hand() or (5 - resulting_attack_value) == myself.right_hand():
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
