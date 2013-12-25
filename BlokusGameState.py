from GameState import GameState
from BlokusGameAction import BlokusGameAction
from BlokusGameConstants import BoardSize, Players, COLORS, LegalActionType, TIE
from BlokusGameUtils import getBorder, getBoardCorners, getBinaryShapeCorners, getIndexesOfTurnedOnBits
from BlokusGameInput import makeShapes
from BlokusGamePlayer import BlokusGamePlayer

class BlokusGameState(GameState):

    def setup(self, boardSize, shapesFilePath, orderedShapesMode = False):
        if boardSize not in BoardSize.valid():
            raise Exception("illegal board size")

        self.boardSize = boardSize
        self.boardSizeWithBorder = boardSize + 2
        self.border = getBorder(self.boardSizeWithBorder)
        self.orderedShapesMode = orderedShapesMode
        self.boardCorners = getBoardCorners(self.boardSizeWithBorder)
        shapes = makeShapes(shapesFilePath, self.boardSizeWithBorder)
        self.numOfShapes = len(shapes) 
        self.currentPlayer = BlokusGamePlayer().setup(Players.FIRST, COLORS[boardSize][Players.FIRST], shapes)
        self.opponentPlayer = BlokusGamePlayer().setup(Players.SECOND, COLORS[boardSize][Players.SECOND], shapes)
        
        return self

    def copy(self):
        newState = BlokusGameState()
        newState.boardSize = self.boardSize
        newState.boardSizeWithBorder = self.boardSizeWithBorder
        newState.border = self.border
        newState.orderedShapesMode = self.orderedShapesMode
        newState.boardCorners = self.boardCorners
        newState.numOfShapes = self.numOfShapes
        newState.currentPlayer = self.currentPlayer.copy()
        newState.opponentPlayer = self.opponentPlayer.copy()
        return newState
    
    def endMove(self):
        tempPlayer = self.currentPlayer
        self.currentPlayer = self.opponentPlayer
        self.opponentPlayer = tempPlayer
    
    def getSuccessors(self):
        successorsList = {}
        
        currentColor = self.currentPlayer.getCurrentColor()

        currentBoard = currentColor.boardBinary
        currentBoardNeighbours = (currentBoard >> 1) | (currentBoard << 1) | (currentBoard >> self.boardSizeWithBorder) | (currentBoard << self.boardSizeWithBorder)
        opponentBoards = 0
        for color in self.currentPlayer.colors:
            if not (color == currentColor):
                opponentBoards |= color.boardBinary
        for color in self.opponentPlayer.colors:
            opponentBoards |= color.boardBinary
        freeSquares = ~(currentBoard | currentBoardNeighbours | opponentBoards | self.border)

        #first move allowed only in board's corners
        availableSquaresToPlay = self.boardCorners

        #if not first move - the board isn't empty
        if currentBoard:
            availableSquaresToPlay = self.__getBoardDiagonalsToCorners(currentBoard)

        availableSquaresToPlay = availableSquaresToPlay & freeSquares

        availableSquaresIndexes = getIndexesOfTurnedOnBits(availableSquaresToPlay)

        for shapeIndex in xrange(len(currentColor.shapes)):
            
            shape = currentColor.shapes[shapeIndex]
    
            for index in availableSquaresIndexes:

                location = self.__fromIndexWithBorderToLocationWithoutBorder(index)
                
                for shapeVariation in shape.shapeVariations:
                
                    for shapeCorner in shapeVariation.corners:
                
                        offsetFromShapeToSquare = index - shapeCorner
                        #move the shape to its chosen position
                        shapeOnBoard = (shapeVariation.binary << offsetFromShapeToSquare) if (offsetFromShapeToSquare > 0) else (shapeVariation.binary >> offsetFromShapeToSquare * (-1))
                        
                        #if the shape placed in forbidden square so this action is not valid 
                        if shapeOnBoard ^ (shapeOnBoard & freeSquares):
                            continue

                        nextState = self.copy()
                        
                        nextStateCurrentColor = nextState.currentPlayer.getCurrentColor() 
                        
                        nextStateCurrentColor.boardBinary |= shapeOnBoard
                        nextStateCurrentColor.shapes = nextStateCurrentColor.shapes[:shapeIndex] + nextStateCurrentColor.shapes[shapeIndex + 1:] 
                        nextStateCurrentColor.passedPrevTurn = False
                        
                        nextState.currentPlayer.endMove()
                        nextState.endMove()

                        successorsList[BlokusGameAction(LegalActionType.SHAPE, shapeVariation, self.__fromIndexWithBorderToLocationWithoutBorder(shapeCorner), location)] = nextState
                                                
            if self.orderedShapesMode and successorsList:
                break
        
        #Pass Action
        nextState = self.copy()
        
        nextState.currentPlayer.getCurrentColor().passedPrevTurn = True
        nextState.currentPlayer.endMove()
        nextState.endMove()
        
        successorsList[BlokusGameAction(LegalActionType.PASS)] = nextState

        return successorsList
    
    def getAllPlayers(self):
        return Players.valid()
    
    def getCurrentPlayer(self):
        return self.currentPlayer.player
    
    def getWinner(self):
        allColorsPassedPrevTurns = [color.passedPrevTurn for color in self.currentPlayer.colors] + [color.passedPrevTurn for color in self.opponentPlayer.colors]
        
        if False in allColorsPassedPrevTurns:
            return None

        (currentPlayerPoints, opponentPlayerPoints) = (self.currentPlayer.getScore(), self.opponentPlayer.getScore())
        
        winner = TIE
        
        if (currentPlayerPoints > opponentPlayerPoints):
            winner = self.currentPlayer.player
        elif (opponentPlayerPoints > currentPlayerPoints):
            winner = self.opponentPlayer.player

        return winner
    
    def getTurnsLeft(self):
        return None        
    
    def __cmp__(self, other):
        return cmp((self.currentPlayer, self.opponentPlayer), (other.currentPlayer, other.opponentPlayer))
    
    def __hash__(self):
        return hash((self.currentPlayer, self.opponentPlayer))
    
    def __str__(self):
        result = "\n"
        result += "    "
    
        for i in xrange(0, self.boardSize):
            result += (" 00" if i < 10 else " 0") + str(i) + " "
        
        result += "\n"
        index = self.boardSizeWithBorder
        
        for i in xrange(0, self.boardSize):
            result += ("00" if i < 10 else "0") + str(i) + " "
            index += 1
        
            for _ in xrange(0, self.boardSize):
                mask = (2 ** index)
                
                currPlayer = "  -  "
                
                for color in self.currentPlayer.colors:
                    if mask & color.boardBinary:
                        currPlayer = "  " + color.__str__() + "  "
                   
                for color in self.opponentPlayer.colors:
                    if mask & color.boardBinary:
                        currPlayer = "  " + color.__str__() + "  "
                                   
                result += currPlayer

                index += 1
            
            index += 1    
            result += "\n"
        
        return result
    
    def __repr__(self):
        return self.__str__()
    
    def __getBoardDiagonalsToCorners(self, currentBoard):

        #first choose the squares that a new shape can be placed near (in diagonal)
        boardCorners = getBinaryShapeCorners(currentBoard, self.boardSizeWithBorder) 
        
        #now choose available squares that a new shape can be placed at
        boardDiagonalsToCorners =   (boardCorners >> self.boardSizeWithBorder + 1) | \
                                    (boardCorners >> self.boardSizeWithBorder - 1) | \
                                    (boardCorners << self.boardSizeWithBorder + 1) | \
                                    (boardCorners << self.boardSizeWithBorder - 1) 
        
        return boardDiagonalsToCorners

    #we don't want the location (row, column) to include the border offset 
    def __fromIndexWithBorderToLocationWithoutBorder(self, index):
        return ((index / self.boardSizeWithBorder) - 1, (index % self.boardSizeWithBorder) - 1)
