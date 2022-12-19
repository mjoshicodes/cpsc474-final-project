def play(inputState, startingPlayer):
    # Getting initial values
    startNode = GameState(inputState, startingPlayer)
    alreadySolvedStates = {}
    stateQueue = Queue()
    stateQueue.put(startNode)

    while not stateQueue.empty():
        currentState = stateQueue.get()
        if isinstance(currentState, ExploredState):
            continue

        if checkForWin(currentState.getState()):
            currentState.setWinner(not currentState.isPlayer())
            continue

        possibleStates = getFollowingMoves(currentState)
        for state in possibleStates:
            if (state, not currentState.isPlayer()) in alreadySolvedStates:
                currentState.addChildren(ExploredState(
                    alreadySolvedStates[(state, not currentState.isPlayer())]))
            else:
                newNodeState = GameState(state, not currentState.isPlayer())
                newNodeState.setParent(stateQueue)
                currentState.addChildren(newNodeState)
                alreadySolvedStates[(
                    state, not currentState.isPlayer())] = newNodeState

                stateQueue.put(newNodeState)

    return startNode


def negamax(node, depth, player):
    if depth > 22:
        return 0
    if isinstance(node, ExploredState):
        node = node.state
    if node.winner != None:
        if node.winner == player:
            node.setEvaluatedValue(20 - depth)
            return 20 - depth
        node.setEvaluatedValue(-20 + depth)
        return -20 + depth
    value = -1000
    bestMove = None
    for child in node.getChildren():
        checkValue = -negamax(child, depth + 1, not player)
        if checkValue > value:
            bestMove = child
            value = checkValue
    node.setEvaluatedValue(value)
    return value
