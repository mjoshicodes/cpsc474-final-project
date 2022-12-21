from time import time
from random import shuffle, choice
from math import log


class MCTS():
    

    def __init__(self, time):
        """
            Creates a tree to be searched while conducting our game of Chopsticks.

            time -- Amount of time in seconds allotted to searching the tree.
        """
        self._time = time
        self._tree = {}


    def mcts_function(self, position):
        """
            Returns the best move to make, given the current game position.

            position -- A current Chopsticks game state.
        """
        move = self.mcts_helper(position, self._time, self._tree)
        return move


    def exploit_value(self, tree, node):
        """
            Returns the exploit parameter of the UCB value.

            tree -- The chopsticks tree being searched.\n
            node -- The node, which corresponds to a game position.
        """
        return tree[node][0] / tree[node][1]


    def explore_value(self, tree, node, successor):
        """
            Returns the explore parameter of the UCB value.

            tree -- The chopsticks tree being searched.\n
            node -- The node, which corresponds to a game position.\n
            successor -- A child of the current node, which also corresponds to a game position.
        """
        constant = 2 ** 0.5
        sqrt_value = (log(tree[node][1] + 1) / tree[successor][1]) ** 0.5
        return constant * sqrt_value


    def ucb(self, node, tree):
        """
            Returns the best child node to go to from the current node with respect
            to each child's UCB value.

            tree -- The chopsticks tree being searched.\n
            node -- The node, which corresponds to a game position.
        """
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
        """
            Returns whether or not there is a child of the 
            current node that has yet to be visited in the tree yet, 
            as well as the corresponding successor if it exists.

            tree -- The chopsticks tree being searched.\n
            node -- The node, which corresponds to a game position.
        """
        for successor in tree[node][3]:
            if not successor in tree:
                return [True, successor]
        return [False, None]


    def traverse(self, root, tree):
        """
            Conducts a tree search from the root. 
            Chooses nodes to visit until it hits an unvisited node or a terminal state, 
            then updates payoff and visit values for each node searched in that iteration.

            root -- The root of the tree, which corresponds to a game position.\n
            tree -- The chopsticks tree being searched.
        """
        pointer_to_visit = root
        path = [root]
        hit = False
        while not hit:
            if pointer_to_visit.is_game_over():
                self.backpropogate(path, pointer_to_visit.payoff(), tree)
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
        self.backpropogate(path, payoff, tree)


    def simulate(self, node):
        """
            Randomly explores children nodes of the current node until we 
            hit a terminal state, then return the terminal position's payoff.

            node -- The current node, which corresponds to a current game position.
        """
        while not node.is_game_over():
            actions = node.get_actions()
            node = node.simulate_action(choice(actions))
        return node.payoff()


    def backpropogate(self, path, payoff, tree):
        """
            Goes through each node in the just-searched path of the tree, 
            updating it with payoff as well as incrementing its number of visits.

            path -- A list of nodes that was just searched within the tree.\n
            payoff -- The reward each node will get for searching\n
            tree -- The chopsticks tree being searched.
        """
        for position in path:
            tree[position][0] += payoff
            tree[position][1] += 1


    def mcts_helper(self, position, duration, tree):
        """
            Helper function that conducts MCTS. Returns the optimal action to take from the given Chopsticks game position.

            position -- The current game position.\n
            duration -- Time alloted for conducting tree search.\n
            tree -- The chopsticks tree being searched.
        """
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
