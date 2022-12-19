import random

class ChopsticksStrategy:
    def __init__(self, plays, prob):
        ''' Creates a game using the given list of possible outcomes
            and the given probability distribution of those outcomes.

            plays -- a list of lists of (yards-gained, ticks-elapsed, turnover)
                     tuples indexed by offensive action then defensive action
            prob -- a probability distribution over the tuples in plays[o][d]
        '''
        self._plays = plays
        self._prob = prob


    def initial_position(self):
        ''' Returns the initial position in this game as a
            (p1_left_hand, p1_right_hand, p2_left_hand, p2_right_hand) tuple.
        '''
        return (5, 5, 5, 5)


    def p1_action_size(self):
        ''' Returns the number of current player (p1) actions available in this game. '''
        return len(self._plays)


    def p2_action_size(self):
        ''' Returns the number of other player (p2) actions available in this game. '''
        return len(self._plays[0])
    
    
    def result(self, pos, p1_play):
        ''' Returns the position that results from the given offensive play
            selection from the given position as a
            (field-position, downs-left, distance, ticks) tuple, and the outcome
            of that play as a (yards-gained, ticks-elapsed, turnover) tuple.

            pos -- a tuple (field_pos, downs_left, distance, time_in_ticks)
            offensive_play -- the index of an offensive play
        '''
        play_outcome = self._outcome(p1_play, random.randrange(len(self._plays[0])))
        return self._update(pos, play_outcome), play_outcome

    
    def _update(self, pos, play_outcome):
        ''' Returns the position that results from the given position
            and the result of a play.

            pos -- a tuple (p1_left_hand, p1_right_hand, p2_left_hand, p2_right_hand)
            play_outcome a tuple  (p1_left_hand_outcome, p1_right_hand_outcome, p2_left_hand_outcome, p2_right_hand_outcome)
        '''
        p1_left_hand, p1_right_hand, p2_left_hand, p2_right_hand = pos
        p1_left_hand_outcome, p1_right_hand_outcome, p2_left_hand_outcome, p2_right_hand_outcome = play_outcome

        if p1_left_hand_outcome < 0:
            p1_left_hand_outcome = 0
        if p2_left_hand_outcome < 0:
            p2_left_hand_outcome
        if p1_right_hand_outcome < 0:
            p1_right_hand_outcome = 0
        if p2_right_hand_outcome < 0:
            p2_right_hand_outcome = 0

        p1_left_hand = p1_left_hand_outcome
        p1_right_hand = p1_right_hand_outcome
        p2_left_hand = p2_left_hand_outcome
        p2_right_hand = p2_right_hand_outcome

        return (p1_left_hand, p1_right_hand, p2_left_hand, p2_right_hand)

    
    def game_over(self, pos):
        ''' Determines if the given position represents a game-over position.
        
            pos -- a tuple (field_pos, down, distance, time)
        '''
        p1_left_hand, p1_right_hand, p2_left_hand, p2_right_hand  = pos

        return (p1_left_hand == 0 and p1_right_hand == 0) or (p2_left_hand == 0 or p2_right_hand == 0)


    def win(self, pos):
        ''' Determines if the given position represents a game-won position.
        
            pos -- a tuple (field_pos, down, distance, time)
        '''
        _, _, p2_left_hand, p2_right_hand = pos

        return (p2_left_hand == 0 and p2_right_hand == 0)


    def _outcome(self, p1_action, p2_action):
        ''' Returns a randomly selected result for the given offensive
            and defensive actions.

            off_action -- the index of an offensive play
            def_action -- the index of an offensive play
        '''
        if p1_action < 0 or p1_action >= len(self._plays):
            raise ValueError("invalid offensive play index %d" % p1_action)
        if p2_action < 0 or p2_action >= len(self._plays[p1_action]):
            raise ValueError("invalid defensive play index %d" % p2_action)

        r = random.random()
        cumulative = self._prob[0]
        i = 0
        while r > cumulative and i + 1 < len(self._prob):
            cumulative += self._prob[i + 1]
            i += 1
        return self._plays[p1_action][p2_action][i]

    
    def simulate(self, policy, n):
        ''' Simulates games using the given policy and returns the
            winning percentage for the policy.

            policy -- a function from game positions to offensive actions
        '''
        wins = 0
        play_count = 0
        for i in range(n):
            pos = self.initial_position()
            while not self.game_over(pos):
                play_count += 1
                pos, _ = self.result(pos, policy(pos))
            if self.win(pos):
                wins += 1
        return wins / n
