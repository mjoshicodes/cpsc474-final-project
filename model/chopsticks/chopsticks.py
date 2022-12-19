import itertools as it
import sys

from enum import Enum
from hand import Hands

import scoring
import random

P1 = 1
P2 = 2

Left = 1
Right = 2


class Game:
    def __init__(self):
        self.p1 = Hands(1, 1)
        self.p2 = Hands(1, 1)

    def reset_game(self):
        self.p1 = Hands(1, 1)
        self.p2 = Hands(1, 1)

    def attack(self, attacked_player_idx, attacked_hand, attacker_hand=None, attack_value=None):
        attacked = self.p1 if attacked_player_idx == P1 else self.p2
        attacker = self.p1 if attacked_player_idx == P2 else self.p2

        if attacker_hand is not None:
            attack_value = attacker.left_hand() if attacker_hand == Left else attacker.right_hand()

        if attacked_hand == Left:
            attacked.attack_left(attack_value)
        else:
            attacked.attack_right(attack_value)

    def get_actions(self):
        """
            Gets all the actions that the next player is able to perform.
            Returns:
                actions:    dictionary consisting of three keys: "attack", "divide", and "split", 
                            each holding an array of actions for that respective type of move.
        """
        actions, p1_hands, p2_hands = {}, [], []
        if not self.p1.left_deaths() == 3:
            p1_hands.append(self.p1.left_hand())
        if not self.p1.right_deaths() == 3:
            p1_hands.append(self.p1.right_hand())
        if not self.p2.left_deaths() == 3:
            p2_hands.append(self.p2.left_hand())
        if not self.p2.right_deaths() == 3:
            p2_hands.append(self.p2.right_hand())
        attack_actions = []
        split_actions = []
        divide_actions = []
        if self.turn == Player.P1:
            for hand in p1_hands:
                for attackable_hand in p2_hands:
                    attack_actions.append((Player.P2, ))
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

    def split(self, player_idx, new_left_hand_value, new_right_hand_value):
        player = self.p1 if player_idx == 1 else self.p2
        player.update_left_hand(new_left_hand_value)
        player.update_right_hand(new_right_hand_value)

    def is_game_over(self):
        if self.p1.lost():
            return True
        elif self.p2.lost():
            return True
        else:
            return False

    def play(self, p1_policy, p2_policy, log):
        p1 = 0
        p2 = 1
        turn = 0

        while not self.is_game_over():
            if turn % 2 == 0:
                random_action = random.randint(0, 1)
                if random_action == 0:
                    left_hand, right_hand = self.p1.left_hand(), self.p1.right_hand()
                    opponent_left_hand, opponent_right_hand = self.p2.left_hand(), self.p2.right_hand()
                    attack_value, attacked_hand_idx = p1_policy.attack(
                        left_hand, right_hand, opponent_left_hand, opponent_right_hand)
                    self.attack(P2, attacked_hand_idx,
                                attack_value=attack_value)
                else:
                    left_hand, right_hand = self.p1.left_hand(), self.p1.right_hand()
                    opponent_left_hand, opponent_right_hand = self.p2.left_hand(), self.p2.right_hand()
                    new_left_hand, new_right_hand = p1_policy.split(
                        left_hand, right_hand, opponent_left_hand, opponent_right_hand)
                    self.split(P1, new_left_hand, new_right_hand)
            else:
                left_hand, right_hand = self.p2.left_hand(), self.p2.right_hand()
                opponent_left_hand, opponent_right_hand = self.p1.left_hand(), self.p1.right_hand()
                attack_value, attacked_hand_idx = p2_policy.attack(
                    left_hand, right_hand, opponent_left_hand, opponent_right_hand)
                self.attack(P1, attacked_hand_idx, attack_value=attack_value)

            turn += 1

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
