import random
from chopsticks import Game
import greedy_ql

class ChopsticksStrategy:
    def __init__(self):
        ''' Creates a game using the given list of possible outcomes
            and the given probability distribution of those outcomes.

            plays -- a list of lists of (yards-gained, ticks-elapsed, turnover)
                     tuples indexed by offensive action then defensive action
            prob -- a probability distribution over the tuples in plays[o][d]
        '''
        self._game = Game()
    
    def reset_game(self):
        self._game = Game()
    
    def get_all_actions_p1(self):
        actions = []
        moves = ['ATTACK', 'DIVIDE', 'SPLIT']
        for left_hand in range(0, 5):
            for right_hand in range(0, 5):
                for move in moves:
                    actions.append((move, left_hand, right_hand))
        return actions


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
    
    def greedy_result(self, p1_play):
        
        self._game.execute_action(self._game.p1, self._game.p2, p1_play)

        # selecting a random valid move to p2
        p2_actions = self.get_all_moves(self._game.p2)
        p2_size = len(p2_actions) - 1
        if p2_size > 0:
            p2_play = greedy_ql.get_greedy_action(p2_actions, self._game.p2, self._game.p1)
            self._game.execute_action(self._game.p2, self._game.p1, p2_play)
        
        return self._game.return_position()

    
    
    def result(self, p1_play):
        ''' Executes selected play and chooses a random play for p2 to execute
        
            Returns the position that results from the given offensive play
            selection from the given position as a
            (field-position, downs-left, distance, ticks) tuple, and the outcome
            of that play as a (yards-gained, ticks-elapsed, turnover) tuple.

            pos -- a tuple (field_pos, downs_left, distance, time_in_ticks)
            offensive_play -- the index of an offensive play
        '''
        # execute p1 move
        self._game.execute_action(self._game.p1, self._game.p2, p1_play)

        # selecting a random valid move to p2
        p2_actions = self.get_all_moves(self._game.p2)

        p2_size = len(p2_actions) - 1
        if p2_size > 0:
            p2_random_action = random.randint(0, p2_size)
            p2_play = p2_actions[p2_random_action]
            self._game.execute_action(self._game.p2, self._game.p1, p2_play)

        # return the position of the game
        return self._game.return_position()

    def p2_greedy(self, actions):
        best_p2_move = None
        best_reward = -10

        # current state space
        old_left_hand = self._game.p2.left_hand()
        old_right_hand = self._game.p2.right_hand()
        opponent_left_hand = self._game.p1.left_hand()
        opponent_right_hand = self._game.p1.right_hand()
        
        for action in actions:
            move, left_hand, right_hand = action
            if move == "ATTACK":
                attacked_hand = opponent_left_hand if right_hand == 1 else opponent_right_hand
                resulting_attack_value = (left_hand + attacked_hand) % 5
                reward = 0
                if resulting_attack_value == 0:
                    reward = 1
                elif (5 - resulting_attack_value) == left_hand or (5 - resulting_attack_value) == right_hand:
                    reward = -1
                else:
                    reward = 0
                if reward >= best_reward:
                    best_reward = reward
                    best_p2_move = action
            elif move == "DIVIDE":
                reward = 0 
                if left_hand + opponent_left_hand == 5 or left_hand + opponent_right_hand == 5 or right_hand + opponent_left_hand == 5 or right_hand + opponent_right_hand == 5:
                    reward -= 1
                elif old_left_hand + opponent_left_hand == 5 or old_left_hand + opponent_right_hand == 5 or old_right_hand + opponent_left_hand == 5 or old_right_hand + opponent_right_hand == 5:
                    reward += 1
                if reward >= best_reward:
                    best_reward = reward
                    best_p2_move = action
            elif move == "SPLIT":
                reward = 0
                if left_hand + opponent_left_hand == 5 or left_hand + opponent_right_hand == 5 or right_hand + opponent_left_hand == 5 or right_hand + opponent_right_hand == 5:
                    reward -= 1
                if old_left_hand + opponent_left_hand == 5 or old_left_hand + opponent_right_hand == 5 or old_right_hand + opponent_left_hand == 5 or old_right_hand + opponent_right_hand == 5:
                    reward += 1
                if reward >= best_reward:
                    best_reward = reward
                    best_p2_move = action
        return best_p2_move
    
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
        # print("im simulate with n", n)
        wins = 0
        play_count = 0
        for i in range(n):
            # print("running game", i)
            self.reset_game()
            while not self.game_over():
                pos = self._game.return_position()
                play_count += 1
                self.result(policy(pos))
            # print(self._game.return_position())
            if self.win():
                wins += 1
        return wins / n
    
    def simulate_greedy(self, policy, n):
        ''' Simulates games using the given policy and returns the
            winning percentage for the policy.

            policy -- a function from game positions to offensive actions
        '''
        # print("im simulate with n", n)
        wins = 0
        play_count = 0
        for i in range(n):
            # print("running game", i)
            self.reset_game()
            while not self.game_over():
                pos = self._game.return_position()
                play_count += 1
                self.greedy_result(policy(pos))
            # print(self._game.return_position())
            if self.win():
                wins += 1
        return wins / n