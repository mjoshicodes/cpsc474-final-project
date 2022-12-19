import itertools as it
import sys

from enum import Enum
from hand import Hands

import scoring

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
        self.turn = Player.P1

    def next(self):
        """
            Updates the turn to the next player.
        """
        if self.turn == Player.P1:
            self.turn = Player.P2
        else:
            self.turn = Player.P1

    def attack(self, attacked_player_idx, attacked_hand, attacker_hand=None, attack_value=None):
        # print("attacked player: ", attacked_player_idx)
        # print("attacked hand: ", attacked_hand)
        # print("attack_value: ", attack_value)

        attacked = self.p1 if attacked_player_idx == Player.P1 else self.p2
        attacker = self.p1 if attacked_player_idx == Player.P2 else self.p2

        if attacker_hand is not None:
            attack_value = attacker.left_hand() if attacker_hand == Hand.Left else attacker.right_hand()

        if attacked_hand == Hand.Left:
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
        if tranfer_hand == Hand.Left:
            player.transfer_left_to_right(transfer_value)
        else:
            player.transfer_right_to_left(transfer_value)

    def is_game_over(self):
        '''
            Checks to see if any of the players have lost.
            Returns boolean that indicates result after check.
        '''
        if self.p1.lost() or self.p2.lost():
            return True
        else:
            return False

    def play(self):
        scores = [0, 0]
        p1 = 0
        p2 = 1

        while not self.is_game_over():
            if self.turn == Player.P1:
                attack_value, attacked_hand_idx, reward = scoring.greedy_attack(self.p1, self.p2)
                self.attack(Player.P2, attacked_hand_idx, attack_value=attack_value)
                scores[p1] += reward
            else:
                attack_value, attacked_hand_idx, reward = scoring.greedy_attack(self.p2, self.p1)
                self.attack(Player.P1, attacked_hand_idx, attack_value=attack_value)
                scores[p2] += reward
            self.next()
        print(scores)
        return scores

def evaluate_policies(game, p1_policy, p2_policy, count):
    p1_total = 0
    p2_total = 0
    scores = dict()
    total_hands = 0
    for g in range(count):
        if g % 2 == 0:
            # results = game.play()
            results = game.play(p1_policy, p2_policy, lambda mess: None)
            p1_pts = results[0]
        else:
            results = game.play()
            results = game.play(p1_policy, p2_policy, lambda mess: None)
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