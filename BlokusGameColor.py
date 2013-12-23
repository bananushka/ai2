class BlokusGameColor():

    def setup(self, color, shapes):
        self.color = color
        #use binaryBoardToArray function in the Utils file if want to convert to its array representation
        self.boardBinary = 0
        self.shapes = shapes
        self.maxScore = sum([shape.numOfSquares for shape in shapes])
        self.passedPrevTurn = False
        return self
    
    def copy(self):
        newPlayer = BlokusGameColor()
        newPlayer.color = self.color
        newPlayer.boardBinary = self.boardBinary
        newPlayer.shapes = self.shapes
        newPlayer.maxScore = self.maxScore
        newPlayer.passedPrevTurn = self.passedPrevTurn
        return newPlayer
    
    def getScore(self):
        return self.maxScore - sum([shape.numOfSquares for shape in self.shapes])
    
    def __cmp__(self, other):
        return cmp((self.color, self.boardBinary), (other.color, other.boardBinary))    
    
    def __hash__(self):
        return hash((self.color, self.boardBinary))

    def __str__(self):
        return self.color
    
    def __repr__(self):
        return self.__str__()