import itertools as it
import random

def greedy_throw(game, deal, crib):
    """ Returns a greedy choice of which cards to throw.  The greedy choice
        is determined by the score of the four cards kept and the two cards
        thrown in isolation, without considering what the turned card
        might be or what the opponent might throw to the crib.  If multiple
        choices result in the same net score, then one is chosen randomly.

        game -- a Cribbage game
        deal -- a list of the cards dealt
        crib -- 1 for owning the crib, -1 for opponent owning the crib
    """
    def score_split(indices):
        keep = []
        throw = []
        for i in range(len(deal)):
            if i in indices:
                throw.append(deal[i])
            else:
                keep.append(deal[i])
        return keep, throw, score(game, keep, None, False)[0] + crib * score(game, throw, None, True)[0]

    throw_indices = game.throw_indices()
    
    # to randomize the order in which throws are considered to have the effect
    # of breaking ties randomly
    random.shuffle(throw_indices)

    # pick the (keep, throw, score) triple with the highest score
    return max(map(lambda i: score_split(i), throw_indices), key=lambda t: t[2])
        

def score(game, player1_hands, player2_hands, am_current_player):
    """ Returns the score for the given hand and turn card.  The score
        is returned as a six-element list with the total score in the
        first element and the pairs, 15s, runs, flushes, and nobs subscores
        in the remaining elements in that order.

        game -- a cribbage game 
        player1_hands -- a tuple for player 1's hand
        player2_hands -- a card, or None
        crib -- true to score by crib scoring rules
    """
    if am_current_player == 0:
        if player2_hands == (0, 0):
            reward = 1
        elif player1_hands == (0, 0):
            reward = -1
        else:
            reward = 0
    elif am_current_player == 1:
        if player1_hands == (0, 0):
            reward = 1
        elif player2_hands == (0, 0):
            reward = -1
        else:
            reward = 0
    return reward