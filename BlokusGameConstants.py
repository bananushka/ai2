TIE = 'TIE'
NO_LIMIT = -1

class BoardSize():
    
    FOURTEEN = 14
    TWENTY = 20

    @staticmethod
    def valid():
        return (BoardSize.FOURTEEN, BoardSize.TWENTY)

class Players():
    
    FIRST = 'FIRST'
    SECOND = 'SECOND'

    @staticmethod
    def valid():
        return (Players.FIRST, Players.SECOND)

class LegalActionType():
    
    SHAPE = 'S'
    PASS = 'P'
    
    @staticmethod
    def valid():
        return (LegalActionType.SHAPE, LegalActionType.PASS)

PURPLE = 'P'
ORANGE = 'O'
BLUE = 'B'
YELLOW = 'Y'
RED = 'R'
GREEN = 'G'

COLORS = {
    BoardSize.FOURTEEN: {
        Players.FIRST: (PURPLE, ),
        Players.SECOND: (ORANGE, )
    },
    BoardSize.TWENTY: {
        Players.FIRST: (BLUE, RED),
        Players.SECOND: (YELLOW, GREEN)
    }
}

ORDERED_SHAPES_MODE = True
NOT_ORDERED_SHAPES_MODE = False

#the options as explained in the assignment
GameOption = {
    1: (BoardSize.FOURTEEN, NOT_ORDERED_SHAPES_MODE, 420),
    2: (BoardSize.TWENTY, ORDERED_SHAPES_MODE, 180),
    3: (BoardSize.FOURTEEN, NOT_ORDERED_SHAPES_MODE, 180),
}