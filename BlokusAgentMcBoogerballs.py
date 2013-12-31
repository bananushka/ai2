from BlokusGameAgentExample import BlokusGameAgentExample
from BlokusAgentSimple import BlokusAgentSimple
from BlokusGameUtils import getIndexesOfTurnedOnBits, getBinaryShapeCorners

class TimeManagement:
    MORE_TIME_AT_THE_END = 1
    ACCORDING_TO_OPEN_CORNERS = 2
    MORE_TIME_AT_THE_BEGINNING = 4

class SelectiveDeepening:
    OPPONENT_PASSED = 1
    HIGH_HEURISTICS = 2
    SKIP_FIRST = 4
    PROXIMITY_TO_OPPONENT = 8

class ChildrenOrdering:
    MOST_CORNERS = 1

class Heuristics:
    SCORE = 1
    CORNERS = 2
    CORNERS_TIMES_SQUARES = 4


class BlokusAgentMcBoogerballs(BlokusAgentSimple):
    def __init__(self, depth=2, heuristicType=0, timeManagement=0, \
            selectiveDeepening=0,\
            childrenOrdering=0):
        self.fixedDepth = depth
        self.heuristicType = heuristicType
        self.timeManagement = timeManagement
        self.selectiveDeepening = selectiveDeepening
        self.childrenOrdering = childrenOrdering

    def heuristic(self, state):
        score = 0
        if self.heuristicType & Heuristics.SCORE:
            score += BlokusGameAgentExample.heuristic(self, state)
        if self.heuristicType & Heuristics.CORNERS:
            score += availableCorners(state)
        if self.heuristicType & Heuristics.CORNERS_TIMES_SQUARES:
            score += availableCorners(state) * \
                    averageSquaresInHand(state.currentPlayer.getCurrentColor())

        return score

    @property
    def turnTimeLimit(self):
        if self.timeManagement & TimeManagement.MORE_TIME_AT_THE_END:
            if self.turnNumber <= 6:
                return self._turnTimeLimit / 1.5
            else:
                return self._turnTimeLimit * 1.5

        if self.timeManagement & TimeManagement.MORE_TIME_AT_THE_BEGINNING:
            if self.turnNumber <= 8:
                return self._turnTimeLimit * 2
            else:
                return self._turnTimeLimit

        return self._turnTimeLimit

def availableCorners(state):
    currentColor = state.currentPlayer.getCurrentColor()

    currentBoard = currentColor.boardBinary
    currentBoardNeighbours = (currentBoard >> 1) | (currentBoard << 1) \
            | (currentBoard >> state.boardSizeWithBorder) \
            | (currentBoard << state.boardSizeWithBorder)
    opponentBoards = 0
    for color in state.currentPlayer.colors:
        if not (color == currentColor):
            opponentBoards |= color.boardBinary
    for color in state.opponentPlayer.colors:
        opponentBoards |= color.boardBinary
    freeSquares = ~(currentBoard | currentBoardNeighbours | \
            opponentBoards | state.border)

    #first move allowed only in board's corners
    availableSquaresToPlay = state.boardCorners

    #if not first move - the board isn't empty
    if currentBoard:
        availableSquaresToPlay = \
                getBoardDiagonalsToCorners(state, currentBoard)

    availableSquaresToPlay = availableSquaresToPlay & freeSquares

    availableSquaresIndexes = \
            getIndexesOfTurnedOnBits(availableSquaresToPlay)
    return len(availableSquaresIndexes)

def getBoardDiagonalsToCorners(state, currentBoard):
    boardCorners = getBinaryShapeCorners(currentBoard, state.boardSizeWithBorder) 
    
    #now choose available squares that a new shape can be placed at
    boardDiagonalsToCorners =   (boardCorners >> state.boardSizeWithBorder + 1) | \
                                (boardCorners >> state.boardSizeWithBorder - 1) | \
                                (boardCorners << state.boardSizeWithBorder + 1) | \
                                (boardCorners << state.boardSizeWithBorder - 1) 
    return boardDiagonalsToCorners

def averageSquaresInHand(color):
    return sum([shape.numOfSquares for shape in color.shapes]) / \
            float(len(color.shapes))

