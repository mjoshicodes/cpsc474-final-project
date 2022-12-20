import itertools as it
import sys

from enum import Enum
from hand import Hands

import random

import sys

P1 = 1
P2 = 2

Left = 1
Right = 2


class Game:

    def __init__(self):
        self.reset_game()
        self._turn = P1

    def reset_game(self):
        self.p1 = Hands(1, 1)
        self.p2 = Hands(1, 1)

    def next_turn(self):
        if self._turn == P1:
            self._turn = P2
        else:
            self._turn = P1

    def get_actions(self):
        """
            Gets all the actions that the next player is able to perform.
            Returns:
                actions:    dictionary consisting of three keys: "attack", "divide", and "split",
                            each holding an array of actions for that respective type of move.
        """
        actions, p1_hands, p2_hands = {}, [], []
        if not self.p1.left_deaths() == 3:
            p1_hands.append((self.p1.left_hand(),  Left))
        if not self.p1.right_deaths() == 3:
            p1_hands.append((self.p1.right_hand(), Right))
        if not self.p2.left_deaths() == 3:
            p2_hands.append((self.p2.left_hand(), Left))
        if not self.p2.right_deaths() == 3:
            p2_hands.append((self.p2.right_hand(), Right))
        attack_actions = []
        split_actions = []
        divide_actions = []
        if self.turn == P1:
            for hand in p1_hands:
                for attackable_hand in p2_hands:
                    attack_actions.append((P2, attackable_hand[1]))
        else:
            for hand in p2_hands:
                pass
        actions["attack"] = attack_actions
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

    def is_game_over(self):
        if self.p1.lost():
            return True
        elif self.p2.lost():
            return True
        else:
            return False

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
                # print(action, " I am P1")
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
                # print(action, " I am P2")
                self.execute_action(self.p2, self.p1, action)

            # print(self.p1.left_hand(), self.p1.right_hand(), self.p2.left_hand(), self.p2.right_hand())

            self.next_turn()

        if self.p1.lost():
            self.reset_game()
            return (0, 1)
        else:
            self.reset_game()
            return (1, 0)

def evaluate_policies(game, p1_policy, p2_policy, count):
    p1_total = 0
    p2_total = 0

    for g in range(count):
        results = game.play(p1_policy, p2_policy, lambda mess: None)
        p1_total += results[0]
        p2_total += results[1]

    return (p1_total / count, p2_total / count)
