from BlokusGameShapeVariation import BlokusGameShapeVariation
from BlokusGameUtils import getBinaryShapeCorners, getIndexesOfTurnedOnBits

class BlokusGameShape:
    
    def setup(self, shape, boardSizeWithBorder):
        self.shapeVariations = self.__makeShapeVariations(shape, boardSizeWithBorder)
        self.numOfSquares = shape[2]
        return self
        
    def __cmp__(self, other):
        return cmp(self.shapeVariations, other.shapeVariations)

    def __hash__(self):
        return hash(self.shapeVariations)
        
    def __str__(self):
        return str(self.shapeVariations[0])

    def __repr__(self):
        return self.__str__()
    
    def __makeShapeVariations(self, shape0, boardSizeWithBorder):
        (rows, columns, n, locations) = shape0
        
        shape90 = [columns, rows, n, []]
        for l in locations:
            shape90[3].append((l / columns) + (((columns - 1) - (l % columns)) * rows))
        
        shape180 = [rows, columns, n, []]
        for l in locations:
            shape180[3].append((((rows - 1) - (l / columns)) * columns) + (l % columns))
        
        shape270 = [columns, rows, n, []]
        for l in locations:
            shape270[3].append(((rows - 1) - (l / columns)) + ((l % columns) * rows))
        
        shapesList = [shape0, shape90, shape180, shape270]
        shapesList.extend(self.__makeMirroredShapes(shapesList))
        
        shapeVariations = []
        
        for shape in shapesList:
            binaryShape = self.__makeBinaryShape(shape, boardSizeWithBorder)
            binaryShapeCorners = self.__makeBinaryShapeCorners(binaryShape, boardSizeWithBorder)
            shapeVariation = BlokusGameShapeVariation((shape[0], shape[1], shape[2], tuple(shape[3])), binaryShape, binaryShapeCorners)
            if shapeVariation not in shapeVariations:
                shapeVariations.append(shapeVariation)

        return tuple(shapeVariations)
    
    def __makeMirroredShapes(self, shapes):
        mirroredShapes = []
        for shape in shapes:
            mirroredShape = [shape[0], shape[1], shape[2], []]
            for location in shape[3]:
                mirroredShape[3].append(((location / shape[1]) * shape[1]) + ((shape[1] - 1) - (location % shape[1])))
            mirroredShapes.append(mirroredShape)
        return mirroredShapes
    
    def __makeBinaryShape(self, shape, boardSizeWithBorder):
        binaryShape = 0
        #every index is located in its place in the binary representation
        for location in shape[3]:
            row = (location / shape[1])
            binaryShape |= (2**location) << (row * (boardSizeWithBorder - shape[1])) #the shift is the border offset - this is the shape's initial location including the border around it
        return binaryShape << (boardSizeWithBorder + 1)
    
    def __makeBinaryShapeCorners(self, binaryShape, boardSizeWithBorder):
        binaryCorners = getBinaryShapeCorners(binaryShape, boardSizeWithBorder)
        return getIndexesOfTurnedOnBits(binaryCorners)