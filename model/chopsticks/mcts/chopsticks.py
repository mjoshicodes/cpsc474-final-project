import itertools as it
import sys

from enum import Enum
from hand import Hands
from itertools import combinations, product, combinations_with_replacement
from action_combinations import get_split_combinations, get_divide_combinations

import random

import sys

P1 = 1
P2 = 2

Left = 1
Right = 2

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

class Game:

    def __init__(self):
        self.reset_game()
        self._turn = P1
        self._hash = str(self).__hash__()

    def reset_game(self):
        self.p1 = Hands(1, 1)
        self.p2 = Hands(1, 1)

    def next_turn(self):
        if self._turn == P1:
            self._turn = P2
        else:
            self._turn = P1

    def make_copy(self):
        new_game = Game()
        new_game.p1.update_left_hand(self.p1.left_hand())
        new_game.p1.update_right_hand(self.p1.right_hand())
        new_game.p2.update_left_hand(self.p2.left_hand())
        new_game.p2.update_right_hand(self.p2.right_hand())
        new_game.p1.update_left_deaths(self.p1.left_deaths())
        new_game.p1.update_right_deaths(self.p1.right_deaths())
        new_game.p2.update_left_deaths(self.p1.left_deaths())
        new_game.p2.update_right_deaths(self.p2.right_deaths())
        if self._turn == P2:
            new_game.next_turn()
        return new_game

    def actor(self):
        return self._turn

    def get_split_actions(self, left_hand, right_hand):
        if left_hand == 0 or right_hand == 0:
            return []
        hand_sum = left_hand + right_hand
        possible_hand_values = [hand for hand in list(range(0, hand_sum + 1)) if hand < 5]
        combos = list(combinations_with_replacement(possible_hand_values, 2))
        split_combinations = [("SPLIT", l, r) for l, r in combos if sum([l, r]) == hand_sum and ((l, r) != (left_hand, right_hand) and (l, r) != (right_hand, left_hand))]
        return split_combinations

    def get_attack_actions(self, left_hand, right_hand, opponent_left_hand, opponent_right_hand):
        possible_attacks = get_valid_attacks(left_hand, right_hand)
        hands_available_for_attack = get_hands_available_for_attack(opponent_left_hand, opponent_right_hand)
        attack_combinations = product(possible_attacks, hands_available_for_attack)
        attack_combinations = list(set([("ATTACK", val, hand_indx) for val, hand_indx in attack_combinations]))
        return attack_combinations

    def get_divide_actions(self, left_hand, right_hand):
        if left_hand != 0 and right_hand != 0:
            return []
        my_hand_sum = left_hand + right_hand
        possible_hand_values = list(range(1, max(left_hand, right_hand)))
        combos = list(combinations_with_replacement(possible_hand_values, 2))
        divide_combinations = [("DIVIDE", l, r) for l, r in combos if sum([l + r]) == my_hand_sum and ((l, r) != (left_hand, right_hand) and (l, r) != (right_hand, left_hand))]
        return divide_combinations

    def get_actions(self):
        """
            Gets all the actions that the next player is able to perform.
            Returns:
                actions:    list of tuples with all the action types: split, attack, divide
        """
        left_hand = 0
        right_hand = 0
        opponent_left_hand = 0
        opponent_right_hand = 0

        if self._turn == P1:
            left_hand = self.p1.left_hand()
            right_hand = self.p1.right_hand()
            opponent_left_hand = self.p2.left_hand()
            opponent_right_hand = self.p2.right_hand()
        else:
            left_hand = self.p2.left_hand()
            right_hand = self.p2.right_hand()
            opponent_left_hand = self.p1.left_hand()
            opponent_right_hand = self.p1.right_hand()

        actions = self.get_split_actions(left_hand, right_hand) + self.get_attack_actions(left_hand, right_hand, opponent_left_hand, opponent_right_hand) + self.get_divide_actions(left_hand, right_hand)
        return actions

    def transfer(self, player_idx, tranfer_hand, transfer_value):
        player = self.p1 if player_idx == 1 else self.p2
        if tranfer_hand == Left:
            player.transfer_left_to_right(transfer_value)
        else:
            player.transfer_right_to_left(transfer_value)

    def split(self, player, new_left_hand_value, new_right_hand_value):
        player.update_left_hand(new_left_hand_value)
        player.update_right_hand(new_right_hand_value)

    def attack(self, attacked_player, attacked_hand, attack_value):
        if attacked_hand == Left:
            attacked_player.attack_left(attack_value)
        else:
            attacked_player.attack_right(attack_value)

    def divide(self, player, new_left_hand_value, new_right_hand_value):
        player.update_left_hand(new_left_hand_value)
        player.update_right_hand(new_right_hand_value)

    def simulate_action(self, action):
        action_type = action[0]
        next_position = self.make_copy()
        if action_type == "SPLIT":
            new_left_hand_value, new_right_hand_value = action[1], action[2]
            if self._turn == P1:
                next_position.p1.update_left_hand(new_left_hand_value)
                next_position.p1.update_right_hand(new_right_hand_value)
                next_position.next_turn()
            else:
                next_position.p2.update_left_hand(new_left_hand_value)
                next_position.p2.update_right_hand(new_right_hand_value)
        elif action_type == "ATTACK":
            attack_value, attacked_hand_idx = action[1], action[2]
            if self._turn == P1:
                if attacked_hand_idx == Left:
                    new_sum = (next_position.p2.left_hand() + attack_value) % 5
                    if new_sum == 0:
                        next_position.p2.update_left_deaths(next_position.p2.left_deaths() + 1)
                    next_position.p2.update_left_hand(new_sum)
                else:
                    new_sum = (next_position.p2.right_hand() + attack_value) % 5
                    if new_sum == 0:
                        next_position.p2.update_right_deaths(next_position.p2.right_deaths() + 1)
                    next_position.p2.update_right_hand(new_sum)
            else:
                if attacked_hand_idx == Left:
                    new_sum = (next_position.p1.left_hand() + attack_value) % 5
                    if new_sum == 0:
                        next_position.p1.update_left_deaths(next_position.p1.left_deaths() + 1)
                    next_position.p1.update_left_hand(new_sum)
                else:
                    new_sum = (next_position.p1.right_hand() + attack_value) % 5
                    if new_sum == 0:
                        next_position.p1.update_right_deaths(next_position.p1.right_deaths() + 1)
                    next_position.p1.update_right_hand(new_sum)
        else:
            new_left_hand_value, new_right_hand_value = action[1], action[2]
            if self._turn == P1:
                next_position.p1.update_left_hand(new_left_hand_value)
                next_position.p1.update_right_hand(new_right_hand_value)
            else:
                next_position.p2.update_left_hand(new_left_hand_value)
                next_position.p2.update_right_hand(new_right_hand_value)
        next_position.next_turn()
        return next_position

    def execute_action(self, myself, opponent, action):
        action_type = action[0]
        if action_type == "SPLIT":
            new_left_hand_value, new_right_hand_value = action[1], action[2]
            self.split(myself, new_left_hand_value, new_right_hand_value)
        elif action_type == "ATTACK":
            attack_value, attacked_hand_idx = action[1], action[2]
            self.attack(opponent, attacked_hand_idx, attack_value)
        else:
            new_left_hand_value, new_right_hand_value = action[1], action[2]
            self.divide(myself, new_left_hand_value, new_right_hand_value)

    def terminal_helper(self):
        if self.p1.lost():
            return True, -1
        elif self.p2.lost():
            return True, 1
        else:
            return False, 0

    # TERMINAL
    def is_game_over(self):
        return self.terminal_helper()[0]

    def payoff(self):
        return self.terminal_helper()[1]

    def play(self, p1_policy, p2_policy, log):
        while not self.is_game_over():
            if self._turn == P1:
                left_hand, right_hand = self.p1.left_hand(), self.p1.right_hand()
                opponent_left_hand, opponent_right_hand = self.p2.left_hand(), self.p2.right_hand()

                split_action = p1_policy.split(left_hand, right_hand, opponent_left_hand, opponent_right_hand)
                attack_action = p1_policy.attack(left_hand, right_hand, opponent_left_hand, opponent_right_hand)
                divide_action = p1_policy.divide(left_hand, right_hand, opponent_left_hand, opponent_right_hand)
                actions = [action for action in [split_action, attack_action, divide_action] if action is not None]
                random.shuffle(actions)

                action = max(actions, key=lambda x: x[3])
                self.execute_action(self.p1, self.p2, action)
            else:
                left_hand, right_hand = self.p2.left_hand(), self.p2.right_hand()
                opponent_left_hand, opponent_right_hand = self.p1.left_hand(), self.p1.right_hand()

                split_action = p2_policy.split(left_hand, right_hand, opponent_left_hand, opponent_right_hand)
                attack_action = p2_policy.attack(left_hand, right_hand, opponent_left_hand, opponent_right_hand)
                divide_action = p2_policy.divide(left_hand, right_hand, opponent_left_hand, opponent_right_hand)
                actions = [action for action in [split_action, attack_action, divide_action] if action is not None]
                random.shuffle(actions)
                action = max(actions, key=lambda x: x[3])
                self.execute_action(self.p2, self.p1, action)

            # print(self.p1.left_hand(), self.p1.right_hand(), self.p2.left_hand(), self.p2.right_hand())

            self.next_turn()

        if self.p1.lost():
            self.reset_game()
            return (0, 1)
        else:
            self.reset_game()
            return (1, 0)
        
    def play_mcts(self, p1_policy, p2_policy):
        while not self.is_game_over():
            if self._turn == P1:
                player_1_policy = p1_policy()
                action = player_1_policy(self.make_copy())
                self.execute_action(self.p1, self.p2, action)
            else:
                left_hand, right_hand = self.p2.left_hand(), self.p2.right_hand()
                opponent_left_hand, opponent_right_hand = self.p1.left_hand(), self.p1.right_hand()

                split_action = p2_policy.split(left_hand, right_hand, opponent_left_hand, opponent_right_hand)
                attack_action = p2_policy.attack(left_hand, right_hand, opponent_left_hand, opponent_right_hand)
                divide_action = p2_policy.divide(left_hand, right_hand, opponent_left_hand, opponent_right_hand)
                actions = [action for action in [split_action, attack_action, divide_action] if action is not None]
                random.shuffle(actions)
                action = max(actions, key=lambda x: x[3])
                self.execute_action(self.p2, self.p1, action)

            # print(self.p1.left_hand(), self.p1.right_hand(), self.p2.left_hand(), self.p2.right_hand())

            self.next_turn()

        if self.p1.lost():
            self.reset_game()
            return (0, 1)
        else:
            self.reset_game()
            return (1, 0)

    def __hash__(self):
        return self._hash

def evaluate_mcts_policies(game, p1_policy, p2_policy, count):
    p1_total = 0
    p2_total = 0
    for _ in range(count):
        results = game.play_mcts(p1_policy, p2_policy)
        p1_total += results[0]
        p2_total += results[1]

    return (p1_total / count, p2_total / count)

def evaluate_policies(game, p1_policy, p2_policy, count):
    p1_total = 0
    p2_total = 0

    for _ in range(count):
        results = game.play(p1_policy, p2_policy, lambda mess: None)
        p1_total += results[0]
        p2_total += results[1]

    return (p1_total / count, p2_total / count)


if __name__ == '__main__':
    """main is used for unit testing functions"""
    game = Game()
    game.p1 = Hands(1, 1)
    game.p2 = Hands(1, 1)
    print(game.get_actions())