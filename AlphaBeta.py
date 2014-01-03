# A bloody large number.
INFINITY = 1.0e400

class AlphaBetaSearch:
    '''
    This search algorithm implements the limited-resource minimax tree search 
    algorithm with alpha-beta pruning for zero-sum games. This version cuts off 
    search by depth alone and uses an evaluation function (utility).
    '''
    
    def __init__(self, player, utility, noMoreTime, ordering=lambda s, x: x, \
            deepening=lambda s, d, o: None):
        '''
        Constructor.
        
        @param player: Your player. This search algorithm will choose the best
                       actions for this player.
        @param utility: An evaluation function for states.
        @param noMoreTime: A cutoff function for time limit.
        '''
        self.player = player
        self.utility = utility
        self.noMoreTime = noMoreTime
        self.ordering = ordering
        self.deepening = deepening
    
    def search(self, maxDepth, currentState):
        '''
        Search game to determine best action; use alpha-beta pruning.
        
        @param maxDepth: The depth of the search tree.
        @param currentState: The current game state to start the search from.
        '''
        self.maxDepth = maxDepth

        bestValue = -INFINITY
        bestAction = None
        
        successors = currentState.getSuccessors().iteritems()
        successors = self.ordering(currentState, successors)
        for action, state in successors:
            valueFunction = self.__getValueFunction(state)
            value = valueFunction(state, bestValue, INFINITY, 1)
            if value is None: return None
            if (value > bestValue):
                bestValue = value
                bestAction = action
        
        return (bestAction, bestValue)
    
    def __getValueFunction(self, state):
        if state.getCurrentPlayer() == self.player:
            return self.__maxValue
        else:
            return self.__minValue
    
    def __cutoffTest(self, state, depth):
        overdepth = self.maxDepth - depth
        winner = state.getWinner()
        if winner is not None:
            return True
        
        selective = self.deepening(state, depth, overdepth)
        
        if selective is None:
            return depth >= self.maxDepth or (state.getWinner() is not None)

        return selective
    
    def __maxValue(self, state, alpha, beta, depth):
        
        if self.noMoreTime():
            return None
        
        if self.__cutoffTest(state, depth):
            return self.utility(state)
        
        value = -INFINITY        
        successors = state.getSuccessors().iteritems()
        successors = self.ordering(state, successors)
        for _ , successor in successors:
            valueFunction = self.__getValueFunction(successor)
            tempVal = valueFunction(successor, alpha, beta, depth + 1)
            if tempVal is None: return None
            value = max(value, tempVal)
            if value >= beta:
                return value
            alpha = max(alpha, value)

        return value
    
    def __minValue(self, state, alpha, beta, depth):

        if self.noMoreTime():
            return None

        if self.__cutoffTest(state, depth):
            return self.utility(state)
        
        value = INFINITY

        successors = state.getSuccessors().iteritems()
        successors = self.ordering(state, successors)
        for _ , successor in successors:
            valueFunction = self.__getValueFunction(successor)
            tempVal = valueFunction(successor, alpha, beta, depth + 1)
            if tempVal is None: return None
            value = min(value, tempVal)
            if value <= alpha:
                return value
            beta = min(beta, value)
        
        return value
