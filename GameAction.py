class GameAction:
    
    def __cmp__(self, other):
        '''
        The comparison method must be implemented to ensure deterministic results.
        @return: Negative if self < other, zero if self == other and strictly 
        positive if self > other.
        '''
        raise NotImplementedError()
    
    def __hash__(self):
        '''
        The hash method must be implemented for actions to be inserted into sets 
        and dictionaries.
        @return: The hash value of the action.
        '''
        raise NotImplementedError()
    
    def __str__(self):
        '''
        @return: The string representation of this object when *str* is called.
        '''
        raise NotImplementedError()
    
    def __repr__(self):
        '''
        Same as __str__, unless overridden.
        
        @return: The string representation of this object when *printed*.
        '''
        return self.__str__()