class GameAgent ():
    '''
    This is an interface for a Game Playing Agent.
    '''
    
    def move(self, gameState):
        '''
        This is the method called by the runner of this agent.
        It includes the code that decides the next move.
        
        @param gameState: The current game state.
        @return: The GameAction that the agent will execute in its next move.
        '''
        raise NotImplementedError()
    
    def setup(self, player, gameState, timeLimit):
        '''
        This is method is called once at the beginning of the game, 
        and enables the agent to prepare for things to come.
        
        @param player: Your player.
        @param gameState: The initial game state.
        @param timeLimit: The time that will be allocated for a game.
        '''
        raise NotImplementedError()
