import random
from abc import ABC, abstractmethod

import scoring

class ChopsticksPolicy(ABC):
    """ An abstract base class for chopsticks policies. """
    def __init__(self, game):
        self._game = game

        
    @abstractmethod
    def split(self, hand, scores, am_current_player):
        """ Returns a pair (keep, throw) determining which cards from the given
            hand to keep under this policy.

            hand -- a list of cards
            scores -- the current scores, with this policy's score first
            am_current_player -- a boolean flag indicating whether you are the current player
        """
        pass

    
    @abstractmethod
    def attack(self, cards, history, scores, am_current_player):
        """ Returns the card to play from the given list.

            cards -- a list of cards
            history -- the pegging history up to the point to decide what to play
            scores -- the current scores, with this policy's score first
            am_current_player -- a boolean flag indicating whether you are the current player

        """
        pass


    def divide(self, cards, history, scores, am_current_player):
        """ Returns the card to play from the given list.

            cards -- a list of cards
            history -- the pegging history up to the point to decide what to play
            scores -- the current scores, with this policy's score first
            am_current_player -- a boolean flag indicating whether you are the current player

        """
        pass
class SplitPolicy(ABC):
    """ An abstract base class for cribbage keep/throw policies. """
    def __init__(self, game):
        """ Creates a policy to play the given game.

            game -- a cribbage Game
        """
        self._game = game

        
    @abstractmethod
    def split(self, hand, scores, am_current_player):
        """ Returns a pair (keep, throw) determining which cards from the given
            hand to keep under this policy.

            hand -- a list of cards
            scores -- the current scores, with this policy's score first
            am_current_player -- a boolean flag indicating whether you are the current player

        """
        pass


class AttackPolicy(ABC):
    """ An abstract base class for chopsticks attacking policies. """
    
    def __init__(self, game):
        """ Creates a policy to play the given game.

            game -- a chopsticks Game
        """
        self._game = game

        
    @abstractmethod
    def attack(self, cards, history, scores, am_current_player):
        """ Returns the card to play from the given list.

            cards -- a list of cards
            history -- the pegging history up to the point to decide what to play
            scores -- the current scores, with this policy's score first
            am_current_player -- a boolean flag indicating whether you are the current player

        """
        pass
    

class DividePolicy(ABC):
    """ An abstract base class for cribbage keep/throw policies. """
    def __init__(self, game):
        """ Creates a policy to play the given game.

            game -- a cribbage Game
        """
        self._game = game

        
    @abstractmethod
    def divide(self, hand, scores, am_current_player):
        """ Returns a pair (hand 1 value, hand 2 value), determining the new hand values 

            hand -- a list of cards
            scores -- the current scores, with this policy's score first
            am_current_player -- a boolean flag indicating whether you are the current player

        """
        pass

class CompositePolicy(ChopsticksPolicy):
    """ A cribbage policy composed of a keep/throw policy and a pegging
        policy.
    """
    
    def __init__(self, game, splitter, attacker, divider):
        """ Creates a policy to play the given game using the given keep/throw
            and pegging policies.

            game -- a cribbage Game
            thrower -- a ThrowPolicy
            pegger -- a PegPolicy
        """
        super().__init__(game)
        self._splitter = splitter
        self._attacker = attacker
        self._divider = divider


    def split(self, hand, scores, am_current_player):
        """ Returns the (keep, throw) pair selected by this policy's
            keep/throw policy.

            hand -- a list of cards
            scores -- the current scores, with this policy's score first
            am_current_player -- a boolean flag indicating whether you are the current player

        """
        return self._thrower.keep(hand, scores, am_current_player)


    def attack(self, cards, history, scores, am_current_player):
        """ Returns the card to play selected by this policy's pegging policy.

            cards -- a list of cards
            history -- the pegging history up to the point to decide what to play
            scores -- the current scores, with this policy's score first
            am_current_player -- a boolean flag indicating whether you are the current player

        """
        return self._pegger.peg(cards, history, scores, am_current_player) 

    def divide(self, cards, history, scores, am_current_player):
        """ Returns the card to play selected by this policy's pegging policy.

            cards -- a list of cards
            history -- the pegging history up to the point to decide what to play
            scores -- the current scores, with this policy's score first
            am_current_player -- a boolean flag indicating whether you are the current player

        """
        return self._pegger.peg(cards, history, scores, am_current_player) 

class RandomSplitter(SplitPolicy):
    """ A cribbage policy for pegging that chooses a card to play uniformly
        randomly.
    """
    
    def __init__(self, game):
        """ Creates a policy to play the given game.
 
            game -- a cribbage Game
        """
        super().__init__(game)


    def split(self, cards, history, scores, am_current_player):
        """ Selects a card to play uniformly randomly from the given cards.

            cards -- a list of cards
            history -- the pegging history up to the point to decide what to play
            scores -- the current scores, with this policy's score first
            am_current_player -- a boolean flag indicating whether you are the current player

        """
        # shuffle cards and play first legal one
        random.shuffle(cards)
        for card in cards:
            if history.score(self._game, card, 0 if am_current_player else 1) is not None:
                return card
        return None
        

class RandomAttacker(AttackPolicy):
    """ A cribbage keep/throw policy that selects cards to keep uniformly
        randomly.
    """
    
    def __init__(self, game):
        """ Creates a policy to play the given game.
 
            game -- a cribbage Game
        """
        super().__init__(game)
        
    
    def attack(self, hand, scores, am_current_player):
        """ Uniformly randomly selects cards to keep and throw.

            hand -- a list of cards
            scores -- the current scores, with this policy's score first
            am_current_player -- a boolean flag indicating whether you are the current player

        """
        keep = hand[:]
        random.shuffle(keep)
        return keep[0:4], keep[4:]


class RandomDivider(DividePolicy):
    """ A cribbage policy for pegging that chooses a card to play uniformly
        randomly.
    """
    
    def __init__(self, game):
        """ Creates a policy to play the given game.
 
            game -- a cribbage Game
        """
        super().__init__(game)


    def divide(self, cards, history, scores, am_current_player):
        """ Selects a card to play uniformly randomly from the given cards.

            cards -- a list of cards
            history -- the pegging history up to the point to decide what to play
            scores -- the current scores, with this policy's score first
            am_current_player -- a boolean flag indicating whether you are the current player

        """
        # shuffle cards and play first legal one
        random.shuffle(cards)
        for card in cards:
            if history.score(self._game, card, 0 if am_current_player else 1) is not None:
                return card
        return None


class GreedyAttacker(SplitPolicy):
    """ A greedy policy for keep/throw in cribbage.  The greedy decision is
        based only on the score obtained by the cards kept and thrown, without
        consideration for how they might interact with the turned card or
        cards thrown by the opponent.
    """
    
    def __init__(self, game):
        """ Creates a greedy keep/throw policy for the given game.

            game -- a cribbage Game
        """
        super().__init__(game)


    def split(self, hand, scores, am_current_player):
        """ Selects the cards to keep to maximize the net score for those cards
            and the cards in the crib.  Points in the crib count toward the
            total if this policy is the dealer and against the total otherwise.

            hand -- a list of cards
            scores -- the current scores, with this policy's score first
            am_current_player -- a boolean flag indicating whether you are the current player

        """
        keep, throw, net_score = scoring.greedy_throw(self._game, hand, 1 if am_current_player else -1)
        return keep, throw
    
    
class GreedyAttacker(AttackPolicy):
    """ A cribbage pegging policy that plays the card that maximizes the
        points earned on the current play.
    """

    def __init__(self, game):
        """ Creates a greedy pegging policy for the given game.

            game -- a cribbage Game
        """
        super().__init__(game)


    def attack(self, cards, history, scores, am_dealer):
        """ Returns the card that maximizes the points earned on the next
            play.  Ties are broken uniformly randomly.

            cards -- a list of cards
            history -- the pegging history up to the point to decide what to play
            scores -- the current scores, with this policy's score first
            am_dealer -- a boolean flag indicating whether the crib
                         belongs to this policy
        """
        # shuffle cards to effectively break ties randomly
        random.shuffle(cards)

        best_card = None
        best_score = None
        for card in cards:
            score = history.score(self._game, card, 0 if am_dealer else 1)
            if score is not None and (best_score is None or score > best_score):
                best_score = score
                best_card = card
        return best_card



class GreedyDivider(DividePolicy):
    """ A cribbage pegging policy that plays the card that maximizes the
        points earned on the current play.
    """

    def __init__(self, game):
        """ Creates a greedy pegging policy for the given game.

            game -- a cribbage Game
        """
        super().__init__(game)


    def attack(self, cards, history, scores, am_dealer):
        """ Returns the card that maximizes the points earned on the next
            play.  Ties are broken uniformly randomly.

            cards -- a list of cards
            history -- the pegging history up to the point to decide what to play
            scores -- the current scores, with this policy's score first
            am_dealer -- a boolean flag indicating whether the crib
                         belongs to this policy
        """
        # shuffle cards to effectively break ties randomly
        random.shuffle(cards)

        best_card = None
        best_score = None
        for card in cards:
            score = history.score(self._game, card, 0 if am_dealer else 1)
            if score is not None and (best_score is None or score > best_score):
                best_score = score
                best_card = card
        return best_card
