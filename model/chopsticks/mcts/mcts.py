from time import time
from random import choice
from math import log


class Position:

    def __init__(self, p1_hands, p2_hands, actor) -> None:
        self._p1_hands = p1_hands
        self._p2_hands = p2_hands


def mcts_policy(time):
    tree = {}
    def mcts_function(position):
        move = mcts_helper(position, time, tree)
        return move
    return mcts_function


def exploit_value(tree, node):
    return tree[node][0] / tree[node][1]


def explore_value(tree, node, successor):
    constant = 2 ** 0.5
    sqrt_value = (log(tree[node][1] + 1) / tree[successor][1]) ** 0.5
    return constant * sqrt_value


def ucb(node, tree):
    successors = tree[node][3]
    optimal_node = None
    optimal_value = float("-inf") if node.actor() == 0 else float("inf")
    for node_successor in successors:
        node_exploit_value = exploit_value(tree, node_successor)
        node_explore_value = explore_value(tree, node, node_successor)
        if node.actor() == 0:
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


def contains_node_to_visit(node, tree):
    for successor in tree[node][3]:
        if not successor in tree:
            return [True, successor]
    return [False, None]


def traverse(root, tree):
    pointer_to_visit = root
    path = [root]
    hit = False
    while not hit:
        if pointer_to_visit.is_terminal():
            backtrack(path, pointer_to_visit.payoff(), tree)
            return
        hit, node_to_visit = contains_node_to_visit(pointer_to_visit, tree)
        if node_to_visit:
            pointer_to_visit = node_to_visit
        else:
            pointer_to_visit = ucb(pointer_to_visit, tree)
        path.append(pointer_to_visit)
    actions = pointer_to_visit.get_actions()
    successors = [pointer_to_visit.successor(action) for action in actions]
    tree[pointer_to_visit] = [0, 0, actions, successors]
    payoff = simulate(pointer_to_visit)
    backtrack(path, payoff, tree)


def simulate(node):
    while not node.is_terminal():
        actions = node.get_actions()
        node = node.successor(choice(actions))
    return node.payoff()


def backtrack(path, payoff, tree):
    for node in path:
        tree[node][0] += payoff
        tree[node][1] += 1


def mcts_helper(position, duration, dictionary):
    # Get current time
    start_time = time()
    # Establish the treev
    if not position in dictionary:
        actions = position.get_actions()
        successors = [position.successor(action) for action in actions]
        dictionary[position] = [0, 0, actions, successors]
    while time() - start_time <= duration:
        traverse(position, dictionary)
    optimal_action = None
    optimal_value = float("-inf") if position.actor() == 0 else float("inf")
    for i, action in enumerate(dictionary[position][2]):
        state = dictionary[position][3][i]
        if state in dictionary:
            root_exploit_value = exploit_value(dictionary, state)
            if (
                (position.actor() == 0 and root_exploit_value > optimal_value) or
                (position.actor() == 1 and root_exploit_value < optimal_value)
            ):
                optimal_value = root_exploit_value
                optimal_action = action
    return optimal_action

# UCB 2
# Edge dictionary: Key is edge,
# next node to visit,
