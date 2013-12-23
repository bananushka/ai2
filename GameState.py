class GameState:
    
    def getSuccessors(self):
        '''
        Generates all the actions that can be performed from this state, and
        the States those actions will create.
        
        @return: A dictionary containing each action as a key, and its state.
        '''
        raise NotImplementedError()

    def getAllPlayers(self):
        '''
        @return: A list of all the players in the game.
        '''
        raise NotImplementedError()
    
    def getCurrentPlayer(self):
        '''
        @return: The player that should play next.
        '''
        raise NotImplementedError()
    
    def getWinner(self):
        '''
        @return: The winner of the game, according to this state. 
        Returns None if this state is not terminal.
        '''
        raise NotImplementedError()
    
    def getTurnsLeft(self):
        '''
        @return: The number of turns left before the game ends.
        None is returned if the game is unlimited.
        '''
        raise NotImplementedError()
    
    def __cmp__(self, other):
        '''
        The comparison method must be implemented to ensure deterministic results.
        @return: Negative if self < other, zero if self == other and strictly 
        positive if self > other.
        '''
        raise NotImplementedError()
    
    def __hash__(self):
        '''
        The hash method must be implemented for states to be inserted into sets 
        and dictionaries.
        @return: The hash value of the state.
        '''
        raise NotImplementedError()
    
    def __str__(self):
        raise NotImplementedError()
    
    def __repr__(self):
        return self.__str__()