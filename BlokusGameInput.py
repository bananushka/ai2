from random import shuffle
from BlokusGameShape import BlokusGameShape

class IllegalShapeFileFormatException():
    pass

#creates the shapes from the input file and validate the format
def makeShapes(shapesFilePath, boardSizeWithBorder):
    
    with open(shapesFilePath) as f:
        shapesList = [[int(x) for x in line.split()] for line in f]
    
    shapes = []
    
    isShapesValid = True
    shapesRepetitions = {}
    shapeSizes = [False for _ in xrange(6)]
    shapeSizes[0] = True
    
    for line in shapesList:
        
        (rows, columns, numOfSquares, locations) = (line[0], line[1], line[2], tuple(line[3:]))
        
        if (numOfSquares != len(locations)) or (numOfSquares > (rows * columns)):
            isShapesValid = False
            break
        
        ranges = [(location < (rows * columns)) for location in locations]
        
        if False in ranges:
            isShapesValid = False
            break            
        
        shape = BlokusGameShape().setup((rows, columns, numOfSquares, locations), boardSizeWithBorder)
        
        if shape.numOfSquares < 1 or shape.numOfSquares > 6:
            isShapesValid = False
            break
        
        shapeVariation = shape.shapeVariations[0]
        if not isConsecutiveness(shapeVariation.binary, boardSizeWithBorder, shapeVariation.corners[0]):
            isShapesValid = False
            break
        
        if shape in shapesRepetitions:

            if shapesRepetitions[shape] >= 3:
                isShapesValid = False
                break
            
            else:
                shapesRepetitions[shape] += 1
                
        else:
            
            shapesRepetitions[shape] = 1
        
        shapeSizes[shape.numOfSquares] = True
        
        shapes.append(shape)
    
    if False in shapeSizes:
        isShapesValid = False
    
    if len(shapes) < 17 or len(shapes) > 25:
        isShapesValid = False
    
    totalNumOfSquares = sum([shape.numOfSquares for shape in shapes])
    
    if totalNumOfSquares < 80 or totalNumOfSquares > 98:
        isShapesValid = False
    
    if not isShapesValid:
        raise IllegalShapeFileFormatException()
    
    shuffle(shapes)
    
    return tuple(shapes)

def isConsecutiveness(binary, boardSizeWithBorder, startIndex):
    prevChain, chain = 0, 2**startIndex
    #extend from some index to its neighbours until covered all of them. if covered all then its consecutive.
    while prevChain != chain:
        prevChain = chain
        chain |= (chain << 1 | chain >> 1 | chain << boardSizeWithBorder | chain >> boardSizeWithBorder) & binary
    return chain == binary
