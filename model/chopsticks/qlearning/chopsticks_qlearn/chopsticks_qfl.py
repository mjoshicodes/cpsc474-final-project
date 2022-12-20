import random
from collections import defaultdict
import time

class QLearn:
    def __init__(self, model, limit, possible_states, possible_actions):
        self.Q = dict([(action, 0) for action in possible_actions])
        # self.Q = [[[.1 for k in range(possible_states)] for j in range(possible_states)] for i in range(possible_states)]
        self.alphas = dict([(action, 0.25) for action in possible_actions])
        # self.alphas = [[[0.25 for k in range(possible_states)] for j in range(possible_states)] for i in range(possible_states)]
        self.eps = 0.2
        self.actions = possible_states
        self.model = model
        self.limit = limit
    
    def choose_action(self, state):
        # find bucket for state - eps greedy method
        actions = self.model._game.get_actions_given_state(state)
        print("CHOOSE ACTIONS FOR STATE", state, actions)
        best_action = 0
        p = random.random()
        print("prob", p)
        if p < self.eps:
            best_action_idx = random.randint(0, len(actions) - 1)
            best_action = actions[best_action]
        else:
            reward, best_action = self.choose_best_action(state)
        print("BEST ACTION GIVEN", best_action)
        new_state = self.model.result(best_action)
        
        return new_state, best_action
    
    def choose_best_action(self, state):
        # choose best action
        actions = self.model._game.get_actions_given_state(state)
        max_reward = -10
        best_action = 0
        for action in actions:
            value = self.Q[action]
            if value > max_reward:
                best_action = action
                max_reward = value
        print("max reward", max_reward)
        # print("best action", best_action)
        return max_reward, best_action
    
    def update(self, action, reward):
        self.Q[action] += self.alphas[action] * (reward - self.Q[action])
        self.alphas[action] *= 0.9999
        print("updated to ", self.Q[action], "with alpha", self.alphas[action])
    
    def q_learning(self):
        time_start = time.time()
        counter = 0
        while time.time() - time_start < self.limit:
            counter += 1
            state = self.model.initial_position()
            while self.model.game_over_pos(state) == False:
                # choose an action - greedy or epsilon
                new_state, action = self.choose_action(state)
                # check if new_state is a terminal state
                reward = 0
                print("current state", state)
                print("new state", new_state)
                if self.model.game_over_pos(state) == True:
                    print("new state is terminal")
                    reward = 1 if self.model.win_pos(new_state) else -1
                else:
                    reward, _ = self.choose_best_action(new_state)
                self.update(action, reward)
                state = new_state

def q_learn(model, limit):
    "Returns a function that takes a non-terminal position in the game"

    # Multiplying limit to deal with warning
    q = QLearn(model, limit * .9999, model.p1_action_size(), model.get_all_actions_p1())

    q.q_learning()

    def policy(pos):

        """Returns index of selected offensive play"""
        # best_action = 1
        # return best_action
        _, best_action = q.choose_best_action(pos)
        print("best action", best_action)
        return best_action

    return policy

