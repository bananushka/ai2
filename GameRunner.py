from time import clock
from BlokusGameConstants import NO_LIMIT

class GameRunnerException(Exception):
    pass

class TimeLimitException(GameRunnerException):
    
    def __init__(self, player):
        self.player = player

    def __str__(self):
        return self.player + ' player failed to finish on time'

    def __repr__(self):
        return self.__str__()

class IllegalMoveException(GameRunnerException):

    def __init__(self, player, action):
        self.player = player
        self.action = action

    def __str__(self):
        return self.player + ' made an illegal move - ' + str(self.action)

    def __repr__(self):
        return self.__str__()

class GameRunner():
    '''
    Runs a game.
    '''
    
    def __init__(self, initialState, agents, timeLimit = NO_LIMIT):
        '''
        Constructor.
        
        @param initialState: The initial game state.
        @param agents: A dictionary that maps players to their agents.
        @param timeLimit: game's time limit of each agent.
        '''
        self.initialState = initialState
        self.agents = agents
        self.timeLimit = timeLimit
        self.agentsPlayedTime = {}        
        
    def run(self):
        '''
        Runs the game. Prints actions and states.
        
        @return: The game's winner.
        '''
        for player, agent in self.agents.items():
            start = clock()
            agent.setup(player, self.initialState, self.timeLimit)
            setupTime = clock() - start
            for _agent in self.agents.values():
                self.agentsPlayedTime[_agent] = setupTime
            if self.timeLimit != NO_LIMIT and self.agentsPlayedTime[agent] > self.timeLimit:
                raise TimeLimitException(player)
        
        state = self.initialState

        while state.getWinner() is None:
            agent = self.agents[state.getCurrentPlayer()]

            start = clock()
            action = agent.move(state)
            self.agentsPlayedTime[agent] += clock() - start
            if self.timeLimit != NO_LIMIT and self.agentsPlayedTime[agent] > self.timeLimit:
                raise TimeLimitException(state.getCurrentPlayer())
            
            successors = state.getSuccessors()
            if action not in successors.keys():
                raise IllegalMoveException(state.getCurrentPlayer(), action)

            #print str(state.currentPlayer) + " player\'s move: " + str(action)

            state = successors[action]
            
            if state.getWinner() is None:
                #print state
                pass
        

        for player, agent in self.agents.items():
            print agent.turnNumber

        return state
