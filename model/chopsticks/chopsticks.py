import itertools as it
import sys

from enum import Enum
from hand import Hands

import scoring

P1 = 1
P2 = 2

Left = 1
Right = 2

class Game:
    def __init__(self):
        self.p1 = Hands(1, 1)
        self.p2 = Hands(1, 1)

    def attack(self, attacked_player_idx, attacked_hand, attacker_hand=None, attack_value=None):
        print("attacked player: ", attacked_player_idx)
        print("attacked hand: ", attacked_hand)
        print("attack_value: ", attack_value)

        attacked = self.p1 if attacked_player_idx == P1 else self.p2
        attacker = self.p1 if attacked_player_idx == P2 else self.p2

        if attacker_hand is not None:
            attack_value = attacker.left_hand() if attacker_hand == Left else attacker.right_hand()

        if attacked_hand == Left:
            attacked.attack_left(attack_value)
        else:
            attacked.attack_right(attack_value)

    def transfer(self, player_idx, tranfer_hand, transfer_value):
        player = self.p1 if player_idx == 1 else self.p2
        if tranfer_hand == Left:
            player.transfer_left_to_right(transfer_value)
        else:
            player.transfer_right_to_left(transfer_value)

    def game_over(self):
        if self.p1.lost():
            return self.p2
        elif self.p2.lost():
            return self.p1
        else:
            return None

    def play(self):
        for i in range(10):
            if i % 2 == 0:
                attack_value, attacked_hand_idx, reward = scoring.greedy_attack(self.p1, self.p2)
                self.attack(2, attacked_hand_idx, attack_value=attack_value)
            else:
                attack_value, attacked_hand_idx, reward = scoring.greedy_attack(self.p2, self.p1)
                self.attack(1, attacked_hand_idx, attack_value=attack_value)

            print(self.p1.left_hand(), self.p1.right_hand())
            print(self.p2.left_hand(), self.p2.right_hand())


    def evaluate_policies(game, p1_policy, p2_policy, count):
        p1_total = 0
        p2_total = 0
        scores = dict()
        total_hands = 0
        for g in range(count):
            if g % 2 == 0:
                results = game.play(p1_policy, p2_policy)
                p1_pts = results[0]
            else:
                results = game.play(p2_policy, p1_policy)
                p1_pts = -results[0]
            if p1_pts not in scores:
                scores[p1_pts] = 0
            scores[p1_pts] += 1
            if p1_pts > 0:
                p0_total += p1_pts
            else:
                p1_total += -p1_pts
        total_hands += results[1]
        return (p1_total - p2_total) / count, p1_total / count, scores, total_hands / count