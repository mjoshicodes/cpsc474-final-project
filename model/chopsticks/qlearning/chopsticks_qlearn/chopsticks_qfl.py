import random
from collections import defaultdict
import time

class QLearn:
    def __init__(self, model, limit, possible_states):
        self.Q = [[[0 for k in range(possible_states)] for j in range(3)] for i in range(4)]
        self.alphas = [[[0.25 for k in range(possible_states)] for j in range(3)] for i in range(4)]
        self.eps = 0.2
        self.actions = possible_states
        self.model = model
        self.limit = limit

    def determine_bucket(self, new_state):
        yts, downsLeft, ytd, timeLeft  = new_state
        ytd_down = (ytd / downsLeft)
        yts_time = (yts / timeLeft)

        idx_0 = 0
        idx_1 = 0

        if ytd_down >= 6:
            idx_0 = 3
        elif ytd_down >= 2.51:
            idx_0 = 2
        elif ytd_down >= 2.49:
            idx_0 = 1
        else:
            idx_0 = 0
        
        if yts_time >= 3.75:
            idx_1 = 0
        elif yts_time >= 1.875:
            idx_1 = 1
        else:
            idx_1 = 2
        
        return idx_0, idx_1

    def update(self, state, action, reward):
        i, j = self.determine_bucket(state)
        self.Q[i][j][action] += self.alphas[i][j][action] * (reward - self.Q[i][j][action])
        self.alphas[i][j][action] *= 0.9999
    
    def choose_action(self, state):
        # find bucket for state - eps greedy method
        best_action = 0
        p = random.random()
        if p < self.eps:
            best_action = random.randint(0, 2)
        else:
            reward, best_action = self.choose_best_action(state)
        new_state, _ = self.model.result(state, best_action)
        
        return new_state, best_action
    
    def choose_best_action(self, state):
        # find best action
        i, j = self.determine_bucket(state)
        max_reward = -10
        best_action = 0
        for action in range(self.actions):
            value = self.Q[i][j][action]
            if value > max_reward:
                best_action = action
                max_reward = value
        return max_reward, best_action
    
    def q_learning(self):
        time_start = time.time()
        counter = 0
        while time.time() - time_start < self.limit:
            counter += 1
            # print("counter", counter)
            state = self.model.initial_position()
            while self.model.game_over(state) == False:
                # choose an action - greedy or epsilon
                i, j = self.determine_bucket(state)
                new_state, action = self.choose_action(state)

                # check if new_state is a terminal state
                reward = 0
                if self.model.game_over(new_state) == True:
                    reward = 1 if self.model.win(new_state) else -1
                else:
                    reward, _ = self.choose_best_action(new_state)
                self.Q[i][j][action] += self.alphas[i][j][action] * (reward - self.Q[i][j][action])
                self.alphas[i][j][action] *= 0.9999
                state = new_state

def q_learn(model, limit):
    "Returns a function that takes a non-terminal position in the game"

    # Multiplying limit to deal with warning
    q = QLearn(model, limit * .9999, model.p1_action_size())
    q.q_learning()

    def policy(pos):

        """Returns index of selected offensive play"""
        best_action = 1
        return best_action
        # _, best_action = q.choose_best_action(pos)
        # return best_action

    return policy

