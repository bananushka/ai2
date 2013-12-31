from time import clock
from GameAgent import GameAgent
from BlokusGameAction import BlokusGameAction
from AlphaBeta import AlphaBetaSearch
from BlokusGameConstants import TIE, NO_LIMIT

#make it False if you don't want to cutoff the alpha beta by time (and remove the iterative deepening respectively in the move method)
CHECK_TIME = True

WIN_VALUE = 10000
TIE_VALUE = 0
LOSE_VALUE = -WIN_VALUE

class BlokusGameAgentException(Exception):
     
    def __init__(self, reason):
        self.reason = reason
        
    def __str__(self):
        return self.reason
    
    def __repr__(self):
        return self.__str__()

class BlokusGameAgentExample(GameAgent):

    #the fixedDepth will be used as the desired search depth, when there is no time limit.
    #if you wish to use this agent in your experiments, you can inherit from this class and set the fixedDepth with a parameter given to the constructor
    def __init__(self, depth):
        self.fixedDepth = depth
    
    #if you want to know in which mode you are you can find it in state.orderedShapesMode
    def setup(self, player, state, timeLimit):
        start = clock()
        self.turnNumber = 0
        self.player = player
        self.alphaBeta = AlphaBetaSearch(self.player, \
                                         lambda state: self.utility(state), \
                                         lambda : self.noMoreTime())
        self.timeLimit = timeLimit            
        if (timeLimit != NO_LIMIT):
            self._turnTimeLimit = (timeLimit - 5.0) / (state.numOfShapes * len(state.currentPlayer.colors))
            self.timeLimit -= 1
        
        self.timePlayed = clock() - start

    @property
    def turnTimeLimit(self):
        return self._turnTimeLimit
    
    def move(self, state):
        self.startTime = clock()
        self.currentState = state
        self.turnNumber += 1
        
        #if there is no time limit - its a fixed depth search
        if (self.timeLimit == NO_LIMIT): 
            
            (bestAction, _) = self.alphaBeta.search(self.fixedDepth, state) #returns (action, value)
            
        #otherwise - its an iterative deepening within the time limitation
        else:
            
            bestAction = BlokusGameAction("P")
            depth = 1
            if (self.timeLimit - self.timePlayed > self.turnTimeLimit):
        
                retval = (bestAction,TIE_VALUE)
                while (retval is not None):
        
                    retval = self.alphaBeta.search(depth, state) #returns (action, value) 
                    if retval is not None:
                        bestAction = retval[0]
                        if (retval[1] == WIN_VALUE):
                            retval = None
                        else:
                            depth += 1
                    else:
                        depth -= 1
        
#            print "depth: " + str(depth)
    
        timePlayed = clock() - self.startTime
#        print timePlayed
        self.timePlayed += timePlayed
        
        return bestAction
    
    def utility(self, state):
 
        winner = state.getWinner()

        if winner is None:
            retval = self.heuristic(state)
        elif winner == self.player:
            retval = WIN_VALUE
        elif winner == TIE:
            retval = TIE_VALUE
        else:
            retval = LOSE_VALUE            
        
        return retval

    def heuristic(self, state):
        return (state.currentPlayer.getScore() - state.opponentPlayer.getScore()) if (self.player == state.getCurrentPlayer()) else (state.opponentPlayer.getScore() - state.currentPlayer.getScore())
        
    def noMoreTime(self):
        return True if (CHECK_TIME and (self.timeLimit != NO_LIMIT) and (clock() - self.startTime > self.turnTimeLimit)) else False
