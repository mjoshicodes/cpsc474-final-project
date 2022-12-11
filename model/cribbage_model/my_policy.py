from policy import CribbagePolicy, CompositePolicy, GreedyThrower, GreedyPegger, PegPolicy, ThrowPolicy
import scoring
import random
import itertools
from deck import Card

class MyPolicy(CribbagePolicy):
    def __init__(self, game):
        super().__init__(game)
        # Change one to the GreedyThrower and change one for GreedyPegger and make your c
        self._policy = CompositePolicy(game, MyThrower(game), MyPegger(game))
        
    def keep(self, hand, scores, am_dealer):
        return self._policy.keep(hand, scores, am_dealer)


    def peg(self, cards, history, scores, am_dealer):
        # Prioritize playing cards that cannot make a 15 in the beginning
        # Can build on top of the greedy algorithm for this one
        return self._policy.peg(cards, history, scores, am_dealer)

class MyThrower(ThrowPolicy):    
    def __init__(self, game):
        super().__init__(game)

    def keep(self, hand, scores, am_dealer):
        def find_keep_subsets(hand):
            return list(itertools.combinations(hand, 4))
        
        def score_split(indices, deal, potential_community, crib):
            keep = []
            throw = []
            for i in range(len(deal)):
                if i in indices:
                    throw.append(deal[i])
                else:
                    keep.append(deal[i])
            score = 0
            for i in range(len(potential_community)):
                turn_card = potential_community[i]
                score += (scoring.score(self._game, keep, turn_card, False)[0] + crib * scoring.score(self._game, throw, turn_card, True)[0])
            return keep, throw, score

        # Get potential community
        throw_indices = self._game.throw_indices()
        potential_community_deck = self._game.deck()
        potential_community_deck.remove(hand)
        potential_community = potential_community_deck._cards
        # random.shuffle(potential_community)
            
        # to randomize the order in which throws are considered to have the effect
        # of breaking ties randomly
        random.shuffle(throw_indices)

        keep, throw, net_score = max(map(lambda i: score_split(i, hand, potential_community, 1 if am_dealer else -1), throw_indices), key=lambda t: t[2])
        return keep, throw



class MyPegger(PegPolicy):
    def __init__(self, game):
        super().__init__(game)
    
    def peg(self, cards, history, scores, am_dealer):
        # Heuristics on pegging - look at history
        # Go look at good heuristics for pegging
        # Leading with a low card
        # Look at each card in hand use rank value
        # If total points in history would go over 15 if you add your card then that is good

        best_card = None
        best_score = None
        for card in cards:
            score = history.score(self._game, card, 0 if am_dealer else 1)
            # Heuristics
            # If it is the start of the round, do not play a 5 or 10, prioritize 4
            if score is not None:
                if history.is_start_round():
                    if self._game.rank_value(card.rank()) == 5:
                        score -= 1
                    elif self._game.rank_value(card.rank()) == 10:
                        score -= 0.5
                    elif self._game.rank_value(card.rank()) == 4:
                        score += 1
                    elif self._game.rank_value(card.rank()) > 5:
                        score += 0.5
                
                # If the total score is below 15, prioritize playing cards that go above 15
                elif history.total_points() < 15:
                    if self._game.rank_value(card.rank()) + history.total_points() > 15:
                        score += 0.5
                    if self._game.rank_value(card.rank()) + history.total_points() == 15:
                        score += 1
                elif  history.total_points() >= 21:
                    if self._game.rank_value(card.rank()) > 2:
                        score += 0.5 
                    if self._game.rank_value(card.rank()) + history.total_points() > 29:
                        score += 1                  
                if score is not None and (best_score is None or score > best_score):
                    best_score = score
                    best_card = card
        return best_card


