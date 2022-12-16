import itertools as it
import random

class Hands:
    def __init__(self, left_hand, right_hand):
        self._left_hand = left_hand
        self._right_hand = right_hand
        self._left_deaths = 0
        self._right_deaths = 0
        self._hash = str(self).__hash__()

    def left_hand(self):
        return self._left_hand

    def right_hand(self):
        return self._right_hand

    def transfer_right_to_left(self, transfer_sum):
        if self._left_hand + transfer_sum <= 4:
            self._left_hand += transfer_sum
            self._right_hand -= transfer_sum
        else:
            return "not legal"

    def transfer_left_to_right(self, transfer_sum):
        if self._right_hand + transfer_sum <= 4:
            self._right_hand += transfer_sum
            self._left_hand -= transfer_sum
        else:
            return "not legal"

    def attack_left(self, attack_sum):
        new_sum = (self._left_hand + attack_sum) % 5
        if new_sum == 0:
            self._left_deaths += 1
            print("left hand dead")
        self._left_hand = new_sum

    def attack_right(self, attack_sum):
        new_sum = (self._right_hand + attack_sum) % 5
        if new_sum == 0:
            self._right_deaths += 1
            print("right hand dead")
        self._right_hand = new_sum

    def left_dead(self):
        return self._left_hand == 0

    def right_dead(self):
        return self._right_hand == 0

    def lost(self):
        return self.left_dead() and self.right_dead()

    def __hash__(self):
        return self._hash