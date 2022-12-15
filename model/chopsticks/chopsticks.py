import itertools as it
import sys

from enum import Enum
from hand import Hands

class Player(Enum):
    P1 = 1
    P2 = 2

class Hand(Enum):
    Left = 1
    Right = 2

class Game:
    def __init__(self):
        self.p1 = Hands(1, 1)
        self.p2 = Hands(1, 1)

    def attack(self, attacked_player, attacked_hand, attacker_hand):
        attacked = self.p1 if attacked_player == Player.P1 else self.p2
        attacker = self.p1 if attacked_player == Player.P2 else self.p2

        attack_value = attacker.left_hand() if attacker_hand == Hand.Left else attacker.right_hand()

        if attacked_hand == Hand.Left:
            attacked.attack_left(attack_value)
        else:
            attacked.attack_right(attack_value)

    def transfer(self, player_idx, tranfer_hand, transfer_value):
        player = self.p1 if player_idx == 1 else self.p2
        if tranfer_hand == Hand.Left:
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

    def play():
        pass

    def evaluate_policies(game, p0_policy, p1_policy, count):
        p0_total = 0
        p1_total = 0
        scores = dict()
        total_hands = 0
        for g in range(count):
            if g % 2 == 0:
                results = game.play(p0_policy, p1_policy)
                p0_pts = results[0]
            else:
                results = game.play(p1_policy, p0_policy)
                p0_pts = -results[0]
            if p0_pts not in scores:
                scores[p0_pts] = 0
            scores[p0_pts] += 1
            if p0_pts > 0:
                p0_total += p0_pts
            else:
                p1_total += -p0_pts
        total_hands += results[1]
        return (p0_total - p1_total) / count, p0_total/count, scores, total_hands/ count