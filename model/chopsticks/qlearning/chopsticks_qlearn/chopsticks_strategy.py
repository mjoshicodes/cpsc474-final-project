import random
from chopsticks import Game

class ChopsticksStrategy:
    def __init__(self):
        ''' Creates a game using the given list of possible outcomes
            and the given probability distribution of those outcomes.

            plays -- a list of lists of (yards-gained, ticks-elapsed, turnover)
                     tuples indexed by offensive action then defensive action
            prob -- a probability distribution over the tuples in plays[o][d]
        '''
        self._game = Game()


    def get_all_moves(self, player):
        """ Returns a list of all possible moves given the player"""
        actions = self._game.get_actions_player(player)
        return actions

    def initial_position(self):
        ''' Returns the initial position in this game as a
            (p1_left_hand, p1_right_hand, p2_left_hand, p2_right_hand) tuple.
        '''
        return self._game.return_position()


    def p1_action_size(self):
        ''' Returns the number of current player (p1) actions available in this game. '''
        # get game p1
        return len(self.get_all_moves(self._game.p1))


    def p2_action_size(self):
        ''' Returns the number of other player (p2) actions available in this game. '''

        # get game p2
        return len(self.get_all_moves(self._game.p2))
    
    
    def result(self, p1_index):
        ''' Executes selected play and chooses a random play for p2 to execute
        
            Returns the position that results from the given offensive play
            selection from the given position as a
            (field-position, downs-left, distance, ticks) tuple, and the outcome
            of that play as a (yards-gained, ticks-elapsed, turnover) tuple.

            pos -- a tuple (field_pos, downs_left, distance, time_in_ticks)
            offensive_play -- the index of an offensive play
        '''
        print("p1_index", p1_index)
        p1_actions = self.get_all_moves(self._game.p1)
        p1_play = p1_actions[p1_index]

        # print("chose to play action", p1_play)

        # execute p1 move
        self._game.execute_action(self._game.p1, self._game.p2, p1_play)

        # print("result after p1 action", self._game.return_position())

        # choose random p2 move
        p2_actions = self.get_all_moves(self._game.p2)
        p2_size = len(p2_actions) - 1
        # print("P2 SIZE", p2_size)
        if p2_size > 0:
            p2_random_action = random.randint(0, p2_size)
            p2_play = p2_actions[p2_random_action]
            #play p2
            # print("P2 chose to play action", p2_play)
            self._game.execute_action(self._game.p2, self._game.p1, p2_play)
            # print("result after p2 action", self._game.return_position())
        # return the position of the game
        return self._game.return_position()
    
    def game_over(self):
        ''' Determines if the given position represents a game-over position.
        
            pos -- a tuple (field_pos, down, distance, time)
        '''
        return self._game.is_game_over()

    def game_over_pos(self, pos):
        p1_l, p1_r, p2_l, p2_r = pos
        if (p1_l <= 0 and p1_r <= 0) or (p2_l <= 0 and p2_r <= 0):
            return True
        else:
            return False


    def win(self):
        ''' Determines if the given position represents a game-won position.
        
            pos -- a tuple (field_pos, down, distance, time)
        '''
        return self._game.p2.lost()
    
    def win_pos(self, pos):
        _, _, p2_l, p2_r = pos
        if p2_l <= 0 and p2_r <= 0:
            return True
        else:
            return False

    def simulate(self, policy, n):
        ''' Simulates games using the given policy and returns the
            winning percentage for the policy.

            policy -- a function from game positions to offensive actions
        '''
        wins = 0
        play_count = 0
        for i in range(n):
            # pos = self.initial_position()
            while not self.game_over():
                pos = self._game.return_position()
                play_count += 1
                self.result(policy(pos))
            if self.win():
                wins += 1
        return wins / n

if __name__ == "__main__":
    strategy = ChopsticksStrategy()
    print(strategy.initial_position())
