import itertools as it
import random

class Hands:
    def __init__(self, left_hand, right_hand):
        """ 
            Creates hands for one player with given sums
            sum -- an integer
        """
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
        if  self._left_hand + transfer_sum <= 4:
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
        self._left_hand = new_sum
    
    def attack_right(self, attack_sum):
        new_sum = (self._right_hand + attack_sum) % 5
        self._right_hand = new_sum
    
    def left_dead(self):
        return self._left_hand == 0
    
    def right_dead(self):
        return self._right_hand == 0

    def lost(self):
        return self.left_dead() and self.right_dead()

    # def __repr__(self):
    #     return "" + str(self._rank) + str(self._suit)


    # def __eq__(self, other):
    #     return self._rank == other._rank and self._suit == other._suit


    def __hash__(self):
        return self._hash