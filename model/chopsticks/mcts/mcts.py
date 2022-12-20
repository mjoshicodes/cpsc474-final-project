from time import time
from random import shuffle, choice
from math import log


class MCTS():
    

    def __init__(self, time):
        self._time = time
        self._tree = {}


    def mcts_function(self, position):
        move = self.mcts_helper(position, self._time, self._tree)
        return move


    def exploit_value(self, tree, node):
        return tree[node][0] / tree[node][1]


    def explore_value(self, tree, node, successor):
        constant = 2 ** 0.5
        sqrt_value = (log(tree[node][1] + 1) / tree[successor][1]) ** 0.5
        return constant * sqrt_value


    def ucb(self, node, tree):
        successors = tree[node][3]
        optimal_node = None
        optimal_value = float("-inf") if node.actor() == 1 else float("inf")
        for node_successor in successors:
            node_exploit_value = self.exploit_value(tree, node_successor)
            node_explore_value = self.explore_value(tree, node, node_successor)
            if node.actor() == 1:
                current_ucb = node_exploit_value + node_explore_value
                if current_ucb > optimal_value:
                    optimal_value = current_ucb
                    optimal_node = node_successor
            else:
                current_ucb = node_exploit_value - node_explore_value
                if current_ucb < optimal_value:
                    optimal_value = current_ucb
                    optimal_node = node_successor
        return optimal_node


    def contains_node_to_visit(self, node, tree):
        for successor in tree[node][3]:
            if not successor in tree:
                return [True, successor]
        return [False, None]


    def traverse(self, root, tree):
        pointer_to_visit = root
        path = [root]
        hit = False
        while not hit:
            if pointer_to_visit.is_game_over():
                self.backtrack(path, pointer_to_visit.payoff(), tree)
                return
            hit, node_to_visit = self.contains_node_to_visit(pointer_to_visit, tree)
            if node_to_visit:
                pointer_to_visit = node_to_visit
            else:
                pointer_to_visit = self.ucb(pointer_to_visit, tree)
            path.append(pointer_to_visit)
        actions = pointer_to_visit.get_actions()
        shuffle(actions)
        successors = [pointer_to_visit.simulate_action(action) for action in actions]
        tree[pointer_to_visit] = [0, 0, actions, successors]
        payoff = self.simulate(pointer_to_visit)
        self.backtrack(path, payoff, tree)


    def simulate(self, node):
        while not node.is_game_over():
            actions = node.get_actions()
            node = node.simulate_action(choice(actions))
        return node.payoff()


    def backtrack(self, path, payoff, tree):
        for node in path:
            tree[node][0] += payoff
            tree[node][1] += 1


    def mcts_helper(self, position, duration, tree):
        start_time = time()
        if position not in tree:
            actions = position.get_actions()
            shuffle(actions)
            successors = [position.simulate_action(action) for action in actions]
            tree[position] = [0, 0, actions, successors]
        while time() - start_time <= duration:
            self.traverse(position, tree)
        optimal_action = None
        optimal_value = float("-inf") if position.actor() == 1 else float("inf")
        for i, action in enumerate(tree[position][2]):
            state = tree[position][3][i]
            if state in tree:
                root_exploit_value = self.exploit_value(tree, state)
                if (
                    (position.actor() == 1 and root_exploit_value > optimal_value) or
                    (position.actor() == 2 and root_exploit_value < optimal_value)
                ):
                    optimal_value = root_exploit_value
                    optimal_action = action
        return optimal_action
