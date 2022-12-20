from itertools import combinations, product, combinations_with_replacement
from action_combinations import get_split_combinations, get_divide_combinations
from hand import Hands
import random


'''
Adjusted reward to be negative 1 for if one of your old hands avoided death
the logic makes no sense lol
'''
P1 = 1
P2 = 2

Left = 1
Right = 2


def rules_split(left_hand, right_hand, opponent_left_hand, opponent_right_hand):
    if left_hand == 0 or right_hand == 0:
        return None
    old_hand = (left_hand, right_hand)
    split_combinations = get_split_combinations(left_hand, right_hand)

    if len(split_combinations) == 0:
        return None


    def score(old_hand, split):
        old_left_hand, old_right_hand = old_hand
        left_hand, right_hand = split
        reward = 0 
        if (left_hand + opponent_left_hand == 5) or (left_hand + opponent_right_hand == 5) or (right_hand + opponent_left_hand == 5) or (right_hand + opponent_right_hand == 5):
            reward -= 1
        if (old_left_hand + opponent_left_hand == 5) or (old_left_hand + opponent_right_hand == 5) or (old_right_hand + opponent_left_hand == 5) or (old_right_hand + opponent_right_hand == 5):
            reward -= 1
        '''
        Beginning of game heuristics:
        this currently messes with the game
        '''
        if (opponent_left_hand == 1 and opponent_right_hand == 1):
            if (old_left_hand == 1 and old_right_hand == 2) or (old_left_hand == 2 and old_right_hand == 1):
                if (left_hand == 3 and right_hand == 0) or (left_hand == 0 and right_hand == 3):
                    reward -= 1
            if (old_left_hand == 4 and old_right_hand == 0) or (old_left_hand == 0 and old_right_hand == 4):
                if (left_hand == 3 and right_hand == 1) or (left_hand == 1 and right_hand == 3):
                    reward += 1


        '''
        From 2,2 against 1,0,--> Split to 3,1. Opponent will have tap 1 hand 

        '''
        
        if (opponent_left_hand == 0 and opponent_right_hand == 1) or (opponent_left_hand == 1 and opponent_right_hand == 0):
            if (old_left_hand == 2 and old_right_hand == 2):
                if (left_hand == 3 and right_hand == 1) or (left_hand == 1 and right_hand == 3):
                    reward += 1
        #             # this is a good move 
        #     '''
        #     From 2,1 against 1,0, (your opponent's turn) is one of the easiest wins in the game. Your opponent will tap one of your hands leaving you with 2,1. Split to 3,0, your opponent will be forced to tap your 3 leaving you with 4,0. Finally, you tap their hand to win the game.
        #     '''
            if (old_left_hand == 2 and old_right_hand == 1) or (old_left_hand == 1 and old_right_hand == 2):
                if (left_hand == 3 and right_hand == 0) or (left_hand == 0 and right_hand == 3):
                    reward -= 5
                    # print("check super neg reward")
                    # this is an instawin because they have to hit your hand --> you have a hand of 4, they have a hand of 1


        return (left_hand, right_hand, reward)
    left_hand, right_hand, best_score = max(map(lambda split: score(old_hand, split), split_combinations), key = lambda t: t[2])
    # print("check:", (left_hand, right_hand, best_score))

    return (left_hand, right_hand, best_score)


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

    all_actions = list(map(lambda attack: score(attack), attack_combinations))
    best_attack_value, best_attacked_hand_idx, best_score = max(map(lambda attack: score(attack), attack_combinations), key = lambda t: t[2])

    return (best_attack_value, best_attacked_hand_idx, best_score)


def rules_division(left_hand, right_hand, opponent_left_hand, opponent_right_hand):
    if left_hand == 0 or right_hand == 0:
        return None
    old_hand = (left_hand, right_hand)

    divide_combinations = get_divide_combinations(left_hand, right_hand)

    if len(divide_combinations) == 0:
        return None

    def score(old_hand, divide):
        old_left_hand, old_right_hand = old_hand
        left_hand, right_hand = divide
        reward = 0 
        if (left_hand + opponent_left_hand == 5) or (left_hand + opponent_right_hand == 5 or right_hand + opponent_left_hand == 5 or right_hand + opponent_right_hand == 5):
            reward -= 1
        if (old_left_hand + opponent_left_hand == 5) or (old_left_hand + opponent_right_hand == 5) or (old_right_hand + opponent_left_hand == 5) or (old_right_hand + opponent_right_hand == 5):
            reward -= 1

        '''
        From (3),(0) against (1,0) and it is your turn, it is ideal to split to (2,1)
        '''
        # if (opponent_left_hand == 1 and opponent_right_hand == 0) or (opponent_left_hand == 0 and opponent_right_hand == 1):
        #     if (old_left_hand == 3 and old_right_hand == 0) or (old_left_hand == 0 and old_right_hand == 3):
        #         if (left_hand == 1 and right_hand == 2) or (left_hand == 2 and right_hand == 1):
        #             reward += 1
        return (left_hand, right_hand, reward)
    left_hand, right_hand, best_score = max(map(lambda divide: score(old_hand, divide), divide_combinations), key = lambda t: t[2])
    return (left_hand, right_hand, best_score)

def does_attack_kill_hand(attack_value, left_hand, right_hand):
    if left_hand != 0 and attack_value + right_hand == 5:
        return True
    if left_hand != 0 and attack_value + right_hand == 5:
        return True
    return False
