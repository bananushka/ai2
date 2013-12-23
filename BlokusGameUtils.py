#creates long that represents border - for example on board 2*2
# (lsb) 1111
#       1001
#       1001
#       1111 (msb)
#and the long is = (msb) 1111100110011111 (lsb)
def getBorder(boardSizeWithBorder):
    border = 0
    for i in xrange(0, boardSizeWithBorder - 1):
        border |= 2**i
    for i in xrange(boardSizeWithBorder - 1, (boardSizeWithBorder) * (boardSizeWithBorder - 1) + 1, boardSizeWithBorder):
        border |= 2**i | 2**(i+1)
    for i in xrange((boardSizeWithBorder) * (boardSizeWithBorder - 1) + 1, (boardSizeWithBorder) * (boardSizeWithBorder)):
        border |= 2**i
    return border
    
#first move allowed only on board corners so it generates longs representations of the corners
def getBoardCorners(boardSizeWithBorder):
    return 2**(boardSizeWithBorder + 1) | 2**(2 * boardSizeWithBorder - 2) | 2**(boardSizeWithBorder * (boardSizeWithBorder - 2) + 1) | 2**(boardSizeWithBorder * (boardSizeWithBorder - 1) - 2)

#new shape can be placed only near corners so it turn off the squares that aren't corners
def getBinaryShapeCorners(binaryShape, boardSizeWithBorder):
    return binaryShape & (~((binaryShape >> 1) & (binaryShape << 1)) & ~((binaryShape >> boardSizeWithBorder) & (binaryShape << boardSizeWithBorder)))    

#to be able to calculate the number of squares a shape need to be moved it is necessary to know the shape's index. as well as the index of its new location
def getIndexesOfTurnedOnBits(num):
    indexes = ()
    indexFromBeginning = 0
    while num:
        index = (num & -num).bit_length()
        indexFromBeginning += index
        indexes = indexes + (indexFromBeginning - 1, )
        num >>= index
    return indexes

#convert the binaryBoard that can be found in state -> player -> color to array representation for agent's evaluation purposes if you doesn't want to work in binary (which is much more efficient)
def binaryBoardToArray(binaryBoard, boardSize, boardSizeWithBorder):
    array = [[0 for _ in xrange(boardSize)] for _ in xrange(boardSize)]

    index = boardSizeWithBorder
    
    for row in xrange(0, boardSize):
        index += 1
        for col in xrange(0, boardSize):
            mask = (2 ** index)
            
            if mask & binaryBoard:
                array[row][col] = 1
                               
            index += 1
        index += 1    
    
    return array