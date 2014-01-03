from BlokusGameAgentExample import BlokusGameAgentExample
from BlokusAgentSimple import BlokusAgentSimple
from BlokusGameUtils import getIndexesOfTurnedOnBits, \
                            getBinaryShapeCorners, \
                            getBoardCorners, \
                            binaryBoardToArray

from AlphaBeta import AlphaBetaSearch

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
    HEURISTIC = 1
    MOST_CORNERS = 2

class Heuristics:
    SCORE = 1
    CORNERS = 2
    CORNERS_TIMES_SQUARES = 4
    ALL_CORNERS = 8
    OPPOSING_CORNERS = 16


class BlokusAgentMcBoogerballs(BlokusAgentSimple):
    def __init__(self, depth=2, heuristicType=0, timeManagement=0, \
            selectiveDeepening=0,\
            childrenOrdering=0):
        self.fixedDepth = depth
        self.heuristicType = heuristicType
        self.timeManagement = timeManagement
        self.selectiveDeepening = selectiveDeepening
        self.childrenOrdering = childrenOrdering

    def setup(self, player, state, timeLimit):
        BlokusGameAgentExample.setup(self, player, state, timeLimit)

        self.alphaBeta = AlphaBetaSearch(self.player, \
                                         lambda state: self.utility(state), \
                                         lambda : self.noMoreTime(), \
                                         lambda state, x: self.order(state, x), \
                                         lambda state, d, o: self.select(state, d, o))

    def select(self, state, depth, overdepth):
        if overdepth > 2:
            return False

        if self.selectiveDeepening & SelectiveDeepening.HIGH_HEURISTICS:
            if corners(self.player, state) < 10:
                return True

        return None

    def order(self, state, successors):
        if self.childrenOrdering & ChildrenOrdering.HEURISTIC:
            return sorted(successors, \
                    lambda pair2, pair1: \
                        availableCorners(pair1[1], pair1[1].currentPlayer.getCurrentColor()) - \
                            availableCorners(pair2[1], pair2[1].currentPlayer.getCurrentColor()), \
                    reverse=self.player == state.getCurrentPlayer())

        return successors

    def heuristic(self, state):
        score = 0
        if self.heuristicType & Heuristics.SCORE:
            score += 1 * BlokusGameAgentExample.heuristic(self, state)
        if self.heuristicType & Heuristics.ALL_CORNERS:
            score += 1 * corners(self.player, state)

        return score

    @property
    def turnTimeLimit(self):
        if self.timeManagement & TimeManagement.MORE_TIME_AT_THE_END:
            if self.turnNumber <= 8:
                return self._turnTimeLimit / 1.5
            else:
                return self._turnTimeLimit * 1.5

        if self.timeManagement & TimeManagement.MORE_TIME_AT_THE_BEGINNING:
            if self.turnNumber <= 20:
                return self._turnTimeLimit * 2
            else:
                return self._turnTimeLimit

        if self.timeManagement & TimeManagement.ACCORDING_TO_OPEN_CORNERS:
            openCorners = availableCorners(self.currentState, \
                    self.currentState.currentPlayer.getCurrentColor())
            openCorners = corners(self.player, self.currentState)
            return self._turnTimeLimit * openCorners / 10


        return self._turnTimeLimit

def opposingCorners(state):
    slimSize = state.boardSize
    size = state.boardSizeWithBorder
    boardCorners = getBoardCorners(size)
    color1 = state.currentPlayer.colors[0].boardBinary
    color2 = state.currentPlayer.colors[1].boardBinary

    corner1 = color1 & boardCorners
    corner2 = color2 & boardCorners

    color1 = binaryBoardToArray(color1, slimSize, size)
    color2 = binaryBoardToArray(color2, slimSize, size)

    retval = 0

    if color1[0][0] == 1 and color2[slimSize - 1][slimSize - 1] == 1:
        retval = 1000

    if color2[0][0] == 1 and color1[slimSize - 1][slimSize - 1] == 1:
        retval = 1000

    if color1[0][slimSize - 1] == 1 and color2[slimSize - 1][0] == 1:
        retval = 1000

    if color2[0][slimSize - 1] == 1 and color1[slimSize - 1][0] == 1:
        retval = 1000

    return retval == 1000

    return retval if player == state.getCurrentPlayer() else -1 * retval

    corner1, corner2 = min(corner1, corner2), max(corner1, corner2)

    if corner1 & topLeftCorner(size) and corner2 & bottomRightCorner(size) \
            or \
        corner1 & topRightCorner(size) and corner2 & bottomLeftCorner(size):
        retval = 1000

    boardCorners = binaryBoardToArray(boardCorners, slimSize, size)
    color1 = binaryBoardToArray(color1, slimSize, size)
    print 'TL: %s, TR: %s, BL: %s, BR: %s' % (color1[0][0], color1[0][slimSize - 1], \
                                            color1[slimSize - 1][0], color1[slimSize - 1][slimSize -1])



def topLeftCorner(boardSizeWithBorder):
    return 2**(boardSizeWithBorder + 1) 

def topRightCorner(boardSizeWithBorder):
    return 2**(2 * boardSizeWithBorder - 2) 

def bottomLeftCorner(boardSizeWithBorder):
    return 2**(boardSizeWithBorder * (boardSizeWithBorder - 2) + 1) 

def bottomRightCorner(boardSizeWithBorder):
    return 2**(boardSizeWithBorder * (boardSizeWithBorder - 1) - 2)

def corners(player, state):
    corners = 0
    for color in state.currentPlayer.colors:
        available = availableCorners(state, color)
        if player == state.getCurrentPlayer():
            corners += available
        else:
            corners -= available

    for color in state.opponentPlayer.colors:
        available = availableCorners(state, color)
        if player == state.getCurrentPlayer():
            corners -= available
        else:
            corners += available

    return corners


def availableCorners(state, currentColor):
    currentBoard = currentColor.boardBinary
    currentBoardNeighbours = (currentBoard >> 1) | (currentBoard << 1) \
            | (currentBoard >> state.boardSizeWithBorder) \
            | (currentBoard << state.boardSizeWithBorder)
    opponentBoards = 0
    for color in state.currentPlayer.colors:
        if not (color == currentColor):
            opponentBoards |= color.boardBinary
    for color in state.opponentPlayer.colors:
        if not (color == currentColor):
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

