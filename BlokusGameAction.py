from GameAction import GameAction
from BlokusGameConstants import LegalActionType

class BlokusGameAction(GameAction):
    '''
    Places a shape (actionType = LegatActionType.SHAPE, actionInfo = shapeVariation, actionInfoLocation = (row, column), actionLocation = (row, column) )
    or
    Passes the turn to the next player (actionType = LegalActionType.PASS)
    '''

    def __init__(self, actionType, actionInfo = None, actionInfoLocation = None, actionLocation = None):
        if actionType not in LegalActionType.valid():
            raise Exception("illegal action")
        
        self.type = actionType
        self.info = actionInfo
        self.infoLocation = actionInfoLocation
        self.location = actionLocation
    
    def __cmp__(self, other):
        return cmp((self.type, self.info, self.infoLocation, self.location), (other.type, other.info, other.infoLocation, other.location))
    
    def __hash__(self):
        return hash((self.type, self.info, self.infoLocation, self.location))
    
    def __str__(self):
        return  self.type + \
                (" , location on board: " + str(self.location) if self.location else "") + \
                (" , location on shape: " + str(self.infoLocation) if self.infoLocation else "") + \
                (" " + str(self.info) if self.info else "")
    
    def __repr__(self):
        return self.__str__()