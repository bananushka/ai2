from BlokusGameAgentExample import BlokusGameAgentExample
from BlokusAgentSimple import BlokusAgentSimple
from BlokusGameUtils import getIndexesOfTurnedOnBits, getBinaryShapeCorners

class BlokusAgentMcBoogerballs(BlokusAgentSimple):
    def heuristic(self, state):
        parentHeuristic = BlokusGameAgentExample.heuristic(self, state)
        return parentHeuristic + \
                availableCorners(state) * \
                averageSquaresInHand(state.currentPlayer.getCurrentColor())

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

